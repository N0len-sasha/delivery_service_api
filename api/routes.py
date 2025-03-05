from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Package, Type
from db.db_setup import get_db
from pydantic_schemas.models_schemas import (PackageAfterCreate, PackageBase,
                                             PackageCreate)

api_router = APIRouter()

@api_router.get('/packages/', response_model=List[PackageBase])
async def _get_packages(db: AsyncSession = Depends(get_db)):
    response = await db.execute(select(Package))
    packages = response.scalars().all()
    return packages

@api_router.post('/packages/')
async def _create_package(package: PackageCreate,
                          db: AsyncSession = Depends(get_db)) -> PackageAfterCreate:
    new_package = Package(
        name=package.name,
        weight = package.weight,
        price = package.price,
        type_id=package.type_id
    )
    db.add(new_package)
    await db.commit()
    await db.refresh(new_package)
    return PackageAfterCreate(
        id=new_package.id
    )

@api_router.get('/packages/{package_id}', response_model=PackageBase)
async def _read_package(package_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Package).filter(Package.id == package_id))
    package = result.scalars().first()

    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    return package

@api_router.get('/types/')
async def _get_types(db: AsyncSession = Depends(get_db)):
    response = await db.execute(select(Type))
    types = response.scalars().all()
    return types