# -*- coding: utf-8 -*-
"""User scheme."""
from marshmallow import EXCLUDE, ValidationError, fields, validates

from evolux_solution.extensions import ma

from .models import User


class UserSchema(ma.SQLAlchemySchema):
    """A scheme for serialization/deserialization user data."""

    id = fields.String(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)

    class Meta:
        """Schema configuration."""

        model = User
        unknown = EXCLUDE
        load_instance = True

    @validates("username")
    def no_duplicate_username(self, value):
        """Checks if username is already in use."""
        if User.query.filter_by(username=value).first() is not None:
            raise ValidationError("There is already a user with this username")

    @validates("email")
    def no_duplicate_email(self, value):
        """Checks if email is already in use."""
        if User.query.filter_by(email=value).first() is not None:
            raise ValidationError("There is already a user with this email")
