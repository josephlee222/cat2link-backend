import os
from flask import Blueprint, jsonify, request, send_file, current_app
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from app.extensions import db
from app.models.Project import Project
from app.models.Media import Media
from sqlalchemy import select
from app.common import generate_error_response

mediaRoutes = Blueprint("media", __name__)

@mediaRoutes.route("/uploads/<filename>", methods=["GET"])
def get_uploaded_file(filename):
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    file_path = os.path.join(upload_dir, filename)
    print(f"Looking for file at: {file_path}")
    if os.path.exists(file_path):
        return send_file(file_path)
    return generate_error_response("File not found", 404)