"""jwt service"""

import os
import datetime
import jwt


def encode(payload):
    """jwt encode abstraction"""
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=2)
    payload['exp'] = expiration_time
    encoded_jwt = jwt.encode(payload, os.getenv('APP_SECRET'), algorithm='HS256')
    return encoded_jwt, expiration_time


def decode(token):
    """jwt decode abstraction"""
    try:
        return jwt.decode(token, os.getenv('APP_SECRET'))
    except Exception as e:
        print(e)
        return False
