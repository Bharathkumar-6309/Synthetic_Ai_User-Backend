from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.insight import Insight
from app.repositories.base import BaseRepository


class InsightRepository(BaseRepository[Insight]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Insight)

    async def get_latest_for_experiment(self, experiment_id: str) -> Insight | None:
        stmt = (
            select(Insight)
            .where(Insight.experiment_id == experiment_id)
            .order_by(Insight.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list_for_experiment(self, experiment_id: str) -> list[Insight]:
        stmt = select(Insight).where(Insight.experiment_id == experiment_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
