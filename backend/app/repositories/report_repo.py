"""Report repository for database operations."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.report import Report
from app.models.base import UUIDPKMixin


class ReportRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, report: Report) -> Report:
        self.session.add(report)
        await self.session.flush()
        await self.session.refresh(report)
        return report

    async def get(self, report_id: str) -> Report | None:
        stmt = select(Report).where(Report.id == report_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_experiment(self, experiment_id: str) -> Report | None:
        stmt = select(Report).where(Report.experiment_id == experiment_id).order_by(Report.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_for_experiment(self, experiment_id: str) -> list[Report]:
        stmt = select(Report).where(Report.experiment_id == experiment_id).order_by(Report.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, report: Report) -> Report:
        await self.session.flush()
        await self.session.refresh(report)
        return report

    async def delete(self, report: Report) -> None:
        await self.session.delete(report)

    async def commit(self) -> None:
        await self.session.commit()
