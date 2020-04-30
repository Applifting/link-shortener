'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config
from unittest import TestCase

from json import loads

from link_shortener.server import create_app


class TestRetrieveDetailAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.active_endpoint = '/api/links/active/1'
        self.inactive_endpoint = '/api/links/inactive/1'
        self.token = config('ACCESS_TOKEN')

    def test_active_detail_with_token(self):
        '''
        Test that a get detail request for an active link with the correct
        token yields an HTTP_200_OK response.
        '''
        headers = {'Bearer': self.token}
        response = self.app.test_client.get(
            self.active_endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-19:], self.active_endpoint)

    def test_inactive_detail_with_token(self):
        '''
        Test that a get detail request for an inactive link with the correct
        token yields an HTTP_200_OK response.
        '''
        headers = {'Bearer': self.token}
        response = self.app.test_client.get(
            self.inactive_endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-21:], self.inactive_endpoint)

    def test_detail_without_token_fails(self):
        '''
        Test that a get detail request without a token yields
        an HTTP_400_BAD_REQUEST response.
        '''
        response = self.app.test_client.get(
            self.active_endpoint,
            gather_request=False
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-19:], self.active_endpoint)

    def test_detail_wrong_token_fails(self):
        '''
        Test that a get detail request with an incorrect token yields
        an HTTP_401_UNAUTHORIZED response.
        '''
        bad_token = 'made-up-wrong-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.get(
            self.active_endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-19:], self.active_endpoint)

    def test_active_detail_wrong_method(self):
        '''
        Test that a POST request method for an active link yields
        an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        headers = {'Bearer': self.token}
        response = self.app.test_client.post(
            self.active_endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-19:], self.active_endpoint)

    def test_inactive_detail_wrong_method(self):
        '''
        Test that a POST request method for an inactive link yields
        an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        headers = {'Bearer': self.token}
        response = self.app.test_client.post(
            self.inactive_endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-21:], self.inactive_endpoint)

    def test_detail_wrong_status(self):
        '''
        Test that a get detail request for links with non-existing status
        yields an HTTP_400_BAD_REQUEST response.
        '''
        endpoint = '/api/links/offline/1'
        headers = {'Bearer': self.token}
        response = self.app.test_client.get(
            endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-20:], endpoint)

    def test_active_detail_wrong_id(self):
        '''
        Test that a get detail request for an active link that does not exist
        yields an HTTP_404_NOT_FOUND response.
        '''
        headers = {'Bearer': self.token}
        endpoint = '/api/links/active/1000000'
        response = self.app.test_client.get(
            endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 404)
        self.assertEqual(str(response.url)[-25:], endpoint)

    def test_inactive_detail_wrong_id(self):
        '''
        Test that a get detail request for an inactive link that does not exist
        yields an HTTP_404_NOT_FOUND response.
        '''
        headers = {'Bearer': self.token}
        endpoint = '/api/links/inactive/1000000'
        response = self.app.test_client.get(
            endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 404)
        self.assertEqual(str(response.url)[-27:], endpoint)

    def test_active_detail_payload(self):
        '''
        Test that a successful get detail request for an active link
        yields the correct payload.
        '''
        headers = {'Bearer': self.token}
        response = self.app.test_client.get(
            self.active_endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(loads(loads(response.text))['id'], 1)

    def test_inactive_detail_payload(self):
        '''
        Test that a successful get detail request for an inactive link
        yields the correct payload.
        '''
        headers = {'Bearer': self.token}
        response = self.app.test_client.get(
            self.inactive_endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(loads(loads(response.text))['id'], 1)
