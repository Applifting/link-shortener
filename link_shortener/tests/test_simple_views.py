import pytest

from unittest import TestCase

from link_shortener.server import create_app


class TestViews(TestCase):

    def setUp(self):
        self.app = create_app()

    def test_about_page(self):
        request, response = self.app.test_client.get('/links/about')
        self.assertEqual(response.status, 200)

    def test_landing_page(self):
        request, response = self.app.test_client.get('/')
        self.assertEqual(response.status, 200)
