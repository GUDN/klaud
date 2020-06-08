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


def test_delete(await_, client, database, john_doe_headers):
    resp = client.delete(
        'some/path',
        headers=john_doe_headers
    )
    assert resp.status_code == 200
    assert await_(database['fs.files'].count_documents({
        'filename': '@john_doe/some/path'
    })) == 0


def test_not_found(client, john_doe_headers):
    resp = client.delete(
        'some/anothed/path',
        headers=john_doe_headers
    )
    assert resp.status_code == 404
