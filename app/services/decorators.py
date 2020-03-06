from flask import request, jsonify
from functools import wraps
from .jwt_service import decode


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token')
        if token and decode(token):
            decoded = decode(token)
            request.decoded = decoded
            return f(*args, **kwargs)
        return jsonify({'message': 'Authentication required'}), 401
    return wrapper


