# -*- coding: utf-8 -*-
"""Currency scheme."""
from marshmallow import EXCLUDE, ValidationError, fields, validates
from sqlalchemy import func

from evolux_solution.extensions import ma

from .models import Currency


class CurrencySchema(ma.SQLAlchemySchema):
    """A scheme for serialization/deserialization currency data."""

    code = fields.String(required=True)
    name = fields.String(required=True)

    class Meta:
        """Schema configuration."""

        model = Currency
        unknown = EXCLUDE
        load_instance = True

    @validates("code")
    def no_duplicate_code(self, value):
        """Checks if code is already in use."""
        if (not self.instance or self.instance.code != value) and Currency.query.filter(
            func.lower(Currency.code) == func.lower(value)
        ).first() is not None:
            raise ValidationError("There is already a currency with this code.")
