"""
Persona Generation Agent.

Orchestrated as a small LangGraph graph:

    generate --> validate --(valid)--> finalize --> END
        ^            |
        | (retry)     (invalid, retries left)
        +-------------+
                       |
                (invalid, out of retries)  --> synthetic_fallback --> finalize --> END

If the LLM layer is entirely unavailable (no Gemini key, Ollama unreachable),
`generate` short-circuits straight to `synthetic_fallback` so the platform
remains fully usable offline/in demos — this matters for early-stage teams
with no research budget, which is the whole premise of the project.
"""
from __future__ import annotations

import hashlib
import random
from typing import Any, TypedDict

from faker import Faker
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field, ValidationError

from app.ai.llm_client import LLMClient
from app.ai.model_router import ModelRouter
from app.ai.prompt_manager import PromptManager
from app.exceptions.llm_exceptions import LLMError

MAX_GENERATION_ATTEMPTS = 2

fake = Faker()


# --------------------------------------------------------------------------
# Structured persona shape produced by the agent (pre-DB-persistence)
# --------------------------------------------------------------------------
class PersonaProfile(BaseModel):
    name: str
    age: int = Field(ge=13, le=95)
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
    quote: str | None = None

    generation_source: str = "llm"

    @property
    def avatar_seed(self) -> str:
        return hashlib.md5(self.name.encode()).hexdigest()[:12]

    @property
    def persona_hash(self) -> str:
        fingerprint = f"{self.name}|{self.age}|{self.occupation}|{self.location}"
        return hashlib.sha256(fingerprint.encode()).hexdigest()

    @property
    def consistency_seed(self) -> int:
        return int(hashlib.sha256(self.persona_hash.encode()).hexdigest(), 16) % (2**31)


class PersonaBatch(BaseModel):
    personas: list[PersonaProfile]


# --------------------------------------------------------------------------
# LangGraph state
# --------------------------------------------------------------------------
class PersonaAgentState(TypedDict):
    product_description: str
    target_audience: str
    research_objectives: str
    persona_count: int

    attempt: int
    raw_personas: list[dict[str, Any]]
    errors: list[str]
    generation_source: str
    final_personas: list[PersonaProfile]


# --------------------------------------------------------------------------
# Node implementations
# --------------------------------------------------------------------------
async def generate_node(state: PersonaAgentState) -> PersonaAgentState:
    router = ModelRouter()
    state["attempt"] += 1

    if not router.has_any_llm_configured():
        # No Gemini key configured. We still let Ollama be attempted inside
        # LLMClient (in case it's running locally), but we don't block on it —
        # any failure there falls through to validate_node with empty output,
        # which routes to synthetic_fallback.
        pass

    client = LLMClient()
    system_prompt = PromptManager.load("persona/system.txt").format(persona_count=state["persona_count"])
    user_prompt = PromptManager.render(
        "persona/user.txt",
        product_description=state["product_description"],
        target_audience=state["target_audience"],
        research_objectives=state["research_objectives"],
        persona_count=state["persona_count"],
    )

    try:
        result = await client.generate_json(system_prompt, user_prompt)
        state["raw_personas"] = result.get("personas", [])
        state["generation_source"] = "llm"
    except LLMError as e:
        state["errors"].append(str(e))
        state["raw_personas"] = []

    return state


def validate_node(state: PersonaAgentState) -> PersonaAgentState:
    try:
        batch = PersonaBatch(personas=state["raw_personas"])
        if len(batch.personas) < 1:
            raise ValueError("LLM returned zero personas")
        state["final_personas"] = [
            p.model_copy(update={"generation_source": state.get("generation_source", "llm")})
            for p in batch.personas
        ]
    except (ValidationError, ValueError) as e:
        state["errors"].append(f"validation failed: {e}")
        state["final_personas"] = []
    return state


def route_after_validate(state: PersonaAgentState) -> str:
    if state["final_personas"]:
        return "finalize"
    if state["attempt"] < MAX_GENERATION_ATTEMPTS:
        return "retry"
    return "fallback"


def synthetic_fallback_node(state: PersonaAgentState) -> PersonaAgentState:
    """
    Deterministic-ish offline generator using Faker. Ensures the platform is
    demoable/testable with zero API keys and never hard-fails a research
    session just because the LLM provider is down.
    """
    traits_pool = [
        "pragmatic", "curious", "skeptical", "early-adopter", "budget-conscious",
        "brand-loyal", "impulsive", "detail-oriented", "social", "introverted",
        "time-poor", "value-driven", "trend-aware", "cautious", "impatient",
    ]
    habits_pool = [
        "checks phone first thing in the morning", "reads reviews before buying",
        "compares prices across apps", "asks friends for recommendations",
        "watches short-form video during commute", "meal-preps on Sundays",
        "listens to podcasts while working out", "uses a to-do app daily",
    ]
    values_pool = ["convenience", "trust", "affordability", "sustainability", "status", "autonomy", "community"]
    motivations_pool = ["saving time", "saving money", "feeling in control", "looking good to peers", "reducing stress", "staying healthy"]
    pain_points_pool = ["too many steps to get started", "hidden costs", "doesn't trust automated recommendations", "clutter and information overload", "poor customer support experiences"]
    occupations = ["Software Engineer", "Nurse", "Teacher", "Small Business Owner", "Graphic Designer", "Sales Manager", "Graduate Student", "Freelance Consultant", "Operations Analyst", "Marketing Coordinator"]
    tech_levels = ["low", "medium", "high"]
    risk_levels = ["low", "medium", "high"]
    income_brackets = ["Low", "Middle", "Upper-middle", "High"]

    personas: list[PersonaProfile] = []
    for _ in range(state["persona_count"]):
        gender = random.choice(["Female", "Male", "Non-binary"])
        name = fake.name_female() if gender == "Female" else fake.name_male() if gender == "Male" else fake.name()
        age = random.randint(19, 65)
        occupation = random.choice(occupations)
        bio = (
            f"{name.split()[0]} is a {age}-year-old {occupation.lower()} based in {fake.city()}. "
            f"{random.choice(['They', 'They']).capitalize()} {random.choice(habits_pool)} and generally "
            f"{random.choice(['prefers simple, no-friction experiences', 'likes to research thoroughly before committing', 'trusts recommendations from people they know'])}."
        )
        personas.append(
            PersonaProfile(
                name=name,
                age=age,
                gender=gender,
                occupation=occupation,
                location=f"{fake.city()}, {fake.country()}",
                income_bracket=random.choice(income_brackets),
                education_level=random.choice(["High School", "Bachelor's Degree", "Master's Degree", "Associate Degree"]),
                personality_traits=random.sample(traits_pool, k=4),
                behavioral_patterns=random.sample(habits_pool, k=3),
                tech_savviness=random.choice(tech_levels),
                daily_habits=random.sample(habits_pool, k=3),
                core_values=random.sample(values_pool, k=3),
                motivations=random.sample(motivations_pool, k=3),
                pain_points=random.sample(pain_points_pool, k=3),
                risk_tolerance=random.choice(risk_levels),
                bio=bio,
                quote=f"\"I just want something that {random.choice(['works without a learning curve', 'actually saves me time', 'I can trust with my money', 'my friends are already using'])}.\"",
                generation_source="synthetic_fallback",
            )
        )

    state["final_personas"] = personas
    state["generation_source"] = "synthetic_fallback"
    return state


def finalize_node(state: PersonaAgentState) -> PersonaAgentState:
    # Personas are already validated PersonaProfile instances at this point.
    # This node is a seam for future enrichment (e.g. dedupe, diversity scoring)
    # without touching generate/validate logic.
    return state


# --------------------------------------------------------------------------
# Graph assembly
# --------------------------------------------------------------------------
def build_persona_graph():
    graph = StateGraph(PersonaAgentState)

    graph.add_node("generate", generate_node)
    graph.add_node("validate", validate_node)
    graph.add_node("synthetic_fallback", synthetic_fallback_node)
    graph.add_node("finalize", finalize_node)

    graph.set_entry_point("generate")
    graph.add_edge("generate", "validate")
    graph.add_conditional_edges(
        "validate",
        route_after_validate,
        {
            "finalize": "finalize",
            "retry": "generate",
            "fallback": "synthetic_fallback",
        },
    )
    graph.add_edge("synthetic_fallback", "finalize")
    graph.add_edge("finalize", END)

    return graph.compile()


_persona_graph = build_persona_graph()


async def generate_personas(
    *,
    product_description: str,
    target_audience: str,
    research_objectives: str,
    persona_count: int,
) -> list[PersonaProfile]:
    """Public entrypoint used by PersonaService."""
    initial_state: PersonaAgentState = {
        "product_description": product_description,
        "target_audience": target_audience,
        "research_objectives": research_objectives,
        "persona_count": persona_count,
        "attempt": 0,
        "raw_personas": [],
        "errors": [],
        "generation_source": "llm",
        "final_personas": [],
    }
    result_state = await _persona_graph.ainvoke(initial_state)
    return result_state["final_personas"]
