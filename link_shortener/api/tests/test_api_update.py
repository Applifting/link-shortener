'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config
from unittest import TestCase
from json import dumps, loads

from link_shortener.server import create_app


class TestUpdateLinkAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.endpoint = '/api/link/4'
        self.headers = {'Bearer': config('ACCESS_TOKEN')}
        self.data = {
            'url': 'http://www.vlk.cz',
            'switch_date': {
                'Year': 2022,
                'Month': 2,
                'Day': 17
            }
        }

    def test_put_data_correct_payload_is_successful(self):
        '''
        Test that a put request to update an existing link with the correct
        data and token yields an HTTP_200_OK response.
        '''
        response = self.app.test_client.put(
            self.endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(self.data)
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-11:], self.endpoint)

        message = 'Link updated successfully'
        self.assertEqual(loads(response.text)['message'], message)

    def test_put_data_correct_payload_output_check(self):
        '''
        Test that a get request for a link updated in the test above
        yields the correct updated data.
        '''
        response = self.app.test_client.get(
            self.endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-11:], self.endpoint)

        link_data = loads(response.text)
        self.assertEqual(link_data['url'], self.data['url'])

    def test_put_data_incomplete_payload_fails(self):
        '''
        Test that a put request to update an existing link with missing
        data yields an HTTP_400_BAD_REQUEST response.
        '''
        data = {}
        response = self.app.test_client.put(
            self.endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(data)
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-11:], self.endpoint)

        message = 'Please provide all data. Missing: url'
        self.assertEqual(loads(response.text)['message'], message)

    def test_put_data_incorrect_payload_fails(self):
        '''
        Test that a put request to update an existing link with incorrect
        data yields an HTTP_400_BAD_REQUEST response.
        '''
        data = {
            'url': 'http://www.vlk.cz',
            'switch_date': {
                'Year': 'incorrectly formated data',
                'Month': 2,
                'Day': 17
            }
        }
        response = self.app.test_client.put(
            self.endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(data)
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-11:], self.endpoint)

        message = 'Please provide correctly formatted data'
        self.assertEqual(loads(response.text)['message'], message)

    def test_put_data_nonexisting_id_fails(self):
        '''
        Test that a put request to update a link that does not exist
        yields an HTTP_404_NOT_FOUND response.
        '''
        endpoint = self.endpoint + '00000'
        response = self.app.test_client.put(
            endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(self.data)
        )
        self.assertEqual(response.status, 404)
        self.assertEqual(str(response.url)[-16:], endpoint)

        message = 'Link does not exist'
        self.assertEqual(loads(response.text)['message'], message)

    def test_put_data_without_token_fails(self):
        '''
        Test that a put request to update an existing link without a token
        yields an HTTP_401_UNAUTHORIZED response.
        '''
        response = self.app.test_client.put(
            self.endpoint,
            gather_request=False,
            data=dumps(self.data)
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-11:], self.endpoint)

        message = 'Unauthorized'
        self.assertEqual(loads(response.text)['message'], message)

    def test_put_data_with_wrong_token_fails(self):
        '''
        Test that a put request to update an existing link with an incorrect
        token yields an HTTP_401_UNAUTHORIZED response.
        '''
        bad_token = 'made-up-wrong-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.put(
            self.endpoint,
            gather_request=False,
            headers=headers,
            data=dumps(self.data)
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-11:], self.endpoint)

        message = 'Unauthorized'
        self.assertEqual(loads(response.text)['message'], message)

    def test_put_data_wrong_method_fails(self):
        '''
        Test that a PATCH request method to update an existing link
        yields an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.patch(
            self.endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(self.data)
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-11:], self.endpoint)
