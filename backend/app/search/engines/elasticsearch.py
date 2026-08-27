from typing import List, Dict, Any, Optional
from elasticsearch import AsyncElasticsearch
from app.core.config import settings
import structlog

logger = structlog.get_logger()
_es_client = None

async def init_elasticsearch():
    global _es_client
    _es_client = AsyncElasticsearch([settings.ELASTICSEARCH_URL])
    logger.info("elasticsearch_initialized")

class ElasticsearchEngine:
    def __init__(self):
        self.client = _es_client

    async def search(self, query: str, filters: Optional[Dict] = None) -> List[Dict]:
        if not self.client:
            return []
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^3", "content", "domain^2"],
                    "type": "best_fields"
                }
            },
            "size": 20
        }
        if filters:
            body["query"] = {"bool": {"must": body["query"], "filter": [{"term": {k: v}} for k, v in filters.items()]}}
        try:
            resp = await self.client.search(index="phdxpert-search", body=body)
            return [{"id": h["_id"], "url": h["_source"].get("url"), "title": h["_source"].get("title"),
                "snippet": h["_source"].get("content", "")[:300], "score": h["_score"],
                "source": "elasticsearch", "domain": h["_source"].get("domain")} for h in resp["hits"]["hits"]]
        except Exception as e:
            logger.error("es_search_error", error=str(e))
            return []

    async def index(self, doc: Dict):
        if self.client:
            await self.client.index(index="phdxpert-search", body=doc)
