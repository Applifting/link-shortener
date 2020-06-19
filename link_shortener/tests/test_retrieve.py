'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from json import loads
from unittest import TestCase

from link_shortener.server import create_app

from link_shortener.commands.retrieve import retrieve_links, retrieve_link

from link_shortener.core.exceptions import NotFoundException


class CustomRequest:

    def __init__(self, app):
        self.app = app


class TestRetrieveLinks(TestCase):

    def setUp(self):
        self.app = create_app()
        self.request = CustomRequest(app=self.app)

    async def test_retrieve_links_no_filter(self):
        '''
        Test that supplying no filters to the retrieve_links async method
        yields all link data.
        '''
        filters = {}
        result = await retrieve_links(self.request, filters=filters)
        data = loads(result)
        self.assertEqual(data[1]['endpoint'], 'vlk')
        self.assertEqual(data[2]['switch_date']['Year'] == 2020)

    async def test_retrieve_links_one_filter(self):
        '''
        Test that supplying an activity filter to the retrieve_links async
        method yields all active links.
        '''
        filters = {'is_active': True}
        result = await retrieve_links(self.request, filters=filters)
        data = loads(result)
        for link in data:
            self.assertTrue(link['is_active'])

    async def test_retrieve_links_multiple_filters(self):
        '''
        Test that supplying multiple filters to the retrieve_links async
        method yields the correct corresponding data.
        '''
        filters = {
            'is_active': False,
            'url': 'https://www.britannica.com/animal/tuna-fish'
        }
        result = await retrieve_links(self.request, filters=filters)
        data = loads(result)
        self.assertEqual(data['endpoint'], 'tunak')


class TestRetrieveLink(TestCase):

    def setUp(self):
        self.app = create_app()
        self.request = CustomRequest(app=self.app)

    async def test_retrieve_existing_link_successful(self):
        '''
        Test that the retrieve_link method with an existing link id yields
        the link's data.
        '''
        result = await retrieve_link(self.request, 1)
        data = loads(result)
        self.assertEqual(data['endpoint'], 'pomuzemesi')

    async def test_retrieve_nonexisting_link_fails(self):
        '''
        Test that the retrieve_link method with a nonexisting link id yields
        an error.
        '''
        self.assertRaises(
            NotFoundException,
            await retrieve_link(self.request, 1000000)
        )
