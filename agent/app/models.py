from datetime import datetime, timezone

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


class CpuSnapshot(BaseModel):
    percent: float
    cores: int
    load_average: list[float] = Field(default_factory=list)


class MemorySnapshot(BaseModel):
    total_gb: float
    used_gb: float
    percent: float


class DiskSnapshot(BaseModel):
    mount_path: str
    total_gb: float
    used_gb: float
    percent: float


class BatterySnapshot(BaseModel):
    percent: float | None = None
    plugged: bool | None = None
    seconds_left: int | None = None


class NetworkSnapshot(BaseModel):
    bytes_sent: int
    bytes_received: int
    upload_mbps: float
    download_mbps: float


class SystemSummary(BaseModel):
    hostname: str
    source: str
    captured_at: datetime = Field(default_factory=utc_now)
    uptime_seconds: int
    cpu: CpuSnapshot
    memory: MemorySnapshot
    disk: DiskSnapshot
    battery: BatterySnapshot
    network: NetworkSnapshot


class ProcessEntry(BaseModel):
    pid: int
    name: str
    cpu_percent: float
    memory_mb: float
    status: str


class AlertItem(BaseModel):
    id: str
    severity: str
    title: str
    detail: str
    metric: str
    threshold: float
    current_value: float
    observed_at: datetime = Field(default_factory=utc_now)

