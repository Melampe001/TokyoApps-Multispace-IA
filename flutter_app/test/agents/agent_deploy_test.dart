/// Tests for Agent_Deploy
library;

import 'package:flutter_test/flutter_test.dart';
import 'package:tokyo_ia/agents/agent_deploy.dart';
import 'package:tokyo_ia/models/agent_task.dart';
import 'package:tokyo_ia/utils/constants.dart';

void main() {
  group('Agent_Deploy Tests', () {
    late AgentDeploy agent;
    
    setUp(() {
      agent = AgentDeploy();
    });
    
    tearDown() async {
      await agent.shutdown();
    });
    
    test('Agent initialization', () async {
      expect(agent.agentId, equals(AppConstants.agentDeployId));
      expect(agent.name, equals(AppConstants.agentDeployName));
      expect(agent.emoji, equals(AppConstants.agentDeployEmoji));
    });
    
    test('Build debug APK', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'buildAPK',
        parameters: {
          'flavor': 'debug',
          'profile': 'debug',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['build_type'], equals('APK'));
      expect(result.output['build_path'], isNotEmpty);
      expect(result.output['build_size'], greaterThan(0));
    });
    
    test('Build release AAB', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'buildAAB',
        parameters: {
          'flavor': 'release',
          'profile': 'release',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['build_type'], equals('AAB'));
      expect(result.output['build_path'], contains('.aab'));
    });
    
    test('Sign build', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'signBuild',
        parameters: {
          'buildPath': '/path/to/app.apk',
          'keystore': 'release',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['signed'], isTrue);
      expect(result.output['signed_path'], contains('-signed'));
    });
    
    test('Upload to Firebase', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'uploadToFirebase',
        parameters: {
          'buildPath': '/path/to/app-signed.apk',
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['uploaded'], isTrue);
      expect(result.output['download_url'], isNotEmpty);
    });
    
    test('Generate release notes', () async {
      await agent.initialize();
      
      final task = AgentTask(
        agentId: agent.agentId,
        action: 'generateReleaseNotes',
        parameters: {
          'changes': [
            'Added new feature',
            'Fixed bug',
          ],
        },
      );
      
      final result = await agent.executeTask(task);
      
      expect(result.success, isTrue);
      expect(result.output['release_notes'], isNotEmpty);
    });
  });
}
