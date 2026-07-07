"""Interview session model for one-on-one persona conversations."""
from __future__ import annotations

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPKMixin


class InterviewSession(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "interview_sessions"

    experiment_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    persona_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("personas.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    messages: Mapped[list[dict]] = mapped_column(JSON, default=list)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    persona: Mapped["Persona"] = relationship(back_populates="interview_sessions")  # noqa: F821
    experiment: Mapped["Experiment"] = relationship(back_populates="interview_sessions")  # noqa: F821

    def __repr__(self) -> str:
        return f"<InterviewSession id={self.id} persona={self.persona_id} status={self.status}>"
