# -*- coding: utf-8 -*-
"""Currency models."""
from evolux_solution.database import Column, Model, db


class Currency(Model):
    """Currency availables when purchasing phone numbers."""

    code = Column(db.String(80), primary_key=True)
    name = Column(db.String(80), nullable=False)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Currency({self.code!r})>"
