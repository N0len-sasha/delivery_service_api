from contextlib import asynccontextmanager

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.exchange_rate import loop_fetch
from api.models import Type
from api.routes import api_router
from db.db_setup import get_db

timezone = 'Europe/Moscow'

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

async def start_loop_fetch(db: AsyncSession):
    await loop_fetch(db)

def create_start_loop_fetch(db: AsyncSession):
    async def wrapper():
        await start_loop_fetch(db)
    return wrapper


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler(timezone=f'{timezone}')

    async for db in get_db():
        await initialize_types(db)

        scheduler.add_job(func=create_start_loop_fetch(db), trigger='interval', seconds=10)
        scheduler.start()

        yield

app = FastAPI(title="delivery_service", lifespan=lifespan)
app.include_router(router=api_router, prefix="/api_v1", tags=["api_v1"])


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
