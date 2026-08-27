from typing import Dict, Any, Optional, List
import openai
import anthropic
import google.generativeai as genai
import structlog
from app.core.config import settings

logger = structlog.get_logger()

class AIOrchestrator:
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.anthropic_client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None
        if settings.GOOGLE_API_KEY:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.gemini_model = genai.GenerativeModel(settings.GOOGLE_MODEL) if settings.GOOGLE_API_KEY else None

    async def generate(self, prompt: str, context: Dict[str, Any], model_preference: str = "auto") -> str:
        if model_preference == "auto":
            model_preference = self._select_model(context)
        if model_preference == "gpt4" and self.openai_client:
            return await self._openai_generate(prompt, context)
        elif model_preference == "claude" and self.anthropic_client:
            return await self._claude_generate(prompt, context)
        elif model_preference == "gemini" and self.gemini_model:
            return await self._gemini_generate(prompt, context)
        else:
            return await self._local_generate(prompt, context)

    def _select_model(self, context: Dict[str, Any]) -> str:
        complexity = context.get("complexity", "medium")
        if complexity == "high":
            return "claude" if self.anthropic_client else "gpt4"
        elif complexity == "medium":
            return "gpt4" if self.openai_client else "claude"
        return "gemini" if self.gemini_model else "local"

    async def _openai_generate(self, prompt: str, context: Dict) -> str:
        system = self._build_system_prompt(context)
        resp = await self.openai_client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            temperature=0.3, max_tokens=4000)
        return resp.choices[0].message.content

    async def _claude_generate(self, prompt: str, context: Dict) -> str:
        system = self._build_system_prompt(context)
        resp = await self.anthropic_client.messages.create(
            model=settings.ANTHROPIC_MODEL, max_tokens=4000, system=system,
            messages=[{"role": "user", "content": prompt}])
        return resp.content[0].text

    async def _gemini_generate(self, prompt: str, context: Dict) -> str:
        resp = await self.gemini_model.generate_content_async(prompt)
        return resp.text

    async def _local_generate(self, prompt: str, context: Dict) -> str:
        import ollama
        resp = ollama.chat(model=settings.OLLAMA_MODEL, messages=[{"role": "user", "content": prompt}])
        return resp["message"]["content"]

    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        user = context.get("user", {})
        return f"""You are PhD Xpert Solver, an elite AI research assistant.
User: {user.get('email', 'unknown')}
Company: {user.get('company', 'unknown')}
Department: {user.get('department', 'unknown')}
Role: {user.get('role', 'user')}
Provide accurate, cited, professional responses tailored to the user's enterprise context."""

    async def summarize_search_results(self, query: str, results: List[Dict], user_profile: Dict) -> str:
        context = {"user": user_profile, "complexity": "medium"}
        result_text = "\n".join([f"{i+1}. {r.get('title', 'Untitled')}: {r.get('snippet', '')[:200]}"
            for i, r in enumerate(results[:10])])
        prompt = f"""Query: {query}
Search Results:
{result_text}
Provide a concise, actionable summary tailored for a {user_profile.get('role', 'user')} in {user_profile.get('department', 'general')}. Include key insights and recommendations."""
        return await self.generate(prompt, context)

_orchestrator = None

def get_ai_orchestrator() -> AIOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AIOrchestrator()
    return _orchestrator

async def init_ai_providers():
    logger.info("ai_providers_initialized")
