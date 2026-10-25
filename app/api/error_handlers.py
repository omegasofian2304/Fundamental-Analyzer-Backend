from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.data.metrics.fundamental_metrics_fetcher import MetricFetchError
from app.data.price.price_fetcher import PriceHistoryError


def register_error_handlers(app: FastAPI):
    """Register all global exception handlers on the FastAPI app."""

    @app.exception_handler(MetricFetchError)
    async def metric_fetch_error_handler(request: Request, exc: MetricFetchError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(PriceHistoryError)
    async def price_history_error_handler(request: Request, exc: PriceHistoryError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(SQLAlchemyError)
    async def database_error_handler(request: Request, exc: SQLAlchemyError):
        return JSONResponse(status_code=503, content={"detail": "Database unavailable"})

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(status_code=503, content={"detail": str(exc)})

    @app.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, exc: Exception):
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})