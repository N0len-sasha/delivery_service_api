import os

from dotenv import load_dotenv
from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@delivery_service_db:5432/postgres"
)
load_dotenv()

class Config:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_KEY = os.getenv("REDIS_KEY", "usd_to_rub_rate")
    REDIS_TTL = int(os.getenv("REDIS_TTL", 3600))
    SQLALCHEMY_URL = os.getenv("SQLALCHEMY_URL")
    TIMEZONE = str(os.getenv("TIMEZONE"))
    CBR_API_URL = os.getenv("CBR_API_URL", "https://www.cbr-xml-daily.ru/daily_json.js")
    RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
    QUEUE_NAME = os.getenv("QUEUE_NAME", "delivery_tasks")
    DB_URL = str(os.getenv("SQLALCHEMY_URL"))


config = Config()