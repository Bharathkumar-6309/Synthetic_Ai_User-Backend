from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.persona import Persona
from app.repositories.base import BaseRepository


class PersonaRepository(BaseRepository[Persona]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Persona)

    async def list_for_experiment(self, experiment_id: str) -> list[Persona]:
        return await self.list(experiment_id=experiment_id)

    async def delete_for_experiment(self, experiment_id: str) -> None:
        await self.session.execute(delete(Persona).where(Persona.experiment_id == experiment_id))
        await self.session.flush()
