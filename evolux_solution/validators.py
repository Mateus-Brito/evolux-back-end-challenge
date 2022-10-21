# -*- coding: utf-8 -*-
"""Custom validators."""
from marshmallow import validate

phone_validator = validate.Regexp(
    regex="^([+]|[00]{2})([0-9]|[ -])*",
    error="Please, enter with a valid phone number.",
)
numeric_validator = [validate.Range(min=0, error="Value must be greater than 0.")]
