/// Tests for Agent_Knowledge
library;

import 'package:flutter_test/flutter_test.dart';
import 'package:tokyo_ia/agents/agent_knowledge.dart';
import 'package:tokyo_ia/models/agent_task.dart';
import 'package:tokyo_ia/utils/constants.dart';

void main() {
  group('Agent_Knowledge Tests', () {
    late AgentKnowledge agent;
    
    setUp(() {
      agent = AgentKnowledge();
    });
    
    tearDown() async {
      await agent.shutdown();
    });
    
    test('Agent initialization', () async {
      expect(agent.agentId, equals(AppConstants.agentKnowledgeId));
      expect(agent.name, equals(AppConstants.agentKnowledgeName));
      expect(agent.emoji, equals(AppConstants.agentKnowledgeEmoji));
    });
    
    test('Web search task', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'search',
        parameters: {
          'query': 'Flutter best practices',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['results'], isList);
      expect(result.output['query'], equals('Flutter best practices'));
    });
    
    test('RAG query task', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'queryRAG',
        parameters: {
          'question': 'What is Flutter?',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['answer'], isNotEmpty);
      expect(result.output['confidence'], isNotNull);
    });
    
    test('Index document task', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'indexDocument',
        parameters: {
          'document': {
            'title': 'Test Document',
            'content': 'This is test content',
          },
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['indexed'], isTrue);
      expect(result.output['document_id'], isNotNull);
    });
    
    test('Fact check task', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'factCheck',
        parameters: {
          'statement': 'Flutter is a UI framework',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['verified'], isNotNull);
      expect(result.output['sources'], isList);
    });
  });
}
