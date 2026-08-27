from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.models.user import User, UserRole, UserStatus
from app.api.v1.endpoints.auth import get_current_active_user
from app.auth.middleware.rbac import require_admin
from app.auth.schemas import UserResponse

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 100,
    current_user: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}/role")
async def update_user_role(user_id: str, role: UserRole,
    current_user: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role
    await db.commit()
    return {"detail": f"User role updated to {role}"}
