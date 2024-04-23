from flask import Flask
from ..models import db, connect_db
from .blueprints.auth import auth_bp
from .blueprints.main import main_bp
from .blueprints.books import books_bp
from .blueprints.reading_lists import reading_lists_bp
from .config import DevelopmentConfig


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    connect_db(app)
    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(reading_lists_bp)

    return app

