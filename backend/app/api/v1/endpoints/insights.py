"""
Insight API endpoints — insight generation and retrieval.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user_id
from app.core.database import get_db
from app.exceptions.api_exceptions import NotFoundError
from app.schemas.response.insight import InsightResponse
from app.services.insight_service import InsightService

router = APIRouter(prefix="/insights", tags=["insights"])


@router.post("/generate/{experiment_id}", response_model=InsightResponse)
async def generate_insights(
    experiment_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Generate insights for an experiment by analyzing survey and interview responses."""
    service = InsightService(db)
    try:
        insight = await service.generate(experiment_id)
        return insight
    except (NotFoundError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{insight_id}", response_model=InsightResponse)
async def get_insight(insight_id: str, db: AsyncSession = Depends(get_db)):
    """Get insight details by ID."""
    service = InsightService(db)
    try:
        return await service.get(insight_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/experiment/{experiment_id}", response_model=InsightResponse)
async def get_insights_by_experiment(experiment_id: str, db: AsyncSession = Depends(get_db)):
    """Get insights for a specific experiment."""
    service = InsightService(db)
    try:
        return await service.get_by_experiment(experiment_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/{insight_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_insight(insight_id: str, db: AsyncSession = Depends(get_db)):
    """Delete an insight."""
    service = InsightService(db)
    try:
        await service.delete(insight_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
