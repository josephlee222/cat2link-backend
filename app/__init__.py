import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from app.extensions import db, jwt
from flask_jwt_extended import JWTManager
from datetime import timedelta

import app.models
from app.models.User import User

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

    # Additional init functions
    def initialize_app():
        # Create user
        with app.app_context():
            if not User.query.filter_by(username="admin").first():
                admin = User(username="admin", email="admin@admin.com", role="admin")
                admin.set_password("admin123")
                db.session.add(admin)
                db.session.commit()

    # Initialize the app with the extension
    db.init_app(app)

    # Initialize JWT Manager with the app
    jwt.init_app(app)

    # Initialisation tasks if required
    initialize_app()

    app.register_blueprint(userRoutes, url_prefix="/admin/users")
    app.register_blueprint(authRoutes, url_prefix="/auth")

    @app.errorhandler(Exception)
    def internal_server_error(e):
        app.logger.error(f"Server error: {e}")
        return {"status": "error",'message': 'Server error has occured!'}, 500

    # Migrate/Update db
    Migrate(app, db)

    return app
