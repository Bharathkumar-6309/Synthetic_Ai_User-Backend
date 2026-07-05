from sqlalchemy.ext.asyncio import AsyncSession

from app.models.experiment import Experiment
from app.repositories.base import BaseRepository


class ExperimentRepository(BaseRepository[Experiment]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Experiment)

    async def list_for_owner(self, owner_id: str) -> list[Experiment]:
        return await self.list(owner_id=owner_id)
