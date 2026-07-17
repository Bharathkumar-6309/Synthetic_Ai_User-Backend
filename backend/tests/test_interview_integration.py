"""
Integration tests for interview mode and insight extraction.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.database import Base
from app.models.experiment import Experiment, ExperimentStatus
from app.models.persona import Persona
from app.models.interview import InterviewSession
from app.models.insight import Insight
from app.models.response import Response
from app.models.survey import Survey, SurveyStatus
from app.services.interview_service import InterviewService
from app.services.insight_service import InsightService
from app.agents.interview_agent import InterviewAgent





@pytest.fixture
async def sample_experiment(db_session: AsyncSession):
    """Create a sample experiment for testing."""
    experiment = Experiment(
        title="Test Product",
        product_description="A test product for validation",
        target_audience="Test users",
        research_objectives="Test objectives",
        persona_count=3,
        status=ExperimentStatus.PERSONAS_READY,
    )
    db_session.add(experiment)
    await db_session.commit()
    await db_session.refresh(experiment)
    return experiment


@pytest.fixture
async def sample_personas(db_session: AsyncSession, sample_experiment):
    """Create sample personas for testing."""
    personas = []
    for i in range(3):
        persona = Persona(
            experiment_id=sample_experiment.id,
            name=f"Persona {i+1}",
            age=25 + i * 5,
            occupation=f"Profession {i+1}",
            personality_traits=["trait1", "trait2"],
            core_values=["value1", "value2"],
            bio=f"Bio for persona {i+1}",
            adoption_score=6.0 + i,
            persona_hash=f"hash_{i}",
            consistency_seed=42 + i,
        )
        db_session.add(persona)
        personas.append(persona)
    
    await db_session.commit()
    for persona in personas:
        await db_session.refresh(persona)
    return personas


class TestInterviewServiceIntegration:
    """Integration tests for InterviewService."""

    @pytest.mark.asyncio
    async def test_create_interview(self, db_session: AsyncSession, sample_experiment, sample_personas):
        """Test creating an interview session."""
        service = InterviewService(db_session)
        
        interview = await service.create(
            experiment_id=sample_experiment.id,
            persona_id=sample_personas[0].id,
        )
        
        assert interview.id is not None
        assert interview.experiment_id == sample_experiment.id
        assert interview.persona_id == sample_personas[0].id
        assert interview.status == "active"
        assert interview.messages == []

    @pytest.mark.asyncio
    async def test_create_interview_invalid_experiment(self, db_session: AsyncSession, sample_personas):
        """Test creating interview with invalid experiment ID."""
        service = InterviewService(db_session)
        
        with pytest.raises(Exception):  # NotFoundError
            await service.create(
                experiment_id="invalid_id",
                persona_id=sample_personas[0].id,
            )

    @pytest.mark.asyncio
    async def test_create_interview_invalid_persona(self, db_session: AsyncSession, sample_experiment):
        """Test creating interview with invalid persona ID."""
        service = InterviewService(db_session)
        
        with pytest.raises(Exception):  # NotFoundError
            await service.create(
                experiment_id=sample_experiment.id,
                persona_id="invalid_id",
            )

    @pytest.mark.asyncio
    async def test_add_message(self, db_session: AsyncSession, sample_experiment, sample_personas):
        """Test adding messages to an interview."""
        service = InterviewService(db_session)
        
        interview = await service.create(
            experiment_id=sample_experiment.id,
            persona_id=sample_personas[0].id,
        )
        
        updated = await service.add_message(
            interview_id=interview.id,
            role="user",
            content="Hello, how are you?",
        )
        
        assert len(updated.messages) == 1
        assert updated.messages[0]["role"] == "user"
        assert updated.messages[0]["content"] == "Hello, how are you?"

    @pytest.mark.asyncio
    async def test_list_interviews_for_experiment(self, db_session: AsyncSession, sample_experiment, sample_personas):
        """Test listing interviews for an experiment."""
        service = InterviewService(db_session)
        
        # Create multiple interviews
        for persona in sample_personas:
            await service.create(
                experiment_id=sample_experiment.id,
                persona_id=persona.id,
            )
        
        interviews = await service.list_for_experiment(sample_experiment.id)
        
        assert len(interviews) == len(sample_personas)

    @pytest.mark.asyncio
    async def test_update_interview_status(self, db_session: AsyncSession, sample_experiment, sample_personas):
        """Test updating interview status."""
        service = InterviewService(db_session)
        
        interview = await service.create(
            experiment_id=sample_experiment.id,
            persona_id=sample_personas[0].id,
        )
        
        updated = await service.update_status(interview.id, "completed")
        
        assert updated.status == "completed"

    @pytest.mark.asyncio
    async def test_delete_interview(self, db_session: AsyncSession, sample_experiment, sample_personas):
        """Test deleting an interview."""
        service = InterviewService(db_session)
        
        interview = await service.create(
            experiment_id=sample_experiment.id,
            persona_id=sample_personas[0].id,
        )
        
        await service.delete(interview.id)
        
        with pytest.raises(Exception):  # NotFoundError
            await service.get(interview.id)


class TestInsightServiceIntegration:
    """Integration tests for InsightService."""

    @pytest.mark.asyncio
    async def test_generate_insights_with_no_data(self, db_session: AsyncSession, sample_experiment, sample_personas):
        """Test generating insights when no survey or interview data exists."""
        service = InsightService(db_session)
        
        insight = await service.generate(sample_experiment.id)
        
        assert insight.id is not None
        assert insight.experiment_id == sample_experiment.id
        assert insight.would_use_pct >= 0
        assert insight.would_use_pct <= 100
        assert len(insight.themes) > 0

    @pytest.mark.asyncio
    async def test_generate_insights_with_survey_data(self, db_session: AsyncSession, sample_experiment, sample_personas):
        """Test generating insights with survey response data."""
        service = InsightService(db_session)
        
        # Create a survey with responses
        survey = Survey(
            experiment_id=sample_experiment.id,
            title="Test Survey",
            questions=["What do you think?", "Would you use this?"],
            status=SurveyStatus.COMPLETED,
            total_personas=len(sample_personas),
            completed_responses=len(sample_personas),
        )
        db_session.add(survey)
        await db_session.commit()
        await db_session.refresh(survey)
        
        # Add responses
        for persona in sample_personas:
            response = Response(
                persona_id=persona.id,
                survey_id=survey.id,
                question_text="What do you think?",
                answer_text="This is a great product!",
                turn_number=1,
            )
            db_session.add(response)
        
        await db_session.commit()
        
        insight = await service.generate(sample_experiment.id)
        
        assert insight.id is not None
        assert insight.experiment_id == sample_experiment.id
        # Should have some feedback to analyze
        assert insight.raw_data["survey_responses_count"] > 0

    @pytest.mark.asyncio
    async def test_generate_insights_with_interview_data(self, db_session: AsyncSession, sample_experiment, sample_personas):
        """Test generating insights with interview conversation data."""
        service = InsightService(db_session)
        
        # Create interview sessions with messages
        for persona in sample_personas:
            interview = InterviewSession(
                experiment_id=sample_experiment.id,
                persona_id=persona.id,
                status="completed",
                messages=[
                    {"role": "user", "content": "What do you think?"},
                    {"role": "assistant", "content": "I think it's great!"},
                ],
            )
            db_session.add(interview)
        
        await db_session.commit()
        
        insight = await service.generate(sample_experiment.id)
        
        assert insight.id is not None
        assert insight.experiment_id == sample_experiment.id
        # Should have interview data to analyze
        assert insight.raw_data["interview_messages_count"] > 0

    @pytest.mark.asyncio
    async def test_get_insights_by_experiment(self, db_session: AsyncSession, sample_experiment, sample_personas):
        """Test retrieving insights for an experiment."""
        service = InsightService(db_session)
        
        # Generate insights
        await service.generate(sample_experiment.id)
        
        # Retrieve insights
        insight = await service.get_by_experiment(sample_experiment.id)
        
        assert insight is not None
        assert insight.experiment_id == sample_experiment.id

    @pytest.mark.asyncio
    async def test_update_existing_insights(self, db_session: AsyncSession, sample_experiment, sample_personas):
        """Test that generating insights updates existing insight record."""
        service = InsightService(db_session)
        
        # Generate initial insights
        insight1 = await service.generate(sample_experiment.id)
        insight1_id = insight1.id
        
        # Generate insights again (should update existing)
        insight2 = await service.generate(sample_experiment.id)
        
        # Should be the same insight record
        assert insight2.id == insight1_id

    @pytest.mark.asyncio
    async def test_delete_insights(self, db_session: AsyncSession, sample_experiment, sample_personas):
        """Test deleting insights."""
        service = InsightService(db_session)
        
        insight = await service.generate(sample_experiment.id)
        
        await service.delete(insight.id)
        
        with pytest.raises(Exception):  # NotFoundError
            await service.get(insight.id)


class TestInterviewAgentIntegration:
    """Integration tests for InterviewAgent."""

    @pytest.mark.asyncio
    async def test_generate_reply_with_memory(self):
        """Test that interview agent maintains memory across turns."""
        agent = InterviewAgent()
        
        persona_attributes = {
            "id": "test_persona",
            "name": "Test User",
            "age": 30,
            "occupation": "Developer",
            "personality_traits": ["tech-savvy"],
            "core_values": ["innovation"],
            "bio": "A test persona",
            "persona_hash": "test_hash",
            "consistency_seed": 42,
        }
        
        product_context = {
            "title": "Test Product",
            "product_description": "A test product",
            "target_audience": "Developers",
        }
        
        # First message
        reply1 = await agent.generate_reply(
            persona_attributes=persona_attributes,
            message="What do you think about this product?",
            history=[],
            product_context=product_context,
        )
        
        assert reply1 is not None
        assert len(reply1) > 0
        
        # Second message (should have memory of first)
        history = [
            {"role": "user", "content": "What do you think about this product?"},
            {"role": "assistant", "content": reply1},
        ]
        
        reply2 = await agent.generate_reply(
            persona_attributes=persona_attributes,
            message="Can you elaborate?",
            history=history,
            product_context=product_context,
        )
        
        assert reply2 is not None
        assert len(reply2) > 0

    @pytest.mark.asyncio
    async def test_fallback_reply_on_llm_failure(self):
        """Test that agent provides fallback response when LLM fails."""
        agent = InterviewAgent()
        
        # Mock LLM failure by using invalid configuration
        agent.llm_client = None  # This will cause fallback
        
        persona_attributes = {
            "id": "test_persona",
            "name": "Test User",
            "age": 30,
            "occupation": "Developer",
            "personality_traits": ["skeptical"],
            "core_values": ["innovation"],
            "bio": "A test persona",
            "persona_hash": "test_hash",
            "consistency_seed": 42,
        }
        
        product_context = {
            "title": "Test Product",
            "product_description": "A test product",
            "target_audience": "Developers",
        }
        
        reply = await agent.generate_reply(
            persona_attributes=persona_attributes,
            message="What do you think about pricing?",
            history=[],
            product_context=product_context,
        )
        
        # Should provide a fallback response
        assert reply is not None
        assert len(reply) > 0
