package com.tokyoia.app.data.repository

import com.tokyoia.app.ui.agents.Agent
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import androidx.compose.runtime.Stable

/**
 * AgentRepository - Data layer for agent operations
 * 
 * Responsibilities:
 * - Fetch agents from Registry API
 * - Cache agent data locally
 * - Handle network errors
 * - Parse JSON responses
 */
class AgentRepository {
    
    private val client = OkHttpClient()
    private val baseUrl = "http://localhost:8080/api" // TODO: Make configurable
    
    private var cachedAgents: List<Agent>? = null
    
    suspend fun getAllAgents(): List<Agent> = withContext(Dispatchers.IO) {
        // Return cache if available
        cachedAgents?.let { return@withContext it }
        
        val request = Request.Builder()
            .url("$baseUrl/agents")
            .get()
            .build()
        
        val response = client.newCall(request).execute()
        
        if (!response.isSuccessful) {
            throw IOException("HTTP ${response.code}: ${response.message}")
        }
        
        val responseBody = response.body?.string() 
            ?: throw IOException("Empty response body")
        
        val agents = parseAgentsJson(responseBody)
        cachedAgents = agents
        
        return@withContext agents
    }
    
    suspend fun getAgentById(agentId: String): Agent = withContext(Dispatchers.IO) {
        // Check cache first
        cachedAgents?.find { it.id == agentId }?.let { return@withContext it }
        
        val request = Request.Builder()
            .url("$baseUrl/agents/$agentId")
            .get()
            .build()
        
        val response = client.newCall(request).execute()
        
        if (!response.isSuccessful) {
            throw IOException("HTTP ${response.code}: ${response.message}")
        }
        
        val responseBody = response.body?.string()
            ?: throw IOException("Empty response body")
        
        return@withContext parseAgentJson(JSONObject(responseBody))
    }
    
    suspend fun getAgentStats(agentId: String): AgentStats = withContext(Dispatchers.IO) {
        val request = Request.Builder()
            .url("$baseUrl/agents/$agentId/stats")
            .get()
            .build()
        
        val response = client.newCall(request).execute()
        
        if (!response.isSuccessful) {
            throw IOException("HTTP ${response.code}: ${response.message}")
        }
        
        val responseBody = response.body?.string()
            ?: throw IOException("Empty response body")
        
        return@withContext parseAgentStats(JSONObject(responseBody))
    }
    
    fun clearCache() {
        cachedAgents = null
    }
    
    private fun parseAgentsJson(json: String): List<Agent> {
        val jsonArray = JSONArray(json)
        val agents = mutableListOf<Agent>()
        
        for (i in 0 until jsonArray.length()) {
            val agentJson = jsonArray.getJSONObject(i)
            agents.add(parseAgentJson(agentJson))
        }
        
        return agents
    }
    
    private fun parseAgentJson(json: JSONObject): Agent {
        val specialtiesArray = json.getJSONArray("specialties")
        val specialties = mutableListOf<String>()
        for (i in 0 until specialtiesArray.length()) {
            specialties.add(specialtiesArray.getString(i))
        }
        
        return Agent(
            id = json.getString("id"),
            name = json.getString("name"),
            role = json.getString("role"),
            model = json.getString("model"),
            specialties = specialties,
            personalityEmoji = json.getString("personality_emoji"),
            status = json.getString("status"),
            totalTasksCompleted = json.getInt("total_tasks_completed"),
            totalTokensUsed = json.getLong("total_tokens_used"),
            successRate = json.getDouble("success_rate")
        )
    }
    
    private fun parseAgentStats(json: JSONObject): AgentStats {
        return AgentStats(
            totalTasks = json.getInt("total_tasks"),
            completedTasks = json.getInt("completed_tasks"),
            failedTasks = json.getInt("failed_tasks"),
            totalTokens = json.getLong("total_tokens"),
            totalCost = json.getDouble("total_cost"),
            avgDurationMs = json.getDouble("avg_duration_ms"),
            successRate = json.getDouble("success_rate")
        )
    }
}

@Stable
data class AgentStats(
    val totalTasks: Int,
    val completedTasks: Int,
    val failedTasks: Int,
    val totalTokens: Long,
    val totalCost: Double,
    val avgDurationMs: Double,
    val successRate: Double
)
