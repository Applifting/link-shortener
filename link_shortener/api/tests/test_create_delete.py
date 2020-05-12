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


class TestDeleteByIdAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.active_endpoint = '/api/link/active/6'
        self.inactive_endpoint = '/api/link/inactive/2'
        self.headers = {'Bearer': config('ACCESS_TOKEN')}

    def test_delete_active_correct_request_successful(self):
        '''
        Test that a DELETE request to delete an existing active link with
        the correct token yields an HTTP_204_NO_CONTENT response.
        '''
        response = self.app.test_client.delete(
            self.active_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 204)
        self.assertEqual(str(response.url)[-18:], self.active_endpoint)

    def test_delete_inactive_correct_request_successful(self):
        '''
        Test that a DELETE request to delete an existing inactive link with
        the correct token yields an HTTP_204_NO_CONTENT response.
        '''
        response = self.app.test_client.delete(
            self.inactive_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 204)
        self.assertEqual(str(response.url)[-20:], self.inactive_endpoint)

    def test_delete_active_without_token_fails(self):
        '''
        Test that a DELETE request to delete an active link without
        a token yields an HTTP_400_BAD_REQUEST response.
        '''
        response = self.app.test_client.delete(
            self.active_endpoint,
            gather_request=False
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-18:], self.active_endpoint)

    def test_delete_inactive_without_token_fails(self):
        '''
        Test that a DELETE request to delete an inactive link without
        a token yields an HTTP_400_BAD_REQUEST response.
        '''
        response = self.app.test_client.delete(
            self.inactive_endpoint,
            gather_request=False
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-20:], self.inactive_endpoint)

    def test_delete_active_wrong_token_fails(self):
        '''
        Test that a DELETE request to delete an active link with
        an incorrect token yields an HTTP_401_UNAUTHORIZED response.
        '''
        bad_token = 'made-up-wrong-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.delete(
            self.active_endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-18:], self.active_endpoint)

    def test_delete_inactive_wrong_token_fails(self):
        '''
        Test that a DELETE request to delete an inactive link with
        an incorrect token yields an HTTP_401_UNAUTHORIZED response.
        '''
        bad_token = 'made-up-wrong-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.delete(
            self.inactive_endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-20:], self.inactive_endpoint)

    def test_delete_active_wrong_method_fails(self):
        '''
        Test that a HEAD request method to delete an active link
        yields an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.head(
            self.active_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-18:], self.active_endpoint)

    def test_delete_inactive_wrong_method_fails(self):
        '''
        Test that a PATCH request method to delete an inactive link
        yields an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.head(
            self.inactive_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-20:], self.inactive_endpoint)

    def test_delete_wrong_status_fails(self):
        '''
        Test that a DELETE request to delete a link with non-existing
        status yields an HTTP_400_BAD_REQUEST response.
        '''
        endpoint = '/api/link/offline/1'
        response = self.app.test_client.delete(
            endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-19:], endpoint)

    def test_delete_active_nonexisting_fails(self):
        '''
        Test that a DELETE request to delete an active link that
        does not exist yields an HTTP_404_NOT_FOUND response.
        '''
        endpoint = '/api/link/active/1000'
        response = self.app.test_client.delete(
            endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 404)
        self.assertEqual(str(response.url)[-21:], endpoint)

    def test_delete_inactive_nonexisting_fails(self):
        '''
        Test that a DELETE request to delete an inactive link that
        does not exist yields an HTTP_404_NOT_FOUND response.
        '''
        endpoint = '/api/link/inactive/1000'
        response = self.app.test_client.delete(
            endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 404)
        self.assertEqual(str(response.url)[-23:], endpoint)
