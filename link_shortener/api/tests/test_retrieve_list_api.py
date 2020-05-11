'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config
from json import loads
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

    def test_retrieve_data(self):
        '''
        Test that a successful get request yields the correct data.
        '''
        headers = {'Bearer': self.token}
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False,
            headers=headers
        )
        data = loads(response.text)
        self.assertEqual(data[1]['endpoint'], 'vlk')

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

    def test_retrieve_wrong_method(self):
        '''
        Test that a PATCH request method yields
        an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        headers = {'Bearer': self.token}
        response = self.app.test_client.patch(
            self.endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-10:], self.endpoint)


class TestRetrieveLinksByStatusAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.active_endpoint = '/api/links/active'
        self.inactive_endpoint = '/api/links/inactive'
        self.headers = {'Bearer': config('ACCESS_TOKEN')}

    def test_retrieve_active_with_token(self):
        '''
        Test that a get request for active links with the correct token
        yields an HTTP_200_OK response.
        '''
        response = self.app.test_client.get(
            self.active_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-17:], self.active_endpoint)

    def test_retrieve_inactive_with_token(self):
        '''
        Test that a get request for inactive links with the correct token
        yields an HTTP_200_OK.
        '''
        response = self.app.test_client.get(
            self.inactive_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-19:], self.inactive_endpoint)

    def test_retrieve_active_data(self):
        '''
        Test that a successful get request for active links yields
        the correct data.
        '''
        response = self.app.test_client.get(
            self.active_endpoint,
            gather_request=False,
            headers=self.headers
        )
        data = loads(response.text)
        self.assertEqual(data[1]['endpoint'], 'vlk')

    def test_retrieve_inactive_data(self):
        '''
        Test that a successful get request for inactive links yields
        the correct data.
        '''
        response = self.app.test_client.get(
            self.inactive_endpoint,
            gather_request=False,
            headers=self.headers
        )
        data = loads(response.text)
        self.assertEqual(data[1]['endpoint'], 'nope')

    def test_retrieve_active_without_token_fails(self):
        '''
        Test that a get request for active links without a token yields
        an HTTP_400_BAD_REQUEST response.
        '''
        response = self.app.test_client.get(
            self.active_endpoint,
            gather_request=False
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-17:], self.active_endpoint)

    def test_retrieve_inactive_without_token_fails(self):
        '''
        Test that a get request for inactive links without a token yields
        an HTTP_400_BAD_REQUEST response.
        '''
        response = self.app.test_client.get(
            self.inactive_endpoint,
            gather_request=False
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-19:], self.inactive_endpoint)

    def test_retrieve_active_wrong_token_fails(self):
        '''
        Test that a get request for active links with an incorrect token
        yields an HTTP_401_UNAUTHORIZED response.
        '''
        bad_token = 'made-up-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.get(
            self.active_endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-17:], self.active_endpoint)

    def test_retrieve_inactive_wrong_token_fails(self):
        '''
        Test that a get request for inactive links with an incorrect token
        yields an HTTP_401_UNAUTHORIZED response.
        '''
        bad_token = 'made-up-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.get(
            self.inactive_endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-19:], self.inactive_endpoint)

    def test_retrieve_active_wrong_method(self):
        '''
        Test that a POST request method for active links yields
        an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.post(
            self.active_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-17:], self.active_endpoint)

    def test_retrieve_inactive_wrong_method(self):
        '''
        Test that a POST request method for inactive links yields
        an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.post(
            self.inactive_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-19:], self.inactive_endpoint)

    def test_retrieve_list_wrong_status(self):
        '''
        Test that a get request for links with non-existing status yields
        an HTTP_400_BAD_REQUEST response.
        '''
        endpoint = '/api/links/error'
        response = self.app.test_client.get(
            endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-16:], endpoint)
