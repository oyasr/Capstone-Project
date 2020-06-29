import os
import unittest
import json
from app import create_app, db
from app.models import Product, Category


class ProductTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.admin_header = {
            'Content-type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authorization': f'Bearer {os.environ.get("ADMIN_TOKEN")}'
        }

        self.header = {
            'Content-type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }

        self.new_category = {
            'name': 'Tools'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ADMIN TEST
    def test_admin_post_new_category(self):
        res = self.client().post('/categories', data=json.dumps(self.new_category),
                                 headers=self.admin_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_categories'])
