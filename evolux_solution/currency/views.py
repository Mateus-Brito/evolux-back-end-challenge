# -*- coding: utf-8 -*-
"""currency view."""
from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import verify_jwt_in_request
from marshmallow import ValidationError
from sqlalchemy import func

from evolux_solution.database import db
from evolux_solution.views import ViewPaginator

from .models import Currency
from .serializer import CurrencySchema

blueprint = Blueprint("currency", __name__, url_prefix="/api/currencies")


class CurrencyAPI(MethodView, ViewPaginator):
    """Currency API CRUD."""

    def __init__(self):
        """Checks access authorization in the requests."""
        verify_jwt_in_request()

    def get(self, code=None):
        """Get currencies availables or filter by code."""
        currency_schema = CurrencySchema()
        if code is None:
            return self.get_paginated_response(Currency.query, CurrencySchema)
        else:
            currency = Currency.query.filter(
                func.lower(Currency.code) == func.lower(code)
            ).first()
            if currency is None:
                return jsonify({"message": "Currency not found"}), 400
            return jsonify(currency_schema.dump(currency))

    def post(self):
        """Create new currency record."""
        try:
            json_data = request.json
            if not json_data:
                return jsonify({"message": "Invalid request"}), 400

            currency_schema = CurrencySchema()
            currency = currency_schema.load(json_data, session=db.session)
            currency.save()
            return jsonify(currency_schema.dump(currency)), 201
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

    def put(self, code):
        """Update currency record."""
        try:
            json_data = request.json
            if not json_data:
                return jsonify({"message": "Invalid request"}), 400

            currency_schema = CurrencySchema()
            currency = Currency.query.filter(
                func.lower(Currency.code) == func.lower(code)
            ).first()
            if currency is None:
                return jsonify({"message": "Currency not found"}), 400

            new_currency = currency_schema.load(json_data, instance=currency)
            new_currency.save()
            return jsonify(currency_schema.dump(currency)), 200
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

    def delete(self, code):
        """Delete currency record."""
        currency = Currency.query.filter(
            func.lower(Currency.code) == func.lower(code)
        ).first()
        if currency is None:
            return jsonify({"message": "Currency not found."}), 400

        currency.delete()
        return jsonify({"message": "Currency deleted."}), 200


currency_view = CurrencyAPI.as_view("currencies")
blueprint.add_url_rule(
    "/",
    view_func=currency_view,
    methods=["GET", "POST"],
)
blueprint.add_url_rule(
    "/<string:code>",
    view_func=currency_view,
    methods=[
        "GET",
        "PUT",
        "DELETE",
    ],
)
