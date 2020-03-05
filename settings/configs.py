import os
import dotenv

dotenv.load_dotenv()


class BaseConfig:
    """Base app configuration class"""

    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('APP_SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = 'app.py'


class ProductionConfig(BaseConfig):
    """Production app configuration class"""

    TESTING = False
    PROPAGATE_EXCEPTIONS = True


class TestingConfig(BaseConfig):
    """Testing app configuration class"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')


class DevelopmentConfig(BaseConfig):
    """Development app configuration class"""

    DEBUG = True


ENV_MAPPER = {
    'production': ProductionConfig,
    'testing': TestingConfig,
    'development': DevelopmentConfig,
}
