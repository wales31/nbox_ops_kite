import asyncio

from fastapi import APIRouter, Depends, HTTPException

from gateway.app.services.agent_client import AgentClient, AgentUnavailableError, get_agent_client

router = APIRouter(tags=["mobile"])


def _raise_unavailable(exc: AgentUnavailableError) -> HTTPException:
    return HTTPException(status_code=503, detail=f"Agent unavailable: {exc}")


@router.get("/api/v1/mobile/dashboard")
async def get_dashboard(agent_client: AgentClient = Depends(get_agent_client)) -> dict[str, object]:
    try:
        summary, processes, alerts = await asyncio.gather(
            agent_client.get_summary(),
            agent_client.get_processes(),
            agent_client.get_alerts(),
        )
    except AgentUnavailableError as exc:
        raise _raise_unavailable(exc) from exc

    return {"summary": summary, "processes": processes, "alerts": alerts}


@router.get("/api/v1/mobile/summary")
async def get_summary(agent_client: AgentClient = Depends(get_agent_client)) -> dict:
    try:
        return await agent_client.get_summary()
    except AgentUnavailableError as exc:
        raise _raise_unavailable(exc) from exc


@router.get("/api/v1/mobile/processes")
async def get_processes(agent_client: AgentClient = Depends(get_agent_client)) -> list[dict]:
    try:
        return await agent_client.get_processes()
    except AgentUnavailableError as exc:
        raise _raise_unavailable(exc) from exc


@router.get("/api/v1/mobile/alerts")
async def get_alerts(agent_client: AgentClient = Depends(get_agent_client)) -> list[dict]:
    try:
        return await agent_client.get_alerts()
    except AgentUnavailableError as exc:
        raise _raise_unavailable(exc) from exc

