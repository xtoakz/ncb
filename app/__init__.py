from flask import Flask
from flask_session import Session
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize Flask-Session
    Session(app)
    
    # Register blueprints
    from app.routes import bp as main_bp
    from app.auth import bp as auth_bp
    from app.newsletter import bp as newsletter_bp
    from app.admin import bp as admin_bp
    from app.todo import bp as todo_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(newsletter_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(todo_bp, url_prefix='/todo')

    return app