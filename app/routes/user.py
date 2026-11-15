from flask import Blueprint, jsonify, request
from app.database import db
from app.models.User import User
from sqlalchemy import select

userRoutes = Blueprint("user", __name__)

# Route to get all users
@userRoutes.route("/", methods=["GET"])
def get_users():
    stmt = select(User)
    users = db.session.scalars(stmt).all()
    return jsonify([{"id": u.id, "username": u.username, "email": u.email} for u in users])

# Route to create a new user
@userRoutes.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    
    if not data or "username" not in data or "email" not in data:
        return jsonify({"error": "Bad request"}), 400

    new_user = User(username=data["username"], email=data["email"])
    
    db.session.add(new_user)
    db.session.commit()  # Commit changes to the database
    
    return jsonify({"message": "User created successfully", "id": new_user.id}), 201
