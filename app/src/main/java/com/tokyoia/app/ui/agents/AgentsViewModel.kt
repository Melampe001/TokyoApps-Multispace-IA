package com.tokyoia.app.ui.agents

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.tokyoia.app.data.repository.AgentRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

/**
 * AgentsViewModel - State management for agents screen
 * 
 * Responsibilities:
 * - Load agents from repository
 * - Manage UI state (loading, success, error)
 * - Handle agent refresh
 * - Expose agent data as StateFlow
 */
class AgentsViewModel(
    private val repository: AgentRepository = AgentRepository()
) : ViewModel() {

    private val _uiState = MutableStateFlow<AgentsUiState>(AgentsUiState.Loading)
    val uiState: StateFlow<AgentsUiState> = _uiState.asStateFlow()

    init {
        loadAgents()
    }

    fun loadAgents() {
        viewModelScope.launch {
            _uiState.value = AgentsUiState.Loading
            
            try {
                val agents = repository.getAllAgents()
                _uiState.value = AgentsUiState.Success(agents)
            } catch (e: Exception) {
                _uiState.value = AgentsUiState.Error(
                    e.message ?: "Failed to load agents"
                )
            }
        }
    }

    fun refreshAgents() {
        loadAgents()
    }

    fun getAgent(agentId: String) {
        viewModelScope.launch {
            try {
                val agent = repository.getAgentById(agentId)
                // Handle agent details
            } catch (e: Exception) {
                // Handle error
            }
        }
    }
}
