import uvicorn
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from api.config import REAL_DATABASE_URL

engine = create_async_engine(REAL_DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

async def get_db():
    async with async_session() as session:
        yield session
