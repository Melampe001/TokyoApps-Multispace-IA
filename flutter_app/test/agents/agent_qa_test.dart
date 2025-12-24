/// Tests for Agent_QA
library;

import 'package:flutter_test/flutter_test.dart';
import 'package:tokyo_ia/agents/agent_qa.dart';
import 'package:tokyo_ia/models/agent_task.dart';
import 'package:tokyo_ia/utils/constants.dart';

void main() {
  group('Agent_QA Tests', () {
    late AgentQA agent;
    
    setUp(() {
      agent = AgentQA();
    });
    
    tearDown() async {
      await agent.shutdown();
    });
    
    test('Agent initialization', () async {
      expect(agent.agentId, equals(AppConstants.agentQaId));
      expect(agent.name, equals(AppConstants.agentQaName));
      expect(agent.emoji, equals(AppConstants.agentQaEmoji));
    });
    
    test('Generate commit message', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'generateCommitMessage',
        parameters: {
          'diff': 'feat: add new feature\n+10 -5 lines',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['commit_message'], isNotEmpty);
      expect(result.output['type'], isNotNull);
    });
    
    test('Review pull request', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'reviewPullRequest',
        parameters: {
          'prData': {
            'number': 123,
            'changed_files': 5,
          },
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['summary'], isNotEmpty);
      expect(result.output['comments'], isList);
    });
    
    test('Suggest tests for code', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'suggestTests',
        parameters: {
          'code': 'class MyClass { void method() {} }',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['test_suggestions'], isList);
    });
    
    test('Check code quality', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'checkCodeQuality',
        parameters: {
          'files': ['lib/main.dart', 'lib/utils.dart'],
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['overall_score'], isNotNull);
    });
  });
}
