# -*- coding: utf-8 -*-
"""phone views."""
from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import verify_jwt_in_request
from marshmallow import ValidationError

from evolux_solution.views import ViewPaginator

from .models import Phone
from .serializer import PhoneSchema

blueprint = Blueprint("phone", __name__, url_prefix="/api/phones")


class PhoneAPI(MethodView, ViewPaginator):
    """Phone API CRUD."""

    def __init__(self):
        """Checks access authorization in the requests."""
        verify_jwt_in_request()

    def get(self, phone_id=None):
        """Get phones availables or filter by id."""
        phone_schema = PhoneSchema()
        if phone_id is None:
            return self.get_paginated_response(Phone.query, PhoneSchema)
        else:
            phone = Phone.query.filter_by(id=phone_id).first()
            if phone is None:
                return jsonify({"message": "Phone not found."}), 400
            return jsonify(phone_schema.dump(phone))

    def post(self):
        """Create new phone record."""
        try:
            json_data = request.json
            if not json_data:
                return jsonify({"message": "Invalid request"}), 400

            phone_schema = PhoneSchema()
            phone = phone_schema.load(json_data)
            phone.save()
            return jsonify(phone_schema.dump(phone)), 201
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

    def put(self, phone_id):
        """Update phone record."""
        try:
            json_data = request.json
            if not json_data:
                return jsonify({"message": "Invalid request"}), 400

            phone_schema = PhoneSchema()
            phone = Phone.query.filter_by(id=phone_id).first()
            if phone is None:
                return jsonify({"message": "Currency not found"}), 400

            updated_phone = phone_schema.load(json_data, instance=phone)
            updated_phone.save()
            return jsonify(phone_schema.dump(phone)), 200
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

    def delete(self, phone_id):
        """Delete phone record."""
        phone = Phone.query.filter_by(id=phone_id).first()
        if phone is None:
            return jsonify({"message": "Phone not found."}), 400

        phone.delete()
        return jsonify({"message": "Phone deleted."}), 200


phone_view = PhoneAPI.as_view("phones")
blueprint.add_url_rule(
    "/",
    view_func=phone_view,
    methods=["GET", "POST"],
)
blueprint.add_url_rule(
    "/<int:phone_id>",
    view_func=phone_view,
    methods=[
        "GET",
        "PUT",
        "DELETE",
    ],
)
