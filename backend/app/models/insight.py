"""Persisted insight extraction results for an experiment."""
from __future__ import annotations

from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDPKMixin


class Insight(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "insights"

    experiment_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    would_use_pct: Mapped[int] = mapped_column(default=0)
    would_pay_pct: Mapped[int] = mapped_column(default=0)
    themes: Mapped[list[dict]] = mapped_column(JSON, default=list)
    sentiment: Mapped[dict[str, int]] = mapped_column(JSON, default=dict)
    key_quotes: Mapped[list[dict]] = mapped_column(JSON, default=list)
    suggestions: Mapped[list[dict]] = mapped_column(JSON, default=list)
    user_wants_summary: Mapped[str] = mapped_column(String(2000), default="")
    persona_scores: Mapped[dict[str, float]] = mapped_column(JSON, default=dict)
    raw_data: Mapped[dict] = mapped_column(JSON, default=dict)

    experiment: Mapped["Experiment"] = relationship(back_populates="insights")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Insight id={self.id} experiment={self.experiment_id}>"
