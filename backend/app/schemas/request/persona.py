from pydantic import BaseModel, Field


class PersonaGenerateRequest(BaseModel):
    """
    Payload for POST /api/personas/generate.
    experiment_id lives in the body (not the path) to match the frontend's
    api_client.py contract.
    """

    experiment_id: str = Field(..., description="Experiment to generate personas for.")
    persona_count: int | None = Field(
        default=None, ge=3, le=12, description="Override experiment's default persona_count."
    )
    regenerate: bool = Field(
        default=False,
        description="If true, deletes existing personas for this experiment before generating new ones.",
    )
