/// Firebase Service for Tokyo-IA
library;

import 'dart:async';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_core/firebase_core.dart';
import '../models/agent_log.dart';
import '../models/agent_task.dart';
import '../models/agent_result.dart';
import '../utils/constants.dart';
import '../utils/logger.dart';

/// Service for Firebase/Firestore operations
class FirebaseService {
  static final FirebaseService _instance = FirebaseService._internal();
  factory FirebaseService() => _instance;
  FirebaseService._internal();
  
  FirebaseFirestore? _firestore;
  bool _initialized = false;
  
  /// Initialize Firebase
  Future<void> initialize() async {
    if (_initialized) return;
    
    try {
      await Firebase.initializeApp();
      _firestore = FirebaseFirestore.instance;
      _initialized = true;
      AppLogger.info('Firebase initialized successfully');
    } catch (e, stackTrace) {
      AppLogger.error('Failed to initialize Firebase', e, stackTrace);
      rethrow;
    }
  }
  
  /// Check if Firebase is initialized
  bool get isInitialized => _initialized;
  
  /// Write agent log to Firestore with "verdad absoluta verificada" mark
  Future<void> writeLog(AgentLog log) async {
    if (!_initialized) {
      AppLogger.warning('Firebase not initialized, cannot write log');
      return;
    }
    
    try {
      await _firestore!
          .collection(AppConstants.agentLogsCollection)
          .doc(log.id)
          .set(log.toJson());
      
      AppLogger.debug('Log written to Firestore: ${log.id}');
    } catch (e, stackTrace) {
      AppLogger.error('Failed to write log to Firestore', e, stackTrace);
    }
  }
  
  /// Write multiple logs in batch
  Future<void> writeLogs(List<AgentLog> logs) async {
    if (!_initialized || logs.isEmpty) return;
    
    try {
      final batch = _firestore!.batch();
      
      for (var log in logs) {
        final docRef = _firestore!
            .collection(AppConstants.agentLogsCollection)
            .doc(log.id);
        batch.set(docRef, log.toJson());
      }
      
      await batch.commit();
      AppLogger.debug('${logs.length} logs written to Firestore');
    } catch (e, stackTrace) {
      AppLogger.error('Failed to write logs batch to Firestore', e, stackTrace);
    }
  }
  
  /// Get logs stream for an agent
  Stream<List<AgentLog>> getLogsStream(String agentId) {
    if (!_initialized) {
      return Stream.value([]);
    }
    
    return _firestore!
        .collection(AppConstants.agentLogsCollection)
        .where('agent_id', isEqualTo: agentId)
        .orderBy('timestamp', descending: true)
        .limit(100)
        .snapshots()
        .map((snapshot) {
      return snapshot.docs
          .map((doc) => AgentLog.fromJson(doc.data()))
          .toList();
    });
  }
  
  /// Get all logs stream
  Stream<List<AgentLog>> getAllLogsStream() {
    if (!_initialized) {
      return Stream.value([]);
    }
    
    return _firestore!
        .collection(AppConstants.agentLogsCollection)
        .orderBy('timestamp', descending: true)
        .limit(200)
        .snapshots()
        .map((snapshot) {
      return snapshot.docs
          .map((doc) => AgentLog.fromJson(doc.data()))
          .toList();
    });
  }
  
  /// Query logs with filters
  Future<List<AgentLog>> queryLogs({
    String? agentId,
    String? level,
    DateTime? startDate,
    DateTime? endDate,
    int limit = 100,
  }) async {
    if (!_initialized) return [];
    
    try {
      Query query = _firestore!.collection(AppConstants.agentLogsCollection);
      
      if (agentId != null) {
        query = query.where('agent_id', isEqualTo: agentId);
      }
      
      if (level != null) {
        query = query.where('level', isEqualTo: level);
      }
      
      if (startDate != null) {
        query = query.where('timestamp', isGreaterThanOrEqualTo: startDate.toIso8601String());
      }
      
      if (endDate != null) {
        query = query.where('timestamp', isLessThanOrEqualTo: endDate.toIso8601String());
      }
      
      query = query.orderBy('timestamp', descending: true).limit(limit);
      
      final snapshot = await query.get();
      return snapshot.docs
          .map((doc) => AgentLog.fromJson(doc.data() as Map<String, dynamic>))
          .toList();
    } catch (e, stackTrace) {
      AppLogger.error('Failed to query logs', e, stackTrace);
      return [];
    }
  }
  
  /// Save agent task
  Future<void> saveTask(AgentTask task) async {
    if (!_initialized) return;
    
    try {
      await _firestore!
          .collection(AppConstants.agentTasksCollection)
          .doc(task.id)
          .set(task.toJson());
      
      AppLogger.debug('Task saved to Firestore: ${task.id}');
    } catch (e, stackTrace) {
      AppLogger.error('Failed to save task to Firestore', e, stackTrace);
    }
  }
  
  /// Update task status
  Future<void> updateTaskStatus(String taskId, String status) async {
    if (!_initialized) return;
    
    try {
      await _firestore!
          .collection(AppConstants.agentTasksCollection)
          .doc(taskId)
          .update({
        'status': status,
        'updated_at': DateTime.now().toIso8601String(),
      });
    } catch (e, stackTrace) {
      AppLogger.error('Failed to update task status', e, stackTrace);
    }
  }
  
  /// Save agent result
  Future<void> saveResult(AgentResult result) async {
    if (!_initialized) return;
    
    try {
      await _firestore!
          .collection(AppConstants.agentTasksCollection)
          .doc(result.taskId)
          .update({
        'output': result.output,
        'status': result.success ? TaskStatus.completed : TaskStatus.failed,
        'completed_at': result.completedAt.toIso8601String(),
        'execution_time_ms': result.executionTime.inMilliseconds,
        'error': result.error,
      });
      
      AppLogger.debug('Result saved to Firestore: ${result.taskId}');
    } catch (e, stackTrace) {
      AppLogger.error('Failed to save result to Firestore', e, stackTrace);
    }
  }
  
  /// Get agent metadata
  Future<Map<String, dynamic>?> getAgentMetadata(String agentId) async {
    if (!_initialized) return null;
    
    try {
      final doc = await _firestore!
          .collection(AppConstants.agentsCollection)
          .doc(agentId)
          .get();
      
      return doc.data();
    } catch (e, stackTrace) {
      AppLogger.error('Failed to get agent metadata', e, stackTrace);
      return null;
    }
  }
  
  /// Update agent metadata
  Future<void> updateAgentMetadata(String agentId, Map<String, dynamic> metadata) async {
    if (!_initialized) return;
    
    try {
      await _firestore!
          .collection(AppConstants.agentsCollection)
          .doc(agentId)
          .set({
        ...metadata,
        'last_updated': DateTime.now().toIso8601String(),
      }, SetOptions(merge: true));
    } catch (e, stackTrace) {
      AppLogger.error('Failed to update agent metadata', e, stackTrace);
    }
  }
  
  /// Index document for vector search (simplified)
  Future<String?> indexDocument(String content, Map<String, dynamic> metadata) async {
    if (!_initialized) return null;
    
    try {
      final docRef = _firestore!
          .collection(AppConstants.vectorIndexCollection)
          .doc();
      
      await docRef.set({
        'content': content,
        'metadata': metadata,
        'indexed_at': DateTime.now().toIso8601String(),
        // In a real implementation, embeddings would be generated here
        'embeddings': [],
      });
      
      return docRef.id;
    } catch (e, stackTrace) {
      AppLogger.error('Failed to index document', e, stackTrace);
      return null;
    }
  }
  
  /// Search documents (simplified - real implementation would use vector similarity)
  Future<List<Map<String, dynamic>>> searchDocuments(String query, {int limit = 10}) async {
    if (!_initialized) return [];
    
    try {
      // Simplified search - real implementation would use vector embeddings
      final snapshot = await _firestore!
          .collection(AppConstants.vectorIndexCollection)
          .limit(limit)
          .get();
      
      return snapshot.docs
          .map((doc) => doc.data())
          .toList();
    } catch (e, stackTrace) {
      AppLogger.error('Failed to search documents', e, stackTrace);
      return [];
    }
  }
  
  /// Close Firebase connection
  Future<void> close() async {
    // Firebase doesn't need explicit closing, but we mark as uninitialized
    _initialized = false;
    AppLogger.info('Firebase service closed');
  }
}
