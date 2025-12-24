/// Tests for Agent_CodeMaster
library;

import 'package:flutter_test/flutter_test.dart';
import 'package:tokyo_ia/agents/agent_code_master.dart';
import 'package:tokyo_ia/models/agent_task.dart';
import 'package:tokyo_ia/utils/constants.dart';

void main() {
  group('Agent_CodeMaster Tests', () {
    late AgentCodeMaster agent;
    
    setUp(() {
      agent = AgentCodeMaster();
    });
    
    tearDown(() async {
      await agent.shutdown();
    });
    
    test('Agent initialization', () async {
      expect(agent.agentId, equals(AppConstants.agentCodeMasterId));
      expect(agent.name, equals(AppConstants.agentCodeMasterName));
      expect(agent.emoji, equals(AppConstants.agentCodeMasterEmoji));
      expect(agent.status, equals(AgentStatus.initializing));
    });
    
    test('Generate code task execution', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'generateCode',
        parameters: {
          'prompt': 'Create a simple Flutter widget',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output, isNotNull);
      expect(result.output['code'], isNotEmpty);
      expect(result.executionTime.inMilliseconds, greaterThan(0));
    });
    
    test('Review code task execution', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'reviewCode',
        parameters: {
          'code': 'class TestClass { void test() {} }',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output, isNotNull);
      expect(result.output['overall_quality'], isNotNull);
      expect(result.output['issues'], isList);
    });
    
    test('Error handling for missing parameters', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'generateCode',
        parameters: {}, // Missing 'prompt' parameter
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isFalse);
      expect(result.error, isNotNull);
    });
    
    test('Health check returns true when initialized', () async {
      await agent.initialize();
      
      final healthy = await agent.healthCheck();
      
      expect(healthy, isTrue);
    });
    
    test('Task increments tasks completed counter', () async {
      await agent.initialize();
      
      final initialCount = agent.tasksCompleted;
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'generateCode',
        parameters: {'prompt': 'test'},
      );
      
      await agent.executeTask(task);
      
      expect(agent.tasksCompleted, equals(initialCount + 1));
    });
  });
}
