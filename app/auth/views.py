import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from . import auth
from .auth0 import AuthError, requires_auth
from .. import db
from ..models import Category, Product


@auth.route('/products', methods=['POST'])
@requires_auth('post:new-product')
def post_new_product(payload):
    body = request.get_json()
    new_name = body.get('name', None)
    new_description = body.get('description', None)
    new_price = body.get('price', None)
    try:
        product_object = Product(
            name=new_name, description=new_description, price=new_price)
        product_object.insert()
    except Exception:
        db.session.rollback()
        abort(422)
    else:
        return jsonify({
            'success': True,
            'created': product_object.id,
            'total_products': len(Product.query.all())
        }), 200


@auth.route('/categories', methods=['POST'])
@requires_auth('post:new-category')
def post_new_category(payload):
    body = request.get_json()
    new_name = body.get('name', None)
    try:
        category_object = Category(name=new_name)
        category_object.insert()
    except Exception:
        db.session.rollback()
        abort(422)
    else:
        return jsonify({
            'success': True,
            'created': category_object.id,
            'total_categories': len(Category.query.all())
        }), 200


@auth.route('/products/<int:id>', methods=['PATCH'])
@requires_auth('patch:products')
def patch_products(payload, id):
    body = request.get_json()
    product_object = Product.query.get(id)
    if product_object is None:
        abort(404)
    try:
        if 'price' in body:
            product_object.price = int(body.get('price'))
            product_object.update()
            return jsonify({
                'success': True,
                'updated': id
            }), 200
    except Exception:
        db.session.rollback()
        abort(400)


@auth.route('/products/<int:id>', methods=['DELETE'])
@requires_auth('delete:products')
def delete_products(payload, id):
    try:
        product_object = Product.query.get(id)
        if not product_object:
            abort(404)
        product_object.delete()
    except Exception:
        db.session.rollback()
        abort(422)
    else:
        return jsonify({
            'success': True,
            'deleted': id
        }), 200
