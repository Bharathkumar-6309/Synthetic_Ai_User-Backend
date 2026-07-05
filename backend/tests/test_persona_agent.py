import pytest

from app.agents.persona_agent import generate_personas


@pytest.mark.asyncio
async def test_generate_personas_offline_fallback():
    """
    With no GEMINI_API_KEY configured (default test env) and no local Ollama
    running, this should transparently use the synthetic fallback and still
    return a valid, fully-populated batch of personas.
    """
    personas = await generate_personas(
        product_description="An AI app that plans weekly meals from pantry inventory.",
        target_audience="Busy urban professionals aged 25-40.",
        research_objectives="Would they trust AI meal planning? Price sensitivity?",
        persona_count=4,
    )

    assert len(personas) == 4
    for p in personas:
        assert p.name
        assert 13 <= p.age <= 95
        assert p.generation_source in ("llm", "synthetic_fallback")
        assert len(p.personality_traits) >= 1
        assert len(p.pain_points) >= 1
        assert p.avatar_seed
        assert p.persona_hash
