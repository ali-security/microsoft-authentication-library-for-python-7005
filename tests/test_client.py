import os
import json
import logging

from oauth2cli.oauth2 import Client
from tests import unittest

from .authcode import AuthCodeReceiver


THIS_FOLDER = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(THIS_FOLDER, 'config.json')


class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(CONFIG_FILE) as f:
            cls.conf = json.load(f)
        cls.client = Client(
            cls.conf['client_id'], cls.conf['client_secret'],
            token_endpoint=cls.conf["token_endpoint"])

    def test_client_credentials(self):
        result = self.client.obtain_token_with_client_credentials(
            self.conf['scope'])
        self.assertIn('access_token', result)

    def test_username_password(self):
        result = self.client.obtain_token_with_username_password(
            self.conf["username"], self.conf["password"],
            data={"resource": self.conf.get("resource")},  # MSFT AAD V1 only
            scope=self.conf.get("scope"))
        self.assertIn('access_token', result)
