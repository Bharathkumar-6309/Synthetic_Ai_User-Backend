from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.experiment import ExperimentStatus


class ExperimentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    owner_id: str
    title: str
    product_description: str
    target_audience: str
    research_objectives: str
    persona_count: int
    status: ExperimentStatus
    created_at: datetime
    updated_at: datetime


class ExperimentListResponse(BaseModel):
    total: int
    items: list[ExperimentResponse]
