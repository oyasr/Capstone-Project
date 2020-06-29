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

        self.new_product = {
            'id': 4,
            'name': 'MacBookPro',
            'description': '15 inch Mac Book Pro',
            'price': 1499,
            'category_id': 1
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

    def test_get_product_by_id(self):
        c = Category(id=1, name='Electronics')
        c.insert()
        p = Product(id=1, category=c)
        p.insert()
        res = self.client().get('/products/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['product'])

    def test_404_requesting_non_existing_product(self):
        res = self.client().get('/products/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_product_by_category(self):
        c = Category(id=1, name='Electronics')
        c.insert()
        p = Product(id=1, category=c)
        p.insert()
        res = self.client().get('/categories/1/products')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['products'])
        self.assertTrue(data['total_category_products'])

    def test_404_get_product_by_category(self):
        c = Category(id=1, name='Electronics')
        c.insert()
        res = self.client().get('/categories/1/products')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_401_customer_no_authorization_post_new_product(self):
        res = self.client().post('/products', data=json.dumps(self.new_product),
                                 headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'no_authorization')

    def test_401_customer_no_authorization_patch(self):
        p = Product(id=1, price=999)
        p.insert()
        res = self.client().patch('/products/1', data=json.dumps(self.new_price),
                                  headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'no_authorization')

    # SELLER TESTS
    def test_seller_post_new_product(self):
        res = self.client().post('/products', data=json.dumps(self.new_product),
                                 headers=self.seller_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_products'])

    def test_403_seller_unauthorized_patch(self):
        p = Product(id=1, price=999)
        p.insert()
        res = self.client().patch('/products/1', data=json.dumps(self.new_price),
                                  headers=self.seller_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')

    def test_403_seller_unauthorized_delete(self):
        p = Product(id=1, price=999)
        p.insert()
        res = self.client().patch('/products/1', data=json.dumps(self.new_price),
                                  headers=self.seller_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')

    # ADMIN TESTS
    def test_admin_post_new_product(self):
        res = self.client().post('/products', data=json.dumps(self.new_product),
                                 headers=self.admin_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_products'])

    def test_admin_patch_products(self):
        p = Product(id=1, price=999)
        p.insert()
        res = self.client().patch('/products/1', data=json.dumps(self.new_price),
                                  headers=self.admin_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 1)

    def test_admin_delete_product(self):
        p = Product(id=1, price=999)
        p.insert()
        res = self.client().delete('/products/1', data=json.dumps(self.new_price),
                                   headers=self.admin_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
