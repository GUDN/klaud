import pytest

from klaud.utils import passwords


@pytest.fixture(scope='function')
def manage_headers(client, create_john_doe):
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
    return {
        'Authorization': f'Bearer {token}'
    }


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
    resp = client.patch(
        '/_me',
        headers={
            'Authorization': f'Bearer {token}'
        },
        json={
            'username': 'katya'
        }
    )
    assert resp.status_code == 403


def get_document(database, username):
    return database.users.find_one({
        'username': username
    })


def test_patch_username(await_, client, database, manage_headers):
    original = await_(get_document(database, 'john_doe'))
    assert original.pop('username') == 'john_doe'
    resp = client.patch(
        '/_me',
        headers=manage_headers,
        json={
            'username': 'katya'
        }
    )
    assert resp.status_code == 200
    patched = await_(get_document(database, 'katya'))
    assert patched
    assert patched.pop('username') == 'katya'
    assert patched == original


def test_patch_password(await_, client, database, manage_headers):
    original = await_(get_document(database, 'john_doe'))
    original.pop('hashed')
    resp = client.patch(
        '/_me',
        headers=manage_headers,
        json={
            'password': 'katya'
        }
    )
    assert resp.status_code == 200
    patched = await_(get_document(database, 'john_doe'))
    assert passwords.checkpw('katya', patched.pop('hashed'))
    assert patched == original


def test_zero_update(await_, client, database, manage_headers):
    original = await_(get_document(database, 'john_doe'))
    resp = client.patch(
        '/_me',
        headers=manage_headers,
        json={}
    )
    assert resp.status_code == 200
    patched = await_(get_document(database, 'john_doe'))
    assert original == patched
