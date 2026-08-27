from fastapi import APIRouter
import redis
import psycopg2
from elasticsearch import Elasticsearch
from app.core.config import settings

router = APIRouter()

@router.get("/")
async def health():
    checks = {}
    try:
        conn = psycopg2.connect(settings.DATABASE_URL.replace("+asyncpg", ""))
        conn.close(); checks["postgres"] = "ok"
    except Exception as e:
        checks["postgres"] = f"error: {str(e)}"
    try:
        r = redis.from_url(settings.REDIS_URL); r.ping(); checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"
    try:
        es = Elasticsearch([settings.ELASTICSEARCH_URL]); es.ping(); checks["elasticsearch"] = "ok"
    except Exception as e:
        checks["elasticsearch"] = f"error: {str(e)}"
    overall = "healthy" if all(v == "ok" for v in checks.values()) else "degraded"
    return {"status": overall, "checks": checks}
