"""Shared model mixins."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class UUIDPKMixin:
    id: Mapped[str] = mapped_column(
        String(36),  # MySQL requires explicit VARCHAR length; UUID is always 36 chars
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )


class TimestampMixin:
    # Python-side defaults (not server_default/onupdate=func.now()) on purpose:
    # server-generated onupdate values require SQLAlchemy to refresh the
    # attribute from the DB after flush/commit, which triggers a synchronous
    # round-trip that raises MissingGreenlet under the async SQLite driver.
    # Python-side defaults avoid that refresh entirely and work identically
    # against Postgres.
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )
