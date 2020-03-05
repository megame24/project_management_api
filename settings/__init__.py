"""This module initializes the API"""

from flask import Flask, jsonify, Blueprint
from flask_restplus import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .configs import ENV_MAPPER
import dotenv

db = SQLAlchemy()
dotenv.load_dotenv()

api_blueprint = Blueprint('api_bp', __name__, url_prefix='/api')
api = Api(api_blueprint)

endpoint = api.route


def create_app(env):
    """
    Create the flask app instance
    :param env: current environment
    :return: Object - Flask instance
    """

    app = Flask(__name__)

    if env == 'developement':
        import logging
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    CORS(app, origins=['*'], supports_credentials=True)
    app.config.from_object(ENV_MAPPER[env])

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(api_blueprint)

    import src.views
    from src.models import models

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
