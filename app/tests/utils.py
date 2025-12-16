def assert_unauthorized(client, url: str, method: str = "get", json: dict | None = None):
    request = getattr(client, method.lower())
    response = request(url)
    assert response.status_code in (401, 403)


def get_list_assert(client, url: str, headers: dict | None):
    response = client.get(url, headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def assert_404(client, url, index, method: str = "get"):
    request = getattr(client, method.lower())
    response = request(f"{url}/{index}")
    assert response.status_code == 404
