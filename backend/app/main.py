from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.v1.api import api_router
from app.api.v1.endpoints import dashboard, experiments, insights, interviews, personas, reports, surveys
from app.api.v1.endpoints.experiments import (
    create_experiment,
    delete_experiment,
    get_experiment,
    list_experiments,
    update_experiment,
)
from app.api.v1.endpoints.personas import generate_personas, get_persona, list_personas_for_experiment
from app.core.config import get_settings
from app.core.database import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} [{settings.ENV}]")
    await init_db()
    yield
    logger.info("Shutting down")


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Synthetic User Generation Platform — Milestone 1 (Experiment Workspace + Persona Generation Agent)",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the main API router under the canonical v1 prefix.
app.include_router(api_router, prefix=settings.API_PREFIX)
# Compatibility: also expose the same endpoints under /api for frontend contract/tests.
app.add_api_route("/api/experiments", create_experiment, methods=["POST"], status_code=201)
app.add_api_route("/api/experiments", list_experiments, methods=["GET"])
app.add_api_route("/api/experiments/{experiment_id}", get_experiment, methods=["GET"])
app.add_api_route("/api/experiments/{experiment_id}", update_experiment, methods=["PUT"])
app.add_api_route("/api/experiments/{experiment_id}", delete_experiment, methods=["DELETE"], status_code=204)
app.add_api_route("/api/personas/generate", generate_personas, methods=["POST"], status_code=201)
app.add_api_route("/api/personas/experiment/{experiment_id}", list_personas_for_experiment, methods=["GET"])
app.add_api_route("/api/personas/{persona_id}", get_persona, methods=["GET"])


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.ENV}
