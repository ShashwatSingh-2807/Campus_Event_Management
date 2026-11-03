"""Operational health endpoints; these are not product API routes."""

import logging

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import get_db

logger = logging.getLogger(__name__)
router = APIRouter(tags=["health"])


@router.get("/health/live", summary="Application liveness")
def liveness() -> dict[str, str]:
    """Confirm that the API process is running."""
    return {"status": "ok"}


@router.get("/health/ready", summary="Application readiness", response_model=None)
def readiness(db: Session = Depends(get_db)) -> dict[str, object] | JSONResponse:
    """Confirm that the API can reach its required database dependency."""
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.exception("Database readiness check failed")
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "dependencies": {"database": "unavailable"},
            },
        )

    return {
        "status": "ready",
        "dependencies": {"database": "ok"},
    }
