# -*- coding: utf-8 -*-
"""phone scheme."""
from marshmallow import EXCLUDE, ValidationError, fields, validates

from evolux_solution.currency.models import Currency
from evolux_solution.extensions import ma
from evolux_solution.schemas import CamelCasedSchema
from evolux_solution.validators import numeric_validator, phone_validator

from .models import Phone


class PhoneSchema(ma.SQLAlchemySchema, CamelCasedSchema):
    """A scheme for serialization/deserialization phone data."""

    id = fields.String(dump_only=True)
    value = fields.String(required=True, validate=phone_validator)
    monthy_price = fields.Decimal(required=True, validate=numeric_validator)
    setup_price = fields.Decimal(required=True, validate=numeric_validator)
    currency = fields.String(required=True, attribute="currency_id")

    class Meta:
        """Schema configuration."""

        model = Phone
        unknown = EXCLUDE
        load_instance = True

    @validates("value")
    def validate_value(self, value: dict):
        """Checks if phone value is already in use."""
        if (
            not self.instance or self.instance.value != value
        ) and Phone.query.filter_by(value=value).first() is not None:
            raise ValidationError("There is already a phone with this value.")

    @validates("currency")
    def validate_currency(self, value: dict):
        """Checks if currency alredy exist."""
        currency = Currency.query.filter_by(code=value).first()
        if not currency:
            raise ValidationError("There is no currency with code.")
