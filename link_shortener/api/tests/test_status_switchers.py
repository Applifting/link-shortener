'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from decouple import config
from unittest import TestCase

from link_shortener.server import create_app


class TestStatusSwitchersAPI(TestCase):

    def setUp(self):
        self.app = create_app()
        self.activate_endpoint = '/api/status/activate'
        self.deactivate_endpoint = '/api/status/deactivate'
        self.headers = {'Bearer': config('ACCESS_TOKEN')}

    def test_activate_with_token(self):
        pass

    def test_deactivate_with_token(self):
        pass
