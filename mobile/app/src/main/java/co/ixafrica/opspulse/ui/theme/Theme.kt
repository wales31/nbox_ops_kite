package co.ixafrica.opspulse.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

private val OpsLightColors = lightColorScheme(
    primary = Cyan500,
    secondary = Lime500,
    tertiary = Amber500,
    background = Fog50,
    surface = Fog50,
    surfaceVariant = androidx.compose.ui.graphics.Color(0xFFE2E8F0),
    onPrimary = androidx.compose.ui.graphics.Color.White,
    onBackground = Slate950,
    onSurface = Slate950,
)

private val OpsDarkColors = darkColorScheme(
    primary = Cyan500,
    secondary = Lime500,
    tertiary = Amber500,
    background = Steel900,
    surface = Slate950,
    surfaceVariant = androidx.compose.ui.graphics.Color(0xFF1E293B),
    onBackground = Fog50,
    onSurface = Fog50,
)

@Composable
fun OpsPulseTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = OpsDarkColors,
        content = content,
    )
}

