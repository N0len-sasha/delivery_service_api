from typing import List

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import Response
from fastapi import Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Package, Type, User
from db.db_setup import get_db
from pydantic_schemas.models_schemas import (PackageAfterCreate, PackageBase,
                                             PackageCreate, TypeResponse, UserCreate,
                                             PUser)

api_router = APIRouter()


@api_router.post('/register/', response_model=UserCreate)
async def _create_user(user: UserCreate,
                       db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user.username))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(username=user.username)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@api_router.post('/login/', response_model=PUser)
async def _login_user(user_data: UserCreate,
                      response: Response,
                      db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user_data.username))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=400, detail=f"User with username '{user_data.username}' does not exist")

    response.set_cookie("user_id", str(user.id))

    return user


async def get_current_user(request: Request,
                           db: AsyncSession = Depends(get_db)) -> User:
    user_id = request.cookies.get("user_id")

    if not user_id:
        raise HTTPException(status_code=400, detail="User is not logged in")

    try:
        user_id = int(user_id)  # Куки приходят строкой, преобразуем в число
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    result = await db.execute(select(User).where(User.id == user_id))
    current_user = result.scalars().first()

    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    return current_user


@api_router.get('/packages/', response_model=Page[PackageBase])
async def _get_packages(type: str = Query(None, description="Filter by package type"),
                        has_price: float = Query(None, description="Filter by delivery price"),
                        db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)):

    query = select(Package).where(Package.package_owner == current_user.id)

    if type:
        query = query.join(Package.type).filter(Type.name == type)

    if has_price is not None:
        if has_price:
            query = query.filter(Package.delivery_price is not None)
        else:
            query = query.filter(Package.delivery_price is None)
    return await paginate(db, query)


@api_router.post('/packages/')
async def _create_package(package: PackageCreate,
                          db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(get_current_user)) -> PackageAfterCreate:
    result = await db.execute(select(Type).filter(Type.id == package.type_id))
    type_exists = result.scalars().first() is not None

    if not type_exists:
        raise HTTPException(status_code=422, detail=f"Type with id {package.type_id} does not exist")

    new_package = Package(
        name=package.name,
        weight=package.weight,
        price=package.price,
        type_id=package.type_id,
        package_owner=current_user.id
    )
    db.add(new_package)
    await db.commit()
    await db.refresh(new_package)
    return PackageAfterCreate(id=new_package.id)


@api_router.get('/packages/{package_id}', response_model=PackageBase)
async def _read_package(package_id: int,
                        db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Package).filter(Package.id == package_id))
    package = result.scalars().first()

    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    return package


@api_router.get('/types/', response_model=List[TypeResponse])
async def _get_types(db: AsyncSession = Depends(get_db)):
    response = await db.execute(select(Type))
    types = response.scalars().all()
    return types
