from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from app.api import bp

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

@bp.app_errorhandler(404)
def not_found_error(error):
    return error_response(404)

@bp.app_errorhandler(500)
def internal_error(error):
    return error_response(500)

@bp.app_errorhandler(401)
def unauthorized_error(error):
    return error_response(401, 'Authentication required')

@bp.app_errorhandler(403)
def forbidden_error(error):
    return error_response(403, 'Forbidden access') 