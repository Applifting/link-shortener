'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config
from unittest import TestCase

from link_shortener.server import create_app


class TestRetrieveAllLinksAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.endpoint = '/api/links'
        self.token = config('ACCESS_TOKEN')

    def test_retrieve_with_token(self):
        '''
        Test that a get request with the correct token yields
        an HTTP_200_OK response.
        '''
        headers = {'Bearer': self.token}
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-10:], self.endpoint)

    def test_retrieve_without_token_fails(self):
        '''
        Test that a get request without a token yields
        an HTTP_400_BAD_REQUEST response.
        '''
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-10:], self.endpoint)

    def test_retrieve_wrong_token_fails(self):
        '''
        Test that a get request with an incorrect token yields
        an HTTP_401_UNAUTHORIZED response.
        '''
        bad_token = 'made-up-wrong-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-10:], self.endpoint)

    def test_wrong_method(self):
        '''
        Test that a POST request method yields
        an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        headers = {'Bearer': self.token}
        response = self.app.test_client.post(
            self.endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-10:], self.endpoint)
