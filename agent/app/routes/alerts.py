from fastapi import APIRouter

from agent.app.models import AlertItem
from agent.app.services.metrics import get_metrics_service

router = APIRouter(tags=["alerts"])


@router.get("/api/v1/alerts", response_model=list[AlertItem])
async def get_alerts() -> list[AlertItem]:
    return get_metrics_service().list_alerts()

