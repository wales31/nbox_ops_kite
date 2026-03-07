package co.ixafrica.opspulse.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import co.ixafrica.opspulse.model.AlertItem

@Composable
fun AlertsScreen(alerts: List<AlertItem>) {
    if (alerts.isEmpty()) {
        EmptyState(message = "No active alerts. The system looks stable.")
        return
    }

    LazyColumn(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        items(alerts) { alert ->
            val tone = if (alert.severity == "critical") Color(0xFF8A1C1C) else Color(0xFF8A5B00)
            Card(
                colors = CardDefaults.cardColors(containerColor = tone),
                modifier = Modifier.fillMaxWidth(),
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(6.dp),
                ) {
                    Text(
                        text = alert.title,
                        style = MaterialTheme.typography.titleMedium,
                        color = Color.White,
                        fontWeight = FontWeight.Bold,
                    )
                    Text(text = alert.detail, color = Color.White)
                    val currentValue = alert.current_value?.let { "Current: $it" } ?: ""
                    Text(text = "${alert.severity.uppercase()}  $currentValue", color = Color.White.copy(alpha = 0.9f))
                }
            }
        }
    }
}

