from pydantic import BaseModel, Field


class InterviewStartRequest(BaseModel):
    experiment_id: str
    persona_id: str


class InterviewMessageRequest(BaseModel):
    session_id: str | None = None
    persona_id: str
    message: str
    history: list[dict[str, str]] = Field(default_factory=list)


class InterviewEndRequest(BaseModel):
    session_id: str
