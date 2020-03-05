from flask import request, jsonify
from functools import wraps
from .jwt_service import decode


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        decoded = decode(token)
        if not decoded:
            return jsonify({'message': 'Authentication required'}), 401
        request.decoded = decoded
        return f(*args, **kwargs)
    return wrapper


