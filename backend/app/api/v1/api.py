from fastapi import APIRouter

from app.api.v1.endpoints import experiments, personas, surveys, interviews, insights, reports, dashboard

api_router = APIRouter()
api_router.include_router(experiments.router)
api_router.include_router(personas.router)
api_router.include_router(surveys.router)
api_router.include_router(interviews.router)
api_router.include_router(insights.router)
api_router.include_router(reports.router)
api_router.include_router(dashboard.router)
