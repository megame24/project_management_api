"""This module initializes the API"""
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import app_config

db = SQLAlchemy()


def create_app(env):
    """
    Create the flask app instance
    :param env: current environment
    :return: Object - Flask instance
    """

    app = Flask(__name__)
    CORS(app)

    app.config.from_object(app_config[env])

    db.init_app(app)
    migrate = Migrate(app, db)

    from app.users.routes import auth_bp
    from app.stories.routes import story_bp
    from app.models import seed_db
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(story_bp, url_prefix='/api/stories')

    @app.before_first_request
    def initialize():
        """Seed the db"""
        seed_db()

    @app.route('/', methods=['GET'])
    def index():
        """
        Index route
        :return: Json
        """
        return jsonify({
            "message": "Welcome to the proj-m API"
        })

    return app


app = create_app(os.getenv('FLASK_ENV', 'development'))
