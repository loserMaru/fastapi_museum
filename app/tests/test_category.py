from app.tests.utils import assert_404, get_list_assert


def test_get_list_category(client):
    get_list_assert(client, "/category/", None)


def test_nonexisting_category(client):
    assert_404(client, "/category/", 555)


def test_post_category(client, auth_headers):
    payload = {
        "title": "Test title",
        "description": "Test description"
    }

    response = client.post("/category/", json=payload)

    assert response.status_code == 200

    # Дополнительная проверка что экземпляр действительно был создан
    data = response.json()
    assert data["id"]
    assert data["title"] == payload["title"]


def test_patch_category(client, test_category, auth_headers):
    payload = {
        "title": "Patched title",
        "description": "Patched description"
    }

    response = client.patch(f"/category/{test_category.id}", json=payload, headers=auth_headers)
    assert response.status_code == 200

    # Доп проверка
    data = response.json()
    assert data["id"] == test_category.id
    assert data["title"] == payload["title"]
