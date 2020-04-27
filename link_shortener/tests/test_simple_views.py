import pytest
from link_shortener.server import app


def test_about_page():
    request, response = app.test_client.get('/links/about')
    assert response.status == 200
