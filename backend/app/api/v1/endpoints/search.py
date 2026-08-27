from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import structlog

from app.db.session import get_db
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_active_user
from app.search.engines.hybrid import HybridSearchEngine
from app.ai.models import get_ai_orchestrator

logger = structlog.get_logger()
router = APIRouter()

@router.post("/")
async def search(query: str, search_type: str = "hybrid", context: Optional[dict] = None,
    current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    engine = HybridSearchEngine()
    ai = get_ai_orchestrator()
    user_context = {
        "user_id": current_user.id, "email": current_user.email,
        "company_id": current_user.company_id, "department": current_user.department,
        "job_title": current_user.job_title, "role": current_user.role.value,
        "preferences": current_user.preferences,
        "search_history": current_user.search_history[-10:] if current_user.search_history else [],
    }
    logger.info("search_query", user=current_user.id, query=query, type=search_type)
    results = await engine.search(query=query, user_context=user_context, search_type=search_type, filters=context or {})
    ai_summary = await ai.summarize_search_results(query=query, results=results, user_profile=user_context)
    return {"query": query, "results": results, "ai_summary": ai_summary, "total": len(results),
        "search_type": search_type, "profile_matched": True}

@router.get("/suggest")
async def search_suggestions(q: str = Query(..., min_length=2), current_user: User = Depends(get_current_active_user)):
    engine = HybridSearchEngine()
    suggestions = await engine.get_suggestions(q, current_user.preferences)
    return {"suggestions": suggestions}

@router.post("/save")
async def save_search(query_data: dict, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    if not current_user.saved_queries:
        current_user.saved_queries = []
    current_user.saved_queries.append(query_data)
    await db.commit()
    return {"detail": "Search saved"}
