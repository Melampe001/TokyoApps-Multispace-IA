/// Tests for AgentOrchestrator
library;

import 'package:flutter_test/flutter_test.dart';
import 'package:tokyo_ia_flutter/services/agent_orchestrator.dart';
import 'package:tokyo_ia_flutter/models/agent_task.dart';
import 'package:tokyo_ia_flutter/utils/constants.dart';

void main() {
  group('AgentOrchestrator Tests', () {
    late AgentOrchestrator orchestrator;
    
    setUp(() {
      orchestrator = AgentOrchestrator();
    });
    
    tearDown(() async {
      if (orchestrator.isInitialized) {
        await orchestrator.shutdownAllAgents();
      }
    });
    
    test('Initialize all agents', () async {
      await orchestrator.initializeAllAgents();
      
      expect(orchestrator.isInitialized, isTrue);
      expect(orchestrator.agents.length, equals(7));
      expect(orchestrator.agents.keys, contains(AppConstants.agentCodeMasterId));
      expect(orchestrator.agents.keys, contains(AppConstants.agentGenAiId));
      expect(orchestrator.agents.keys, contains(AppConstants.agentKnowledgeId));
      expect(orchestrator.agents.keys, contains(AppConstants.agentSentimentId));
      expect(orchestrator.agents.keys, contains(AppConstants.agentUnrestrictedId));
      expect(orchestrator.agents.keys, contains(AppConstants.agentQaId));
      expect(orchestrator.agents.keys, contains(AppConstants.agentDeployId));
    });
    
    test('Execute task on specific agent', () async {
      await orchestrator.initializeAllAgents();
      
      final task = AgentTask(
        agentId: AppConstants.agentCodeMasterId,
        action: 'generateCode',
        parameters: {'prompt': 'test'},
      );
      
      final result = await orchestrator.executeTask(
        AppConstants.agentCodeMasterId,
        task,
      );
      
      expect(result, isNotNull);
      expect(result.agentId, equals(AppConstants.agentCodeMasterId));
    });
    
    test('Health check all agents', () async {
      await orchestrator.initializeAllAgents();
      
      final healthStatuses = await orchestrator.checkAllAgentsHealth();
      
      expect(healthStatuses.length, equals(7));
      
      for (var status in healthStatuses.values) {
        expect(status.healthy, isTrue);
        expect(status.checkedAt, isNotNull);
      }
    });
    
    test('Get agent by ID', () async {
      await orchestrator.initializeAllAgents();
      
      final agent = orchestrator.getAgent(AppConstants.agentCodeMasterId);
      
      expect(agent, isNotNull);
      expect(agent!.agentId, equals(AppConstants.agentCodeMasterId));
    });
    
    test('Get all agents metadata', () async {
      await orchestrator.initializeAllAgents();
      
      final metadata = orchestrator.getAllAgentsMetadata();
      
      expect(metadata.length, equals(7));
      
      for (var agentMetadata in metadata.values) {
        expect(agentMetadata['agent_id'], isNotNull);
        expect(agentMetadata['name'], isNotNull);
        expect(agentMetadata['emoji'], isNotNull);
        expect(agentMetadata['status'], isNotNull);
      }
    });
    
    test('Shutdown all agents gracefully', () async {
      await orchestrator.initializeAllAgents();
      
      expect(orchestrator.isInitialized, isTrue);
      
      await orchestrator.shutdownAllAgents();
      
      expect(orchestrator.isInitialized, isFalse);
      expect(orchestrator.agents.length, equals(0));
    });
    
    test('Execute workflow with multiple agents', () async {
      await orchestrator.initializeAllAgents();
      
      final workflow = orchestrator.createIdeaToMediaWorkflow('beautiful sunset');
      
      final results = await orchestrator.executeWorkflow(workflow);
      
      expect(results, isNotEmpty);
      expect(results.length, equals(workflow.steps.length));
      
      for (var result in results) {
        expect(result, isNotNull);
      }
    });
  });
}
