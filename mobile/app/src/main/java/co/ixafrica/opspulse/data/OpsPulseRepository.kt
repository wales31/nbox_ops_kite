package co.ixafrica.opspulse.data

import co.ixafrica.opspulse.model.AlertItem
import co.ixafrica.opspulse.model.ProcessEntry
import co.ixafrica.opspulse.model.SystemSummary
import co.ixafrica.opspulse.network.ApiProvider

class OpsPulseRepository {
    suspend fun loadSummary(baseUrl: String): SystemSummary = ApiProvider.create(baseUrl).summary()

    suspend fun loadProcesses(baseUrl: String): List<ProcessEntry> = ApiProvider.create(baseUrl).processes()

    suspend fun loadAlerts(baseUrl: String): List<AlertItem> = ApiProvider.create(baseUrl).alerts()
}

