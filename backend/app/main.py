from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import structlog
import time

from app.core.config import settings
from app.core.events import startup_event, shutdown_event
from app.api.v1.router import api_router
from app.db.session import engine
from app.models.base import Base

logger = structlog.get_logger()

app = FastAPI(
    title="PhD Xpert Solver API",
    description="AI-Powered OSINT Search Browser - Enterprise API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(
        "request_processed",
        method=request.method,
        path=request.url.path,
        duration=process_time,
        status=response.status_code,
    )
    return response

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("unhandled_exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error_id": str(time.time())},
    )

# Events
@app.on_event("startup")
async def on_startup():
    await startup_event()
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def on_shutdown():
    await shutdown_event()

# API Routes
app.include_router(api_router, prefix="/api/v1")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0", "service": "phdxpert-api"}

# Root
@app.get("/")
async def root():
    return {
        "name": "PhD Xpert Solver API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }
