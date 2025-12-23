package com.tokyoia.app.ui.agents

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.compose.runtime.Stable

/**
 * AgentsScreen - Main screen displaying all Tokyo-IA agents
 * 
 * Features:
 * - List of all 5 specialized agents
 * - Agent status (active/inactive)
 * - Statistics cards (tasks, tokens, success rate)
 * - Navigation to agent details
 */
@Composable
fun AgentsScreen(
    viewModel: AgentsViewModel = viewModel(),
    onAgentClick: (String) -> Unit
) {
    val uiState by viewModel.uiState.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("🗼 Tokyo-IA Agents") }
            )
        }
    ) { padding ->
        when (uiState) {
            is AgentsUiState.Loading -> {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding),
                    contentAlignment = androidx.compose.ui.Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }
            
            is AgentsUiState.Success -> {
                val agents = (uiState as AgentsUiState.Success).agents
                
                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    items(
                        items = agents,
                        key = { agent -> agent.id }
                    ) { agent ->
                        AgentCard(
                            agent = agent,
                            onClick = { onAgentClick(agent.id) }
                        )
                    }
                }
            }
            
            is AgentsUiState.Error -> {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding),
                    contentAlignment = androidx.compose.ui.Alignment.Center
                ) {
                    Column(
                        horizontalAlignment = androidx.compose.ui.Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = "Failed to load agents",
                            style = MaterialTheme.typography.titleMedium
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Button(onClick = { viewModel.loadAgents() }) {
                            Text("Retry")
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun AgentCard(
    agent: Agent,
    onClick: () -> Unit
) {
    // Remember the click handler to prevent recomposition
    val stableOnClick = remember(agent.id) { onClick }
    
    Card(
        onClick = stableOnClick,
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            // Agent header with emoji and name
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Row {
                    Text(
                        text = agent.personalityEmoji,
                        style = MaterialTheme.typography.headlineMedium
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Column {
                        Text(
                            text = agent.name,
                            style = MaterialTheme.typography.titleLarge
                        )
                        Text(
                            text = agent.role,
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
                
                // Status badge
                Surface(
                    color = if (agent.status == "active") 
                        MaterialTheme.colorScheme.primaryContainer
                    else 
                        MaterialTheme.colorScheme.errorContainer,
                    shape = MaterialTheme.shapes.small
                ) {
                    Text(
                        text = agent.status.uppercase(),
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                        style = MaterialTheme.typography.labelSmall
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(12.dp))
            
            // Statistics
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                StatItem("Tasks", agent.totalTasksCompleted.toString())
                StatItem("Tokens", formatNumber(agent.totalTokensUsed))
                StatItem("Success", "${agent.successRate}%")
            }
        }
    }
}

@Composable
@Stable
fun StatItem(label: String, value: String) {
    Column(horizontalAlignment = androidx.compose.ui.Alignment.CenterHorizontally) {
        Text(
            text = value,
            style = MaterialTheme.typography.titleMedium
        )
        Text(
            text = label,
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Stable
fun formatNumber(num: Long): String {
    return when {
        num >= 1_000_000 -> "${num / 1_000_000}M"
        num >= 1_000 -> "${num / 1_000}K"
        else -> num.toString()
    }
}

// Data models
@Stable
data class Agent(
    val id: String,
    val name: String,
    val role: String,
    val model: String,
    val specialties: List<String>,
    val personalityEmoji: String,
    val status: String,
    val totalTasksCompleted: Int,
    val totalTokensUsed: Long,
    val successRate: Double
)

@Stable
sealed interface AgentsUiState {
    object Loading : AgentsUiState
    data class Success(val agents: List<Agent>) : AgentsUiState
    data class Error(val message: String) : AgentsUiState
}
