/// Tests for Agent_GenAI
library;

import 'package:flutter_test/flutter_test.dart';
import 'package:tokyo_ia/agents/agent_gen_ai.dart';
import 'package:tokyo_ia/models/agent_task.dart';
import 'package:tokyo_ia/utils/constants.dart';

void main() {
  group('Agent_GenAI Tests', () {
    late AgentGenAI agent;
    
    setUp(() {
      agent = AgentGenAI();
    });
    
    tearDown(() async {
      await agent.shutdown();
    });
    
    test('Agent initialization', () async {
      expect(agent.agentId, equals(AppConstants.agentGenAiId));
      expect(agent.name, equals(AppConstants.agentGenAiName));
      expect(agent.emoji, equals(AppConstants.agentGenAiEmoji));
    });
    
    test('Generate image task', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'generateImage',
        parameters: {
          'prompt': 'A beautiful sunset over mountains',
          'resolution': '4K',
          'style': 'realistic',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output, isNotNull);
      expect(result.output['image_url'], isNotEmpty);
      expect(result.output['resolution'], equals('4K'));
    });
    
    test('Generate voice task', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'generateVoice',
        parameters: {
          'text': 'Hello, this is a test',
          'voice': 'default',
          'emotion': 'neutral',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['audio_url'], isNotEmpty);
      expect(result.output['text'], equals('Hello, this is a test'));
    });
    
    test('Generate music task', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'generateMusic',
        parameters: {
          'prompt': 'Calm ambient music',
          'duration': 30,
          'genre': 'ambient',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['audio_url'], isNotEmpty);
      expect(result.output['genre'], equals('ambient'));
    });
  });
}
