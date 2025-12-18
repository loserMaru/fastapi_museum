from app.tests.utils import assert_unauthorized, assert_404


def test_get_exhibits_unauthorized(client):
    assert_unauthorized(client, url="/exhibit/")


def test_get_exhibits(client, auth_headers):
    response = client.get("/exhibit/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_nonexisting_category(client):
    assert_404(client, "/category/", 555)


def test_create_exhibit_unauthorized(client):
    assert_unauthorized(
        client,
        "/exhibit/",
        "POST",
    )


def test_patch_exhibit(client, test_exhibit, auth_headers):
    payload = {
        "title": "Patched title",
        "description": "Patched description",
    }

    response = client.patch(f"/exhibit/{test_exhibit.id}", data=payload, headers=auth_headers)

    assert response.status_code == 200

    # Доп проверка
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
