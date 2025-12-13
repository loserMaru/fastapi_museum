def assert_unauthorized(client, url: str, method: str = "get", json: dict | None = None):
    request = getattr(client, method.lower())
    response = request(url, json=json)
    assert response.status_code in (401, 403)