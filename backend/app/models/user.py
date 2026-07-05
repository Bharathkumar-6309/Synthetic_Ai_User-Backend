"""
Minimal user model. Full auth (JWT issuing/validation, bcrypt hashing flows)
is a Milestone-4-adjacent concern per the middleware/auth module, but the
table exists now so Experiment.owner_id has somewhere to point.
"""
from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPKMixin


class User(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    experiments: Mapped[list["Experiment"]] = relationship(  # noqa: F821
        back_populates="owner", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r}>"
