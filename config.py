import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    RAGY_API = os.environ.get('RAGY_API')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
