from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from typing import Optional
import json
import structlog

from app.models.user import User
from app.api.v1.endpoints.auth import get_current_active_user
from app.ai.models import get_ai_orchestrator

logger = structlog.get_logger()
router = APIRouter()

@router.post("/chat")
async def ai_chat(message: str, model: Optional[str] = "auto", context: Optional[dict] = None,
    current_user: User = Depends(get_current_active_user)):
    ai = get_ai_orchestrator()
    user_context = {
        "user": {"email": current_user.email, "company": current_user.company_id,
            "department": current_user.department, "role": current_user.role.value},
        "complexity": context.get("complexity", "medium") if context else "medium"
    }
    response = await ai.generate(message, user_context, model)
    return {"response": response, "model_used": model, "user_context_applied": True}

@router.post("/analyze")
async def analyze_content(content: str, analysis_type: str = "summary", current_user: User = Depends(get_current_active_user)):
    ai = get_ai_orchestrator()
    prompts = {
        "summary": f"Summarize this content for a {current_user.role.value}: {content}",
        "threat": f"Analyze threats in this content from a security perspective: {content}",
        "legal": f"Analyze legal implications: {content}",
        "sentiment": f"Analyze sentiment and tone: {content}",
    }
    prompt = prompts.get(analysis_type, prompts["summary"])
    response = await ai.generate(prompt, {"user": {"role": current_user.role.value}, "complexity": "high"}, "claude")
    return {"analysis": response, "type": analysis_type}

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    ai = get_ai_orchestrator()
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            context = msg.get("context", {})
            response = await ai.generate(msg["message"], context, msg.get("model", "auto"))
            await websocket.send_json({"response": response, "type": "ai_response"})
    except WebSocketDisconnect:
        logger.info("websocket_disconnected")
    except Exception as e:
        logger.error("websocket_error", error=str(e))
        await websocket.close()
