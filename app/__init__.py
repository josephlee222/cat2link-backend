import os
from dotenv import load_dotenv
from flask import Flask
import app.models
from flask_migrate import Migrate
from app.extensions import db, jwt
from flask_jwt_extended import JWTManager
from datetime import timedelta


#Import Routes
from app.routes.admin.user import userRoutes
from app.routes.auth import authRoutes

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    # Configure SQLite database path (saves to the 'instance' folder)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['WTF_CSRF_ENABLED'] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=int(os.environ.get("JWT_TIMEOUT")))

    # Initialize the app with the extension
    db.init_app(app)

    # Initialize JWT Manager with the app
    jwt.init_app(app)

    app.register_blueprint(userRoutes, url_prefix="/admin/users")
    app.register_blueprint(authRoutes, url_prefix="/auth")

    

    # Migrate/Update db
    Migrate(app, db)

    return app
