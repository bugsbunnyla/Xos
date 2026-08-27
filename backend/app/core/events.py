import structlog
from app.db.session import init_db, close_db

logger = structlog.get_logger()

async def startup_event():
    logger.info("Starting up PhD Xpert Solver API...")
    await init_db()
    logger.info("Startup complete!")

async def shutdown_event():
    logger.info("Shutting down...")
    await close_db()
    logger.info("Shutdown complete!")
