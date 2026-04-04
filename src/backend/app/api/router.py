from fastapi import APIRouter

from app.api.routes import health, financial_reports, advanced_financial

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(
    financial_reports.router, prefix="/financial", tags=["Financial Reports"]
)
api_router.include_router(
    advanced_financial.router, prefix="/advanced", tags=["Advanced Financial Analysis"]
)
