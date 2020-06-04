from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError

from .settings import settings

uri = 'mongodb://{}:{}@{}:{}'.format(
    settings.db_user,
    settings.db_password,
    settings.db_host,
    settings.db_port
)

_client = AsyncIOMotorClient(uri)


def db(name=settings.db_name) -> AsyncIOMotorDatabase:
    return _client[name]


async def ping() -> bool:
    try:
        await db().command('ping')
        return True
    except ServerSelectionTimeoutError:
        return False
