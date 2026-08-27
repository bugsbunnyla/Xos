from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.db.session import get_db
from app.models.user import User
from app.models.osint import OSINTReport, OSINTReportStatus
from app.api.v1.endpoints.auth import get_current_active_user
from app.osint.engine import OSINTEngine

router = APIRouter()

@router.post("/investigate")
async def investigate(target: str, target_type: str = "domain", modules: Optional[List[str]] = None,
    background: bool = True, current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db), bg_tasks: BackgroundTasks = None):
    if current_user.api_quota_remaining <= 0:
        raise HTTPException(status_code=429, detail="API quota exceeded")
    report = OSINTReport(user_id=current_user.id, target=target, target_type=target_type,
        status=OSINTReportStatus.PENDING, modules=modules or [])
    db.add(report); await db.commit(); await db.refresh(report)
    if background and bg_tasks:
        bg_tasks.add_task(_run_investigation, report.id, target, target_type, modules, db)
        return {"report_id": report.id, "status": "pending", "message": "Investigation started"}
    else:
        return await _run_investigation_sync(report.id, target, target_type, modules, db)

async def _run_investigation(report_id: str, target: str, target_type: str, modules: list, db: AsyncSession):
    engine = OSINTEngine()
    result = await engine.investigate(target, target_type, modules)
    from sqlalchemy import select
    result_db = await db.execute(select(OSINTReport).where(OSINTReport.id == report_id))
    report = result_db.scalar_one()
    report.status = OSINTReportStatus.COMPLETED
    report.findings = result["findings"]
    report.risk_assessment = {"score": result["risk_score"], "level": result["risk_level"]}
    report.graph_nodes = result["graph_nodes"]
    report.graph_edges = result["graph_edges"]
    report.progress = 100.0
    await db.commit()

async def _run_investigation_sync(report_id: str, target: str, target_type: str, modules: list, db: AsyncSession):
    await _run_investigation(report_id, target, target_type, modules, db)
    from sqlalchemy import select
    result = await db.execute(select(OSINTReport).where(OSINTReport.id == report_id))
    return result.scalar_one()

@router.get("/reports")
async def list_reports(current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(OSINTReport).where(
        OSINTReport.user_id == current_user.id).order_by(OSINTReport.created_at.desc()))
    return result.scalars().all()

@router.get("/reports/{report_id}")
async def get_report(report_id: str, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(OSINTReport).where(
        OSINTReport.id == report_id, OSINTReport.user_id == current_user.id))
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
