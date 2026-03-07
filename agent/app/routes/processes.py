from fastapi import APIRouter

from agent.app.models import ProcessEntry
from agent.app.services.metrics import get_metrics_service

router = APIRouter(tags=["processes"])


@router.get("/api/v1/processes", response_model=list[ProcessEntry])
async def get_processes() -> list[ProcessEntry]:
    return get_metrics_service().list_processes()

