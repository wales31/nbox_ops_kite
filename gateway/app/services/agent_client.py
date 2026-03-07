import httpx

from gateway.app.config import Settings, get_settings


class AgentUnavailableError(RuntimeError):
    pass


class AgentClient:
    def __init__(self, settings: Settings):
        self._settings = settings

    async def get_health(self) -> dict:
        return await self._fetch_json("/health")

    async def get_summary(self) -> dict:
        return await self._fetch_json("/api/v1/summary")

    async def get_processes(self) -> list[dict]:
        return await self._fetch_json("/api/v1/processes")

    async def get_alerts(self) -> list[dict]:
        return await self._fetch_json("/api/v1/alerts")

    async def _fetch_json(self, path: str):
        try:
            async with httpx.AsyncClient(
                base_url=self._settings.agent_base_url,
                timeout=self._settings.request_timeout_seconds,
            ) as client:
                response = await client.get(path)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise AgentUnavailableError(str(exc)) from exc

        return response.json()


_agent_client = AgentClient(get_settings())


def get_agent_client() -> AgentClient:
    return _agent_client

