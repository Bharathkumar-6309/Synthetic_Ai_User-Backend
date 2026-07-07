"""
Interview Service — manages interview sessions and conversation tracking.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.api_exceptions import NotFoundError
from app.models.experiment import ExperimentStatus
from app.models.interview import InterviewSession
from app.models.persona import Persona
from app.repositories.experiment_repo import ExperimentRepository
from app.repositories.interview_repo import InterviewRepository
from app.repositories.persona_repo import PersonaRepository


class InterviewService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.interview_repo = InterviewRepository(session)
        self.experiment_repo = ExperimentRepository(session)
        self.persona_repo = PersonaRepository(session)

    async def create(
        self,
        experiment_id: str,
        persona_id: str,
    ) -> InterviewSession:
        """Create a new interview session."""
        experiment = await self.experiment_repo.get(experiment_id)
        if experiment is None:
            raise NotFoundError(f"Experiment {experiment_id} not found")

        if experiment.status != ExperimentStatus.PERSONAS_READY:
            raise ValueError(f"Experiment must have personas ready to create an interview")

        persona = await self.persona_repo.get(persona_id)
        if persona is None:
            raise NotFoundError(f"Persona {persona_id} not found")

        if persona.experiment_id != experiment_id:
            raise ValueError(f"Persona {persona_id} does not belong to experiment {experiment_id}")

        interview = InterviewSession(
            experiment_id=experiment_id,
            persona_id=persona_id,
            status="active",
            messages=[],
        )
        await self.interview_repo.create(interview)
        await self.interview_repo.commit()
        return interview

    async def get(self, interview_id: str) -> InterviewSession:
        interview = await self.interview_repo.get(interview_id)
        if interview is None:
            raise NotFoundError(f"Interview {interview_id} not found")
        return interview

    async def list_for_experiment(self, experiment_id: str) -> list[InterviewSession]:
        experiment = await self.experiment_repo.get(experiment_id)
        if experiment is None:
            raise NotFoundError(f"Experiment {experiment_id} not found")
        return await self.interview_repo.list_for_experiment(experiment_id)

    async def list_for_persona(self, persona_id: str) -> list[InterviewSession]:
        persona = await self.persona_repo.get(persona_id)
        if persona is None:
            raise NotFoundError(f"Persona {persona_id} not found")
        return await self.interview_repo.list_for_persona(persona_id)

    async def add_message(
        self,
        interview_id: str,
        role: str,
        content: str,
    ) -> InterviewSession:
        """Add a message to the interview conversation."""
        interview = await self.get(interview_id)
        
        message = {
            "role": role,
            "content": content,
            "timestamp": interview.updated_at.isoformat(),
        }
        interview.messages.append(message)
        
        await self.interview_repo.commit()
        return interview

    async def update_status(self, interview_id: str, status: str) -> InterviewSession:
        interview = await self.get(interview_id)
        interview.status = status
        await self.interview_repo.commit()
        return interview

    async def delete(self, interview_id: str) -> None:
        interview = await self.get(interview_id)
        await self.interview_repo.delete(interview)
        await self.interview_repo.commit()
