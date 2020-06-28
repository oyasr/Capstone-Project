from . import auth
from .auth0 import AuthError
from flask import jsonify


@auth.app_errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@auth.app_errorhandler(422)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'bad request'
    }), 422


@auth.app_errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


@auth.app_errorhandler(400)
def bad_syntax(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad syntax'
    }), 400


@auth.app_errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500


@auth.errorhandler(AuthError)
def authentication_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error
    }), error.status_code
