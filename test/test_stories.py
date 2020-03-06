"""Module for testing stories' functionalities"""

import os
import json
import unittest
from app import create_app, db

story1 = {
    "summary": "summary",
    "description": "des",
    "type": "enhancement",
    "complexity": "low",
    "cost": 2,
    "estimated_hrs": 2
}

user1 = {
    'first_name': 'First',
    'email': 'first@email.com',
    'password': 'P@ssw0rd!'
}

user_token = None
admin_token = None


class StoriesTestCase(unittest.TestCase):
    """Stories test case"""

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            res = self.client.post('/api/register', data=json.dumps(user1))
            global user_token, admin_token
            user_token = json.loads(res.data.decode())['token']
            login_res = self.client.post('/api/login', data=json.dumps({
                'email': os.getenv('ADMIN_EMAIL'),
                'password': os.getenv('ADMIN_PASSWORD')
            }))
            admin_token = json.loads(login_res.data.decode())['token']

    def test_create_story_success(self):
        """Create story success"""
        res = self.client.post('/api/stories', headers={'token': user_token}, data=json.dumps(story1))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'success')
        self.assertEqual(res.status_code, 201)

    def test_create_story_no_token(self):
        """Create story no token"""
        res = self.client.post('/api/stories', headers={'token': ''}, data=json.dumps(story1))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Authentication required')
        self.assertEqual(res.status_code, 401)

    def test_create_story_invalid_token(self):
        """Create story invalid token"""
        res = self.client.post('/api/stories', headers={'token': 'invalid'}, data=json.dumps(story1))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Authentication required')
        self.assertEqual(res.status_code, 401)

    def test_create_story_invalid_form_data(self):
        """Create story invalid form data"""
        res = self.client.post('/api/stories', headers={'token': user_token}, data=json.dumps({}))
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Required fields are missing or invalid')

    def test_get_stories_success(self):
        """Get stories success"""
        self.client.post('/api/stories', headers={'token': user_token}, data=json.dumps(story1))
        res = self.client.get('/api/stories', headers={'token': user_token})
        result = json.loads(res.data.decode())
        self.assertEqual(result[0]['summary'], 'summary')
        self.assertEqual(res.status_code, 200)

    def test_admin_get_all_stories(self):
        """Admin get all stories"""
        self.client.post('/api/stories', headers={'token': user_token}, data=json.dumps(story1))
        res = self.client.get('/api/stories', headers={'token': admin_token})
        result = json.loads(res.data.decode())
        self.assertEqual(result[0]['summary'], 'summary')
        self.assertEqual(res.status_code, 200)

    def test_review_story_success(self):
        """Review story success"""
        self.client.post('/api/stories', headers={'token': user_token}, data=json.dumps(story1))
        res = self.client.put('/api/stories/1/review', headers={'token': admin_token}, data=json.dumps({
            'status': 'Approved'
        }))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'success')
        self.assertEqual(res.status_code, 200)

    def test_review_story_restrict_to_only_admin(self):
        """Only admin can review story"""
        self.client.post('/api/stories', headers={'token': user_token}, data=json.dumps(story1))
        res = self.client.put('/api/stories/1/review', headers={'token': user_token}, data=json.dumps({
            'status': 'Approved'
        }))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Permission denied')
        self.assertEqual(res.status_code, 403)

    def test_review_story_invalid_status(self):
        """Review story invalid status"""
        self.client.post('/api/stories', headers={'token': user_token}, data=json.dumps(story1))
        res = self.client.put('/api/stories/1/review', headers={'token': admin_token}, data=json.dumps({
            'status': 'Invalid'
        }))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], 'Invalid status')
        self.assertEqual(res.status_code, 400)

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()


if __name__ == "__main__":
    unittest.main()