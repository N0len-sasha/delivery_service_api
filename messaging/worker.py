from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.config import Config
from api.exchange_rate import update_delivery_price
from celery_app import celery_app

engine = create_async_engine(Config.DB_URL, future=True)
AsyncSessionMaker = async_sessionmaker(engine, expire_on_commit=False)

@celery_app.task
def recalculate_prices():
    import asyncio

    async def run():
        async with AsyncSessionMaker() as session:
            await update_delivery_price(session)

    asyncio.run(run())
