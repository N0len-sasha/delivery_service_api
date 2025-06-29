from sqlalchemy.ext.asyncio import (AsyncAttrs, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from api.config import Config

engine = create_async_engine(Config.REAL_DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

async def get_db():
    async with async_session() as session:
        yield session
