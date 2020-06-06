import pytest

from klaud.utils import passwords


@pytest.fixture(scope='function', autouse=True)
def create_john_doe(await_, database):
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


def test_without_scope(client):
    resp = client.post(
        '/_token',
        data={
            'grant_type': 'password',
            'username': 'john_doe',
            'password': 'password'
        }
    )
    token = resp.json()['access_token']
    resp = client.delete(
        '/_me',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )
    assert resp.status_code == 403
    resp = client.get(
        '/_me',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )
    assert resp.status_code == 200


def test_with_scope(client):
    resp = client.post(
        '/_token',
        data={
            'grant_type': 'password',
            'scope': 'manage',
            'username': 'john_doe',
            'password': 'password'
        }
    )
    token = resp.json()['access_token']
    resp = client.delete(
        '/_me',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )
    assert resp.status_code == 200
    resp = client.get(
        '/_me',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )
    assert resp.status_code == 401
