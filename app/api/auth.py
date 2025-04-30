from flask import request, jsonify, g
from flask_httpauth import HTTPTokenAuth
from app.models.user import User
from app.api.errors import error_response
import jwt
from app import db
from flask import current_app

token_auth = HTTPTokenAuth()

@token_auth.verify_token
def verify_token(token):
    try:
        payload = jwt.decode(
            token, 
            current_app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        user = User.query.get(payload['sub'])
        if user:
            g.current_user = user
            return True
        return False
    except jwt.ExpiredSignatureError:
        return False
    except (jwt.InvalidTokenError, Exception):
        return False

@token_auth.error_handler
def token_auth_error():
    return error_response(401, 'Invalid token or token expired')

# Simple function to get current user instead of decorator
def current_user():
    return g.current_user if hasattr(g, 'current_user') else None 