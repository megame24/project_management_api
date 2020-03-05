from settings import endpoint
from flask import jsonify
from flask_restplus import Resource


@endpoint('/login')
class Login(Resource):
    def post(self):
        return jsonify({'name': 'John wick'})
