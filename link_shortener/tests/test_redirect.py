'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
import asyncio

from json import loads
from unittest import TestCase

from link_shortener.server import create_app

from link_shortener.commands.redirect import redirect_link

from link_shortener.core.exceptions import NotFoundException


class CustomRequest:

    def __init__(self, app):
        self.app = app


class TestRedirectLink(TestCase):

    def setUp(self):
        self.app = create_app()
        self.request = CustomRequest(app=self.app)

    def test_redirect_existing_link_successful(self):
        '''
        Test that calling the redirect_link async method with an existing
        active link's endpoint yields the correct link url.
        '''
        result = asyncio.run(redirect_link(self.request, 'vlk'))
        url = 'http://www.vlk.cz'
        self.assertEqual(result, url)

    def test_redirect_inactive_link_fails(self):
        '''
        Test that calling the redirect_link async method with an existing
        inactive link's endpoint yields an error.
        '''
        self.assertRaises(
            NotFoundException,
            asyncio.run(redirect_link(self.request, 'tunak'))
        )

    async def test_redirect_nonexisting_link_fails(self):
        '''
        Test that calling the redirect_link async method with a nonexisting
        link's endpoint yields an error.
        '''
        self.assertRaises(
            NotFoundException,
            await redirect_link(self.request, 'I-do-not-exist-brah')
        )

    async def test_redirect_password_protected_link_authorize(self):
        '''
        Test that calling the redirect_link async method with an existing
        active link's endpoint that is password protected yields a url
        of its authorization page.
        '''
        result = await redirect_link(self.request, 'meta')
        auth_url = '/authorize/3'
        self.assertEqual(result, auth_url)
