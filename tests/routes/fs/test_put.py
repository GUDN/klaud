from io import BytesIO


def test_base_put(await_, client, database, john_doe_headers):
    resp = client.put(
        '/some/path',
        headers=john_doe_headers,
        files=[
            ('file_parts', ('filename', BytesIO(b'Hello, World!'), 'text/plain'))
        ]
    )
    assert resp.status_code == 201
    assert resp.json() == {
        'path': '/some/path',
        'owner': 'john_doe',
        'length': len(b'Hello, World!'),
        'content_type': 'text/plain'
    }
    doc = await_(database['fs.files'].find_one({
        'filename': '@john_doe/some/path'
    }))
    assert doc
    assert doc['metadata']['content_type'] == 'text/plain'
    assert doc['length'] == len(b'Hello, World!')


def test_multiply_put(await_, client, database, john_doe_headers):
    resp = client.put(
        '/some/path',
        headers=john_doe_headers,
        files=[
            ('file_parts', ('filename', BytesIO(b'H'), 'text/plain')),
            ('file_parts', ('filename', BytesIO(b'e'), 'text/plain')),
            ('file_parts', ('filename', BytesIO(b'l'), 'text/plain')),
            ('file_parts', ('filename', BytesIO(b'l'), 'text/plain')),
            ('file_parts', ('filename', BytesIO(b'o'), 'text/plain')),
            ('file_parts', ('filename', BytesIO(b','), 'text/plain')),
            ('file_parts', ('filename', BytesIO(b' '), 'text/plain')),
            ('file_parts', ('filename', BytesIO(b'W'), 'text/plain')),
            ('file_parts', ('filename', BytesIO(b'o'), 'text/plain')),
            ('file_parts', ('filename', BytesIO(b'r'), 'text/plain')),
            ('file_parts', ('filename', BytesIO(b'l'), 'text/plain')),
            ('file_parts', ('filename', BytesIO(b'd'), 'text/plain')),
            ('file_parts', ('filename', BytesIO(b'!'), 'text/plain'))
        ]
    )
    assert resp.status_code == 201
    assert resp.json() == {
        'path': '/some/path',
        'owner': 'john_doe',
        'length': len(b'Hello, World!'),
        'content_type': 'text/plain'
    }
    doc = await_(database['fs.files'].find_one({
        'filename': '@john_doe/some/path'
    }))
    assert doc
    assert doc['metadata']['content_type'] == 'text/plain'
    assert doc['length'] == len(b'Hello, World!')


def test_rewrite(await_, client, database, john_doe_headers):
    resp = client.put(
        '/some/path',
        headers=john_doe_headers,
        files=[
            ('file_parts', ('filename', BytesIO(b'Hello, World!'), 'text/plain'))
        ]
    )
    assert resp.status_code == 201
    assert resp.json() == {
        'path': '/some/path',
        'owner': 'john_doe',
        'length': len(b'Hello, World!'),
        'content_type': 'text/plain'
    }
    doc = await_(database['fs.files'].find_one({
        'filename': '@john_doe/some/path'
    }))
    assert doc
    assert doc['metadata']['content_type'] == 'text/plain'
    assert doc['length'] == len(b'Hello, World!')
    resp = client.put(
        '/some/path',
        headers=john_doe_headers,
        files=[
            ('file_parts', ('filename', BytesIO(b'Hello, John!'), 'text/plain'))
        ]
    )
    assert resp.status_code == 201
    assert resp.json() == {
        'path': '/some/path',
        'owner': 'john_doe',
        'length': len(b'Hello, John!'),
        'content_type': 'text/plain'
    }
    doc = await_(database['fs.files'].find_one({
        'filename': '@john_doe/some/path'
    }))
    assert doc
    assert doc['metadata']['content_type'] == 'text/plain'
    assert doc['length'] == len(b'John, World!')


def test_bad_content_type(client, john_doe_headers):
    resp = client.put(
        '/some/path',
        headers=john_doe_headers,
        files=[
            ('file_parts', ('filename', BytesIO(b'H'), 'text/plain')),
            ('file_parts', ('filename', BytesIO(b'!'), 'text/x-python'))
        ]
    )
    assert resp.status_code == 400
