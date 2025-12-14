def assert_unauthorized(client, url: str, method: str = "get", json: dict | None = None):
    request = getattr(client, method.lower())
    response = request(url)
    assert response.status_code in (401, 403)


def assert_404(client, url, index, method: str = "get"):
    request = getattr(client, method.lower())
    response = request(f"{url}/{index}")
    assert response.status_code == 404