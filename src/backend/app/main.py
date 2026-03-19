from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.config import settings
from app.utils.logger import setup_logger
from app.utils.error_handlers import setup_global_exception_handlers

logger = setup_logger(__name__)


@asynccontextmanager # is used for startup and shutdown events
async def lifespan(app: FastAPI):  # noqa: ARG001
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"   Environment : {settings.ENVIRONMENT}")
    logger.info(f"   Groq model: {settings.GROQ_MODEL}")
    yield
    logger.info("👋 Shutting down AI Business Intelligence Platform...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description=(
        "Agentic AI platform for startup validation, financial analysis, "
        "and forecasting powered by LangGraph & GPT-4o."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Setup global exception handlers
setup_global_exception_handlers(app)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "running",
        "api_docs": "/docs",
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
