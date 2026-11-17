from flask import Blueprint, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length
from app.extensions import db
from app.models.User import User
from sqlalchemy import select

userRoutes = Blueprint("user", __name__)

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=80, message="Username must be less than 80 characters")])
    email = StringField('Email', validators=[DataRequired(), Email("Must be a valid e-mail"), Length(max=120, message="Email must be less than 120 characters")])
    password = StringField('Password', validators=[DataRequired()])

# Route to get all users
@userRoutes.route("/", methods=["GET"])
def get_users():
    stmt = select(User)
    users = db.session.scalars(stmt).all()
    return jsonify([{"id": u.id, "username": u.username, "email": u.email} for u in users])



@userRoutes.route('/', methods=['POST'])
def register():
    json_data = request.get_json(silent=True) or {}
    form = RegisterForm(data=json_data)

    if form.validate():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
    else:
        return jsonify({"status": "error", "errors": form.errors}), 400

    db.session.add(user)
    db.session.commit()

    return jsonify({"status": "success", "message": "User registered successfully"}), 200
