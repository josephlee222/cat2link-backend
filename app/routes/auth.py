from flask import Blueprint, jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Email
from app.extensions import db
from app.models.User import User
from sqlalchemy import select
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from app.common import generate_error_response

authRoutes = Blueprint("auth", __name__)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=80, message="Username must be less than 80 characters")])
    password = StringField('Password', validators=[DataRequired()])

@authRoutes.route('/login', methods=['POST'])
def login():
    json_data = request.get_json(silent=True) or {}
    form = LoginForm(data=json_data)

    if form.validate():
        user = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar_one_or_none()

        if user is not None:
            if user.check_password(form.password.data):
                # Correct, make new jwt
                access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
                refresh_token = create_refresh_token(identity=str(user.id), additional_claims={"role": user.role})

                # create cookie for refresh token
                response = jsonify({"status": "success", "access_token": access_token, "user": user.get_profile()})
                response.set_cookie("refresh_token", refresh_token, httponly=True, path="/auth/refresh", secure=True, samesite="Strict")
                return response, 200
            else:
                return generate_error_response("Username or password is incorrect", 401)
        else:
            return generate_error_response("Username or password is incorrect", 401)



    return generate_error_response("Validation failed", 400, errors=form.errors)


@authRoutes.route('/refresh', methods=['GET'])
@jwt_required(refresh=True, locations=["cookies"])
def refresh():
    current_user_id = get_jwt_identity()
    user = db.session.execute(db.select(User).filter_by(id=current_user_id)).scalar_one_or_none()

    if user is None:
        return generate_error_response("User not found", 404)

    access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})

    response = jsonify({"status": "success", "access_token": access_token, "user": user.get_profile()})
    return response, 200

@authRoutes.route('/logout', methods=['GET'])
def logout():
    response = jsonify({"status": "success"})
    response.set_cookie("refresh_token", "", expires=0, httponly=True, path="/auth/refresh", secure=True, samesite="Strict")
    return response, 200