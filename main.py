from contextlib import asynccontextmanager
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from sqlalchemy.ext.asyncio import AsyncSession
from messaging.tasks import recalculate_prices
from sqlalchemy.future import select
from api.models import Type
from api.routes import api_router
from db.db_setup import get_db
from alembic import command
from alembic.config import Config as AlembicConfig

lock = asyncio.Lock()

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

async def run_migrations():
    alembic_cfg = AlembicConfig("alembic.ini")
    await asyncio.to_thread(command.upgrade, alembic_cfg, "head")

def create_start_celery_task():
    def wrapper():
        recalculate_prices.delay()
    return wrapper


@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_migrations()
    async for db in get_db():
        await initialize_types(db)
        yield

app = FastAPI(title="delivery_service", lifespan=lifespan)
add_pagination(app)
app.include_router(router=api_router, prefix="/api_v1", tags=["api_v1"])

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
