import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from app.extensions import db, jwt
from flask_jwt_extended import JWTManager
from datetime import timedelta
from app.common import generate_error_response
from flask_cors import CORS

import app.models
from app.models.User import User
from app.models.Category import Category

#Import Routes
from app.routes.admin.user import userRoutes
from app.routes.admin.project import adminProjectRoutes
from app.routes.admin.media import adminMediaRoutes
from app.routes.media import mediaRoutes
from app.routes.auth import authRoutes
from app.routes.project import projectRoutes
from app.routes.category import categoryRoutes


def create_app():
    load_dotenv()
    app = Flask(__name__)
    print(f"Project root path: {app.root_path}")
    UPLOAD_FOLDER = os.path.abspath(os.path.join(app.root_path, '..', os.environ.get("UPLOAD_FOLDER", "uploads")))
    print(f"Upload folder path: {UPLOAD_FOLDER}")
    
    # Configure SQLite database path (saves to the 'instance' folder)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['WTF_CSRF_ENABLED'] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=int(os.environ.get("JWT_ACCESS_TIMEOUT")))
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=int(os.environ.get("JWT_REFRESH_TIMEOUT")))
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024

    # Additional init functions
    def initialize_app():
        # Create user
        with app.app_context():
            if not User.query.filter_by(username="admin").first():
                admin = User(username="admin", name="Admin User", email="admin@admin.com", role="admin")
                admin.set_password("admin123")
                db.session.add(admin)
                db.session.commit()

            # Create default categories if the category table is empty
            default_categories = ["Category 1", "Category 2"]
            if not Category.query.first():
                for category_name in default_categories:
                    category = Category(name=category_name)
                    db.session.add(category)
                db.session.commit()

            # Create uploads directory if it doesn't exist
            upload_dir = UPLOAD_FOLDER
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

    # Initialize the app with the extension
    db.init_app(app)

    # Initialize JWT Manager with the app
    jwt.init_app(app)

    # Configure CORS for the app
    CORS(app, origins=[os.environ.get("CORS_ORIGIN"), "http://localhost:5173"], supports_credentials=True, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    # Initialisation tasks if required
    # initialize_app()

    app.register_blueprint(userRoutes, url_prefix="/admin/users")
    app.register_blueprint(adminProjectRoutes, url_prefix="/admin/projects")
    app.register_blueprint(authRoutes, url_prefix="/auth")
    app.register_blueprint(projectRoutes, url_prefix="/projects")
    app.register_blueprint(adminMediaRoutes, url_prefix="/admin/media")
    app.register_blueprint(mediaRoutes, url_prefix="/media")
    app.register_blueprint(categoryRoutes, url_prefix="/categories")

    @app.errorhandler(Exception)
    def internal_server_error(e):

        if hasattr(e, "code") and e.code == 404:
            return generate_error_response("Resource not found", 404)
        
        app.logger.error(f"Server error: {e}")
        return generate_error_response("Server error has occured!", 500)

    # Migrate/Update db
    Migrate(app, db)

    return app
