from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError

from .settings import settings

uri = 'mongodb://{}:{}@{}:{}'.format(
    settings.db_user,
    settings.db_password,
    settings.db_host,
    settings.db_port
)

_client = None


def db(name: Optional[str] = None) -> AsyncIOMotorDatabase:
    if not name:
        return _client[settings.db_name]
    return _client[name]


def client() -> AsyncIOMotorClient:
    return _client


def init():
    global _client
    _client = AsyncIOMotorClient(uri)


async def ping() -> bool:
    try:
        await db().command('ping')
        return True
    except ServerSelectionTimeoutError:
        return False
