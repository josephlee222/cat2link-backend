from flask import Blueprint, jsonify
from app.extensions import db
from app.models.Category import Category
from app.models.Project import Project
from sqlalchemy import select

categoryRoutes = Blueprint("category", __name__)

@categoryRoutes.route("/<int:category_id>", methods=["GET"]) 
@categoryRoutes.route("/", methods=["GET"]) 
def get_category(category_id=None):
    if category_id is None:
        stmt = select(Category)
        categories = db.session.execute(stmt).scalars().all()
        return jsonify([category.get_info() for category in categories]), 200

    # Fetch the category from the database using the category_id
    stmt = select(Category).where(Category.id == category_id)
    category = db.session.execute(stmt).scalar_one_or_none()

    if category:
        # Return the category data as JSON
        return jsonify(category.get_info()), 200
    else:
        # Return an error message if the category is not found
        return jsonify({"error": "Category not found"}), 404
