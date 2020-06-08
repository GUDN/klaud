from io import BytesIO

import pytest


@pytest.fixture(scope='function', autouse=True)
def make_file(client, john_doe_headers):
    client.put(
        'some/path',
        headers=john_doe_headers,
        files=[
            ('file_parts', ('filename', BytesIO(b'Hello, World!'), 'text/plain'))
        ]
    )


def test_get(client, john_doe_headers):
    resp = client.get(
        'some/path',
        headers=john_doe_headers
    )
    assert resp.status_code == 200
    assert resp.text == 'Hello, World!'


def test_not_found(client, john_doe_headers):
    resp = client.get(
        'some/another/path',
        headers=john_doe_headers
    )
    assert resp.status_code == 404
