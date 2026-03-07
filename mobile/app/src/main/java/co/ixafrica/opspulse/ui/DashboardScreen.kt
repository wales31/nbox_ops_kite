package co.ixafrica.opspulse.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import co.ixafrica.opspulse.model.SystemSummary

@Composable
fun DashboardScreen(summary: SystemSummary?) {
    if (summary == null) {
        EmptyState(message = "No system summary yet. Connect to the gateway and refresh.")
        return
    }

    LazyColumn(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        item {
            Text(
                text = summary.hostname,
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
            )
        }
        item {
            Text(
                text = "Source: ${summary.source}  •  Uptime: ${formatUptime(summary.uptime_seconds)}",
                style = MaterialTheme.typography.bodyMedium,
            )
        }
        item {
            MetricCard(
                title = "CPU",
                value = "${summary.cpu.percent}%",
                progress = (summary.cpu.percent / 100).toFloat(),
                detail = "Cores: ${summary.cpu.cores}  •  Load: ${summary.cpu.load_average.joinToString()}",
            )
        }
        item {
            MetricCard(
                title = "Memory",
                value = "${summary.memory.percent}%",
                progress = (summary.memory.percent / 100).toFloat(),
                detail = "${summary.memory.used_gb} GB / ${summary.memory.total_gb} GB",
            )
        }
        item {
            MetricCard(
                title = "Disk",
                value = "${summary.disk.percent}%",
                progress = (summary.disk.percent / 100).toFloat(),
                detail = "${summary.disk.used_gb} GB / ${summary.disk.total_gb} GB at ${summary.disk.mount_path}",
            )
        }
        item {
            MetricCard(
                title = "Network",
                value = "Up ${summary.network.upload_mbps} Mbps",
                progress = (summary.network.upload_mbps / 10).coerceAtMost(1.0).toFloat(),
                detail = "Down ${summary.network.download_mbps} Mbps",
            )
        }
        item {
            val batteryText = summary.battery.percent?.let { "$it%" } ?: "Unavailable"
            MetricCard(
                title = "Battery",
                value = batteryText,
                progress = ((summary.battery.percent ?: 0.0) / 100).toFloat(),
                detail = if (summary.battery.plugged == true) "Charging" else "On battery",
            )
        }
    }
}

@Composable
private fun MetricCard(
    title: String,
    value: String,
    progress: Float,
    detail: String,
) {
    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
            ) {
                Text(text = title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
                Text(text = value, style = MaterialTheme.typography.titleMedium)
            }
            LinearProgressIndicator(progress = { progress.coerceIn(0f, 1f) }, modifier = Modifier.fillMaxWidth())
            Text(text = detail, style = MaterialTheme.typography.bodyMedium)
        }
    }
}

private fun formatUptime(seconds: Int): String {
    val hours = seconds / 3600
    val minutes = (seconds % 3600) / 60
    return "${hours}h ${minutes}m"
}

