'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config
from unittest import TestCase

from link_shortener.server import create_app


class TestDeleteLinkAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.endpoint = '/api/link/5'
        self.headers = {'Bearer': config('ACCESS_TOKEN')}

    def test_d_delete_link_correct_request_successful(self):
        '''
        Test that a delete request to delete an existing link with the correct
        token yields an HTTP_200_OK response.
        '''
        response = self.app.test_client.delete(
            self.endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-11:], self.endpoint)

    def test_e_delete_link_nonexisting_id_fails(self):
        '''
        Test that a delete request to delete a link that does not exist
        yields an HTTP_404_NOT_FOUND response.
        '''
        response = self.app.test_client.delete(
            self.endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 404)
        self.assertEqual(str(response.url)[-11:], self.endpoint)

    def test_a_delete_link_without_token_fails(self):
        '''
        Test that a delete request to delete an existing link without
        a token yields an HTTP_401_UNAUTHORIZED response.
        '''
        response = self.app.test_client.delete(
            self.endpoint,
            gather_request=False
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-11:], self.endpoint)

    def test_b_delete_link_with_wrong_token_fails(self):
        '''
        Test that a delete request to delete an existing link with
        an incorrect token yields an HTTP_401_UNAUTHORIZED response.
        '''
        bad_token = 'made-up-wrong-token'
        headers = {'Bearer': bad_token}
        response = self.app.test_client.delete(
            self.endpoint,
            gather_request=False,
            headers=headers
        )
        self.assertEqual(response.status, 401)
        self.assertEqual(str(response.url)[-11:], self.endpoint)

    def test_c_delete_link_wrong_method_fails(self):
        '''
        Test that a HEAD request method to delete an existing link yields
        an HTTP_405_METHOD_NOT_ALLOWED response.
        '''
        response = self.app.test_client.head(
            self.endpoint,
            gather_request=False,
            headers=self.headers
        )
        self.assertEqual(response.status, 405)
        self.assertEqual(str(response.url)[-11:], self.endpoint)
