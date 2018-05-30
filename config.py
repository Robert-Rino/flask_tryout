import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'development-key'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'develpment-key'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.db')
    SECRET_KEY = 'test-key'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')

config = {
'development': DevelopmentConfig,
'test': TestingConfig,
'default': DevelopmentConfig,
'production':ProductionConfig
}
