"""Persisted research reports for experiments."""
from __future__ import annotations

from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPKMixin


class Report(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "reports"

    experiment_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), default="")
    summary: Mapped[str] = mapped_column(String(5000), default="")
    persona_profiles: Mapped[list[dict]] = mapped_column(JSON, default=list)
    response_highlights: Mapped[list[dict]] = mapped_column(JSON, default=list)
    insight_summary: Mapped[dict] = mapped_column(JSON, default=dict)
    validation_scoring: Mapped[dict] = mapped_column(JSON, default=dict)
    recommendations: Mapped[list[dict]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(50), default="generating")  # generating, ready, failed
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    error_message: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    experiment: Mapped["Experiment"] = relationship(back_populates="reports")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Report id={self.id} experiment={self.experiment_id} status={self.status}>"
