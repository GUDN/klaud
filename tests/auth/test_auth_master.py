from klaud.settings import settings


def test_master_wrong_scope(client):
    resp = client.post(
        '/_token',
        data={
            'grant_type': 'password',
            'username': settings.master_name,
            'password': settings.master_password
        }
    )
    assert resp.status_code == 200
    token = resp.json()['access_token']
    resp = client.get(
        '/_master/',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )
    assert resp.status_code == 403


def test_master_right_scope(client):
    resp = client.post(
        '/_token',
        data={
            'grant_type': 'password',
            'scope': 'master',
            'username': settings.master_name,
            'password': settings.master_password
        }
    )
    assert resp.status_code == 200
    token = resp.json()['access_token']
    resp = client.get(
        '/_master/',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )
    assert resp.status_code == 200
