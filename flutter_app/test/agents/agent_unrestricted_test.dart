/// Tests for Agent_Unrestricted
library;

import 'package:flutter_test/flutter_test.dart';
import 'package:tokyo_ia_flutter/agents/agent_unrestricted.dart';
import 'package:tokyo_ia_flutter/models/agent_task.dart';
import 'package:tokyo_ia_flutter/utils/constants.dart';

void main() {
  group('Agent_Unrestricted Tests', () {
    late AgentUnrestricted agent;
    
    setUp(() {
      agent = AgentUnrestricted();
    });
    
    tearDown(() async {
      await agent.shutdown();
    });
    
    test('Agent initialization', () async {
      expect(agent.agentId, equals(AppConstants.agentUnrestrictedId));
      expect(agent.name, equals(AppConstants.agentUnrestrictedName));
      expect(agent.emoji, equals(AppConstants.agentUnrestrictedEmoji));
    });
    
    test('Verify correct PIN', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'verifyPIN',
        parameters: {
          'pin': '1234', // Test PIN
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['verified'], isTrue);
    });
    
    test('Verify incorrect PIN', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'verifyPIN',
        parameters: {
          'pin': 'wrong-pin',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['verified'], isFalse);
    });
    
    test('Enable unrestricted mode with correct PIN', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'enableUnrestrictedMode',
        parameters: {
          'pin': '1234',
          'confirmation': true,
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['enabled'], isTrue);
      expect(result.output['timeout_minutes'], equals(30));
    });
    
    test('Disable unrestricted mode', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'disableUnrestrictedMode',
        parameters: {},
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['enabled'], isFalse);
    });
    
    test('Check restrictions for query', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'checkRestrictions',
        parameters: {
          'query': 'Tell me about Flutter',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['can_proceed'], isNotNull);
    });
  });
}
