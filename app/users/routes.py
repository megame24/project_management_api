"""Authentication routes"""

from flask import Blueprint, jsonify

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user route"""
    return jsonify({'name': 'John Wick'})
