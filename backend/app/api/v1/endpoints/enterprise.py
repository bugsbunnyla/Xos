from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.session import get_db
from app.models.user import User, Company, Team, TeamMember
from app.api.v1.endpoints.auth import get_current_active_user
from app.auth.middleware.rbac import require_admin

router = APIRouter()

@router.get("/company")
async def get_company(current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    if not current_user.company_id:
        raise HTTPException(status_code=404, detail="No company associated")
    from sqlalchemy import select
    result = await db.execute(select(Company).where(Company.id == current_user.company_id))
    return result.scalar_one_or_none()

@router.post("/teams")
async def create_team(name: str, description: Optional[str] = None,
    current_user: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    if not current_user.company_id:
        raise HTTPException(status_code=400, detail="User not in a company")
    team = Team(company_id=current_user.company_id, name=name, description=description)
    db.add(team); await db.commit()
    return team

@router.get("/billing")
async def get_billing(current_user: User = Depends(get_current_active_user)):
    return {"tier": current_user.subscription_tier, "quota_remaining": current_user.api_quota_remaining,
        "quota_total": current_user.api_quota_total, "expires": current_user.subscription_expires_at}

@router.get("/reports/usage")
async def usage_report(current_user: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select, func
    from app.models.search import SearchQuery
    from app.models.osint import OSINTReport
    search_count = await db.execute(select(func.count(SearchQuery.id)).where(SearchQuery.user_id == current_user.id))
    osint_count = await db.execute(select(func.count(OSINTReport.id)).where(OSINTReport.user_id == current_user.id))
    return {"searches": search_count.scalar(), "osint_reports": osint_count.scalar(),
        "quota_used": current_user.api_quota_total - current_user.api_quota_remaining,
        "quota_total": current_user.api_quota_total}
