from pydantic import BaseModel, Field, field_validator


class ExperimentCreateRequest(BaseModel):
    """Payload for creating a new experiment workspace."""

    title: str = Field(..., min_length=3, max_length=200, examples=["Meal-Prep App Validation"])
    product_description: str = Field(
        ...,
        min_length=10,
        description="What the product/feature is and what it does.",
        examples=["An AI-powered app that plans weekly meals based on pantry inventory."],
    )
    target_audience: str = Field(
        ...,
        min_length=5,
        description="Who the product is for (demographics, segment, behavior).",
        examples=["Busy urban professionals aged 25-40 who cook 3-5x/week."],
    )
    research_objectives: str = Field(
        ...,
        min_length=5,
        description="What the user wants to learn/validate from this experiment.",
        examples=["Would they trust an AI to plan meals? What's the price sensitivity?"],
    )
    persona_count: int = Field(
        default=6, ge=3, le=12, description="Number of synthetic personas to generate (3-12)."
    )

    @field_validator("title", "product_description", "target_audience", "research_objectives")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class ExperimentUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    product_description: str | None = Field(default=None, min_length=10)
    target_audience: str | None = Field(default=None, min_length=5)
    research_objectives: str | None = Field(default=None, min_length=5)
