package co.ixafrica.opspulse.network

import co.ixafrica.opspulse.model.AlertItem
import co.ixafrica.opspulse.model.DashboardPayload
import co.ixafrica.opspulse.model.ProcessEntry
import co.ixafrica.opspulse.model.SystemSummary
import retrofit2.http.GET

interface OpsPulseApi {
    @GET("/api/v1/mobile/dashboard")
    suspend fun dashboard(): DashboardPayload

    @GET("/api/v1/mobile/summary")
    suspend fun summary(): SystemSummary

    @GET("/api/v1/mobile/processes")
    suspend fun processes(): List<ProcessEntry>

    @GET("/api/v1/mobile/alerts")
    suspend fun alerts(): List<AlertItem>
}

