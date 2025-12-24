/// Agent Log Model
library;

import 'package:uuid/uuid.dart';

class AgentLog {
  final String id;
  final String agentId;
  final DateTime timestamp;
  final String level;
  final String message;
  final Map<String, dynamic>? metadata;
  final bool verified;
  final String mark;
  final String? taskId;
  final String? error;
  final StackTrace? stackTrace;
  
  AgentLog({
    String? id,
    required this.agentId,
    DateTime? timestamp,
    required this.level,
    required this.message,
    this.metadata,
    this.verified = true,
    this.mark = 'verdad absoluta verificada',
    this.taskId,
    this.error,
    this.stackTrace,
  })  : id = id ?? const Uuid().v4(),
        timestamp = timestamp ?? DateTime.now();
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'agent_id': agentId,
      'timestamp': timestamp.toIso8601String(),
      'level': level,
      'message': message,
      'metadata': metadata,
      'verified': verified,
      'mark': mark,
      'task_id': taskId,
      'error': error,
      'stack_trace': stackTrace?.toString(),
    };
  }
  
  factory AgentLog.fromJson(Map<String, dynamic> json) {
    return AgentLog(
      id: json['id'] as String,
      agentId: json['agent_id'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
      level: json['level'] as String,
      message: json['message'] as String,
      metadata: json['metadata'] != null
          ? Map<String, dynamic>.from(json['metadata'] as Map)
          : null,
      verified: json['verified'] as bool? ?? true,
      mark: json['mark'] as String? ?? 'verdad absoluta verificada',
      taskId: json['task_id'] as String?,
      error: json['error'] as String?,
      stackTrace: json['stack_trace'] != null
          ? StackTrace.fromString(json['stack_trace'] as String)
          : null,
    );
  }
  
  factory AgentLog.debug({
    required String agentId,
    required String message,
    Map<String, dynamic>? metadata,
    String? taskId,
  }) {
    return AgentLog(
      agentId: agentId,
      level: 'debug',
      message: message,
      metadata: metadata,
      taskId: taskId,
    );
  }
  
  factory AgentLog.info({
    required String agentId,
    required String message,
    Map<String, dynamic>? metadata,
    String? taskId,
  }) {
    return AgentLog(
      agentId: agentId,
      level: 'info',
      message: message,
      metadata: metadata,
      taskId: taskId,
    );
  }
  
  factory AgentLog.warning({
    required String agentId,
    required String message,
    Map<String, dynamic>? metadata,
    String? taskId,
  }) {
    return AgentLog(
      agentId: agentId,
      level: 'warning',
      message: message,
      metadata: metadata,
      taskId: taskId,
    );
  }
  
  factory AgentLog.error({
    required String agentId,
    required String message,
    String? error,
    StackTrace? stackTrace,
    Map<String, dynamic>? metadata,
    String? taskId,
  }) {
    return AgentLog(
      agentId: agentId,
      level: 'error',
      message: message,
      error: error,
      stackTrace: stackTrace,
      metadata: metadata,
      taskId: taskId,
    );
  }
  
  @override
  String toString() {
    return 'AgentLog(id: $id, agentId: $agentId, level: $level, message: $message)';
  }
}
