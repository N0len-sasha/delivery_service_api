from fastapi import FastAPI

import uvicorn
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from sqlalchemy.orm import Session

from api.models import Type
from api.routes import api_router
from db.db_setup import get_db, engine


async def initialize_types(session: AsyncSession):
    result = await session.execute(select(Type))
    existing_types = result.scalars().all()

    if not existing_types:
        types_data = [
            Type(name="Electronics"),
            Type(name="Clothing"),
            Type(name="Others"),
        ]
        session.add_all(types_data)
        await session.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSession(engine) as session:
        await initialize_types(session)

    yield


app = FastAPI(title="delivery_service", lifespan=lifespan)
app.include_router(router=api_router, prefix="/api_v1", tags=["api_v1"])

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
