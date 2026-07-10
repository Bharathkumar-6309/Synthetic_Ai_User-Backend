"""
Insight Service — manages insight generation and storage for experiments.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.insight_agent import InsightAgent, InsightResult
from app.exceptions.api_exceptions import NotFoundError
from app.models.experiment import Experiment
from app.models.insight import Insight
from app.models.persona import Persona
from app.models.response import Response
from app.models.survey import Survey
from app.repositories.experiment_repo import ExperimentRepository
from app.repositories.insight_repo import InsightRepository
from app.repositories.persona_repo import PersonaRepository
from app.repositories.response_repo import ResponseRepository
from app.repositories.survey_repo import SurveyRepository


class InsightService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.insight_repo = InsightRepository(session)
        self.experiment_repo = ExperimentRepository(session)
        self.persona_repo = PersonaRepository(session)
        self.response_repo = ResponseRepository(session)
        self.survey_repo = SurveyRepository(session)
        self.insight_agent = InsightAgent()

    async def generate(self, experiment_id: str) -> Insight:
        """Generate insights for an experiment by analyzing survey and interview responses."""
        experiment = await self.experiment_repo.get(experiment_id)
        if experiment is None:
            raise NotFoundError(f"Experiment {experiment_id} not found")

        personas = await self.persona_repo.list_for_experiment(experiment_id)
        if not personas:
            raise ValueError(f"No personas found for experiment {experiment_id}")

        # Collect survey responses
        surveys = await self.survey_repo.list_for_experiment(experiment_id)
        survey_responses = []
        for survey in surveys:
            responses = await self.response_repo.list_for_survey(survey.id)
            survey_responses.extend(responses)

        # Collect interview messages
        from app.models.interview import InterviewSession
        from app.repositories.interview_repo import InterviewRepository
        interview_repo = InterviewRepository(self.session)
        interviews = await interview_repo.list_for_experiment(experiment_id)
        
        interview_transcript = []
        for interview in interviews:
            for message in interview.messages or []:
                interview_transcript.append({
                    "persona_id": interview.persona_id,
                    "role": message.get("role"),
                    "content": message.get("content"),
                })

        # Build feedback transcript
        feedback_lines = []
        for response in survey_responses:
            persona = next((p for p in personas if str(p.id) == response.persona_id), None)
            if persona:
                feedback_lines.append(f"[Survey] {persona.name}: {response.answer_text}")
        
        for msg in interview_transcript:
            persona = next((p for p in personas if str(p.id) == msg["persona_id"]), None)
            if persona and msg["role"] == "assistant":
                feedback_lines.append(f"[Interview] {persona.name}: {msg['content']}")
        
        feedback_transcript = "\n".join(feedback_lines)

        # Generate insights using the agent
        experiment_dict = {
            "id": experiment.id,
            "title": experiment.title,
            "product_description": experiment.product_description,
            "target_audience": experiment.target_audience,
            "research_objectives": experiment.research_objectives,
        }
        
        personas_dict = [
            {
                "id": str(p.id),
                "name": p.name,
                "age": p.age,
                "occupation": p.occupation,
                "personality_traits": p.personality_traits,
                "core_values": p.core_values,
                "bio": p.bio,
                "adoption_score": getattr(p, "adoption_score", None),
                "product_fit_score": getattr(p, "product_fit_score", None),
            }
            for p in personas
        ]

        insight_result = await self.insight_agent.extract(
            experiment=experiment_dict,
            personas=personas_dict,
            feedback_transcript=feedback_transcript,
        )

        # Create or update insight record
        existing = await self.insight_repo.get_by_experiment(experiment_id)
        if existing:
            insight = existing
            insight.would_use_pct = insight_result.would_use_pct
            insight.would_pay_pct = insight_result.would_pay_pct
            insight.themes = [t.model_dump() for t in insight_result.themes]
            insight.sentiment = insight_result.sentiment
            insight.key_quotes = [q.model_dump() for q in insight_result.key_quotes]
            insight.suggestions = [s.model_dump() for s in insight_result.suggestions]
            insight.user_wants_summary = insight_result.user_wants_summary
            insight.persona_scores = insight_result.persona_scores
            insight.raw_data = {
                "survey_responses_count": len(survey_responses),
                "interview_messages_count": len(interview_transcript),
                "feedback_transcript_length": len(feedback_transcript),
            }
        else:
            insight = Insight(
                experiment_id=experiment_id,
                would_use_pct=insight_result.would_use_pct,
                would_pay_pct=insight_result.would_pay_pct,
                themes=[t.model_dump() for t in insight_result.themes],
                sentiment=insight_result.sentiment,
                key_quotes=[q.model_dump() for q in insight_result.key_quotes],
                suggestions=[s.model_dump() for s in insight_result.suggestions],
                user_wants_summary=insight_result.user_wants_summary,
                persona_scores=insight_result.persona_scores,
                raw_data={
                    "survey_responses_count": len(survey_responses),
                    "interview_messages_count": len(interview_transcript),
                    "feedback_transcript_length": len(feedback_transcript),
                },
            )
            await self.insight_repo.create(insight)

        await self.insight_repo.commit()
        return insight

    async def get(self, insight_id: str) -> Insight:
        insight = await self.insight_repo.get(insight_id)
        if insight is None:
            raise NotFoundError(f"Insight {insight_id} not found")
        return insight

    async def get_by_experiment(self, experiment_id: str) -> Insight:
        insight = await self.insight_repo.get_by_experiment(experiment_id)
        if insight is None:
            raise NotFoundError(f"No insights found for experiment {experiment_id}")
        return insight

    async def delete(self, insight_id: str) -> None:
        insight = await self.get(insight_id)
        await self.insight_repo.delete(insight)
        await self.insight_repo.commit()
