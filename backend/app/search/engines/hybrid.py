from typing import List, Dict, Any, Optional
import asyncio
import structlog
from app.search.engines.elasticsearch import ElasticsearchEngine
from app.search.engines.vector import VectorSearchEngine
from app.search.engines.graph import GraphSearchEngine

logger = structlog.get_logger()

class HybridSearchEngine:
    def __init__(self):
        self.es = ElasticsearchEngine()
        self.vector = VectorSearchEngine()
        self.graph = GraphSearchEngine()

    async def search(self, query: str, user_context: Dict[str, Any], search_type: str = "hybrid",
        filters: Optional[Dict] = None) -> List[Dict]:
        tasks = []
        if search_type in ["web", "hybrid", "enterprise"]:
            tasks.append(self.es.search(query, filters))
        if search_type in ["vector", "hybrid", "ai"]:
            tasks.append(self.vector.search(query, user_context))
        if search_type in ["graph", "osint", "hybrid"]:
            tasks.append(self.graph.search(query, user_context))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        merged = self._merge_results(results, user_context)
        ranked = self._profile_rank(merged, user_context)
        return ranked[:50]

    def _merge_results(self, results_list, user_context):
        seen = set(); merged = []
        for results in results_list:
            if isinstance(results, Exception):
                logger.error("search_engine_error", error=str(results)); continue
            for r in results:
                key = r.get("url") or r.get("id")
                if key and key not in seen:
                    seen.add(key); merged.append(r)
        return merged

    def _profile_rank(self, results, user_context):
        company = user_context.get("company_id")
        dept = user_context.get("department")
        role = user_context.get("role")
        for r in results:
            score = r.get("score", 1.0)
            if company and r.get("company_id") == company: score *= 1.5
            if dept and r.get("department") == dept: score *= 1.3
            if role in ["admin", "analyst"] and r.get("source") == "osint": score *= 1.2
            r["score"] = score
        return sorted(results, key=lambda x: x["score"], reverse=True)

    async def get_suggestions(self, query: str, preferences: dict) -> List[str]:
        return [
            f"{query} in {preferences.get('industry', 'enterprise')}",
            f"{query} site:{preferences.get('preferred_domain', '')}" if preferences.get("preferred_domain") else f"{query} latest",
            f"AI analysis of {query}",
        ]
