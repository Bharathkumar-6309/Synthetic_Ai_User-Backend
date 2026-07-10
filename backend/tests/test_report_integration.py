"""
End-to-end integration tests for Milestone 4: Reports and Dashboard.
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.database import Base
from app.models.experiment import Experiment, ExperimentStatus
from app.models.persona import Persona
from app.models.insight import Insight
from app.models.report import Report
from app.models.user import User
from app.models.survey import Survey
from app.models.response import Response
from app.models.interview import InterviewSession
from app.repositories.experiment_repo import ExperimentRepository
from app.repositories.persona_repo import PersonaRepository
from app.repositories.insight_repo import InsightRepository
from app.repositories.report_repo import ReportRepository
from app.services.report_service import ReportService


# Test database setup
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def db_session():
    """Create a test database session."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.mark.asyncio
async def test_report_generation_full_flow(db_session: AsyncSession):
    """Test complete report generation flow: experiment -> personas -> insights -> report."""
    # Create experiment (using a dummy owner_id since we don't have User repo)
    experiment_repo = ExperimentRepository(db_session)
    experiment = Experiment(
        owner_id="test-user-id",
        title="Test Product",
        product_description="AI-powered productivity tool",
        target_audience="Remote workers",
        research_objectives="Validate market fit",
        persona_count=3,
        status=ExperimentStatus.PERSONAS_READY,
    )
    await experiment_repo.create(experiment)
    await experiment_repo.commit()

    # Create personas
    persona_repo = PersonaRepository(db_session)
    personas = []
    for i in range(3):
        persona = Persona(
            experiment_id=experiment.id,
            name=f"Persona {i+1}",
            age=25 + i * 5,
            gender="other",
            occupation="Software Engineer",
            location="San Francisco",
            income_bracket="$80k-$100k",
            education_level="Bachelor's",
            personality_traits=["analytical", "creative"],
            behavioral_patterns=["remote work", "tech-savvy"],
            tech_savviness="high",
            daily_habits=["coding", "meetings"],
            core_values=["efficiency", "innovation"],
            motivations=["productivity", "growth"],
            pain_points=["distraction", "context switching"],
            risk_tolerance="moderate",
            bio=f"Experienced professional {i+1}",
            avatar_seed=f"seed_{i}",
            quote="I need better tools",
            product_fit_score=6.0 + i,
            persona_hash=f"hash_{i}",
            consistency_seed=i,
        )
        await persona_repo.create(persona)
        personas.append(persona)
    await persona_repo.commit()

    # Create insights
    insight_repo = InsightRepository(db_session)
    insight = Insight(
        experiment_id=experiment.id,
        would_use_pct=80,
        would_pay_pct=60,
        themes=[
            {"theme": "Productivity", "mentions_pct": 90},
            {"theme": "Ease of use", "mentions_pct": 70},
        ],
        sentiment={"positive": 12, "neutral": 5, "negative": 2},
        key_quotes=[
            {"quote": "This would save me hours", "persona": "Persona 1"},
            {"quote": "Interface looks clean", "persona": "Persona 2"},
        ],
        suggestions=[
            {"suggestion": "Add mobile app", "category": "Feature", "priority": "high"},
        ],
        user_wants_summary="Users want better productivity tools with mobile support",
        persona_scores={"persona_1": 8.5, "persona_2": 7.0, "persona_3": 9.0},
    )
    await insight_repo.create(insight)
    await insight_repo.commit()

    # Generate report
    report_service = ReportService(db_session)
    report = await report_service.generate(experiment.id)

    # Verify report
    assert report is not None
    assert report.experiment_id == experiment.id
    assert report.status == "ready"
    assert len(report.persona_profiles) == 3
    assert report.validation_scoring["would_use_percentage"] == 80
    assert report.validation_scoring["would_pay_percentage"] == 60
    assert len(report.recommendations) > 0
    assert report.summary is not None

    # Verify experiment status updated
    await db_session.refresh(experiment)
    assert experiment.status == ExperimentStatus.COMPLETED


@pytest.mark.asyncio
async def test_dashboard_endpoint_data(db_session: AsyncSession):
    """Test dashboard data aggregation."""
    # Create experiment (using a dummy owner_id)
    experiment_repo = ExperimentRepository(db_session)
    experiment = Experiment(
        owner_id="dashboard-user-id",
        title="Dashboard Test",
        product_description="Test product",
        target_audience="Test audience",
        research_objectives="Test objectives",
        persona_count=2,
        status=ExperimentStatus.PERSONAS_READY,
    )
    await experiment_repo.create(experiment)
    await experiment_repo.commit()

    # Create personas
    persona_repo = PersonaRepository(db_session)
    for i in range(2):
        persona = Persona(
            experiment_id=experiment.id,
            name=f"Dashboard Persona {i+1}",
            age=30,
            gender="other",
            occupation="Developer",
            location="NYC",
            income_bracket="$100k+",
            education_level="Master's",
            personality_traits=["focused"],
            behavioral_patterns=["coding"],
            tech_savviness="high",
            daily_habits=["work"],
            core_values=["quality"],
            motivations=["success"],
            pain_points=["bugs"],
            risk_tolerance="low",
            bio="Test persona",
            avatar_seed=f"dash_seed_{i}",
            quote="Test quote",
            product_fit_score=7.0,
            persona_hash=f"dash_hash_{i}",
            consistency_seed=i,
        )
        await persona_repo.create(persona)
    await persona_repo.commit()

    # Create insight
    insight_repo = InsightRepository(db_session)
    insight = Insight(
        experiment_id=experiment.id,
        would_use_pct=75,
        would_pay_pct=50,
        themes=[{"theme": "Test Theme", "mentions_pct": 100}],
        sentiment={"positive": 5, "neutral": 2, "negative": 0},
        key_quotes=[{"quote": "Test quote", "persona": "Dashboard Persona 1"}],
        suggestions=[],
        user_wants_summary="Test summary",
        persona_scores={},
    )
    await insight_repo.create(insight)
    await insight_repo.commit()

    # Generate report
    report_service = ReportService(db_session)
    report = await report_service.generate(experiment.id)

    # Verify dashboard data can be retrieved
    report_repo = ReportRepository(db_session)
    retrieved_report = await report_repo.get_by_experiment(experiment.id)
    assert retrieved_report is not None
    assert retrieved_report.status == "ready"
    assert retrieved_report.validation_scoring["would_use_percentage"] == 75


@pytest.mark.asyncio
async def test_report_without_insights(db_session: AsyncSession):
    """Test report generation when no insights exist yet."""
    # Create experiment (using a dummy owner_id)
    experiment_repo = ExperimentRepository(db_session)
    experiment = Experiment(
        owner_id="no-insights-user-id",
        title="No Insights Test",
        product_description="Test product",
        target_audience="Test audience",
        research_objectives="Test objectives",
        persona_count=2,
        status=ExperimentStatus.PERSONAS_READY,
    )
    await experiment_repo.create(experiment)
    await experiment_repo.commit()

    # Create personas
    persona_repo = PersonaRepository(db_session)
    for i in range(2):
        persona = Persona(
            experiment_id=experiment.id,
            name=f"No Insight Persona {i+1}",
            age=28,
            gender="other",
            occupation="Designer",
            location="LA",
            income_bracket="$60k-$80k",
            education_level="Bachelor's",
            personality_traits=["creative"],
            behavioral_patterns=["designing"],
            tech_savviness="medium",
            daily_habits=["sketching"],
            core_values=["aesthetics"],
            motivations=["beauty"],
            pain_points=["ugly UI"],
            risk_tolerance="high",
            bio="Designer persona",
            avatar_seed=f"no_insight_seed_{i}",
            quote="Make it pretty",
            product_fit_score=5.0,
            persona_hash=f"no_insight_hash_{i}",
            consistency_seed=i,
        )
        await persona_repo.create(persona)
    await persona_repo.commit()

    # Generate report without insights
    report_service = ReportService(db_session)
    report = await report_service.generate(experiment.id)

    # Verify report still generates with empty insights
    assert report is not None
    assert report.experiment_id == experiment.id
    assert report.status == "ready"
    assert len(report.persona_profiles) == 2
    assert report.insight_summary == {}
    assert report.validation_scoring["overall_product_fit_score"] == 5.0  # Average of 5 and 5


@pytest.mark.asyncio
async def test_report_crud_operations(db_session: AsyncSession):
    """Test report CRUD operations."""
    report_repo = ReportRepository(db_session)

    # Create
    report = Report(
        experiment_id="test-exp-id",
        title="Test Report",
        summary="Test summary",
        status="ready",
    )
    await report_repo.create(report)
    await report_repo.commit()

    # Read
    retrieved = await report_repo.get(report.id)
    assert retrieved is not None
    assert retrieved.title == "Test Report"

    # Update
    retrieved.title = "Updated Report"
    await report_repo.update(retrieved)
    await report_repo.commit()

    updated = await report_repo.get(report.id)
    assert updated.title == "Updated Report"

    # Delete
    await report_repo.delete(updated)
    await report_repo.commit()

    deleted = await report_repo.get(report.id)
    assert deleted is None
