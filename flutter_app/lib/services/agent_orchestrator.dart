/// Agent Orchestrator - Coordinates all autonomous agents
library;

import 'dart:async';
import '../agents/agent_base.dart';
import '../agents/agent_code_master.dart';
import '../agents/agent_gen_ai.dart';
import '../agents/agent_knowledge.dart';
import '../agents/agent_sentiment.dart';
import '../agents/agent_unrestricted.dart';
import '../agents/agent_qa.dart';
import '../agents/agent_deploy.dart';
import '../models/agent_task.dart';
import '../models/agent_result.dart';
import '../models/agent_log.dart';
import '../utils/constants.dart';
import '../utils/logger.dart';
import 'firebase_service.dart';

/// Health status for an agent
class AgentHealthStatus {
  final String agentId;
  final bool healthy;
  final DateTime checkedAt;
  final String? message;
  
  AgentHealthStatus({
    required this.agentId,
    required this.healthy,
    DateTime? checkedAt,
    this.message,
  }) : checkedAt = checkedAt ?? DateTime.now();
  
  Map<String, dynamic> toJson() {
    return {
      'agent_id': agentId,
      'healthy': healthy,
      'checked_at': checkedAt.toIso8601String(),
      'message': message,
    };
  }
}

/// Workflow definition
class Workflow {
  final String id;
  final String name;
  final List<WorkflowStep> steps;
  final Map<String, dynamic>? metadata;
  
  Workflow({
    required this.id,
    required this.name,
    required this.steps,
    this.metadata,
  });
}

/// Workflow step
class WorkflowStep {
  final String agentId;
  final String action;
  final Map<String, dynamic> Function(Map<String, AgentResult>)? parameterBuilder;
  final List<String> dependsOn;
  
  WorkflowStep({
    required this.agentId,
    required this.action,
    this.parameterBuilder,
    this.dependsOn = const [],
  });
}

/// Agent Orchestrator - manages all agents and coordinates workflows
class AgentOrchestrator {
  static final AgentOrchestrator _instance = AgentOrchestrator._internal();
  factory AgentOrchestrator() => _instance;
  AgentOrchestrator._internal();
  
  final Map<String, AgentBase> _agents = {};
  final FirebaseService _firebaseService = FirebaseService();
  final StreamController<AgentLog> _logsController = StreamController<AgentLog>.broadcast();
  
  bool _initialized = false;
  Timer? _healthCheckTimer;
  
  /// Stream of all agent logs
  Stream<AgentLog> get logsStream => _logsController.stream;
  
  /// Check if orchestrator is initialized
  bool get isInitialized => _initialized;
  
  /// Get all agents
  Map<String, AgentBase> get agents => Map.unmodifiable(_agents);
  
  /// Initialize all agents
  Future<void> initializeAllAgents() async {
    if (_initialized) {
      AppLogger.warning('Orchestrator already initialized');
      return;
    }
    
    AppLogger.info('🚀 Initializing Agent Orchestrator...');
    
    try {
      // Initialize Firebase first
      await _firebaseService.initialize();
      
      // Create all 7 agents
      _agents[AppConstants.agentCodeMasterId] = AgentCodeMaster();
      _agents[AppConstants.agentGenAiId] = AgentGenAI();
      _agents[AppConstants.agentKnowledgeId] = AgentKnowledge();
      _agents[AppConstants.agentSentimentId] = AgentSentiment();
      _agents[AppConstants.agentUnrestrictedId] = AgentUnrestricted();
      _agents[AppConstants.agentQaId] = AgentQA();
      _agents[AppConstants.agentDeployId] = AgentDeploy();
      
      // Initialize each agent
      final initFutures = _agents.values.map((agent) async {
        try {
          await agent.initialize();
          AppLogger.info('${agent.emoji} ${agent.name} initialized');
          
          // Subscribe to agent logs
          agent.logs.listen((log) {
            _logsController.add(log);
            _firebaseService.writeLog(log);
          });
        } catch (e, stackTrace) {
          AppLogger.error('Failed to initialize ${agent.name}', e, stackTrace);
          rethrow;
        }
      });
      
      await Future.wait(initFutures);
      
      // Start health check timer
      _startHealthCheckTimer();
      
      _initialized = true;
      AppLogger.info('✅ All agents initialized successfully');
      
      // Write initialization log
      final initLog = AgentLog.info(
        agentId: 'orchestrator',
        message: 'Agent orchestrator initialized with ${_agents.length} agents',
        metadata: {
          'agents': _agents.keys.toList(),
        },
      );
      await _firebaseService.writeLog(initLog);
    } catch (e, stackTrace) {
      AppLogger.error('Failed to initialize agents', e, stackTrace);
      rethrow;
    }
  }
  
  /// Execute a task on a specific agent
  Future<AgentResult> executeTask(String agentId, AgentTask task) async {
    if (!_initialized) {
      throw Exception('Orchestrator not initialized');
    }
    
    final agent = _agents[agentId];
    if (agent == null) {
      throw Exception('Agent not found: $agentId');
    }
    
    AppLogger.info('Executing task ${task.id} on ${agent.name}');
    
    // Save task to Firestore
    await _firebaseService.saveTask(task);
    
    // Execute with retry logic
    AgentResult? result;
    int attempt = 0;
    
    while (attempt < AppConstants.maxRetries) {
      try {
        result = await agent.executeTask(task);
        break;
      } catch (e) {
        attempt++;
        if (attempt >= AppConstants.maxRetries) {
          AppLogger.error('Task ${task.id} failed after $attempt attempts', e);
          result = AgentResult.failure(
            taskId: task.id,
            agentId: agentId,
            error: 'Failed after $attempt attempts: $e',
            executionTime: const Duration(seconds: 0),
          );
        } else {
          final delay = Duration(
            milliseconds: (AppConstants.initialRetryDelayMs *
                    AppConstants.retryBackoffMultiplier.pow(attempt))
                .toInt(),
          );
          AppLogger.warning('Task ${task.id} attempt $attempt failed, retrying in ${delay.inMilliseconds}ms');
          await Future.delayed(delay);
        }
      }
    }
    
    // Save result to Firestore
    if (result != null) {
      await _firebaseService.saveResult(result);
    }
    
    return result!;
  }
  
  /// Execute a workflow with multiple agents
  Future<List<AgentResult>> executeWorkflow(Workflow workflow) async {
    if (!_initialized) {
      throw Exception('Orchestrator not initialized');
    }
    
    AppLogger.info('Executing workflow: ${workflow.name}');
    
    final results = <String, AgentResult>{};
    final pendingSteps = List<WorkflowStep>.from(workflow.steps);
    
    while (pendingSteps.isNotEmpty) {
      // Find steps that can be executed (dependencies met)
      final readySteps = pendingSteps.where((step) {
        return step.dependsOn.every((dep) => results.containsKey(dep));
      }).toList();
      
      if (readySteps.isEmpty && pendingSteps.isNotEmpty) {
        throw Exception('Workflow deadlock: no steps can be executed');
      }
      
      // Execute ready steps in parallel
      final stepFutures = readySteps.map((step) async {
        // Build parameters using previous results
        final parameters = step.parameterBuilder?.call(results) ?? {};
        
        final task = AgentTask(
          agentId: step.agentId,
          action: step.action,
          parameters: parameters,
        );
        
        final result = await executeTask(step.agentId, task);
        results[task.id] = result;
        pendingSteps.remove(step);
        
        return result;
      });
      
      await Future.wait(stepFutures);
    }
    
    AppLogger.info('Workflow ${workflow.name} completed with ${results.length} steps');
    return results.values.toList();
  }
  
  /// Check health of all agents
  Future<Map<String, AgentHealthStatus>> checkAllAgentsHealth() async {
    if (!_initialized) {
      return {};
    }
    
    final healthStatuses = <String, AgentHealthStatus>{};
    
    final healthFutures = _agents.entries.map((entry) async {
      try {
        final healthy = await entry.value.healthCheck();
        healthStatuses[entry.key] = AgentHealthStatus(
          agentId: entry.key,
          healthy: healthy,
          message: healthy ? 'OK' : 'Health check failed',
        );
      } catch (e) {
        healthStatuses[entry.key] = AgentHealthStatus(
          agentId: entry.key,
          healthy: false,
          message: e.toString(),
        );
      }
    });
    
    await Future.wait(healthFutures);
    
    return healthStatuses;
  }
  
  /// Shutdown all agents gracefully
  Future<void> shutdownAllAgents() async {
    AppLogger.info('Shutting down all agents...');
    
    _healthCheckTimer?.cancel();
    
    final shutdownFutures = _agents.values.map((agent) async {
      try {
        await agent.shutdown();
        AppLogger.info('${agent.emoji} ${agent.name} shutdown complete');
      } catch (e, stackTrace) {
        AppLogger.error('Error shutting down ${agent.name}', e, stackTrace);
      }
    });
    
    await Future.wait(shutdownFutures);
    
    _agents.clear();
    await _logsController.close();
    await _firebaseService.close();
    
    _initialized = false;
    AppLogger.info('All agents shutdown complete');
  }
  
  /// Get agent by ID
  AgentBase? getAgent(String agentId) {
    return _agents[agentId];
  }
  
  /// Get agent metadata for all agents
  Map<String, Map<String, dynamic>> getAllAgentsMetadata() {
    return Map.fromEntries(
      _agents.entries.map((entry) => MapEntry(
            entry.key,
            entry.value.getMetadata(),
          )),
    );
  }
  
  void _startHealthCheckTimer() {
    _healthCheckTimer = Timer.periodic(
      const Duration(seconds: AppConstants.healthCheckIntervalSeconds),
      (_) async {
        try {
          final healthStatuses = await checkAllAgentsHealth();
          final unhealthyAgents = healthStatuses.entries
              .where((e) => !e.value.healthy)
              .map((e) => e.key)
              .toList();
          
          if (unhealthyAgents.isNotEmpty) {
            AppLogger.warning('Unhealthy agents detected: $unhealthyAgents');
          }
        } catch (e, stackTrace) {
          AppLogger.error('Health check failed', e, stackTrace);
        }
      },
    );
  }
  
  // Predefined workflows
  
  /// Workflow: Analyze and fix code
  Workflow createAnalyzeAndFixCodeWorkflow(String code) {
    return Workflow(
      id: 'analyze-fix-code',
      name: 'Analyze and Fix Code',
      steps: [
        WorkflowStep(
          agentId: AppConstants.agentCodeMasterId,
          action: 'reviewCode',
          parameterBuilder: (_) => {'code': code},
        ),
        WorkflowStep(
          agentId: AppConstants.agentCodeMasterId,
          action: 'refactorCode',
          parameterBuilder: (results) {
            final reviewResult = results.values.first;
            return {
              'code': code,
              'goals': reviewResult.output['suggestions'] ?? [],
            };
          },
          dependsOn: [],
        ),
        WorkflowStep(
          agentId: AppConstants.agentQaId,
          action: 'suggestTests',
          parameterBuilder: (_) => {'code': code},
        ),
      ],
    );
  }
  
  /// Workflow: Idea to media
  Workflow createIdeaToMediaWorkflow(String idea) {
    return Workflow(
      id: 'idea-to-media',
      name: 'Idea to Media',
      steps: [
        WorkflowStep(
          agentId: AppConstants.agentKnowledgeId,
          action: 'search',
          parameterBuilder: (_) => {'query': idea},
        ),
        WorkflowStep(
          agentId: AppConstants.agentGenAiId,
          action: 'generateImage',
          parameterBuilder: (_) => {'prompt': idea, 'resolution': '4K'},
        ),
      ],
    );
  }
  
  /// Workflow: Smart chat with sentiment adaptation
  Workflow createSmartChatWorkflow(String message) {
    return Workflow(
      id: 'smart-chat',
      name: 'Smart Chat',
      steps: [
        WorkflowStep(
          agentId: AppConstants.agentSentimentId,
          action: 'analyzeText',
          parameterBuilder: (_) => {'text': message},
        ),
        WorkflowStep(
          agentId: AppConstants.agentKnowledgeId,
          action: 'search',
          parameterBuilder: (_) => {'query': message},
        ),
        WorkflowStep(
          agentId: AppConstants.agentSentimentId,
          action: 'adaptResponse',
          parameterBuilder: (results) {
            final sentimentResult = results.values.first;
            return {
              'message': 'Based on your query, here are the results...',
              'sentiment': sentimentResult.output['sentiment'],
            };
          },
          dependsOn: [],
        ),
      ],
    );
  }
}

extension on num {
  int pow(int exponent) {
    return (this * exponent).toInt();
  }
}
