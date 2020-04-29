'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from unittest import TestCase

from link_shortener.server import create_app


class TestFormViews(TestCase):

    def setUp(self):
        self.app = create_app()

    def test_redirect_link_with_password(self):
        '''
        Test that accessing link with a password redirects to password form.
        '''
        response = self.app.test_client.get(
            '/manatee',
            gather_request=False
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-12:], '/authorize/3')

    def test_getting_password_form(self):
        '''
        Test that getting the password form of an existing link is successfull.
        '''
        response = self.app.test_client.get(
            '/authorize/1',
            gather_request=False
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(str(response.url)[-12:], '/authorize/1')

    def test_getting_invalid_form_fails(self):
        '''
        Test that the POST method fails on an invalid form.
        '''
        response = self.app.test_client.post(
            '/authorize/3',
            gather_request=False,
        )
        self.assertEqual(response.status, 400)

    # def test_invalid_request_fails(self):
    #     '''
    #     Test that accessing link that does not exist fails.
    #     '''
    #     response = self.app.test_client.get(
    #         '/authorize/100000',
    #         gather_request=False
    #     )
    #     self.assertEqual(response.status, 400)
