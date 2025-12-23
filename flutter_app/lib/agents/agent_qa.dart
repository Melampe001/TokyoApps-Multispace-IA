/// Agent_QA - Quality Assurance and Code Review
library;

import 'dart:async';
import '../models/agent_task.dart';
import '../models/agent_result.dart';
import '../utils/constants.dart';
import 'agent_base.dart';

/// Agent_QA: Generates exact and compact commit messages and PR reviews
/// ID: agent-qa-006
/// Role: Commit messages, PR reviews, changelog, test suggestions, code quality
/// Integration: GitHub API
class AgentQA extends AgentBase {
  String? _githubToken;
  
  AgentQA()
      : super(
          agentId: AppConstants.agentQaId,
          name: AppConstants.agentQaName,
          emoji: AppConstants.agentQaEmoji,
        );
  
  @override
  Future<void> onInitialize() async {
    _githubToken = const String.fromEnvironment('GITHUB_TOKEN', defaultValue: '');
  }
  
  @override
  Future<AgentResult> onExecuteTask(AgentTask task) async {
    final startTime = DateTime.now();
    
    try {
      switch (task.action) {
        case 'generateCommitMessage':
          return await _generateCommitMessage(task, startTime);
        case 'reviewPullRequest':
          return await _reviewPullRequest(task, startTime);
        case 'generateChangelogEntry':
          return await _generateChangelogEntry(task, startTime);
        case 'suggestTests':
          return await _suggestTests(task, startTime);
        case 'checkCodeQuality':
          return await _checkCodeQuality(task, startTime);
        default:
          throw Exception('Unknown action: ${task.action}');
      }
    } catch (e) {
      final executionTime = DateTime.now().difference(startTime);
      return AgentResult.failure(
        taskId: task.id,
        agentId: agentId,
        error: e.toString(),
        executionTime: executionTime,
      );
    }
  }
  
  Future<AgentResult> _generateCommitMessage(AgentTask task, DateTime startTime) async {
    final diff = task.parameters['diff'] as String?;
    if (diff == null) {
      throw Exception('Missing parameter: diff');
    }
    
    // Simulate commit message generation
    await Future.delayed(const Duration(milliseconds: 400));
    
    // Analyze diff to generate compact message
    final message = _analyzeAndGenerateMessage(diff);
    
    final executionTime = DateTime.now().difference(startTime);
    return AgentResult.success(
      taskId: task.id,
      agentId: agentId,
      output: {
        'commit_message': message,
        'type': _detectCommitType(diff),
        'scope': _detectScope(diff),
      },
      executionTime: executionTime,
      metadata: {
        'diff_size': diff.length,
        'lines_changed': diff.split('\n').length,
      },
    );
  }
  
  Future<AgentResult> _reviewPullRequest(AgentTask task, DateTime startTime) async {
    final prData = task.parameters['prData'] as Map<String, dynamic>?;
    if (prData == null) {
      throw Exception('Missing parameter: prData');
    }
    
    // Simulate PR review
    await Future.delayed(const Duration(seconds: 1));
    
    final review = {
      'summary': 'Overall changes look good with minor suggestions',
      'comments': [
        {
          'file': 'lib/main.dart',
          'line': 42,
          'severity': 'suggestion',
          'comment': 'Consider extracting this logic into a separate method',
        },
        {
          'file': 'lib/utils/helper.dart',
          'line': 15,
          'severity': 'warning',
          'comment': 'Add null safety check here',
        },
      ],
      'approval': 'approved_with_suggestions',
      'score': 8.5,
    };
    
    final executionTime = DateTime.now().difference(startTime);
    return AgentResult.success(
      taskId: task.id,
      agentId: agentId,
      output: review,
      executionTime: executionTime,
      metadata: {
        'pr_number': prData['number'],
        'files_reviewed': prData['changed_files'] ?? 0,
      },
    );
  }
  
  Future<AgentResult> _generateChangelogEntry(AgentTask task, DateTime startTime) async {
    final changes = task.parameters['changes'] as List<dynamic>?;
    if (changes == null) {
      throw Exception('Missing parameter: changes');
    }
    
    // Simulate changelog generation
    await Future.delayed(const Duration(milliseconds: 300));
    
    final entry = _formatChangelogEntry(changes);
    
    final executionTime = DateTime.now().difference(startTime);
    return AgentResult.success(
      taskId: task.id,
      agentId: agentId,
      output: {
        'changelog_entry': entry,
        'version': '1.0.0',
        'date': DateTime.now().toIso8601String().split('T')[0],
      },
      executionTime: executionTime,
    );
  }
  
  Future<AgentResult> _suggestTests(AgentTask task, DateTime startTime) async {
    final code = task.parameters['code'] as String?;
    if (code == null) {
      throw Exception('Missing parameter: code');
    }
    
    // Simulate test suggestion
    await Future.delayed(const Duration(milliseconds: 500));
    
    final suggestions = [
      'Add unit test for main function logic',
      'Add edge case test for null inputs',
      'Add integration test for full flow',
      'Add test for error handling',
    ];
    
    final executionTime = DateTime.now().difference(startTime);
    return AgentResult.success(
      taskId: task.id,
      agentId: agentId,
      output: {
        'test_suggestions': suggestions,
        'coverage_gaps': ['error_handling', 'edge_cases'],
        'priority': 'high',
      },
      executionTime: executionTime,
    );
  }
  
  Future<AgentResult> _checkCodeQuality(AgentTask task, DateTime startTime) async {
    final files = task.parameters['files'] as List<dynamic>?;
    if (files == null) {
      throw Exception('Missing parameter: files');
    }
    
    // Simulate quality check
    await Future.delayed(const Duration(milliseconds: 600));
    
    final qualityReport = {
      'overall_score': 8.7,
      'maintainability': 9.0,
      'reliability': 8.5,
      'security': 8.8,
      'issues': [
        {
          'type': 'code_smell',
          'severity': 'minor',
          'message': 'Function too long',
          'file': files.first,
        },
      ],
      'suggestions': [
        'Reduce cyclomatic complexity',
        'Add more documentation',
      ],
    };
    
    final executionTime = DateTime.now().difference(startTime);
    return AgentResult.success(
      taskId: task.id,
      agentId: agentId,
      output: qualityReport,
      executionTime: executionTime,
      metadata: {
        'files_checked': files.length,
      },
    );
  }
  
  String _analyzeAndGenerateMessage(String diff) {
    // Simple analysis - in real app, use more sophisticated parsing
    if (diff.contains('feat:') || diff.contains('new ')) {
      return 'feat: Add new functionality';
    } else if (diff.contains('fix:') || diff.contains('bug')) {
      return 'fix: Resolve issue';
    } else if (diff.contains('docs:') || diff.contains('README')) {
      return 'docs: Update documentation';
    } else if (diff.contains('test:')) {
      return 'test: Add tests';
    }
    return 'chore: Update code';
  }
  
  String _detectCommitType(String diff) {
    if (diff.contains('feat:')) return 'feat';
    if (diff.contains('fix:')) return 'fix';
    if (diff.contains('docs:')) return 'docs';
    if (diff.contains('test:')) return 'test';
    return 'chore';
  }
  
  String _detectScope(String diff) {
    if (diff.contains('lib/agents/')) return 'agents';
    if (diff.contains('lib/services/')) return 'services';
    if (diff.contains('lib/models/')) return 'models';
    return 'core';
  }
  
  String _formatChangelogEntry(List<dynamic> changes) {
    final buffer = StringBuffer();
    buffer.writeln('## [1.0.0] - ${DateTime.now().toIso8601String().split('T')[0]}');
    buffer.writeln();
    
    final features = changes.where((c) => c.toString().startsWith('feat')).toList();
    final fixes = changes.where((c) => c.toString().startsWith('fix')).toList();
    
    if (features.isNotEmpty) {
      buffer.writeln('### Added');
      for (var feat in features) {
        buffer.writeln('- $feat');
      }
      buffer.writeln();
    }
    
    if (fixes.isNotEmpty) {
      buffer.writeln('### Fixed');
      for (var fix in fixes) {
        buffer.writeln('- $fix');
      }
    }
    
    return buffer.toString();
  }
  
  @override
  Future<bool> onHealthCheck() async {
    return true; // GitHub token is optional
  }
}
