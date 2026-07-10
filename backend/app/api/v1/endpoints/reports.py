"""
Report API endpoints — research report generation and retrieval.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user_id
from app.core.database import get_db
from app.exceptions.api_exceptions import NotFoundError
from app.schemas.response.report import ReportResponse
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/generate/{experiment_id}", response_model=ReportResponse)
async def generate_report(
    experiment_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Generate a research report for an experiment."""
    service = ReportService(db)
    try:
        report = await service.generate(experiment_id)
        return report
    except (NotFoundError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: str, db: AsyncSession = Depends(get_db)):
    """Get report details by ID."""
    service = ReportService(db)
    try:
        return await service.get(report_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/experiment/{experiment_id}", response_model=ReportResponse)
async def get_report_by_experiment(experiment_id: str, db: AsyncSession = Depends(get_db)):
    """Get the latest report for a specific experiment."""
    service = ReportService(db)
    try:
        return await service.get_by_experiment(experiment_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(report_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a report."""
    service = ReportService(db)
    try:
        await service.delete(report_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
