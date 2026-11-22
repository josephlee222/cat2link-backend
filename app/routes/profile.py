from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.User import User
from sqlalchemy import select
from app.decorators import auth_required

profileRoutes = Blueprint("profile", __name__)

@profileRoutes.route("/profile", methods=["GET"]) 
@auth_required
def get_profile(user_id):
    # Fetch the user from the database using the user_id
    stmt = select(User).where(User.id == user_id)
    user = db.session.execute(stmt).scalar_one_or_none()

    if user:
        # Return the user data as JSON
        return jsonify(user.get_profile()), 200
    else:
        # Return an error message if the user is not found
        return jsonify({"error": "User not found"}), 404
    
