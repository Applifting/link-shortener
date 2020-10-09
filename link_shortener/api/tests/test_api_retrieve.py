'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from unittest import TestCase
from json import loads

from decouple import config

from link_shortener.server import create_app


class TestRetrieveLinksAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.endpoint = '/api/links'
        self.headers = {'Bearer': config('ACCESS_TOKEN')}

    def test_get_list_correct_request_successful(self):
        '''
        Test that a get request for a list of all links with the correct token
        yields an HTTP_200_OK response and the correct data.
        '''
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-10:], self.endpoint)

        data = loads(response.text)
        self.assertEqual(data[1]['endpoint'], 'vlk')

    def test_get_list_without_token_fails(self):
        '''
        Test that a get request for a list of all links without a token
        yields an HTTP_401_UNAUTHORIZED response.
        '''
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-10:], self.endpoint)

    def test_get_list_with_wrong_token_fails(self):
        '''
        Test that a get request for a list of all links with an incorrect
        token yields an HTTP_401_UNAUTHORIZED response.
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

    def test_get_list_wrong_method_fails(self):
        '''
        Test that a HEAD request method for a list of all links yields
        an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.head(
            self.endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-10:], self.endpoint)


class TestRetrieveLinkAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.endpoint = '/api/link/2'
        self.headers = {'Bearer': config('ACCESS_TOKEN')}

    def test_get_detail_with_token_successful(self):
        '''
        Test that a get request for a specific link with the correct token
        yields an HTTP_200_OK response and the correct data.
        '''
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-11:], self.endpoint)

        data = loads(response.text)
        self.assertEqual(data['endpoint'], 'vlk')

    def test_get_detail_nonexisting_id_fails(self):
        '''
        Test that a get request for a specific link that does not exist
        yields an HTTP_404_NOT_FOUND response.
        '''
        bad_endpoint = '/api/link/200000'
        response = self.app.test_client.get(
            bad_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 404)
        self.assertEqual(str(response.url)[-16:], bad_endpoint)

    def test_get_detail_without_token_fails(self):
        '''
        Test that a get request for a specific link without a token
        yields an HTTP_401 response.
        '''
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-11:], self.endpoint)

    def test_get_detail_with_wrong_token_fails(self):
        '''
        Test that a get request for a specific link with an incorrect
        token yields an HTTP_401_UNAUTHORIZED response.
        '''
        bad_token = 'made-up-wrong-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-11:], self.endpoint)

    def test_get_detail_wrong_method_fails(self):
        '''
        Test that a HEAD request method for a specific link yields
        an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.head(
            self.endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-11:], self.endpoint)
