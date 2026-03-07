import asyncio

from gateway.app.routes.health import health_check
from gateway.app.routes.mobile import get_dashboard


class FakeAgentClient:
    async def get_health(self) -> dict:
        return {"status": "ok", "hostname": "demo-agent"}

    async def get_summary(self) -> dict:
        return {"hostname": "demo-agent", "cpu": {"percent": 21.5}}

    async def get_processes(self) -> list[dict]:
        return [{"pid": 1001, "name": "python", "cpu_percent": 10.2, "memory_mb": 120.0, "status": "running"}]

    async def get_alerts(self) -> list[dict]:
        return [{"id": "cpu-high", "severity": "warning"}]


def test_gateway_dashboard_aggregates_agent_payloads() -> None:
    payload = asyncio.run(get_dashboard(FakeAgentClient()))

    assert payload["summary"]["hostname"] == "demo-agent"
    assert len(payload["processes"]) == 1
    assert len(payload["alerts"]) == 1


def test_gateway_health_reports_agent_status() -> None:
    payload = asyncio.run(health_check(FakeAgentClient()))

    assert payload["status"] == "ok"
    assert payload["agent"]["hostname"] == "demo-agent"
