from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.api_exceptions import NotFoundError
from app.models.experiment import Experiment
from app.repositories.experiment_repo import ExperimentRepository
from app.schemas.request.experiment import ExperimentCreateRequest, ExperimentUpdateRequest


class ExperimentService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = ExperimentRepository(session)

    async def create(self, owner_id: str, payload: ExperimentCreateRequest) -> Experiment:
        experiment = Experiment(
            owner_id=owner_id,
            title=payload.title,
            product_description=payload.product_description,
            target_audience=payload.target_audience,
            research_objectives=payload.research_objectives,
            persona_count=payload.persona_count,
        )
        experiment = await self.repo.create(experiment)
        await self.repo.commit()
        return experiment

    async def get(self, experiment_id: str) -> Experiment:
        experiment = await self.repo.get(experiment_id)
        if experiment is None:
            raise NotFoundError(f"Experiment {experiment_id} not found")
        return experiment

    async def list_for_owner(self, owner_id: str) -> list[Experiment]:
        return await self.repo.list_for_owner(owner_id)

    async def update(self, experiment_id: str, payload: ExperimentUpdateRequest) -> Experiment:
        experiment = await self.get(experiment_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(experiment, field, value)
        await self.repo.commit()
        return experiment

    async def delete(self, experiment_id: str) -> None:
        experiment = await self.get(experiment_id)
        await self.repo.delete(experiment)
        await self.repo.commit()
