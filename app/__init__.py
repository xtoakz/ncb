from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_lucide import Lucide

# SQLAlchemy-Instanz erzeugen
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize Bootstrap
    Bootstrap(app)
    
    # SQLAlchemy initialisieren
    db.init_app(app)
    # Initialize Flask-Lucide
    lucide = Lucide(app)

    # Blueprint registrieren
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
