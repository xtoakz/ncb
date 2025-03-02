import os
from datetime import timedelta

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
    
    # Supabase configuration
    SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')
    
    # Flask session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True