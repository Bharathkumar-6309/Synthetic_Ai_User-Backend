from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.interview import InterviewSession
from app.repositories.base import BaseRepository


class InterviewRepository(BaseRepository[InterviewSession]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, InterviewSession)

    async def list_for_experiment(self, experiment_id: str) -> list[InterviewSession]:
        stmt = select(InterviewSession).where(InterviewSession.experiment_id == experiment_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_active_for_persona(self, persona_id: str) -> InterviewSession | None:
        stmt = (
            select(InterviewSession)
            .where(InterviewSession.persona_id == persona_id, InterviewSession.status == "active")
            .order_by(InterviewSession.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
