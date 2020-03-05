"""Authentication routes"""

from flask import request, Blueprint, jsonify
from app.models import Story
from app.services.decorators import login_required

story_bp = Blueprint('story', __name__)


@story_bp.route('', methods=['POST'])
@login_required
def create():
    """Create story"""
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
