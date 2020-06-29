import os
import unittest
import json
from app import create_app, db
from app.models import Product


class ProductTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client
        db.create_all()

        self.new_product = {
            'name': 'MacBookPro',
            'description': '15 inch Mac Book Pro',
            'price': 1499,
            'category_id': 3
        }

        self.header = {
            'Content-type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }

        self.admin_header = {
            'Content-type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authorization': f'Bearer {os.environ.get("ADMIN_TOKEN")}'
        }

        self.seller_header = {
            'Content-type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authorization': f'Bearer {os.environ.get("SELLER_TOKEN")}'
        }

        self.new_price = {'price': 499}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # CUSTOMER TESTS
    def test_get_paginated_products(self):
        res = self.client().get('/products')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_requesting_beyond_valid_page(self):
        res = self.client().get('/products/?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_requesting_non_existing_product(self):
        res = self.client().get('/products/0')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # SELLER TESTS
    def test_seller_post_new_product(self):
        res = self.client().post('/products', data=json.dumps(self.new_product),
                                 headers=self.seller_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_products'])

    def test_401_unauthorized_patch(self):
        res = self.client().post('/products', data=json.dumps(self.new_product),
                                 headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'no_authorization')

    # ADMIN TESTS
