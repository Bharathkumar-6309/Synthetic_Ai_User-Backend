from pydantic import BaseModel, Field


class ReportGenerateRequest(BaseModel):
    experiment: dict = Field(default_factory=dict)
    personas: list[dict] = Field(default_factory=list)
    insights: dict = Field(default_factory=dict)
    experiment_id: str | None = None
