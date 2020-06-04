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
    from klaud.database import _client, db
    database_name = 'test_' + str(uuid.uuid4()).replace('-', '_')
    settings.db_name = database_name
    yield db(database_name)
    await_(_client.drop_database(database_name))


@pytest.fixture(scope='session')
def client():
    from klaud import app
    with TestClient(app) as client:
        yield client
