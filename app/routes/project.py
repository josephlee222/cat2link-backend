import os

from flask import Blueprint, current_app, jsonify
from app.extensions import db
from app.models.Project import Project
from sqlalchemy import select

projectRoutes = Blueprint("project", __name__)

@projectRoutes.route("/<int:project_id>", methods=["GET"]) 
@projectRoutes.route("/", methods=["GET"]) 
def get_project(project_id=None):
    if project_id is None:
        stmt = select(Project)
        projects = db.session.execute(stmt).scalars().all()
        return jsonify([project.get_summary() for project in projects]), 200

    # Fetch the project from the database using the project_id
    stmt = select(Project).where(Project.id == project_id)
    project = db.session.execute(stmt).scalar_one_or_none()

    if project:
        # Return the project data as JSON
        return jsonify(project.get_info()), 200
    else:
        # Return an error message if the project is not found
        return jsonify({"error": "Project not found"}), 404


@projectRoutes.route("/<int:project_id>/thumbnail", methods=["GET"])
def get_project_thumbnail(project_id):
    stmt = select(Project).where(Project.id == project_id)
    project = db.session.execute(stmt).scalar_one_or_none()

    if project and project.thumbnail_media:
        upload_dir = current_app.config["UPLOAD_FOLDER"]
        filename = project.thumbnail_media.url  # Assuming the URL is the filename
        file_path = os.path.join(upload_dir, filename)
        print(f"Looking for file at: {file_path}")
        if os.path.exists(file_path):
            from flask import send_file
            return send_file(file_path)
        return jsonify({"error": "File not found"}), 404
    elif project:
        return jsonify({"error": "Thumbnail not found"}), 404
    else:
        return jsonify({"error": "Project not found"}), 404
