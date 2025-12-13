from app.tests.utils import assert_unauthorized


def test_get_exhibits(client, auth_headers):
    response = client.get("/exhibit/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_exhibits_unauthorized(client):
    response = client.get("/exhibit/")  # без токена
    assert response.status_code == 403


def test_create_exhibit_unauthorized(client):
    assert_unauthorized(
        client,
        "/exhibit/",
        "POST",
        json={
            "title": "test",
            "description": "test",
            "category_id": 1
        }
    )
