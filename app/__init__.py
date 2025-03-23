from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from .extensions import db, bcrypt, login_manager
# from flask_bcrypt import Bcrypt
from sqlalchemy import text  # Import the text function
from flask_login import LoginManager
from flask_login import current_user
from .routes import ui_routes

# db = SQLAlchemy()  # Initialize SQLAlchemy
# bcrypt = Bcrypt()  # Initialize Bcrypt
# login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Load the configuration from the config.py file
    app.config.from_object(Config)

    # Initialize SQLAlchemy
    db.init_app(app)  
    login_manager.init_app(app)

    from .routes import main_routes, ui_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(ui_routes)

    bcrypt.init_app(app)

    return app

# Initialize Flask app