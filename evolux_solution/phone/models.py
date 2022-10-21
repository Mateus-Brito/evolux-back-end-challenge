# -*- coding: utf-8 -*-
"""Phone models."""
from evolux_solution.database import Column, PkModel, db, reference_col


class Phone(PkModel):
    """Phones availables to purchase."""

    value = Column(db.String(80), unique=True)
    monthy_price = db.Column(db.Numeric(9, 2))
    setup_price = db.Column(db.Numeric(9, 2))
    currency_id = reference_col("currency", pk_name="code", nullable=False)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Phone({self.value!r})>"
