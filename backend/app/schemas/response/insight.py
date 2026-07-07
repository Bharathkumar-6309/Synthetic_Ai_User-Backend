from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ThemeItem(BaseModel):
    theme: str
    mentions_pct: int


class QuoteItem(BaseModel):
    quote: str
    persona: str


class SuggestionItem(BaseModel):
    suggestion: str
    category: str
    priority: str = "medium"
    personas: list[str] = Field(default_factory=list)
    mentions_pct: int | None = None


class InsightResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | None = None
    experiment_id: str | None = None
    would_use_pct: int = 0
    would_pay_pct: int = 0
    themes: list[ThemeItem] = Field(default_factory=list)
    sentiment: dict[str, int] = Field(default_factory=dict)
    key_quotes: list[QuoteItem] = Field(default_factory=list)
    suggestions: list[SuggestionItem] = Field(default_factory=list)
    user_wants_summary: str = ""
    persona_scores: dict[str, float] = Field(default_factory=dict)
    created_at: datetime | None = None
