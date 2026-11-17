from flask import Blueprint, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Email
from app.extensions import db
from app.models.User import User
from sqlalchemy import select
from flask_jwt_extended import create_access_token

authRoutes = Blueprint("auth", __name__)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=80, message="Username must be less than 80 characters")])
    password = StringField('Password', validators=[DataRequired()])

@authRoutes.route('/login', methods=['POST'])
def login():
    json_data = request.get_json(silent=True) or {}
    form = LoginForm(data=json_data)

    if form.validate():
        q = select(User).where(User.username == form.username)
        user = db.session.scalar(q).first()

        if user is not None:
            if user.check_password(form.password):
                # Correct, make new jwt
                token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})

                return jsonify({"status": "success", "access_token": token}), 400
            else:
                return jsonify({"status": "error", "errors": ["User password is incorrect"]}), 400
        else:
            return jsonify({"status": "error", "errors": ["User does not exist"]}), 400



    return jsonify({"status": "error", "errors": form.errors}), 400