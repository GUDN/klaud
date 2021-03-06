from typing import Optional

from motor.motor_asyncio import (AsyncIOMotorClient, AsyncIOMotorDatabase,
                                 AsyncIOMotorGridFSBucket)
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError

from .settings import settings

uri = 'mongodb://{}:{}@{}:{}'.format(
    settings.db_user,
    settings.db_password,
    settings.db_host,
    settings.db_port
)

_client = None
_gfs = None


def db(name: Optional[str] = None) -> AsyncIOMotorDatabase:
    if not name:
        return _client[settings.db_name]
    return _client[name]


def client() -> AsyncIOMotorClient:
    return _client


def gfs() -> AsyncIOMotorGridFSBucket:
    return _gfs


async def init():
    global _client, _gfs
    _client = AsyncIOMotorClient(uri)
    await setup_indexes()
    _gfs = AsyncIOMotorGridFSBucket(db())


async def setup_indexes():
    async def _create_index(collection: str, *args, **kwargs):
        try:
            await db()[collection].create_index(*args, **kwargs)
        except OperationFailure:
            pass
    await _create_index('users', 'username', unique=True)


async def ping() -> bool:
    try:
        await db().command('ping')
        return True
    except ServerSelectionTimeoutError:
        return False
