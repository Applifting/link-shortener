'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from unittest import TestCase
from json import loads

from decouple import config

from link_shortener.server import create_app


class TestRedirectLinkAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.endpoint = '/api/vlk'
        self.headers = {'Bearer': config('ACCESS_TOKEN')}
        self.url = 'http://www.vlk.cz'

    def test_get_target_url_request_successful(self):
        '''
        Test that a get request for target url corresponding to the input
        endpoint with the correct token yields an HTTP_200_OK response
        and the correct data.
        '''
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-8:], self.endpoint)
        self.assertEqual(loads(response.text)['url'], self.url)

    def test_get_target_url_nonexisting_endpoint_fails(self):
        '''
        Test that a get request for target url corresponding to an endpoint
        that does not exist yields an HTTP_404_NOT_FOUND response.
        '''
        bad_endpoint = '/api/notvlk'
        response = self.app.test_client.get(
            bad_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 404)
        self.assertEqual(str(response.url)[-11:], bad_endpoint)

        message = 'Link inactive or does not exist'
        self.assertEqual(loads(response.text)['message'], message)

    def test_get_target_url_without_token_fails(self):
        '''
        Test that a get request for target url corresponding to the input
        endpoint without a token yields and HTTP_401_UNAUTHORIZED response.
        '''
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-8:], self.endpoint)

        message = 'Unauthorized'
        self.assertEqual(loads(response.text)['message'], message)

    def test_get_target_url_wrong_token_fails(self):
        '''
        Test that a get request for target url corresponding to the input
        endpoint with an incorrect token yields an HTTP_401_UNAUTHORIZED
        response.
        '''
        bad_token = 'made-up-wrong-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-8:], self.endpoint)

        message = 'Unauthorized'
        self.assertEqual(loads(response.text)['message'], message)

    def test_get_target_url_wrong_method_fails(self):
        '''
        Test that a HEAD request method for target url corresponding
        to the input endpoint yields an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.head(
            self.endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-8:], self.endpoint)
