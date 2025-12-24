/// Agent Result Model
library;

class AgentResult {
  final String taskId;
  final String agentId;
  final bool success;
  final dynamic output;
  final String? error;
  final DateTime completedAt;
  final Duration executionTime;
  final Map<String, dynamic>? metadata;
  
  AgentResult({
    required this.taskId,
    required this.agentId,
    required this.success,
    this.output,
    this.error,
    DateTime? completedAt,
    required this.executionTime,
    this.metadata,
  }) : completedAt = completedAt ?? DateTime.now();
  
  Map<String, dynamic> toJson() {
    return {
      'task_id': taskId,
      'agent_id': agentId,
      'success': success,
      'output': output,
      'error': error,
      'completed_at': completedAt.toIso8601String(),
      'execution_time_ms': executionTime.inMilliseconds,
      'metadata': metadata,
    };
  }
  
  factory AgentResult.fromJson(Map<String, dynamic> json) {
    return AgentResult(
      taskId: json['task_id'] as String,
      agentId: json['agent_id'] as String,
      success: json['success'] as bool,
      output: json['output'],
      error: json['error'] as String?,
      completedAt: DateTime.parse(json['completed_at'] as String),
      executionTime: Duration(milliseconds: json['execution_time_ms'] as int),
      metadata: json['metadata'] != null
          ? Map<String, dynamic>.from(json['metadata'] as Map)
          : null,
    );
  }
  
  factory AgentResult.success({
    required String taskId,
    required String agentId,
    required dynamic output,
    required Duration executionTime,
    Map<String, dynamic>? metadata,
  }) {
    return AgentResult(
      taskId: taskId,
      agentId: agentId,
      success: true,
      output: output,
      executionTime: executionTime,
      metadata: metadata,
    );
  }
  
  factory AgentResult.failure({
    required String taskId,
    required String agentId,
    required String error,
    required Duration executionTime,
    Map<String, dynamic>? metadata,
  }) {
    return AgentResult(
      taskId: taskId,
      agentId: agentId,
      success: false,
      error: error,
      executionTime: executionTime,
      metadata: metadata,
    );
  }
  
  @override
  String toString() {
    return 'AgentResult(taskId: $taskId, agentId: $agentId, success: $success, error: $error)';
  }
}
