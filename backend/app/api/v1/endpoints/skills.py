from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List

from app.models.user import User
from app.api.v1.endpoints.auth import get_current_active_user
from app.skills.templates import get_skill_template, list_skills, SKILL_TEMPLATES
from app.ai.models import get_ai_orchestrator

router = APIRouter()

@router.get("/")
async def get_skills(category: Optional[str] = None, current_user: User = Depends(get_current_active_user)):
    skills = list_skills(category=category, role=current_user.role.value)
    return [{"id": s.id, "name": s.name, "description": s.description, "category": s.category} for s in skills]

@router.post("/{skill_id}/invoke")
async def invoke_skill(skill_id: str, query: str, context: Optional[dict] = None,
    current_user: User = Depends(get_current_active_user)):
    template = get_skill_template(skill_id)
    if not template:
        raise HTTPException(status_code=404, detail="Skill not found")
    ai = get_ai_orchestrator()
    enriched_context = {
        "user": {"email": current_user.email, "company": current_user.company_id,
            "department": current_user.department, "role": current_user.role.value},
        "skill_context": context or {}, "complexity": "high"
    }
    system = template.system_prompt
    prompt = f"{system}\n\nUser Query: {query}\nContext: {enriched_context}"
    response = await ai.generate(prompt, enriched_context, "claude")
    return {"skill": skill_id, "query": query, "response": response,
        "tools_available": template.tools, "context_applied": True}
