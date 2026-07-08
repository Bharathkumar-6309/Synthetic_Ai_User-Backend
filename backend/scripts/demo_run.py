"""Simple demo runner to exercise Interview Mode and Insight generation without a frontend.

Run with: python -m backend.scripts.demo_run
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.database import Base
from app.models.experiment import Experiment, ExperimentStatus
from app.services.persona_service import PersonaService
from app.services.survey_service import SurveyService
from app.services.interview_service import InterviewService
from app.services.insight_service import InsightService


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


async def main() -> None:
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Create an experiment
        experiment = Experiment(
            title="Demo Product",
            product_description="A demo product for running insights",
            target_audience="Demo users",
            research_objectives="Validate demo flow",
            persona_count=3,
            status=ExperimentStatus.PERSONAS_READY,
        )
        session.add(experiment)
        await session.commit()
        await session.refresh(experiment)

        # Generate personas using PersonaService
        persona_service = PersonaService(session)
        personas = await persona_service.generate_for_experiment(experiment.id, persona_count=3)
        print(f"Created {len(personas)} personas")

        # Create a simple survey and generate responses
        survey_service = SurveyService(session)
        survey = await survey_service.create(
            experiment_id=experiment.id,
            title="Demo Survey",
            questions=["What do you think?", "Would you use this product?"],
        )
        # Generate responses via SurveyService (it uses agents internally)
        await survey_service.generate_responses_for_survey(survey.id)
        print("Generated survey responses")

        # Create interview sessions and run one message per persona
        interview_service = InterviewService(session)
        interview_agent = None
        from app.agents.interview_agent import InterviewAgent
        interview_agent = InterviewAgent()

        interviews = []
        for p in personas:
            interview = await interview_service.create(experiment.id, p.id)
            # send a user message and get persona reply
            await interview_service.add_message(interview.id, "user", "What do you think about this product?")
            reply = await interview_agent.generate_reply(
                persona_attributes={
                    "id": str(p.id),
                    "name": p.name,
                    "age": p.age,
                    "occupation": p.occupation,
                    "personality_traits": p.personality_traits,
                    "core_values": p.core_values,
                    "bio": p.bio,
                    "persona_hash": p.persona_hash,
                    "consistency_seed": p.consistency_seed,
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
            interviews.append(interview)

        print(f"Created and ran {len(interviews)} interviews")

        # Generate insights
        insight_service = InsightService(session)
        insight = await insight_service.generate(experiment.id)

        print("Insight result:")
        print(f"Would use: {insight.would_use_pct}%")
        print(f"Would pay: {insight.would_pay_pct}%")
        print(f"Themes: {insight.themes}")
        print(f"Sentiment: {insight.sentiment}")


if __name__ == "__main__":
    asyncio.run(main())
