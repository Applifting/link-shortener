'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config
from unittest import TestCase

from link_shortener.server import create_app


class TestStatusSwitchersAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.activate_endpoint = '/api/links/activate'
        self.deactivate_endpoint = '/api/links/deactivate'
        self.headers = {'Bearer': config('ACCESS_TOKEN')}
        self.data = {
            'Year': 2020,
            'Month': 6,
            'Day': 1
        }

    def test_activate_with_token_successful(self):
        '''
        Test that a POST request to activate due links if at least one exists
        with the correct token yields an HTTP_200_OK response.
        '''
        response = self.app.test_client.post(
            self.activate_endpoint,
            gather_request=False,
            headers=self.headers,
            data=self.data
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-19:], self.activate_endpoint)

    def test_deactivate_with_token(self):
        '''
        Test that a POST request to deactivate due links if at least one exists
        with the correct token yields an HTTP_200_OK response.
        '''
        data = {
            'Year': 2020,
            'Month': 5,
            'Day': 6
        }
        response = self.app.test_client.post(
            self.deactivate_endpoint,
            gather_request=False,
            headers=self.headers,
            data=data
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-21:], self.deactivate_endpoint)

    def test_activate_with_token_successful_empty(self):
        '''
        Test that a POST request to activate due links if none exists
        with the correct token yields an HTTP_204_NO_CONTENT response.
        '''
        data = {
            'Year': 2021,
            'Month': 3,
            'Day': 20
        }
        response = self.app.test_client.post(
            self.activate_endpoint,
            gather_request=False,
            headers=self.headers,
            data=data
        )
        self.assertEqual(response.status, 204)
        self.assertEqual(str(response.url)[-19:], self.activate_endpoint)

    def test_deactivate_with_token_successful_empty(self):
        '''
        Test that a POST request to deactivate due links if none exists
        with the correct token yields an HTTP_204_NO_CONTENT response.
        '''
        data = {
            'Year': 2021,
            'Month': 3,
            'Day': 20
        }
        response = self.app.test_client.post(
            self.deactivate_endpoint,
            gather_request=False,
            headers=self.headers,
            data=data
        )
        self.assertEqual(response.status, 204)
        self.assertEqual(str(response.url)[-21:], self.deactivate_endpoint)

    def test_activate_without_token_fails(self):
        '''
        Test that a POST request to activate due links without a token
        yields an HTTP_400_BAD_REQUEST response.
        '''
        response = self.app.test_client.post(
            self.activate_endpoint,
            gather_request=False,
            data=self.data
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-19:], self.activate_endpoint)

    def test_deactivate_without_token_fails(self):
        '''
        Test that a POST request to deactivate due links without a token
        yields an HTTP_400_BAD_REQUEST response.
        '''
        response = self.app.test_client.post(
            self.deactivate_endpoint,
            gather_request=False,
            data=self.data
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-21:], self.deactivate_endpoint)

    def test_activate_wrong_token_fails(self):
        '''
        Test that a POST request to activate due links with an incorrect
        token yields an HTTP_401_UNAUTHORIZED response.
        '''
        bad_token = 'made-up-wrong-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.post(
            self.activate_endpoint,
            gather_request=False,
            headers=headers,
            data=self.data
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-19:], self.activate_endpoint)

    def test_deactivate_wrong_token_fails(self):
        '''
        Test that a POST request to deactivate due links with an incorrect
        token yields an HTTP_401_UNAUTHORIZED response.
        '''
        bad_token = 'made-up-wrong-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.post(
            self.deactivate_endpoint,
            gather_request=False,
            headers=headers,
            data=self.data
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-21:], self.deactivate_endpoint)

    def test_activate_wrong_method_fails(self):
        '''
        Test that a GET request to activate due links yields
        an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.get(
            self.activate_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-19:], self.activate_endpoint)

    def test_deactivate_wrong_method_fails(self):
        '''
        Test that a GET request to deactivate due links yields
        an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.get(
            self.deactivate_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-21:], self.deactivate_endpoint)

    def test_activate_without_date_fails(self):
        '''
        Test that a POST request to activate due links without providing
        a date yields an HTTP_400_BAD_REQUEST response.
        '''
        response = self.app.test_client.post(
            self.activate_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-19:], self.activate_endpoint)

    def test_deactivate_without_date_fails(self):
        '''
        Test that a POST request to deactivate due links without providing
        a date yields an HTTP_400_BAD_REQUEST response.
        '''
        response = self.app.test_client.post(
            self.deactivate_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-21:], self.deactivate_endpoint)

    def test_activate_incorrect_date_format_fails(self):
        '''
        Test that a POST request to activate due links providing an
        incorrectly formatted date yields an HTTP_400_BAD_REQUEST response.
        '''
        data = {
            'Year': 'this',
            'Month': 'is',
            'Day': 'no'
        }
        response = self.app.test_client.post(
            self.activate_endpoint,
            gather_request=False,
            headers=self.headers,
            data=data
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-19:], self.activate_endpoint)

    def test_deactivate_incorrect_date_format_fails(self):
        '''
        Test that a POST request to deactivate due links providing an
        incorrectly formatted date yields an HTTP_400_BAD_REQUEST response.
        '''
        data = {
            'Year': 'this',
            'Month': 'is',
            'Day': 'no'
        }
        response = self.app.test_client.post(
            self.deactivate_endpoint,
            gather_request=False,
            headers=self.headers,
            data=data
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-21:], self.deactivate_endpoint)
