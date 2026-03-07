from agent.app.models import AlertItem, SystemSummary


def build_alerts(summary: SystemSummary) -> list[AlertItem]:
    alerts: list[AlertItem] = []

    if summary.cpu.percent >= 85:
        alerts.append(
            AlertItem(
                id="cpu-high",
                severity="critical",
                title="CPU usage is high",
                detail="CPU utilisation crossed the 85% threshold.",
                metric="cpu.percent",
                threshold=85,
                current_value=summary.cpu.percent,
            )
        )

    if summary.memory.percent >= 80:
        alerts.append(
            AlertItem(
                id="memory-high",
                severity="warning",
                title="Memory pressure detected",
                detail="RAM usage crossed the 80% threshold.",
                metric="memory.percent",
                threshold=80,
                current_value=summary.memory.percent,
            )
        )

    if summary.disk.percent >= 90:
        alerts.append(
            AlertItem(
                id="disk-high",
                severity="critical",
                title="Disk capacity almost full",
                detail="Disk usage crossed the 90% threshold.",
                metric="disk.percent",
                threshold=90,
                current_value=summary.disk.percent,
            )
        )

    if summary.battery.percent is not None and summary.battery.percent <= 20 and not summary.battery.plugged:
        alerts.append(
            AlertItem(
                id="battery-low",
                severity="warning",
                title="Battery is running low",
                detail="Battery charge dropped below 20% while unplugged.",
                metric="battery.percent",
                threshold=20,
                current_value=summary.battery.percent,
            )
        )

    return alerts

