from app.tests.utils import assert_404


def test_nonexisting_category(client):
    assert_404(client, "/category/", 555)