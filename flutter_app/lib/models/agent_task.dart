/// Agent Task Model
library;

import 'package:uuid/uuid.dart';

class AgentTask {
  final String id;
  final String agentId;
  final String action;
  final Map<String, dynamic> parameters;
  final String status;
  final DateTime createdAt;
  final DateTime? startedAt;
  final DateTime? completedAt;
  final int priority;
  final Map<String, dynamic>? metadata;
  
  AgentTask({
    String? id,
    required this.agentId,
    required this.action,
    required this.parameters,
    this.status = 'pending',
    DateTime? createdAt,
    this.startedAt,
    this.completedAt,
    this.priority = 0,
    this.metadata,
  })  : id = id ?? const Uuid().v4(),
        createdAt = createdAt ?? DateTime.now();
  
  AgentTask copyWith({
    String? id,
    String? agentId,
    String? action,
    Map<String, dynamic>? parameters,
    String? status,
    DateTime? createdAt,
    DateTime? startedAt,
    DateTime? completedAt,
    int? priority,
    Map<String, dynamic>? metadata,
  }) {
    return AgentTask(
      id: id ?? this.id,
      agentId: agentId ?? this.agentId,
      action: action ?? this.action,
      parameters: parameters ?? this.parameters,
      status: status ?? this.status,
      createdAt: createdAt ?? this.createdAt,
      startedAt: startedAt ?? this.startedAt,
      completedAt: completedAt ?? this.completedAt,
      priority: priority ?? this.priority,
      metadata: metadata ?? this.metadata,
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'agent_id': agentId,
      'action': action,
      'parameters': parameters,
      'status': status,
      'created_at': createdAt.toIso8601String(),
      'started_at': startedAt?.toIso8601String(),
      'completed_at': completedAt?.toIso8601String(),
      'priority': priority,
      'metadata': metadata,
    };
  }
  
  factory AgentTask.fromJson(Map<String, dynamic> json) {
    return AgentTask(
      id: json['id'] as String,
      agentId: json['agent_id'] as String,
      action: json['action'] as String,
      parameters: Map<String, dynamic>.from(json['parameters'] as Map),
      status: json['status'] as String? ?? 'pending',
      createdAt: DateTime.parse(json['created_at'] as String),
      startedAt: json['started_at'] != null
          ? DateTime.parse(json['started_at'] as String)
          : null,
      completedAt: json['completed_at'] != null
          ? DateTime.parse(json['completed_at'] as String)
          : null,
      priority: json['priority'] as int? ?? 0,
      metadata: json['metadata'] != null
          ? Map<String, dynamic>.from(json['metadata'] as Map)
          : null,
    );
  }
  
  @override
  String toString() {
    return 'AgentTask(id: $id, agentId: $agentId, action: $action, status: $status)';
  }
}
