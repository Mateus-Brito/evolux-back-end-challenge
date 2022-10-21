# -*- coding: utf-8 -*-
"""user view."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from marshmallow import ValidationError

from evolux_solution.database import db

from .serializer import UserSchema

blueprint = Blueprint("user", __name__, url_prefix="/api/users")


@blueprint.route("/self", methods=["GET"])
@jwt_required()
def get_current_user():
    """Get authentiqued user data."""
    user_schema = UserSchema()
    return jsonify(user_schema.dump(current_user))


@blueprint.route("/signup", methods=["POST"])
def register_user():
    """Register new user."""
    user_schema = UserSchema()
    try:
        user = user_schema.load(request.get_json(), session=db.session)
        user.save()
        return jsonify(user_schema.dump(user)), 201
    except ValidationError as err:
        return {"errors": err.messages}, 400
