from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, search, osint, ai, enterprise, skills, health

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(osint.router, prefix="/osint", tags=["OSINT"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI"])
api_router.include_router(enterprise.router, prefix="/enterprise", tags=["Enterprise"])
api_router.include_router(skills.router, prefix="/skills", tags=["Skills"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
