from datetime import timedelta

import httpx
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.config import Config
from api.models import Package

redis_client = redis.from_url(url=f"redis://{Config.REDIS_HOST}", decode_responses=True)


async def get_rate_value():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(Config.CBR_API_URL)
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise Exception(f"HTTP error: status {response.status_code} - {response.text}")
        except httpx.RequestError as e:
            raise Exception(f"Request error: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
        response_data = response.json()

    rate = float(response_data["Valute"]["USD"]["Value"])
    return rate


async def get_chached_rate():
    cached_rate = await redis_client.get(Config.REDIS_KEY)

    if cached_rate:
        return float(cached_rate)

    rate = await get_rate_value()
    await redis_client.setex(Config.REDIS_KEY, timedelta(seconds=Config.REDIS_TTL), rate)

    return rate

async def update_delivery_price(db: AsyncSession):
    rate = await get_chached_rate()
    result = await db.execute(select(Package))
    packages = result.scalars().all()


    for package in packages:
        new_price = (package.weight * 0.5 + package.price * 0.01) * rate

        if package.delivery_price != new_price:
            package.delivery_price = new_price
            db.add(package)

    await db.commit()



