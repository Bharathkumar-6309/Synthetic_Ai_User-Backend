"""
DI wiring for the API layer.

get_current_user_id is a stub for Milestone 1: full JWT auth (middleware/auth.py)
lands in a later milestone. It transparently creates/reuses a single demo user
so the experiment workspace endpoints are usable end-to-end today, without
requiring endpoint signatures to change once real auth is wired in.
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User

_DEMO_EMAIL = "demo@vidzai.local"


async def get_current_user_id(db: AsyncSession = Depends(get_db)) -> str:
    from sqlalchemy import select

    result = await db.execute(select(User).where(User.email == _DEMO_EMAIL))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(email=_DEMO_EMAIL, hashed_password="unset", full_name="Demo User")
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user.id
