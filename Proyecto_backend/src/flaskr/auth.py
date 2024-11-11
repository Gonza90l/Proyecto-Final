#auth.py
from functools import wraps
from flask import request, jsonify, current_app
import jwt
import time
from flaskr.cache.memory_cache import cache

def decode_and_cache_token():

    token = request.headers.get('Authorization')

    if not token:
        return None, jsonify({'message': 'Token is missing!'}), 401

    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    cached_data = cache.get(token)
    if cached_data:
        return cached_data, None, None

    try:
        secret_key = current_app.config['SECRET_KEY']
        data = jwt.decode(token, secret_key, algorithms=["HS256"])
        ttl = data['exp'] - time.time()
        cache.set(token, data, ttl)
        return data, None, None
    except jwt.ExpiredSignatureError:
        return None, jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return None, jsonify({'message': 'Token is invalid!'}), 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, error_response, status_code = decode_and_cache_token()
        if error_response:
            return error_response, status_code
        return f(*args, **kwargs)
    return decorated

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            data, error_response, status_code = decode_and_cache_token()
            if error_response:
                return error_response, status_code

            user_role = data.get('role')
            if user_role not in roles:
                return jsonify({'message': 'You do not have permission to access this resource'}), 403

            return f(*args, **kwargs)
        return decorated
    return decorator

def get_user_id():
    data, error_response, status_code = decode_and_cache_token()
    if error_response:
        return None
    return data.get('id')

def get_user_role():
    data, error_response, status_code = decode_and_cache_token()
    if error_response:
        return None
    return data.get('role')