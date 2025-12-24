/// Chat Screen - Interact with agents
library;

import 'package:flutter/material.dart';
import '../services/agent_orchestrator.dart';
import '../models/agent_task.dart';
import '../utils/constants.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});
  
  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final AgentOrchestrator _orchestrator = AgentOrchestrator();
  final TextEditingController _messageController = TextEditingController();
  final List<ChatMessage> _messages = [];
  bool _isProcessing = false;
  String _selectedAgentId = AppConstants.agentCodeMasterId;
  
  @override
  void dispose() {
    _messageController.dispose();
    super.dispose();
  }
  
  Future<void> _sendMessage() async {
    final message = _messageController.text.trim();
    if (message.isEmpty || _isProcessing) return;
    
    setState(() {
      _messages.add(ChatMessage(
        text: message,
        isUser: true,
        timestamp: DateTime.now(),
      ));
      _isProcessing = true;
    });
    
    _messageController.clear();
    
    try {
      // Execute workflow based on message
      final workflow = _orchestrator.createSmartChatWorkflow(message);
      final results = await _orchestrator.executeWorkflow(workflow);
      
      // Get the last result as response
      final lastResult = results.last;
      final responseText = lastResult.output.toString();
      
      setState(() {
        _messages.add(ChatMessage(
          text: responseText,
          isUser: false,
          timestamp: DateTime.now(),
          agentId: _selectedAgentId,
        ));
      });
    } catch (e) {
      setState(() {
        _messages.add(ChatMessage(
          text: 'Error: $e',
          isUser: false,
          timestamp: DateTime.now(),
          isError: true,
        ));
      });
    } finally {
      setState(() {
        _isProcessing = false;
      });
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Chat with Agents'),
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.smart_toy),
            onSelected: (value) {
              setState(() {
                _selectedAgentId = value;
              });
            },
            itemBuilder: (context) => [
              PopupMenuItem(
                value: AppConstants.agentCodeMasterId,
                child: Text('${AppConstants.agentCodeMasterEmoji} CodeMaster'),
              ),
              PopupMenuItem(
                value: AppConstants.agentGenAiId,
                child: Text('${AppConstants.agentGenAiEmoji} GenAI'),
              ),
              PopupMenuItem(
                value: AppConstants.agentKnowledgeId,
                child: Text('${AppConstants.agentKnowledgeEmoji} Knowledge'),
              ),
              PopupMenuItem(
                value: AppConstants.agentSentimentId,
                child: Text('${AppConstants.agentSentimentEmoji} Sentiment'),
              ),
            ],
          ),
        ],
      ),
      body: Column(
        children: [
          // Messages list
          Expanded(
            child: _messages.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(
                          Icons.chat_bubble_outline,
                          size: 64,
                          color: Colors.grey,
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'Start chatting with AI agents',
                          style: Theme.of(context).textTheme.titleMedium,
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    padding: const EdgeInsets.all(16.0),
                    itemCount: _messages.length,
                    itemBuilder: (context, index) {
                      return _buildMessageBubble(_messages[index]);
                    },
                  ),
          ),
          
          // Input field
          if (_isProcessing)
            const LinearProgressIndicator(),
          
          Container(
            padding: const EdgeInsets.all(8.0),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surface,
              boxShadow: [
                BoxShadow(
                  offset: const Offset(0, -2),
                  blurRadius: 4,
                  color: Colors.black.withOpacity(0.1),
                ),
              ],
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    decoration: const InputDecoration(
                      hintText: 'Type a message...',
                      border: OutlineInputBorder(),
                      contentPadding: EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 12,
                      ),
                    ),
                    maxLines: null,
                    textInputAction: TextInputAction.send,
                    onSubmitted: (_) => _sendMessage(),
                    enabled: !_isProcessing,
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  icon: const Icon(Icons.send),
                  onPressed: _isProcessing ? null : _sendMessage,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _buildMessageBubble(ChatMessage message) {
    return Align(
      alignment: message.isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 8.0),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: BoxDecoration(
          color: message.isError
              ? Colors.red.withOpacity(0.1)
              : message.isUser
                  ? Theme.of(context).colorScheme.primary
                  : Colors.grey.shade200,
          borderRadius: BorderRadius.circular(16),
        ),
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.7,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (!message.isUser && message.agentId != null)
              Padding(
                padding: const EdgeInsets.only(bottom: 4.0),
                child: Text(
                  _getAgentName(message.agentId!),
                  style: const TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            Text(
              message.text,
              style: TextStyle(
                color: message.isUser ? Colors.white : Colors.black87,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              _formatTimestamp(message.timestamp),
              style: TextStyle(
                fontSize: 10,
                color: message.isUser
                    ? Colors.white.withOpacity(0.7)
                    : Colors.grey,
              ),
            ),
          ],
        ),
      ),
    );
  }
  
  String _getAgentName(String agentId) {
    switch (agentId) {
      case AppConstants.agentCodeMasterId:
        return '${AppConstants.agentCodeMasterEmoji} CodeMaster';
      case AppConstants.agentGenAiId:
        return '${AppConstants.agentGenAiEmoji} GenAI';
      case AppConstants.agentKnowledgeId:
        return '${AppConstants.agentKnowledgeEmoji} Knowledge';
      case AppConstants.agentSentimentId:
        return '${AppConstants.agentSentimentEmoji} Sentiment';
      default:
        return 'Agent';
    }
  }
  
  String _formatTimestamp(DateTime timestamp) {
    return '${timestamp.hour.toString().padLeft(2, '0')}:${timestamp.minute.toString().padLeft(2, '0')}';
  }
}

class ChatMessage {
  final String text;
  final bool isUser;
  final DateTime timestamp;
  final String? agentId;
  final bool isError;
  
  ChatMessage({
    required this.text,
    required this.isUser,
    required this.timestamp,
    this.agentId,
    this.isError = false,
  });
}
