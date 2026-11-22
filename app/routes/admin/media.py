import os
import uuid
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from app.extensions import db
from app.models.Project import Project
from app.models.Media import Media
from sqlalchemy import select
from app.decorators import admin_auth_required
from app.common import generate_error_response

adminMediaRoutes = Blueprint("admin_media", __name__)


class MediaForm(FlaskForm):
    alt_text = StringField('Alt Text', validators=[DataRequired(), Length(max=255, message="Alt Text must be less than 255 characters")])
    project_id = StringField('Project ID', validators=[DataRequired()])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


# Route to upload media
@adminMediaRoutes.route("/", methods=["POST"])
@admin_auth_required
def add_media():
    if "file" not in request.files:
        return generate_error_response("No file part", 400)

    # get uploaded file and form data from multipart form
    file = request.files["file"]
    json_data = request.form.to_dict()
    

    if file.filename == "":
        return generate_error_response("No selected file", 400)

    
    form = MediaForm(data=json_data)
    if form.validate():
        if not allowed_file(file.filename):
            return generate_error_response("Invalid file type", 400)
        project_id = form.project_id.data
        stmt = select(Project).where(Project.id == project_id)
        project = db.session.execute(stmt).scalar_one_or_none()
        if project:
            media = Media(
                alt_text=form.alt_text.data,
                project_id=project.id
            )

            filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
            file_path = os.path.join(os.environ.get("UPLOAD_FOLDER", "uploads"), filename)
            file.save(file_path)
            media.url = filename

            db.session.add(media)
            db.session.commit()
            return jsonify({"status": "success", "media": media.get_summary()}), 201
        else:
            return generate_error_response("Project not found", 404)
    return generate_error_response("Validation failed", 400, errors=form.errors)


@adminMediaRoutes.route("/", methods=["GET"])
@admin_auth_required
def get_media():
    media_list = db.session.query(Media).all()
    return jsonify({"status": "success", "media": [m.get_summary() for m in media_list]}), 200


@adminMediaRoutes.route("/<int:media_id>", methods=["GET"])
@admin_auth_required
def get_media_by_id(media_id):
    media = db.session.query(Media).filter_by(id=media_id).first()
    if media:
        return jsonify({"status": "success", "media": media.get_summary()}), 200
    return generate_error_response("Media not found", 404)


@adminMediaRoutes.route("/<int:media_id>", methods=["DELETE"])
@admin_auth_required
def delete_media(media_id):
    media = db.session.query(Media).filter_by(id=media_id).first()
    if media:
        db.session.delete(media)
        db.session.commit()
        return jsonify({"status": "success", "message": "Media deleted"}), 200
    return generate_error_response("Media not found", 404)

