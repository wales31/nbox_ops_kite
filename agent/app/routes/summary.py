from fastapi import APIRouter

from agent.app.models import SystemSummary
from agent.app.services.metrics import get_metrics_service

router = APIRouter(tags=["summary"])


@router.get("/api/v1/summary", response_model=SystemSummary)
async def get_summary() -> SystemSummary:
    return get_metrics_service().get_summary()

