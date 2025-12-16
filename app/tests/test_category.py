from app.tests.utils import assert_404, get_list_assert


def test_get_list_category(client):
    get_list_assert(client, "/category/", None)

def test_nonexisting_category(client):
    assert_404(client, "/category/", 555)