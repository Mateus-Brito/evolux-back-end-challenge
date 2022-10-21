# -*- coding: utf-8 -*-
"""Auth models."""
from evolux_solution.database import Column, PkModel, db, reference_col, relationship


class TokenBlocklist(PkModel):
    """Blocklist representation."""

    jti = Column(db.String(36), nullable=False, unique=True)
    token_type = Column(db.String(10), nullable=False)
    user_id = reference_col("users", nullable=False)
    revoked = Column(db.Boolean, nullable=False)
    expires = Column(db.DateTime, nullable=False)

    user = relationship("User", lazy="joined")

    def to_dict(self):
        """Represent instance as a dictionary."""
        return {
            "token_id": self.id,
            "jti": self.jti,
            "token_type": self.token_type,
            "user_identity": self.user_identity,
            "revoked": self.revoked,
            "expires": self.expires,
        }
