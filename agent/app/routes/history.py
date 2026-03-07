from fastapi import APIRouter, Query

from agent.app.models import SystemSummary
from agent.app.services.metrics import get_metrics_service

router = APIRouter(tags=["history"])


@router.get("/api/v1/history", response_model=list[SystemSummary])
async def get_history(limit: int = Query(default=30, ge=1, le=120)) -> list[SystemSummary]:
    return get_metrics_service().get_history(limit=limit)

