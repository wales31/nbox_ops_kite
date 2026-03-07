from fastapi import APIRouter, Depends

from gateway.app.config import get_settings
from gateway.app.services.agent_client import AgentClient, AgentUnavailableError, get_agent_client

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check(agent_client: AgentClient = Depends(get_agent_client)) -> dict[str, object]:
    settings = get_settings()
    try:
        agent_health = await agent_client.get_health()
        agent_status = agent_health.get("status", "unknown")
    except AgentUnavailableError as exc:
        agent_health = {"status": "unreachable", "detail": str(exc)}
        agent_status = "degraded"

    return {
        "status": "ok" if agent_status == "ok" else "degraded",
        "agent_base_url": settings.agent_base_url,
        "agent": agent_health,
    }

