from pydantic import BaseModel, Field


class PersonaGenerateRequest(BaseModel):
    """Optional overrides when (re)generating personas for an experiment."""

    persona_count: int | None = Field(
        default=None, ge=3, le=12, description="Override experiment's default persona_count."
    )
    regenerate: bool = Field(
        default=False,
        description="If true, deletes existing personas for this experiment before generating new ones.",
    )
