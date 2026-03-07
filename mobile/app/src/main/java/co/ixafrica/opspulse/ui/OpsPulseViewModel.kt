package co.ixafrica.opspulse.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import co.ixafrica.opspulse.data.OpsPulseRepository
import co.ixafrica.opspulse.model.AlertItem
import co.ixafrica.opspulse.model.ProcessEntry
import co.ixafrica.opspulse.model.SystemSummary
import kotlinx.coroutines.async
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class OpsPulseUiState(
    val gatewayUrl: String = "http://10.0.2.2:8090/",
    val summary: SystemSummary? = null,
    val processes: List<ProcessEntry> = emptyList(),
    val alerts: List<AlertItem> = emptyList(),
    val isLoading: Boolean = false,
    val errorMessage: String? = null,
)

class OpsPulseViewModel(
    private val repository: OpsPulseRepository = OpsPulseRepository(),
) : ViewModel() {
    private val _uiState = MutableStateFlow(OpsPulseUiState())
    val uiState: StateFlow<OpsPulseUiState> = _uiState.asStateFlow()

    init {
        refreshAll()
    }

    fun updateGatewayUrl(value: String) {
        _uiState.update { current -> current.copy(gatewayUrl = value) }
    }

    fun connectToGateway() {
        refreshAll()
    }

    fun refreshAll() {
        viewModelScope.launch {
            val baseUrl = uiState.value.gatewayUrl
            _uiState.update { current -> current.copy(isLoading = true, errorMessage = null) }

            runCatching {
                val summaryDeferred = async { repository.loadSummary(baseUrl) }
                val processesDeferred = async { repository.loadProcesses(baseUrl) }
                val alertsDeferred = async { repository.loadAlerts(baseUrl) }

                Triple(summaryDeferred.await(), processesDeferred.await(), alertsDeferred.await())
            }.onSuccess { (summary, processes, alerts) ->
                _uiState.update { current ->
                    current.copy(
                        summary = summary,
                        processes = processes,
                        alerts = alerts,
                        isLoading = false,
                    )
                }
            }.onFailure { error ->
                _uiState.update { current ->
                    current.copy(
                        isLoading = false,
                        errorMessage = error.message ?: "Unable to reach the gateway.",
                    )
                }
            }
        }
    }
}

