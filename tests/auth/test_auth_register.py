import pytest

from klaud.settings import settings
from klaud.utils import passwords


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


def test_right_register(await_, client, database, master_headers):
    resp = client.post(
        '/_master/register',
        headers=master_headers,
        json={
            'username': 'user',
            'password': 'pass'
        }
    )
    assert resp.status_code == 200
    doc = await_(database.users.find_one({'username': 'user'}))
    doc.pop('_id')
    hashed = doc.pop('hashed')
    assert doc == {
        'username': 'user',
        'is_master': False
    }
    assert passwords.checkpw('pass', hashed)


def test_error_register(client, master_headers):
    resp = client.post(
        '/_master/register',
        headers=master_headers,
        json={
            'username': settings.master_name,
            'password': 'pass'
        }
    )
    assert resp.status_code == 409
