"""Authentication routes"""

from flask import request, Blueprint, jsonify
from app.models import Story
from app.services.decorators import login_required

story_bp = Blueprint('story', __name__)


@story_bp.route('', methods=['GET', 'POST'])
@login_required
def create():
    """Create and get stories"""
    if request.method == 'POST':
        request_data = request.get_json()
        summary = request_data.get('summary', '')
        description = request_data.get('description', '')
        story_type = request_data.get('type', '')
        complexity = request_data.get('complexity', '')
        estimated_hrs = request_data.get('estimated_hrs', '')
        cost = request_data.get('cost', '')

        if (not summary or not story_type or not
                complexity or not estimated_hrs or not cost):
            return jsonify({'message': 'Required fields are missing or invalid'}), 400

        try:
            Story.create(type=story_type, summary=summary, description=description,
                         estimated_hrs=estimated_hrs, cost=cost, complexity=complexity, created_by=request.decoded['id'])
            return jsonify({'message': 'success'}), 201
        except Exception as e:
            print(e)
            return jsonify({'message': 'Internal server error'}), 500

    if request.method == 'GET':
        role = request.decoded['role']
        if role == 'User':
            filter_by = request.decoded['id']

        try:
            stories = []
            if role == 'User':
                stories = Story.query.filter_by(created_by=filter_by).all()
            if role == 'Admin':
                stories = Story.query.all()
            return jsonify([story.get_attributes() for story in stories]), 200
        except Exception as e:
            print(e)
            return jsonify({'message': 'Internal server error'}), 500
