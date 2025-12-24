/// Base Agent Abstract Class
library;

import 'dart:async';
import 'dart:isolate';
import 'package:flutter/foundation.dart';
import '../models/agent_task.dart';
import '../models/agent_result.dart';
import '../models/agent_log.dart';
import '../utils/constants.dart';
import '../utils/logger.dart';

/// Abstract base class for all autonomous agents
abstract class AgentBase {
  final String agentId;
  final String name;
  final String emoji;
  
  String _status = AgentStatus.initializing;
  Isolate? _isolate;
  ReceivePort? _receivePort;
  SendPort? _sendPort;
  
  final StreamController<AgentLog> _logController = StreamController<AgentLog>.broadcast();
  final StreamController<String> _statusController = StreamController<String>.broadcast();
  
  DateTime? _lastHealthCheck;
  DateTime? _lastActive;
  int _tasksCompleted = 0;
  int _tasksFailed = 0;
  
  AgentBase({
    required this.agentId,
    required this.name,
    required this.emoji,
  });
  
  /// Stream of logs from this agent
  Stream<AgentLog> get logs => _logController.stream;
  
  /// Stream of status changes
  Stream<String> get statusChanges => _statusController.stream;
  
  /// Current status of the agent
  String get status => _status;
  
  /// Statistics
  int get tasksCompleted => _tasksCompleted;
  int get tasksFailed => _tasksFailed;
  DateTime? get lastActive => _lastActive;
  DateTime? get lastHealthCheck => _lastHealthCheck;
  
  /// Initialize the agent and spawn isolate
  Future<void> initialize() async {
    try {
      _updateStatus(AgentStatus.initializing);
      _log(LogLevel.info, 'Initializing agent $name ($agentId)');
      
      // Create receive port for communication
      _receivePort = ReceivePort();
      
      // Spawn isolate
      _isolate = await Isolate.spawn(
        _isolateEntry,
        _receivePort!.sendPort,
        debugName: '$name-isolate',
      );
      
      // Get send port from isolate
      _sendPort = await _receivePort!.first as SendPort;
      
      // Setup message handler
      _receivePort!.listen(_handleMessage);
      
      // Agent-specific initialization
      await onInitialize();
      
      _updateStatus(AgentStatus.idle);
      _log(LogLevel.info, 'Agent $name initialized successfully');
      _lastHealthCheck = DateTime.now();
    } catch (e, stackTrace) {
      _updateStatus(AgentStatus.error);
      _log(LogLevel.error, 'Failed to initialize agent $name: $e', error: e.toString(), stackTrace: stackTrace);
      rethrow;
    }
  }
  
  /// Execute a task
  Future<AgentResult> executeTask(AgentTask task) async {
    final startTime = DateTime.now();
    
    try {
      _updateStatus(AgentStatus.running);
      _lastActive = DateTime.now();
      _log(LogLevel.info, 'Executing task ${task.id}: ${task.action}', taskId: task.id);
      
      // Execute the task
      final result = await onExecuteTask(task);
      
      _tasksCompleted++;
      _updateStatus(AgentStatus.idle);
      _log(LogLevel.info, 'Task ${task.id} completed successfully', taskId: task.id);
      
      return result;
    } catch (e, stackTrace) {
      _tasksFailed++;
      _updateStatus(AgentStatus.error);
      _log(LogLevel.error, 'Task ${task.id} failed: $e', taskId: task.id, error: e.toString(), stackTrace: stackTrace);
      
      final executionTime = DateTime.now().difference(startTime);
      return AgentResult.failure(
        taskId: task.id,
        agentId: agentId,
        error: e.toString(),
        executionTime: executionTime,
      );
    } finally {
      _updateStatus(AgentStatus.idle);
    }
  }
  
  /// Health check
  Future<bool> healthCheck() async {
    try {
      _lastHealthCheck = DateTime.now();
      final healthy = await onHealthCheck();
      
      if (!healthy) {
        _log(LogLevel.warning, 'Health check failed for agent $name');
      }
      
      return healthy;
    } catch (e, stackTrace) {
      _log(LogLevel.error, 'Health check error: $e', error: e.toString(), stackTrace: stackTrace);
      return false;
    }
  }
  
  /// Shutdown the agent
  Future<void> shutdown() async {
    try {
      _log(LogLevel.info, 'Shutting down agent $name');
      _updateStatus(AgentStatus.stopped);
      
      await onShutdown();
      
      _isolate?.kill(priority: Isolate.immediate);
      _receivePort?.close();
      await _logController.close();
      await _statusController.close();
      
      _log(LogLevel.info, 'Agent $name shutdown complete');
    } catch (e, stackTrace) {
      _log(LogLevel.error, 'Error during shutdown: $e', error: e.toString(), stackTrace: stackTrace);
    }
  }
  
  /// Abstract methods to be implemented by subclasses
  
  /// Called during initialization
  @protected
  Future<void> onInitialize();
  
  /// Execute a specific task
  @protected
  Future<AgentResult> onExecuteTask(AgentTask task);
  
  /// Perform health check
  @protected
  Future<bool> onHealthCheck() async => true;
  
  /// Called during shutdown
  @protected
  Future<void> onShutdown() async {}
  
  /// Isolate entry point
  static void _isolateEntry(SendPort sendPort) {
    final receivePort = ReceivePort();
    sendPort.send(receivePort.sendPort);
    
    receivePort.listen((message) {
      // Handle messages from main isolate
    });
  }
  
  /// Handle messages from isolate
  void _handleMessage(dynamic message) {
    // Handle responses from isolate
  }
  
  /// Update agent status
  void _updateStatus(String newStatus) {
    _status = newStatus;
    _statusController.add(newStatus);
  }
  
  /// Log a message
  void _log(
    String level,
    String message, {
    String? taskId,
    String? error,
    StackTrace? stackTrace,
    Map<String, dynamic>? metadata,
  }) {
    final log = AgentLog(
      agentId: agentId,
      level: level,
      message: message,
      taskId: taskId,
      error: error,
      stackTrace: stackTrace,
      metadata: metadata,
    );
    
    _logController.add(log);
    
    // Also log to console
    switch (level) {
      case LogLevel.debug:
        AppLogger.debug('[$emoji $name] $message', error, stackTrace);
        break;
      case LogLevel.info:
        AppLogger.info('[$emoji $name] $message', error, stackTrace);
        break;
      case LogLevel.warning:
        AppLogger.warning('[$emoji $name] $message', error, stackTrace);
        break;
      case LogLevel.error:
        AppLogger.error('[$emoji $name] $message', error, stackTrace);
        break;
      case LogLevel.critical:
        AppLogger.critical('[$emoji $name] $message', error, stackTrace);
        break;
    }
  }
  
  /// Get agent metadata
  Map<String, dynamic> getMetadata() {
    return {
      'agent_id': agentId,
      'name': name,
      'emoji': emoji,
      'status': status,
      'tasks_completed': tasksCompleted,
      'tasks_failed': tasksFailed,
      'last_active': lastActive?.toIso8601String(),
      'last_health_check': lastHealthCheck?.toIso8601String(),
    };
  }
}
