package co.ixafrica.opspulse

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import co.ixafrica.opspulse.ui.OpsPulseApp
import co.ixafrica.opspulse.ui.theme.OpsPulseTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            OpsPulseTheme {
                OpsPulseApp()
            }
        }
    }
}

