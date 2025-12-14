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
