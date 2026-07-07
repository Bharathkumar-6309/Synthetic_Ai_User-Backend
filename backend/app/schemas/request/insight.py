from pydantic import BaseModel, Field


class InsightExtractRequest(BaseModel):
    experiment_id: str | None = None
    persona_ids: list[str] = Field(default_factory=list)
    personas: list[dict] = Field(default_factory=list)
    survey_responses: dict | list = Field(default_factory=dict)
    chat_history: dict[str, list[dict]] = Field(default_factory=dict)
