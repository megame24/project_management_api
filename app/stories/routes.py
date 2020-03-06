"""Authentication routes"""

import json
from flask import request, Blueprint, jsonify
from app.models import Story
from app.services.decorators import login_required
from app.models import db

story_bp = Blueprint('story', __name__)


@story_bp.route('', methods=['GET', 'POST'])
@login_required
def create():
    """Create and get stories"""
    if request.method == 'POST':
        request_data = json.loads(request.data)
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

        try:
            stories = []
            if role == 'User':
                stories = Story.query.filter_by(created_by=request.decoded['id']).all()
            if role == 'Admin':
                stories = Story.query.all()
            return jsonify([story.get_attributes() for story in stories]), 200
        except Exception as e:
            print(e)
            return jsonify({'message': 'Internal server error'}), 500


@story_bp.route('/<int:story_id>/review', methods=['PUT'])
@login_required
def review(story_id):
    """Admin review story"""
    role = request.decoded['role']
    if role != 'Admin':
        return jsonify({'message': 'Permission denied'}), 409

    status = json.loads(request.data).get('status', '')
    status_options = ['Approved', 'Rejected']
    if status.capitalize() not in status_options:
        return jsonify({'message': 'Invalid status'}), 400

    try:
        story = Story.query.filter_by(id=story_id).first()
        story.status = status
        db.session.commit()
        return jsonify({'message': 'success'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Internal server error'}), 500



