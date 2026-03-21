from fastapi import APIRouter

from app.api.routes import health, startup_validation, financial_reports, forecasting, market_intelligence, database

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(
    startup_validation.router, prefix="/startup", tags=["Startup Validation"]
)
api_router.include_router(
    financial_reports.router, prefix="/financial", tags=["Financial Reports"]
)
api_router.include_router(
    forecasting.router, prefix="/forecasting", tags=["Forecasting"]
)
api_router.include_router(
    market_intelligence.router, prefix="/market", tags=["Market Intelligence"]
)
api_router.include_router(
    database.router, prefix="/database", tags=["Database"]
)
