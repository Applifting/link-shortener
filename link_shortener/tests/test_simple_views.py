'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import pytest

from unittest import TestCase

from link_shortener.server import create_app


class TestSimpleViews(TestCase):

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
        self.assertEqual(str(response.url)[-12:], '/links/about')

    def test_getting_landing_page(self):
        '''
        Test that getting the landing page is successful.
        '''
        response = self.app.test_client.get(
            '/',
            gather_request=False
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-12:], '/links/about')

    def test_existing_endpoint_redirect(self):
        '''
        Test that using an existing endpoint is successful.
        '''
        response = self.app.test_client.get(
            '/vlk',
            gather_request=False
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url), 'http://www.vlk.cz')

    def test_wrong_endpoint_redirect(self):
        '''
        Test that using a non-existing endpoint fails.
        '''
        response = self.app.test_client.get(
            '/nevlk',
            gather_request=False
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-6:], '/nevlk')
