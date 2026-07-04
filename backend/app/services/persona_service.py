from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.persona_agent import PersonaProfile, generate_personas
from app.exceptions.api_exceptions import NotFoundError
from app.models.experiment import ExperimentStatus
from app.models.persona import Persona
from app.repositories.experiment_repo import ExperimentRepository
from app.repositories.persona_repo import PersonaRepository


class PersonaService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.persona_repo = PersonaRepository(session)
        self.experiment_repo = ExperimentRepository(session)

    @staticmethod
    def _to_orm(profile: PersonaProfile, experiment_id: str) -> Persona:
        return Persona(
            experiment_id=experiment_id,
            name=profile.name,
            age=profile.age,
            gender=profile.gender,
            occupation=profile.occupation,
            location=profile.location,
            income_bracket=profile.income_bracket,
            education_level=profile.education_level,
            personality_traits=profile.personality_traits,
            behavioral_patterns=profile.behavioral_patterns,
            tech_savviness=profile.tech_savviness,
            daily_habits=profile.daily_habits,
            core_values=profile.core_values,
            motivations=profile.motivations,
            pain_points=profile.pain_points,
            risk_tolerance=profile.risk_tolerance,
            bio=profile.bio,
            avatar_seed=profile.avatar_seed,
            quote=profile.quote,
            persona_hash=profile.persona_hash,
            consistency_seed=profile.consistency_seed,
            generation_source=profile.generation_source,
        )

    async def generate_for_experiment(
        self, experiment_id: str, *, persona_count: int | None = None, regenerate: bool = False
    ) -> list[Persona]:
        experiment = await self.experiment_repo.get(experiment_id)
        if experiment is None:
            raise NotFoundError(f"Experiment {experiment_id} not found")

        if regenerate:
            await self.persona_repo.delete_for_experiment(experiment_id)

        count = persona_count or experiment.persona_count

        profiles = await generate_personas(
            product_description=experiment.product_description,
            target_audience=experiment.target_audience,
            research_objectives=experiment.research_objectives,
            persona_count=count,
        )

        personas = [self._to_orm(p, experiment_id) for p in profiles]
        for persona in personas:
            await self.persona_repo.create(persona)

        experiment.status = ExperimentStatus.PERSONAS_READY
        await self.persona_repo.commit()

        return personas

    async def list_for_experiment(self, experiment_id: str) -> list[Persona]:
        experiment = await self.experiment_repo.get(experiment_id)
        if experiment is None:
            raise NotFoundError(f"Experiment {experiment_id} not found")
        return await self.persona_repo.list_for_experiment(experiment_id)
