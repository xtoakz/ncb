import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
    RAGY_API = os.environ.get('RAGY_API', 'dummy-api-key')