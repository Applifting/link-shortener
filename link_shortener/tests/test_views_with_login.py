'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from unittest import TestCase, mock

from link_shortener.server import create_app


class TestViewsWithLogin(TestCase):

    def setUp(self):
        self.app = create_app()

    def test_google_redirect_with_login_required(self):
        '''
        Test that getting any route with a login_required decorator
        successfully redirects to google account page.
        '''
        response = self.app.test_client.get(
            '/links/all',
            gather_request=False
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(
            str(response.url)[:28],
            'https://accounts.google.com/'
        )

    # def test_getting_all_links_page(self):
    #     '''
    #     Test that getting the 'all links' page is successful.
    #     '''
    #     response = self.app.test_client.get(
    #         '/links/all',
    #         gather_request=False
    #     )
    #     self.assertEqual(response.status, 200)
    #
    # def test_getting_owner_links_page(self):
    #     '''
    #     Test that getting the 'owner specific links' page is successful.
    #     '''
    #     response = self.app.test_client.get(
    #         '/links/me',
    #         gather_request=False
    #     )
    #     self.assertEqual(response.status, 200)
    #
    #
    # def test_deleting_link_bad_status_fails(self, mock_login_required):
    #     '''
    #     Test that deleting a link with a non-existing status fails.
    #     '''
    #     params = {'status': 'bad', 'link_id': 1}
    #     response = self.app.test_client.get(
    #         '/delete/bad/1',
    #         gather_request=False
    #         params=params
    #     )
    #     self.assertEqual(response.url, '/delete/bad/1')
    #     self.assertEqual(response.status, 400)
    #
    # def test_deleting_existing_active_link_successful(self):
    #     '''
    #     Test that deleting an existing active link is successful.
    #     '''
    #     response = self.app.test_client.get(
    #         '/delete/active/1',
    #         gather_request=False
    #     )
    #     self.assertEqual(response.status, 200)
    #
    # def test_deleting_nonexisting_active_link_fails(self):
    #     '''
    #     Test that deleting a non-existing active link fails.
    #     '''
    #     response = self.app.test_client.get(
    #         '/delete/active/10000000',
    #         gather_request=False
    #     )
    #     self.assertEqual(response.status, 500)
