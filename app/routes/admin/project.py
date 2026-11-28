from flask import Blueprint, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Email
from app.extensions import db
from app.models.Project import Project
from sqlalchemy import select
from app.decorators import admin_auth_required
from app.common import generate_error_response

adminProjectRoutes = Blueprint("admin_project", __name__)

class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=80, message="Name must be less than 80 characters")])
    description = StringField('Description', validators=[DataRequired()])
    short_description = StringField('Short Description', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired(), Length(max=1024, message="URL must be less than 1024 characters")])
    category_id = StringField('Category ID', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])

@adminProjectRoutes.route("/<int:project_id>", methods=["GET"]) 
@adminProjectRoutes.route("/", methods=["GET"])
@admin_auth_required
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
        return generate_error_response("Project not found", 404)


@adminProjectRoutes.route("/", methods=["POST"])
@admin_auth_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            name=form.name.data,
            description=form.description.data,
            short_description=form.short_description.data,
            url=form.url.data,
            category_id=form.category_id.data,
            year=form.year.data
        )
        db.session.add(project)
        db.session.commit()
        return jsonify({"status": "success", "project": project.get_summary()}), 201
    return generate_error_response("Validation failed", 400, errors=form.errors)


@adminProjectRoutes.route("/<int:project_id>", methods=["DELETE"])
@admin_auth_required
def delete_project(project_id):
    stmt = select(Project).where(Project.id == project_id)
    project = db.session.execute(stmt).scalar_one_or_none()
    if project:
        db.session.delete(project)
        db.session.commit()
        return jsonify({"status": "success"}), 200
    else:
        return generate_error_response("Project not found", 404)


@adminProjectRoutes.route("/<int:project_id>", methods=["PUT"])
@admin_auth_required
def update_project(project_id):
    form = ProjectForm()
    if form.validate_on_submit():
        stmt = select(Project).where(Project.id == project_id)
        project = db.session.execute(stmt).scalar_one_or_none()
        if project:
            project.name = form.name.data
            project.description = form.description.data
            project.short_description = form.short_description.data
            project.url = form.url.data
            project.category_id = form.category_id.data
            project.year = form.year.data
            db.session.commit()
            return jsonify({"status": "success", "project": project.get_summary()}), 200
        else:
            return generate_error_response("Project not found", 404)

    return generate_error_response("Validation failed", 400, errors=form.errors)