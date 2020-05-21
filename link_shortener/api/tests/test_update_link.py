'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config
from unittest import TestCase

from json import dumps, loads

from link_shortener.server import create_app


class TestUpdateLinkByIdAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.active_endpoint = '/api/link/active/4'
        self.inactive_endpoint = '/api/link/inactive/3'
        self.headers = {'Bearer': config('ACCESS_TOKEN')}
        self.data = dumps({'url': 'test-url'})

    def test_update_active_link_by_id_with_token_successful(self):
        '''
        Test that a put request to update an active link specified by id with
        the correct token and data yields an HTTP_200_OK response.
        '''
        response = self.app.test_client.put(
            self.active_endpoint,
            gather_request=False,
            headers=self.headers,
            data=self.data
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-18:], self.active_endpoint)

    def test_update_inactive_link_by_id_with_token_successful(self):
        '''
        Test that a put request to update an inactive link specified by id with
        the correct token and data yields an HTTP_200_OK response.
        '''
        response = self.app.test_client.put(
            self.inactive_endpoint,
            gather_request=False,
            headers=self.headers,
            data=self.data
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-20:], self.inactive_endpoint)

    def test_update_active_link_by_id_without_token_fails(self):
        '''
        Test that a put request to update an active link specified by id
        without a token yield an HTTP_400_BAD_REQUEST response.
        '''
        response = self.app.test_client.put(
            self.active_endpoint,
            gather_request=False,
            data=self.data
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-18:], self.active_endpoint)

    def test_update_inactive_link_by_id_without_token_fails(self):
        '''
        Test that a put request to update an inactive link specified by id
        without a token yields an HTTP_400_BAD_REQUEST response.
        '''
        response = self.app.test_client.put(
            self.inactive_endpoint,
            gather_request=False,
            data=self.data
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-20:], self.inactive_endpoint)

    def test_update_active_link_by_id_wrong_token_fails(self):
        '''
        Test that a put request to update an active link specified by id with
        an incorrect token yields an HTTP_401_UNAUTHORIZED response.
        '''
        bad_token = 'made-up-wrong-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.put(
            self.active_endpoint,
            gather_request=False,
            headers=headers,
            data=self.data
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-18:], self.active_endpoint)

    def test_update_inactive_link_by_id_wrong_token_fails(self):
        '''
        Test that a put request to update an inactive link specified by id with
        an incorrect token yields an HTTP_401_UNAUTHORIZED response.
        '''
        bad_token = 'made-up-wrong-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.put(
            self.inactive_endpoint,
            gather_request=False,
            headers=headers,
            data=self.data
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-20:], self.inactive_endpoint)

    def test_update_active_link_by_id_wrong_method_fails(self):
        '''
        Test that a POST request method to update an active link specified
        by id yields an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.post(
            self.active_endpoint,
            gather_request=False,
            headers=self.headers,
            data=self.data
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-18:], self.active_endpoint)

    def test_update_inactive_link_by_id_wrong_method_fails(self):
        '''
        Test that a POST request method to update an inactive link specified
        by id yields an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.post(
            self.inactive_endpoint,
            gather_request=False,
            headers=self.headers,
            data=self.data
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-20:], self.inactive_endpoint)

    def test_update_link_by_id_wrong_status_fails(self):
        '''
        Test that a put request to update a link specified by id with
        non-existing status yields an HTTP_400_BAD_REQUEST response.
        '''
        endpoint = '/api/link/offline/1'
        response = self.app.test_client.put(
            endpoint,
            gather_request=False,
            headers=self.headers,
            data=self.data
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-19:], endpoint)

    def test_update_active_link_by_id_wrong_id_fails(self):
        '''
        Test that a put request to update an active link specified by an id
        that does not exist yields an HTTP_404_NOT_FOUND response.
        '''
        endpoint = '/api/link/active/1000000'
        response = self.app.test_client.put(
            endpoint,
            gather_request=False,
            headers=self.headers,
            data=self.data
        )
        self.assertEqual(response.status, 404)
        self.assertEqual(str(response.url)[-24:], endpoint)

    def test_update_inactive_link_by_id_wrong_id_fails(self):
        '''
        Test that a put request to update an inactive link specified by an id
        that does not exist yields an HTTP_404_NOT_FOUND response.
        '''
        endpoint = '/api/link/inactive/1000000'
        response = self.app.test_client.put(
            endpoint,
            gather_request=False,
            headers=self.headers,
            data=self.data
        )
        self.assertEqual(response.status, 404)
        self.assertEqual(str(response.url)[-26:], endpoint)

    def test_update_active_link_by_id_incorrect_payload_fails(self):
        '''
        Test that a put request to update an active link specified by id
        with an incorrect payload yields an HTTP_400_BAD_REQUEST response.
        '''
        data = 'wrong_data_format'
        response = self.app.test_client.put(
            self.active_endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(data)
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-18:], self.active_endpoint)

    def test_update_inactive_link_by_id_incorrect_payload_fails(self):
        '''
        Test that a put request to update an inactive link specified by id
        with an incorrect payload yields an HTTP_400_BAD_REQUEST response.
        '''
        data = 'wrong_data_format'
        response = self.app.test_client.put(
            self.inactive_endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(data)
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-20:], self.inactive_endpoint)

    def test_update_active_link_by_id_incomplete_payload_fails(self):
        '''
        Test that a put request to update an active link specified by id
        with an incomplete payload yields an HTTP_400_BAD_REQUEST response.
        '''
        data = {}
        response = self.app.test_client.put(
            self.active_endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(data)
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-18:], self.active_endpoint)

    def test_update_inactive_link_by_id_incomplete_payload_fails(self):
        '''
        Test that a put request to update an inactive link specified by id
        with an incomplete payload yields an HTTP_400_BAD_REQUEST response.
        '''
        data = {}
        response = self.app.test_client.put(
            self.inactive_endpoint,
            gather_request=False,
            headers=self.headers,
            data=dumps(data)
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(str(response.url)[-20:], self.inactive_endpoint)


class TestCheckDataAfterUpdate(TestCase):

    def setUp(self):
        self.app = create_app()
        self.active_endpoint = '/api/link/active/4'
        self.inactive_endpoint = '/api/link/inactive/3'
        self.headers = {'Bearer': config('ACCESS_TOKEN')}

    def test_update_active_link_by_id_data_changed_successfully(self):
        '''
        Test that a detail get request for an active link updated via a test
        put request specified by id yields the updated data.
        '''
        response = self.app.test_client.get(
            self.active_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(loads(loads(response.text))['url'], 'test-url')

    def test_update_inactive_link_by_id_data_changed_successfully(self):
        '''
        Test that a detail get request for an inactive link updated via a test
        put request specified by id yields the updated data.
        '''
        response = self.app.test_client.get(
            self.inactive_endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(loads(loads(response.text))['url'], 'test-url')
