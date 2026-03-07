from agent.app.config import Settings
from agent.app.models import (
    BatterySnapshot,
    CpuSnapshot,
    DiskSnapshot,
    MemorySnapshot,
    NetworkSnapshot,
    SystemSummary,
)
from agent.app.services.alerts import build_alerts
from agent.app.services.metrics import MetricsService


def test_demo_summary_contains_expected_sections() -> None:
    service = MetricsService(Settings(demo_mode=True, sample_interval_seconds=999))

    summary = service.sample_summary()
    processes = service.list_processes()

    assert summary.source == "demo"
    assert 0 <= summary.cpu.percent <= 100
    assert 0 <= summary.memory.percent <= 100
    assert summary.network.download_mbps >= 0
    assert len(processes) == service.settings.process_limit


def test_history_returns_requested_limit() -> None:
    service = MetricsService(Settings(demo_mode=True, sample_interval_seconds=999))

    for _ in range(6):
        service.sample_summary()

    history = service.get_history(limit=4)

    assert len(history) == 4


def test_history_samples_when_empty() -> None:
    service = MetricsService(Settings(demo_mode=True, sample_interval_seconds=999))

    history = service.get_history(limit=4)

    assert len(history) == 1
    assert history[0].source == "demo"


def test_alert_generation_catches_pressure_conditions() -> None:
    summary = SystemSummary(
        hostname="test-host",
        source="test",
        uptime_seconds=1200,
        cpu=CpuSnapshot(percent=91.2, cores=8, load_average=[1.0, 0.8, 0.7]),
        memory=MemorySnapshot(total_gb=16, used_gb=14.2, percent=88.7),
        disk=DiskSnapshot(mount_path="/", total_gb=256, used_gb=242.1, percent=94.5),
        battery=BatterySnapshot(percent=12.0, plugged=False, seconds_left=1200),
        network=NetworkSnapshot(bytes_sent=10, bytes_received=20, upload_mbps=1.2, download_mbps=2.6),
    )

    alerts = build_alerts(summary)
    alert_ids = {alert.id for alert in alerts}

    assert {"cpu-high", "memory-high", "disk-high", "battery-low"} <= alert_ids
