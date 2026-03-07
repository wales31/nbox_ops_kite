from fastapi import APIRouter

from agent.app.config import get_settings
from agent.app.services.metrics import get_metrics_service

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, object]:
    summary = get_metrics_service().get_summary()
    settings = get_settings()
    return {
        "status": "ok",
        "demo_mode": settings.demo_mode,
        "hostname": summary.hostname,
        "source": summary.source,
    }

