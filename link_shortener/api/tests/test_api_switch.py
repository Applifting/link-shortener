'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config
from unittest import TestCase

from link_shortener.server import create_app


class TestActivateLinkAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.endpoint = '/api/activate/7'
        self.headers = {'Bearer': config('ACCESS_TOKEN')}

    def test_activate_link_correct_request_successful(self):
        '''
        Test that a get request to activate a specific link with the correct
        token yields an HTTP_200_OK response.
        '''
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-15:], self.endpoint)

    def test_activate_link_nonexisting_id_fails(self):
        '''
        Test that a get request to activate a specific link that does not
        exist yields an HTTP_404_NOT_FOUND response.
        '''
        bad_endpoint = '/api/activate/200000'
        response = self.app.test_client.get(
            bad_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 404)
        self.assertEqual(str(response.url)[-20:], bad_endpoint)

    def test_activate_duplicate_link_fails(self):
        '''
        Test that a get request to activate a specific link whose
        endpoint is already used by another active link
        yields an HTTP_400_BAD_REQUEST response.
        '''
        duplicate_endpoint = '/api/activate/9'
        response = self.app.test_client.get(
            duplicate_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-15:], duplicate_endpoint)

    def test_activate_link_without_token_fails(self):
        '''
        Test that a get request to activate a specific link without a token
        yields an HTTP_401_UNAUTHORIZED response.
        '''
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-15:], self.endpoint)

    def test_activate_link_with_wrong_token_fails(self):
        '''
        Test that a get request to activate a specific link with an incorrect
        token yields an HTTP_401_UNAUTHORIZED.
        '''
        bad_token = 'made-up-wrong-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-15:], self.endpoint)

    def test_activate_link_wrong_method_fails(self):
        '''
        Test that a HEAD request to activate a specific link yields
        an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.head(
            self.endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-15:], self.endpoint)


class TestDeactivateLinkAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.endpoint = '/api/deactivate/1'
        self.headers = {'Bearer': config('ACCESS_TOKEN')}

    def test_deactivate_link_with_token_successful(self):
        '''
        Test that a get request to deactivate a specific link with the correct
        token yields an HTTP_200_OK response.
        '''
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-17:], self.endpoint)

    def test_deactivate_link_nonexisting_id_fails(self):
        '''
        Test that a get request to deactivate a specific link that does not
        exist yields an HTTP_404_NOT_FOUND response.
        '''
        bad_endpoint = '/api/deactivate/200000'
        response = self.app.test_client.get(
            bad_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 404)
        self.assertEqual(str(response.url)[-22:], bad_endpoint)

    def test_deactivate_link_without_token_fails(self):
        '''
        Test that a get request to deactivate a specific link without a token
        yields an HTTP_401_UNAUTHORIZED response.
        '''
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-17:], self.endpoint)

    def test_deactivate_link_with_wrong_token_fails(self):
        '''
        Test that a get request to deactivate a specific link with an incorrect
        token yields an HTTP_401_UNAUTHORIZED.
        '''
        bad_token = 'made-up-wrong-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-17:], self.endpoint)

    def test_deactivate_link_wrong_method_fails(self):
        '''
        Test that a HEAD request to deactivate a specific link yields
        an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.head(
            self.endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-17:], self.endpoint)
