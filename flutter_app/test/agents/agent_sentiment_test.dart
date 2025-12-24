/// Tests for Agent_Sentiment
library;

import 'package:flutter_test/flutter_test.dart';
import 'package:tokyo_ia/agents/agent_sentiment.dart';
import 'package:tokyo_ia/models/agent_task.dart';
import 'package:tokyo_ia/utils/constants.dart';

void main() {
  group('Agent_Sentiment Tests', () {
    late AgentSentiment agent;
    
    setUp(() {
      agent = AgentSentiment();
    });
    
    tearDown(() async {
      await agent.shutdown();
    });
    
    test('Agent initialization', () async {
      expect(agent.agentId, equals(AppConstants.agentSentimentId));
      expect(agent.name, equals(AppConstants.agentSentimentName));
      expect(agent.emoji, equals(AppConstants.agentSentimentEmoji));
    });
    
    test('Analyze positive text', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'analyzeText',
        parameters: {
          'text': 'I am so happy and excited about this!',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output, isNotNull);
      expect(result.output['sentiment'], equals('positive'));
      expect(result.output['score'], greaterThan(0));
    });
    
    test('Analyze negative text', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'analyzeText',
        parameters: {
          'text': 'This is terrible and awful',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['sentiment'], equals('negative'));
      expect(result.output['score'], lessThan(0));
    });
    
    test('Analyze neutral text', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'analyzeText',
        parameters: {
          'text': 'The weather is normal today',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['sentiment'], equals('neutral'));
    });
    
    test('Adapt response based on sentiment', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'adaptResponse',
        parameters: {
          'message': 'Here is the information you requested',
          'sentiment': 'negative',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['adapted_message'], isNotNull);
      expect(result.output['adapted_message'], isNot(equals(result.output['original_message'])));
    });
    
    test('Health check returns true when initialized', () async {
      await agent.initialize();
      
      final healthy = await agent.healthCheck();
      
      expect(healthy, isTrue);
    });
  });
}
