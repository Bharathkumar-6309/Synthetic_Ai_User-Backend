"""Simple demo runner to exercise persona generation, surveys, interview mode, and insights.

Run with: python -m backend.scripts.demo_run
"""
import asyncio
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.agents.interview_agent import InterviewAgent
from app.core.database import Base
from app.core.config import get_settings
from app.models.experiment import Experiment, ExperimentStatus
from app.models.persona import Persona
from app.services.insight_service import InsightService
from app.services.interview_service import InterviewService
from app.services.persona_service import PersonaService
from app.services.survey_service import SurveyService

_settings = get_settings()
DEMO_DATABASE_URL = _settings.DATABASE_URL  # MySQL — same DB as the application


async def _create_demo_experiment(session: AsyncSession) -> Experiment:
    experiment = Experiment(
        owner_id="demo-owner",
        title="Demo Product",
        product_description="An AI-powered productivity assistant for small teams",
        target_audience="Startup founders and remote teams",
        research_objectives="Validate demand and uncover early adoption concerns",
        persona_count=3,
        status=ExperimentStatus.PERSONAS_READY,
    )
    session.add(experiment)
    await session.commit()
    await session.refresh(experiment)
    return experiment


async def _seed_survey_responses(session: AsyncSession, experiment: Experiment, personas: list[Persona]) -> None:
    survey_service = SurveyService(session)
    survey = await survey_service.create(
        experiment_id=experiment.id,
        title="Demo Survey",
        questions=["What do you think about this product?", "Would you use it?"],
    )

    for persona in personas:
        await survey_service.add_response(
            survey_id=survey.id,
            persona_id=str(persona.id),
            question_text="What do you think about this product?",
            answer_text=f"{persona.name} sees clear value and would try it if onboarding is simple.",
        )
        await survey_service.add_response(
            survey_id=survey.id,
            persona_id=str(persona.id),
            question_text="Would you use it?",
            answer_text="Yes, especially if the setup is straightforward.",
        )


async def _run_demo_interviews(session: AsyncSession, experiment: Experiment, personas: list[Persona]) -> None:
    interview_service = InterviewService(session)
    interview_agent = InterviewAgent()

    for persona in personas:
        interview = await interview_service.create(experiment.id, str(persona.id))
        await interview_service.add_message(interview.id, "user", "What do you think about this product?")
        reply = await interview_agent.generate_reply(
            persona_attributes={
                "id": str(persona.id),
                "name": persona.name,
                "age": persona.age,
                "occupation": persona.occupation,
                "personality_traits": persona.personality_traits,
                "core_values": persona.core_values,
                "bio": persona.bio,
                "persona_hash": persona.persona_hash,
                "consistency_seed": persona.consistency_seed,
            },
            message="What do you think about this product?",
            history=[],
            product_context={
                "title": experiment.title,
                "product_description": experiment.product_description,
                "target_audience": experiment.target_audience,
            },
        )
        await interview_service.add_message(interview.id, "assistant", reply)


async def main() -> None:
    engine = create_async_engine(DEMO_DATABASE_URL, echo=False)
    AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        experiment = await _create_demo_experiment(session)

        persona_service = PersonaService(session)
        personas = await persona_service.generate_for_experiment(experiment.id, persona_count=3)
        print(f"Created {len(personas)} personas")

        await _seed_survey_responses(session, experiment, personas)
        print("Generated survey responses")

        await _run_demo_interviews(session, experiment, personas)
        print("Completed demo interviews")

        insight_service = InsightService(session)
        insight = await insight_service.generate(experiment.id)

        print("\nInsight result:")
        print(f"Would use: {insight.would_use_pct}%")
        print(f"Would pay: {insight.would_pay_pct}%")
        print(f"Themes: {insight.themes}")
        print(f"Sentiment: {insight.sentiment}")


if __name__ == "__main__":
    asyncio.run(main())
