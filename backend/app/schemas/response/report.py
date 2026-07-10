from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | None = None
    experiment_id: str | None = None
    title: str = ""
    summary: str = ""
    persona_profiles: list[dict] = Field(default_factory=list)
    response_highlights: list[dict] = Field(default_factory=list)
    insight_summary: dict = Field(default_factory=dict)
    validation_scoring: dict = Field(default_factory=dict)
    recommendations: list[dict] = Field(default_factory=list)
    status: str = "generating"
    file_path: str | None = None
    error_message: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
