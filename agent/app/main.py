from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from agent.app.config import get_settings
from agent.app.routes.alerts import router as alerts_router
from agent.app.routes.health import router as health_router
from agent.app.routes.history import router as history_router
from agent.app.routes.processes import router as processes_router
from agent.app.routes.summary import router as summary_router
from agent.app.services.metrics import get_metrics_service


@asynccontextmanager
async def lifespan(_: FastAPI):
    service = get_metrics_service()
    await service.start()
    try:
        yield
    finally:
        await service.stop()


settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(summary_router)
app.include_router(processes_router)
app.include_router(alerts_router)
app.include_router(history_router)
app.mount("/metrics", make_asgi_app())

