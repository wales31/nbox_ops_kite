package co.ixafrica.opspulse.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun SetupScreen(
    gatewayUrl: String,
    onGatewayUrlChanged: (String) -> Unit,
    onConnectClicked: () -> Unit,
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        Text(
            text = "Gateway URL",
            style = MaterialTheme.typography.headlineSmall,
        )
        Text(
            text = "Point the app to the laptop running the OpsPulse gateway. Use the laptop IP on the same Wi-Fi network.",
            style = MaterialTheme.typography.bodyMedium,
        )
        OutlinedTextField(
            value = gatewayUrl,
            onValueChange = onGatewayUrlChanged,
            modifier = Modifier.fillMaxWidth(),
            label = { Text("Base URL") },
            supportingText = { Text("Examples: http://10.0.2.2:8090/ or http://192.168.1.15:8090/") },
            singleLine = true,
        )
        Button(onClick = onConnectClicked) {
            Text(text = "Connect and Refresh")
        }
    }
}

