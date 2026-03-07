import asyncio
import math
import os
import socket
import time
from collections import deque
from contextlib import suppress
from dataclasses import dataclass
from threading import Lock

import psutil
from prometheus_client import Gauge

from agent.app.config import Settings, get_settings
from agent.app.models import (
    AlertItem,
    BatterySnapshot,
    CpuSnapshot,
    DiskSnapshot,
    MemorySnapshot,
    NetworkSnapshot,
    ProcessEntry,
    SystemSummary,
)
from agent.app.services.alerts import build_alerts

CPU_GAUGE = Gauge("device_cpu_percent", "Current host CPU usage percent")
MEMORY_GAUGE = Gauge("device_memory_percent", "Current host memory usage percent")
DISK_GAUGE = Gauge("device_disk_percent", "Current host disk usage percent")
NETWORK_UPLOAD_GAUGE = Gauge("device_network_upload_mbps", "Host network upload throughput in Mbps")
NETWORK_DOWNLOAD_GAUGE = Gauge("device_network_download_mbps", "Host network download throughput in Mbps")
ALERT_GAUGE = Gauge("device_alert_count", "Number of generated alerts for the current sample")


@dataclass
class _NetworkCounterSample:
    captured_at: float
    bytes_sent: int
    bytes_received: int


class MetricsService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._history: deque[SystemSummary] = deque(maxlen=settings.history_size)
        self._lock = Lock()
        self._network_sample: _NetworkCounterSample | None = None
        self._task: asyncio.Task[None] | None = None
        self._demo_boot_time = time.time() - 60 * 60 * 7
        self._demo_bytes_sent = 320_000_000
        self._demo_bytes_received = 910_000_000

    async def start(self) -> None:
        if self._task is None:
            self._task = asyncio.create_task(self._collector(), name="ops-pulse-sampler")

    async def stop(self) -> None:
        if self._task is None:
            return
        self._task.cancel()
        with suppress(asyncio.CancelledError):
            await self._task
        self._task = None

    async def _collector(self) -> None:
        while True:
            self.sample_summary()
            await asyncio.sleep(self.settings.sample_interval_seconds)

    def get_summary(self) -> SystemSummary:
        with self._lock:
            if self._history:
                return self._history[-1]
        return self.sample_summary()

    def get_history(self, limit: int = 30) -> list[SystemSummary]:
        with self._lock:
            history = list(self._history)

        if not history:
            return [self.sample_summary()]

        return history[-limit:]

    def list_processes(self) -> list[ProcessEntry]:
        if self.settings.demo_mode:
            return self._demo_processes()

        primed_processes: list[psutil.Process] = []
        for proc in psutil.process_iter(["pid", "name", "status", "memory_info"]):
            try:
                proc.cpu_percent(interval=None)
                primed_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        time.sleep(0.1)

        processes: list[ProcessEntry] = []
        for proc in primed_processes:
            try:
                memory_info = proc.info.get("memory_info")
                memory_mb = round((memory_info.rss / 1024 / 1024), 1) if memory_info else 0.0
                processes.append(
                    ProcessEntry(
                        pid=proc.info["pid"],
                        name=proc.info.get("name") or "unknown",
                        cpu_percent=round(proc.cpu_percent(interval=None), 1),
                        memory_mb=memory_mb,
                        status=proc.info.get("status") or "unknown",
                    )
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        processes.sort(key=lambda item: (item.cpu_percent, item.memory_mb), reverse=True)
        return processes[: self.settings.process_limit]

    def list_alerts(self) -> list[AlertItem]:
        return build_alerts(self.get_summary())

    def sample_summary(self) -> SystemSummary:
        summary = self._sample_demo_summary() if self.settings.demo_mode else self._sample_live_summary()
        alerts = build_alerts(summary)

        CPU_GAUGE.set(summary.cpu.percent)
        MEMORY_GAUGE.set(summary.memory.percent)
        DISK_GAUGE.set(summary.disk.percent)
        NETWORK_UPLOAD_GAUGE.set(summary.network.upload_mbps)
        NETWORK_DOWNLOAD_GAUGE.set(summary.network.download_mbps)
        ALERT_GAUGE.set(len(alerts))

        with self._lock:
            self._history.append(summary)

        return summary

    def _sample_live_summary(self) -> SystemSummary:
        now = time.time()
        cpu_percent = round(psutil.cpu_percent(interval=0.15), 1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(self.settings.disk_path)
        network = psutil.net_io_counters()
        battery_reading = getattr(psutil, "sensors_battery", lambda: None)()

        upload_mbps = 0.0
        download_mbps = 0.0
        if self._network_sample is not None:
            elapsed = max(now - self._network_sample.captured_at, 1e-6)
            upload_mbps = round(((network.bytes_sent - self._network_sample.bytes_sent) * 8) / elapsed / 1_000_000, 2)
            download_mbps = round(((network.bytes_recv - self._network_sample.bytes_received) * 8) / elapsed / 1_000_000, 2)

        self._network_sample = _NetworkCounterSample(
            captured_at=now,
            bytes_sent=network.bytes_sent,
            bytes_received=network.bytes_recv,
        )

        try:
            load_average = [round(value, 2) for value in os.getloadavg()]
        except OSError:
            load_average = []

        battery = BatterySnapshot()
        if battery_reading is not None:
            seconds_left = None
            if battery_reading.secsleft not in (psutil.POWER_TIME_UNKNOWN, psutil.POWER_TIME_UNLIMITED):
                seconds_left = int(battery_reading.secsleft)
            battery = BatterySnapshot(
                percent=round(battery_reading.percent, 1),
                plugged=battery_reading.power_plugged,
                seconds_left=seconds_left,
            )

        return SystemSummary(
            hostname=socket.gethostname(),
            source="live-host",
            uptime_seconds=int(now - psutil.boot_time()),
            cpu=CpuSnapshot(
                percent=cpu_percent,
                cores=psutil.cpu_count(logical=True) or 1,
                load_average=load_average,
            ),
            memory=MemorySnapshot(
                total_gb=round(memory.total / 1024 / 1024 / 1024, 2),
                used_gb=round(memory.used / 1024 / 1024 / 1024, 2),
                percent=round(memory.percent, 1),
            ),
            disk=DiskSnapshot(
                mount_path=self.settings.disk_path,
                total_gb=round(disk.total / 1024 / 1024 / 1024, 2),
                used_gb=round(disk.used / 1024 / 1024 / 1024, 2),
                percent=round(disk.percent, 1),
            ),
            battery=battery,
            network=NetworkSnapshot(
                bytes_sent=network.bytes_sent,
                bytes_received=network.bytes_recv,
                upload_mbps=upload_mbps,
                download_mbps=download_mbps,
            ),
        )

    def _sample_demo_summary(self) -> SystemSummary:
        now = time.time()
        phase = now / 18

        cpu_percent = round(20 + 45 * ((math.sin(phase) + 1) / 2), 1)
        memory_percent = round(38 + 24 * ((math.sin(phase / 2) + 1) / 2), 1)
        disk_percent = round(57 + 6 * ((math.sin(phase / 3) + 1) / 2), 1)
        battery_percent = round(82 - ((now - self._demo_boot_time) / 5000), 1)

        self._demo_bytes_sent += int(85_000 + 35_000 * ((math.sin(phase) + 1) / 2))
        self._demo_bytes_received += int(140_000 + 60_000 * ((math.cos(phase) + 1) / 2))

        return SystemSummary(
            hostname="ops-pulse-demo",
            source="demo",
            uptime_seconds=int(now - self._demo_boot_time),
            cpu=CpuSnapshot(percent=cpu_percent, cores=8, load_average=[1.22, 1.07, 0.88]),
            memory=MemorySnapshot(total_gb=16.0, used_gb=round(16.0 * memory_percent / 100, 2), percent=memory_percent),
            disk=DiskSnapshot(mount_path="/", total_gb=512.0, used_gb=round(512.0 * disk_percent / 100, 2), percent=disk_percent),
            battery=BatterySnapshot(percent=max(battery_percent, 12.0), plugged=False, seconds_left=7400),
            network=NetworkSnapshot(
                bytes_sent=self._demo_bytes_sent,
                bytes_received=self._demo_bytes_received,
                upload_mbps=round(1.2 + 3.8 * ((math.sin(phase) + 1) / 2), 2),
                download_mbps=round(2.0 + 6.2 * ((math.cos(phase) + 1) / 2), 2),
            ),
        )

    def _demo_processes(self) -> list[ProcessEntry]:
        phase = time.time() / 10
        seed = [
            ("AndroidStudio", 920.0, 24.3),
            ("docker", 480.0, 12.1),
            ("chrome", 730.0, 17.8),
            ("python", 150.0, 6.9),
            ("code", 610.0, 9.4),
        ]
        processes: list[ProcessEntry] = []
        for index, (name, memory_mb, cpu_base) in enumerate(seed, start=1001):
            processes.append(
                ProcessEntry(
                    pid=index,
                    name=name,
                    cpu_percent=round(cpu_base + 4 * ((math.sin(phase + index) + 1) / 2), 1),
                    memory_mb=memory_mb,
                    status="running",
                )
            )
        processes.sort(key=lambda item: (item.cpu_percent, item.memory_mb), reverse=True)
        return processes[: self.settings.process_limit]


_metrics_service = MetricsService(get_settings())


def get_metrics_service() -> MetricsService:
    return _metrics_service
