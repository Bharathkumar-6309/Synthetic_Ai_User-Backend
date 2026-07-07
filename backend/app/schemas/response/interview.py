from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InterviewSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    experiment_id: str
    persona_id: str
    status: str
    messages: list[dict]
    summary: str | None
    created_at: datetime
    updated_at: datetime


class InterviewStartResponse(BaseModel):
    session_id: str
    persona_id: str
    experiment_id: str
    status: str = "active"


class InterviewMessageResponse(BaseModel):
    session_id: str
    response: str
    persona_id: str


class InterviewHistoryResponse(BaseModel):
    session_id: str
    persona_id: str
    messages: list[dict]
