/// Agent_Sentiment - Multimodal Sentiment Analysis
library;

import 'dart:async';
import '../models/agent_task.dart';
import '../models/agent_result.dart';
import '../utils/constants.dart';
import 'agent_base.dart';

/// Agent_Sentiment: Analyzes mood multimodally and adapts responses
/// ID: agent-sentiment-004
/// Role: Text, voice, and image sentiment analysis, response adaptation
/// APIs: Gemini Multimodal, Speech-to-text, Vision API
class AgentSentiment extends AgentBase {
  String? _geminiApiKey;
  
  AgentSentiment()
      : super(
          agentId: AppConstants.agentSentimentId,
          name: AppConstants.agentSentimentName,
          emoji: AppConstants.agentSentimentEmoji,
        );
  
  @override
  Future<void> onInitialize() async {
    _geminiApiKey = const String.fromEnvironment('GEMINI_API_KEY', defaultValue: '');
  }
  
  @override
  Future<AgentResult> onExecuteTask(AgentTask task) async {
    final startTime = DateTime.now();
    
    try {
      switch (task.action) {
        case 'analyzeText':
          return await _analyzeText(task, startTime);
        case 'analyzeVoice':
          return await _analyzeVoice(task, startTime);
        case 'analyzeImage':
          return await _analyzeImage(task, startTime);
        case 'adaptResponse':
          return await _adaptResponse(task, startTime);
        case 'detectEmotion':
          return await _detectEmotion(task, startTime);
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
  
  Future<AgentResult> _analyzeText(AgentTask task, DateTime startTime) async {
    final text = task.parameters['text'] as String?;
    if (text == null) {
      throw Exception('Missing parameter: text');
    }
    
    // Simulate sentiment analysis
    await Future.delayed(const Duration(milliseconds: 400));
    
    final sentiment = _calculateSentiment(text);
    
    final executionTime = DateTime.now().difference(startTime);
    return AgentResult.success(
      taskId: task.id,
      agentId: agentId,
      output: {
        'sentiment': sentiment,
        'score': sentiment == 'positive' ? 0.8 : (sentiment == 'negative' ? -0.7 : 0.0),
        'emotions': _detectEmotionsFromText(text),
        'text': text,
      },
      executionTime: executionTime,
      metadata: {
        'api': 'gemini-multimodal',
        'text_length': text.length,
      },
    );
  }
  
  Future<AgentResult> _analyzeVoice(AgentTask task, DateTime startTime) async {
    final audioData = task.parameters['audioData'];
    if (audioData == null) {
      throw Exception('Missing parameter: audioData');
    }
    
    // Simulate voice analysis
    await Future.delayed(const Duration(milliseconds: 600));
    
    final executionTime = DateTime.now().difference(startTime);
    return AgentResult.success(
      taskId: task.id,
      agentId: agentId,
      output: {
        'tone': 'calm',
        'energy': 0.6,
        'emotion': 'content',
        'confidence': 0.85,
      },
      executionTime: executionTime,
      metadata: {
        'api': 'speech-to-text-analysis',
      },
    );
  }
  
  Future<AgentResult> _analyzeImage(AgentTask task, DateTime startTime) async {
    final imageData = task.parameters['imageData'];
    if (imageData == null) {
      throw Exception('Missing parameter: imageData');
    }
    
    // Simulate facial expression analysis
    await Future.delayed(const Duration(milliseconds: 700));
    
    final executionTime = DateTime.now().difference(startTime);
    return AgentResult.success(
      taskId: task.id,
      agentId: agentId,
      output: {
        'expression': 'happy',
        'confidence': 0.92,
        'emotions': {
          'happy': 0.92,
          'neutral': 0.06,
          'surprised': 0.02,
        },
      },
      executionTime: executionTime,
      metadata: {
        'api': 'vision-api',
      },
    );
  }
  
  Future<AgentResult> _adaptResponse(AgentTask task, DateTime startTime) async {
    final message = task.parameters['message'] as String?;
    final sentiment = task.parameters['sentiment'] as String?;
    
    if (message == null || sentiment == null) {
      throw Exception('Missing parameters: message and sentiment required');
    }
    
    // Simulate response adaptation
    await Future.delayed(const Duration(milliseconds: 300));
    
    String adaptedMessage = message;
    if (sentiment == 'negative') {
      adaptedMessage = '😊 I understand this might be frustrating. $message';
    } else if (sentiment == 'positive') {
      adaptedMessage = '✨ Great! $message';
    }
    
    final executionTime = DateTime.now().difference(startTime);
    return AgentResult.success(
      taskId: task.id,
      agentId: agentId,
      output: {
        'original_message': message,
        'adapted_message': adaptedMessage,
        'sentiment': sentiment,
        'adaptation_applied': true,
      },
      executionTime: executionTime,
    );
  }
  
  Future<AgentResult> _detectEmotion(AgentTask task, DateTime startTime) async {
    final multimodalData = task.parameters['multimodalData'] as Map<String, dynamic>?;
    if (multimodalData == null) {
      throw Exception('Missing parameter: multimodalData');
    }
    
    // Simulate multimodal emotion detection
    await Future.delayed(const Duration(milliseconds: 800));
    
    final executionTime = DateTime.now().difference(startTime);
    return AgentResult.success(
      taskId: task.id,
      agentId: agentId,
      output: {
        'primary_emotion': 'happy',
        'confidence': 0.88,
        'emotions': {
          'happy': 0.88,
          'excited': 0.08,
          'neutral': 0.04,
        },
        'modalities_analyzed': multimodalData.keys.toList(),
      },
      executionTime: executionTime,
      metadata: {
        'api': 'gemini-multimodal',
      },
    );
  }
  
  String _calculateSentiment(String text) {
    final lowerText = text.toLowerCase();
    final positiveWords = ['good', 'great', 'excellent', 'happy', 'love', 'wonderful'];
    final negativeWords = ['bad', 'terrible', 'awful', 'sad', 'hate', 'horrible'];
    
    int positiveCount = positiveWords.where((word) => lowerText.contains(word)).length;
    int negativeCount = negativeWords.where((word) => lowerText.contains(word)).length;
    
    if (positiveCount > negativeCount) return 'positive';
    if (negativeCount > positiveCount) return 'negative';
    return 'neutral';
  }
  
  List<String> _detectEmotionsFromText(String text) {
    final emotions = <String>[];
    final lowerText = text.toLowerCase();
    
    if (lowerText.contains('happy') || lowerText.contains('joy')) emotions.add('joy');
    if (lowerText.contains('sad') || lowerText.contains('unhappy')) emotions.add('sadness');
    if (lowerText.contains('angry') || lowerText.contains('mad')) emotions.add('anger');
    if (lowerText.contains('fear') || lowerText.contains('scared')) emotions.add('fear');
    
    return emotions.isEmpty ? ['neutral'] : emotions;
  }
  
  @override
  Future<bool> onHealthCheck() async {
    return _geminiApiKey != null && _geminiApiKey!.isNotEmpty;
  }
}
