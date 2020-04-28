import pytest

from unittest import TestCase

from link_shortener.server import create_app


class TestViews(TestCase):

    def setUp(self):
        self.app = create_app()

    def test_getting_about_page(self):
        '''
        Test that getting the about page is successful.
        '''
        response = self.app.test_client.get(
            '/links/about',
            gather_request=False
        )
        self.assertEqual(response.status, 200)

    def test_getting_landing_page(self):
        '''
        Test that getting the landing page is successful.
        '''
        response = self.app.test_client.get(
            '/',
            gather_request=False
        )
        self.assertEqual(response.status, 200)

    def test_existing_endpoint_redirect(self):
        '''
        Test that using an existing endpoint is successful.
        '''
        response = self.app.test_client.get(
            '/vlk',
            gather_request=False
        )
        self.assertEqual(response.status, 200)

    def test_wrong_endpoint_redirect(self):
        '''
        Test that using a non-existing endpoint fails.
        '''
        response = self.app.test_client.get(
            '/nevlk',
            gather_request=False
        )
        self.assertEqual(response.status, 400)
