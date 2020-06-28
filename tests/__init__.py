import unittest
import json
from app import create_app, db


class ProductTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client

    def tearDown(self):
        pass

    def test_given_behavior(self):
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)
