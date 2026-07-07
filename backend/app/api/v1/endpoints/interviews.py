"""
Interview API endpoints — conversational persona interaction.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.interview_agent import InterviewAgent
from app.api.v1.deps import get_current_user_id
from app.core.database import get_db
from app.exceptions.api_exceptions import NotFoundError
from app.models.experiment import Experiment
from app.models.persona import Persona
from app.repositories.experiment_repo import ExperimentRepository
from app.repositories.persona_repo import PersonaRepository
from app.schemas.request.interview import InterviewStartRequest, InterviewMessageRequest
from app.schemas.response.interview import InterviewSessionResponse
from app.services.interview_service import InterviewService

router = APIRouter(prefix="/interviews", tags=["interviews"])


@router.post("", response_model=InterviewSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_interview(
    payload: InterviewStartRequest,
    db: AsyncSession = Depends(get_db),
):
    """Create a new interview session with a persona."""
    service = InterviewService(db)
    interview = await service.create(
        experiment_id=payload.experiment_id,
        persona_id=payload.persona_id,
    )
    return interview


@router.get("")
async def list_interviews(
    experiment_id: str | None = None,
    persona_id: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """List interview sessions, optionally filtered by experiment or persona."""
    service = InterviewService(db)
    
    if experiment_id:
        interviews = await service.list_for_experiment(experiment_id)
    elif persona_id:
        interviews = await service.list_for_persona(persona_id)
    else:
        interviews = []
    
    return {"total": len(interviews), "items": interviews}


@router.get("/{interview_id}", response_model=InterviewSessionResponse)
async def get_interview(interview_id: str, db: AsyncSession = Depends(get_db)):
    """Get interview session details."""
    service = InterviewService(db)
    try:
        return await service.get(interview_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("/{interview_id}/message", response_model=InterviewSessionResponse)
async def send_message(
    interview_id: str,
    payload: InterviewMessageRequest,
    db: AsyncSession = Depends(get_db),
):
    """Send a message to the persona and get a response."""
    service = InterviewService(db)
    agent = InterviewAgent()
    
    # Get interview session
    interview = await service.get(interview_id)
    
    # Get persona and experiment context
    persona_repo = PersonaRepository(db)
    experiment_repo = ExperimentRepository(db)
    
    persona = await persona_repo.get(interview.persona_id)
    experiment = await experiment_repo.get(interview.experiment_id)
    
    if persona is None or experiment is None:
        raise HTTPException(status_code=404, detail="Persona or experiment not found")
    
    # Add user message
    await service.add_message(interview_id, "user", payload.message)
    
    # Generate persona response
    persona_attributes = {
        "id": str(persona.id),
        "name": persona.name,
        "age": persona.age,
        "occupation": persona.occupation,
        "personality_traits": persona.personality_traits,
        "core_values": persona.core_values,
        "bio": persona.bio,
        "persona_hash": persona.persona_hash,
        "consistency_seed": persona.consistency_seed,
    }
    
    product_context = {
        "title": experiment.title,
        "product_description": experiment.product_description,
        "target_audience": experiment.target_audience,
    }
    
    history = [
        {"role": msg.get("role"), "content": msg.get("content")}
        for msg in interview.messages
    ]
    
    reply = await agent.generate_reply(
        persona_attributes=persona_attributes,
        message=payload.message,
        history=history,
        product_context=product_context,
    )
    
    # Add assistant message
    await service.add_message(interview_id, "assistant", reply)
    
    # Return updated interview
    return await service.get(interview_id)


@router.delete("/{interview_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_interview(interview_id: str, db: AsyncSession = Depends(get_db)):
    """Delete an interview session."""
    service = InterviewService(db)
    try:
        await service.delete(interview_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
