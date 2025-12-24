/// Constants for Tokyo-IA Flutter App
library;

class AppConstants {
  // Agent IDs
  static const String agentCodeMasterId = 'agent-codemaster-001';
  static const String agentGenAiId = 'agent-genai-002';
  static const String agentKnowledgeId = 'agent-knowledge-003';
  static const String agentSentimentId = 'agent-sentiment-004';
  static const String agentUnrestrictedId = 'agent-unrestricted-005';
  static const String agentQaId = 'agent-qa-006';
  static const String agentDeployId = 'agent-deploy-007';
  
  // Agent Names
  static const String agentCodeMasterName = 'CodeMaster';
  static const String agentGenAiName = 'GenAI';
  static const String agentKnowledgeName = 'Knowledge';
  static const String agentSentimentName = 'Sentiment';
  static const String agentUnrestrictedName = 'Unrestricted';
  static const String agentQaName = 'QA';
  static const String agentDeployName = 'Deploy';
  
  // Agent Emojis
  static const String agentCodeMasterEmoji = '👨‍💻';
  static const String agentGenAiEmoji = '🎨';
  static const String agentKnowledgeEmoji = '🧠';
  static const String agentSentimentEmoji = '😊';
  static const String agentUnrestrictedEmoji = '🔓';
  static const String agentQaEmoji = '✅';
  static const String agentDeployEmoji = '🚀';
  
  // Firestore Collections
  static const String agentsCollection = 'agents';
  static const String agentLogsCollection = 'agent_logs';
  static const String agentTasksCollection = 'agent_tasks';
  static const String vectorIndexCollection = 'vector_index';
  
  // Log Verification Mark
  static const String verificationMark = 'verdad absoluta verificada';
  
  // Unrestricted Mode
  static const int unrestrictedModeTimeoutMinutes = 30;
  
  // API Endpoints
  static const String geminiApiBaseUrl = 'https://generativelanguage.googleapis.com';
  static const String openaiApiBaseUrl = 'https://api.openai.com';
  static const String anthropicApiBaseUrl = 'https://api.anthropic.com';
  static const String elevenLabsApiBaseUrl = 'https://api.elevenlabs.io';
  static const String serpApiBaseUrl = 'https://serpapi.com';
  
  // Retry Configuration
  static const int maxRetries = 3;
  static const int initialRetryDelayMs = 1000;
  static const double retryBackoffMultiplier = 2.0;
  
  // Health Check
  static const int healthCheckIntervalSeconds = 60;
  
  // Build Configuration
  static const String buildFlavorRelease = 'release';
  static const String buildFlavorDebug = 'debug';
  static const String buildFlavorProfile = 'profile';
}

class AgentStatus {
  static const String initializing = 'initializing';
  static const String idle = 'idle';
  static const String running = 'running';
  static const String error = 'error';
  static const String stopped = 'stopped';
}

class TaskStatus {
  static const String pending = 'pending';
  static const String running = 'running';
  static const String completed = 'completed';
  static const String failed = 'failed';
  static const String cancelled = 'cancelled';
}

class LogLevel {
  static const String debug = 'debug';
  static const String info = 'info';
  static const String warning = 'warning';
  static const String error = 'error';
  static const String critical = 'critical';
}
