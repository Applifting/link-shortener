'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config
from unittest import TestCase
from json import loads, dumps

from link_shortener.server import create_app


class TestCreateLinkAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.endpoint = '/api/links'
        self.headers = {'Bearer': config('ACCESS_TOKEN')}
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

    def test_post_correct_payload_is_successful(self):
        '''
        Test that a post request to create a new active link with the correct
        data and token yields an HTTP_201_CREATED response.
        '''
        response = self.app.test_client.post(
            self.endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(self.data)
        )
        self.assertEqual(response.status, 201)
        self.assertEqual(str(response.url)[-10:], self.endpoint)

    def test_post_correct_payload_output_check(self):
        '''
        Test that a get request for a link created in the test above
        yields the correct data.
        '''
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-10:], self.endpoint)

        endpoint_list = [link['endpoint'] for link in loads(response.text)]
        self.assertIn(self.data['endpoint'], endpoint_list)

    def test_post_incomplete_payload_fails(self):
        '''
        Test that a post request to create a new active link with missing
        data yields an HTTP_400_BAD_REQUEST response.
        '''
        data = {
            'endpoint': 'no data for you'
        }
        response = self.app.test_client.post(
            self.endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(data)
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-10:], self.endpoint)

        message = 'Please provide all data. Missing: owner'
        self.assertEqual(loads(response.text)['message'], message)

    def test_post_incorrect_payload_fails(self):
        '''
        Test that a post request to create a new active link with incorrect
        data yields an HTTP_400_BAD_REQUEST response.
        '''
        data = {
            'owner': 'test.user@applifting.cz',
            'owner_id': '1234567890',
            'endpoint': 'new-endpoint',
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

        message = 'Please provide correctly formatted data'
        self.assertEqual(loads(response.text)['message'], message)

    def test_post_duplicate_data_fails(self):
        '''
        Test that a post request to create a new active link with endpoint
        that already exists yields an HTTP_409_CONFLICT response.
        '''
        data = {
            'owner': 'test.user@applifting.cz',
            'owner_id': '1234567890',
            'endpoint': 'vlk',
            'url': 'http://www.vlk.cz',
            'switch_date': {
                'Year': 2021,
                'Month': 1,
                'Day': 8
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

    def test_post_data_without_token_fails(self):
        '''
        Test that a post request to create a new active link without a token
        yields an HTTP_401_UNAUTHORIZED response.
        '''
        response = self.app.test_client.post(
            self.endpoint,
            gather_request=False,
            data=dumps(self.data)
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-10:], self.endpoint)

    def test_post_data_with_wrong_token_fails(self):
        '''
        Test that a post request to create a new active link with an incorrect
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

    def test_post_data_wrong_method_fails(self):
        '''
        Test that a PATCH request method to create a new active link
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
