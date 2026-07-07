from datetime import datetime

from pydantic import BaseModel, Field


class ReportSection(BaseModel):
    title: str
    content: str | list[str]


class ReportResponse(BaseModel):
    id: str
    experiment_id: str | None = None
    title: str
    generated_at: datetime
    sections: list[ReportSection] = Field(default_factory=list)
    experiment: dict = Field(default_factory=dict)
    personas: list[dict] = Field(default_factory=list)
    insights: dict = Field(default_factory=dict)
    validation_score: int = 0
    summary: str = ""
