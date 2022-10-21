# -*- coding: utf-8 -*-
"""Custom schemas."""
import re
from functools import partial

from marshmallow import Schema

_camel_case = re.compile(r"(?<!^)(?=[A-Z])")
_snake_case = re.compile(r"(?<=\w)_(\w)")

_to_camel_case = partial(_snake_case.sub, lambda m: m[1].upper())
_to_snake_case = partial(_camel_case.sub, "_")


def dict_to_snake_case(_dict):
    """Convert a dictionary to snake_case."""
    _snake_dict = {}
    for key, value in _dict.items():
        _snake_dict[_to_snake_case(key).lower()] = value
    return _snake_dict


class CamelCasedSchema(Schema):
    """Gives fields a camelCased data key."""

    def on_bind_field(self, field_name, field_obj, _cc=_to_camel_case):
        """Hook to modify a field to snack_case when it is bound to the Schema."""
        field_obj.data_key = _cc(field_name.lower())
