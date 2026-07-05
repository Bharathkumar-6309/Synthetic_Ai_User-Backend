from pydantic import BaseModel, ConfigDict


class PersonaResponse(BaseModel):
    """Shape returned to clients — this is the 'persona card' payload."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    experiment_id: str

    name: str
    age: int
    gender: str
    occupation: str
    location: str
    income_bracket: str
    education_level: str

    personality_traits: list[str]
    behavioral_patterns: list[str]
    tech_savviness: str
    daily_habits: list[str]

    core_values: list[str]
    motivations: list[str]
    pain_points: list[str]
    risk_tolerance: str

    bio: str
    avatar_seed: str
    quote: str | None

    generation_source: str
    product_fit_score: float | None


class PersonaListResponse(BaseModel):
    total: int
    experiment_id: str
    items: list[PersonaResponse]
