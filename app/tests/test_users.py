from app.tests.utils import get_list_assert, assert_unauthorized


def test_get_users(client, auth_headers):
    get_list_assert(client, "/user/", auth_headers)


def test_get_users_unauthorized(client):
    assert_unauthorized(client, "/user/")


def test_post_user(client):
    payload = {
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "strongpassword123"
    }

    response = client.post("/user/", json=payload)

    assert response.status_code in (200, 201)

    data = response.json()
    assert "id" in data
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert "password" not in data
