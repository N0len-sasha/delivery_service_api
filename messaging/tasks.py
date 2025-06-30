import asyncio

from celery import Celery
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from api.config import Config
from api.exchange_rate import update_delivery_price

celery_app_conf = Celery("delivery_service", broker=..., backend=...)

@celery_app_conf.task(name="messaging.tasks.recalculate_prices")
def recalculate_prices():
    loop = None
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(_run_recalculate())

async def _run_recalculate():
    engine = create_async_engine(Config.DB_URL, future=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        await update_delivery_price(session)


