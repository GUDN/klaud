import asyncio
import uuid

import pytest
from fastapi.testclient import TestClient

_loop = asyncio.get_event_loop()


@pytest.fixture(scope='session')
def await_():
    return _loop.run_until_complete


@pytest.fixture(scope='function')
def database(await_):
    from klaud.settings import settings
    from klaud.database import client, db, init
    database_name = 'test_' + str(uuid.uuid4()).replace('-', '_')
    settings.db_name = database_name
    await_(init())
    yield db(database_name)
    await_(client().drop_database(database_name))


@pytest.fixture(scope='function')
def client(database):
    from klaud import app
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='function', autouse=True)
def create_john_doe(await_, database):
    from klaud.utils import passwords
    await_(
        database.users.find_one_and_update(
            {'username': 'john_doe'},
            {'$set': {
                'hashed': passwords.hashpw('password'),
                'is_master': False
            }},
            upsert=True
        )
    )
