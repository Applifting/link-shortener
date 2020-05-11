'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config
from unittest import TestCase
from json import dumps

from link_shortener.server import create_app


class TestCreateAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.endpoint = '/api/links'
        self.headers = {
            'Content-Type': 'application/json',
            'Bearer': config('ACCESS_TOKEN')
        }
        self.data = {
            'owner': 'test.user@applifting.cz',
            'owner_id': '1234567890',
            'endpoint': 'google',
            'url': 'https://google.com',
            'switch_date': {
                'Year': 2020,
                'Month': 6,
                'Day': 10
            }
        }

    def test_create_correct_request_successful(self):
        '''
        Test that a POST request to create a new link with the correct token
        and payload data yields an HTTP_201_CREATED response.
        '''
        response = self.app.test_client.post(
            self.endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(self.data)
        )
        self.assertEqual(response.status, 201)
        self.assertEqual(str(response.url)[-10:], self.endpoint)

    def test_create_existing_fails(self):
        '''
        Test that a POST request to create a link with endpoint that already
        exists yields an HTTP_409_CONFLICT response.
        '''
        data = {
            'owner': 'test.user@applifting.cz',
            'owner_id': '1234567890',
            'endpoint': 'vlk',
            'url': 'http://www.vlk.cz',
            'switch_date': {
                'Year': 2020,
                'Month': 6,
                'Day': 10
            }
        }
        response = self.app.test_client.post(
            self.endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(data)
        )
        self.assertEqual(response.status, 409)
        self.assertEqual(str(response.url)[-10:], self.endpoint)

    def test_create_with_incorrect_payload_fails(self):
        '''
        Test that a POST request to create a link with an incorrect payload
        yields an HTTP_400_BAD_REQUEST response.
        '''
        data = {
            'owner': 'test.user@applifting.cz',
            'owner_id': '1234567890',
            'endpoint': 'unique-endpoint',
            'url': 'http://www.vlk.cz',
            'switch_date': {
                'Year': 'wrong year format',
                'Month': 6,
                'Day': 10
            }
        }
        response = self.app.test_client.post(
            self.endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(data)
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-10:], self.endpoint)

    def test_create_with_incomplete_payload_fails(self):
        '''
        Test that a POST request to create a link with an incomplete payload
        yields an HTTP_400_BAD_REQUEST response.
        '''
        data = {
            'endpoint': 'even-more-unique-endpoint'
        }
        response = self.app.test_client.post(
            self.endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(data)
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-10:], self.endpoint)

    def test_create_without_token_fails(self):
        '''
        Test that a POST request to create a link without a token
        yields an HTTP_400_BAD_REQUEST response.
        '''
        response = self.app.test_client.post(
            self.endpoint,
            gather_request=False,
            data=dumps(self.data)
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-10:], self.endpoint)

    def test_create_wrong_token_fails(self):
        '''
        Test that a POST request to create a link with an incorrect
        token yields an HTTP_401_UNAUTHORIZED response.
        '''
        bad_token = 'made-up-wrong-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.post(
            self.endpoint,
            gather_request=False,
            headers=headers,
            data=dumps(self.data)
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-10:], self.endpoint)

    def test_create_wrong_method_fails(self):
        '''
        Test that a PATCH request method to create a link
        yields an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.patch(
            self.endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(self.data)
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-10:], self.endpoint)
