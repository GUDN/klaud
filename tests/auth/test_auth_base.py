import pytest

from klaud.utils import passwords


@pytest.fixture(scope='function', autouse=True)
def create_john_doe(await_, database):
    await_(
        database.users.find_one_and_update(
            {'username': 'john_doe'},
            {'$set': {'hashed': passwords.hashpw('password')}},
            upsert=True
        )
    )


def test_right_login(client):
    resp = client.post(
        '/_token',
        data={
            'grant_type': 'password',
            'username': 'john_doe',
            'password': 'password'
        }
    )
    assert resp.status_code == 200
    token = resp.json()['access_token']
    resp = client.get(
        '/_me',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )
    assert resp.status_code == 200
    assert resp.json()['username'] == 'john_doe'


def test_wrong_login(client):
    resp = client.post(
        '/_token',
        data={
            'grant_type': 'password',
            'username': 'john_doe',
            'password': 'wrong_password'
        }
    )
    assert resp.status_code == 401
