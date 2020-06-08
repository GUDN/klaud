import pytest

from klaud.settings import settings


@pytest.fixture(scope='function')
def master_headers(client):
    resp = client.post(
        '/_token',
        data={
            'grant_type': 'password',
            'scope': 'master',
            'username': settings.master_name,
            'password': settings.master_password
        }
    )
    token = resp.json()['access_token']
    return {
        'Authorization': f'Bearer {token}'
    }


@pytest.fixture(scope='function')
def get_john_doe(await_, database):
    def _get_document():
        return await_(database.users.find_one({
            'username': 'john_doe'
        }))
    return _get_document


def test_john_doe_status(client, get_john_doe, master_headers):
    resp = client.put(
        '/_master/manage',
        headers=master_headers,
        json={
            'target': 'john_doe',
            'status': True
        }
    )
    assert resp.status_code == 200
    assert get_john_doe()['is_master']
    resp = client.put(
        '/_master/manage',
        headers=master_headers,
        json={
            'target': 'john_doe',
            'status': False
        }
    )
    assert resp.status_code == 200
    assert not get_john_doe()['is_master']


def test_target_not_found(client, master_headers):
    resp = client.put(
        '/_master/manage',
        headers=master_headers,
        json={
            'target': 'katya',
            'status': False
        }
    )
    assert resp.status_code == 404
