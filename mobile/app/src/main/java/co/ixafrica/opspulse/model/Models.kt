package co.ixafrica.opspulse.model

data class CpuSnapshot(
    val percent: Double,
    val cores: Int,
    val load_average: List<Double> = emptyList(),
)

data class MemorySnapshot(
    val total_gb: Double,
    val used_gb: Double,
    val percent: Double,
)

data class DiskSnapshot(
    val mount_path: String,
    val total_gb: Double,
    val used_gb: Double,
    val percent: Double,
)

data class BatterySnapshot(
    val percent: Double? = null,
    val plugged: Boolean? = null,
    val seconds_left: Int? = null,
)

data class NetworkSnapshot(
    val bytes_sent: Long,
    val bytes_received: Long,
    val upload_mbps: Double,
    val download_mbps: Double,
)

data class SystemSummary(
    val hostname: String,
    val source: String,
    val captured_at: String,
    val uptime_seconds: Int,
    val cpu: CpuSnapshot,
    val memory: MemorySnapshot,
    val disk: DiskSnapshot,
    val battery: BatterySnapshot,
    val network: NetworkSnapshot,
)

data class ProcessEntry(
    val pid: Int,
    val name: String,
    val cpu_percent: Double,
    val memory_mb: Double,
    val status: String,
)

data class AlertItem(
    val id: String,
    val severity: String,
    val title: String,
    val detail: String,
    val metric: String? = null,
    val threshold: Double? = null,
    val current_value: Double? = null,
    val observed_at: String? = null,
)

data class DashboardPayload(
    val summary: SystemSummary,
    val processes: List<ProcessEntry>,
    val alerts: List<AlertItem>,
)
