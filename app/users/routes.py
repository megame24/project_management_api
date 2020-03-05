"""Authentication routes"""

import re
from flask import request, Blueprint, jsonify
from app.models import User
from app.services.jwt_service import encode

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register user route"""
    request_data = request.get_json()
    email = request_data.get('email', '')
    password = request_data.get('password', '')
    first_name = request_data.get('first_name', '')
    last_name = request_data.get('last_name', '')

    valid_password = re.match(
        r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!”#$%&'()*+,\-./:;<=>?@\[\]^_`{|}~]).{8,}$", password)
    valid_email = re.match(
        r'(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|'
        r'(\".+\"))@(([^<>()\.,;\s@\"]+\.{0,1})+[^<>()\.,;:\s@\"]{2,})$', email)

    if not first_name or not valid_email or not valid_password:
        return jsonify({'message': 'Required fields are mission or invalid'}), 400

    try:
        duplicate_user = User.query.filter_by(email=email).first()
        if duplicate_user:
            return jsonify({'message': 'User with that email already exists'}), 400

        new_user = User.register(password, email=email, first_name=first_name, last_name=last_name)

        encoded_jwt, token_expiration_time = encode({'id': new_user.id, 'role': new_user.role})
        return jsonify({
            'user': {
                'id': new_user.id,
                'email': new_user.email,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'role': new_user.role
            },
            'token': encoded_jwt.decode('utf-8'),
            'exp': token_expiration_time
        }), 201
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal server error'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user route"""
    request_data = request.get_json()
    email = request_data.get('email', '')
    password = request_data.get('password', '')
    if not email or not password:
        return jsonify({'message': 'Required fields are mission or invalid'}), 400
    try:
        user = User.get_and_auth_user(email, password)
        if user:
            encoded_jwt, token_expiration_time = encode({'id': user.id, 'role': user.role})
            return jsonify({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role
                },
                'token': encoded_jwt.decode('utf-8'),
                'exp': token_expiration_time
            }), 201
        else:
            return jsonify({'message': 'Invalid password'}), 401
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal server error'}), 500
