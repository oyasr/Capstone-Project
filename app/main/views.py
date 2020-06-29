import os
from . import main
from .. import db
from ..models import Category, Product
from flask import jsonify, abort, request, redirect


products_per_page = 10


def paginate(page, product_objects):
    start = (page - 1)*products_per_page
    end = start + products_per_page
    products = [product.format() for product in product_objects]
    return products[start:end]


@main.route('/')
def index():
    return redirect(f"{os.getenv('AUTH_ENDPOINT')}")


@main.route('/welcome')
def welcome():
    return "<h1>Welcome!</h1>"


@main.route('/categories')
def get_categories():
    try:
        category_objects = Category.query.order_by('id').all()
        categories = [category.format() for category in category_objects]
    except Exception:
        abort(422)
    else:
        return jsonify({
            'success': True,
            'categories': categories
        }), 200


@main.route('/products')
def get_products():
    try:
        page = request.args.get('page', 1, type=int)
        product_objects = Product.query.order_by('id').all()
        paginated_products = paginate(page, product_objects)
    except Exception:
        abort(422)
    else:
        return jsonify({
            'success': True,
            'products': paginated_products,
            'total_products': len(product_objects),
            'page': page
        }), 200


@main.route('/products/<int:id>')
def get_product_by_id(id):
    product_object = Product.query.get(id)
    if not product_object:
        abort(404)
    product = product_object.format()
    return jsonify({
        'success': True,
        'product': product,
        'current_category': product_object.category.format()
    }), 200


@main.route('/categories/<int:category_id>/products')
def get_products_by_category(category_id):
    page = request.args.get('page', 1, type=int)
    category_object = Category.query.get(category_id)
    if not category_object:
        abort(404)
    product_objects = category_object.products.order_by('id').all()
    if not product_objects:
        abort(404)
    paginated_products = paginate(page, product_objects)
    return jsonify({
        'success': True,
        'products': paginated_products,
        'total_category_products': len(product_objects),
        'current_category': category_object.format(),
        'page': page
    }), 200
