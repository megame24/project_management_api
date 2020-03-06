"""Module for testing users' functionalities"""

import json
import unittest
from app import create_app, db

user1 = {
    'first_name': 'First',
    'email': 'first@email.com',
    'password': 'P@ssw0rd!'
}


class UsersTestCase(unittest.TestCase):
    """Users test case"""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_user_registration(self):
        """Successful registration"""
        res = self.client.post('/api/register', data=json.dumps(user1))
        result = json.loads(res.data.decode())
        self.assertEqual(result['user']['email'], 'first@email.com')
        self.assertEqual(res.status_code, 201)

    def test_invalid_password_on_registration(self):
        """Invalid password on registration"""
        res = self.client.post('/api/register', data=json.dumps({
            'first_name': 'First',
            'email': 'first@email.com',
            'password': 'invalid'
        }))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Required fields are missing or invalid')
        self.assertEqual(res.status_code, 400)

    def test_invalid_email_on_registration(self):
        """Invalid email on registration"""
        res = self.client.post('/api/register', data=json.dumps({
            'first_name': 'First',
            'email': 'invalid',
            'password': 'P@ssw0rd!'
        }))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Required fields are missing or invalid')
        self.assertEqual(res.status_code, 400)

    def test_invalid_first_name_on_registration(self):
        """Invalid first_name on registration"""
        res = self.client.post('/api/register', data=json.dumps({
            'first_name': '',
            'email': 'first1@gmail.com',
            'password': 'P@ssw0rd!'
        }))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Required fields are missing or invalid')
        self.assertEqual(res.status_code, 400)

    def test_unique_user_on_registration(self):
        """Unique user on registration"""
        res = self.client.post('/api/register', data=json.dumps(user1))
        self.assertEqual(res.status_code, 201)
        res = self.client.post('/api/register', data=json.dumps(user1))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'User with that email already exists')
        self.assertEqual(res.status_code, 400)

    def test_user_login(self):
        """Successful login"""
        self.client.post('/api/register', data=json.dumps(user1))
        res = self.client.post('/api/login', data=json.dumps(user1))
        result = json.loads(res.data.decode())
        self.assertEqual(result['user']['email'], 'first@email.com')
        self.assertEqual(res.status_code, 200)

    def test_no_email_login(self):
        """No email provided on login"""
        self.client.post('/api/register', data=json.dumps(user1))
        res = self.client.post('/api/login', data=json.dumps({
            'email': '',
            'password': 'P@ssw0rd!'
        }))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Required fields are missing or invalid')
        self.assertEqual(res.status_code, 400)

    def test_no_password_login(self):
        """No password provided on  login"""
        self.client.post('/api/register', data=json.dumps(user1))
        res = self.client.post('/api/login', data=json.dumps({
            'email': 'first@email.com',
            'password': ''
        }))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Required fields are missing or invalid')
        self.assertEqual(res.status_code, 400)

    def test_invalid_password_login(self):
        """Invalid password on login"""
        self.client.post('/api/register', data=json.dumps(user1))
        res = self.client.post('/api/login', data=json.dumps({
            'email': 'first@email.com',
            'password': 'invalid'
        }))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Invalid email or password')
        self.assertEqual(res.status_code, 401)

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()


if __name__ == "__main__":
    unittest.main()