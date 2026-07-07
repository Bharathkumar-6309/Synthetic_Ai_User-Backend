from pydantic import BaseModel, ConfigDict, computed_field


def _derive_adoption_score(product_fit_score: float | None, consistency_seed: int) -> float:
    if product_fit_score is not None:
        return round(product_fit_score, 1)
    return round(3.0 + (consistency_seed % 70) / 10.0, 1)


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
    consistency_seed: int = 0

    @computed_field  # type: ignore[prop-decorator]
    @property
    def tags(self) -> list[str]:
        return self.personality_traits[:4]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def adoption_score(self) -> float:
        return _derive_adoption_score(self.product_fit_score, self.consistency_seed)


class PersonaListResponse(BaseModel):
    total: int
    experiment_id: str
    items: list[PersonaResponse]
