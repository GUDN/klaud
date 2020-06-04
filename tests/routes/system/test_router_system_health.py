def test_health_ok(client):
    resp = client.get('/_sys/health')
    assert resp.status_code == 200
    assert all(resp.json().values())
