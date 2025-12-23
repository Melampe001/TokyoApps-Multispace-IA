/// Home Screen - Main entry screen
library;

import 'package:flutter/material.dart';
import '../services/agent_orchestrator.dart';
import '../utils/constants.dart';
import 'agents_dashboard_screen.dart';
import 'chat_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final AgentOrchestrator _orchestrator = AgentOrchestrator();
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🗼 Tokyo-IA'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [
          IconButton(
            icon: const Icon(Icons.dashboard),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const AgentsDashboardScreen(),
                ),
              );
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Welcome message
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Welcome to Tokyo-IA',
                      style: Theme.of(context).textTheme.headlineSmall,
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      '7 Autonomous AI Agents at Your Service',
                      style: TextStyle(color: Colors.grey),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            
            // Agents grid
            Text(
              'Agents',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            GridView.count(
              crossAxisCount: 2,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              mainAxisSpacing: 12,
              crossAxisSpacing: 12,
              children: [
                _buildAgentCard(
                  emoji: AppConstants.agentCodeMasterEmoji,
                  name: AppConstants.agentCodeMasterName,
                  description: 'Code generation & review',
                  color: Colors.blue,
                ),
                _buildAgentCard(
                  emoji: AppConstants.agentGenAiEmoji,
                  name: AppConstants.agentGenAiName,
                  description: 'Image, video & music',
                  color: Colors.purple,
                ),
                _buildAgentCard(
                  emoji: AppConstants.agentKnowledgeEmoji,
                  name: AppConstants.agentKnowledgeName,
                  description: 'RAG & web search',
                  color: Colors.green,
                ),
                _buildAgentCard(
                  emoji: AppConstants.agentSentimentEmoji,
                  name: AppConstants.agentSentimentName,
                  description: 'Sentiment analysis',
                  color: Colors.orange,
                ),
                _buildAgentCard(
                  emoji: AppConstants.agentUnrestrictedEmoji,
                  name: AppConstants.agentUnrestrictedName,
                  description: 'Unrestricted mode',
                  color: Colors.red,
                ),
                _buildAgentCard(
                  emoji: AppConstants.agentQaEmoji,
                  name: AppConstants.agentQaName,
                  description: 'Quality assurance',
                  color: Colors.teal,
                ),
                _buildAgentCard(
                  emoji: AppConstants.agentDeployEmoji,
                  name: AppConstants.agentDeployName,
                  description: 'Build & deployment',
                  color: Colors.indigo,
                ),
              ],
            ),
            const SizedBox(height: 24),
            
            // Quick actions
            Text(
              'Quick Actions',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            _buildQuickAction(
              icon: Icons.chat,
              title: 'Start Chat',
              description: 'Chat with AI agents',
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const ChatScreen(),
                  ),
                );
              },
            ),
            _buildQuickAction(
              icon: Icons.dashboard,
              title: 'Agents Dashboard',
              description: 'Monitor all agents',
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const AgentsDashboardScreen(),
                  ),
                );
              },
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => const ChatScreen(),
            ),
          );
        },
        child: const Icon(Icons.chat),
      ),
    );
  }
  
  Widget _buildAgentCard({
    required String emoji,
    required String name,
    required String description,
    required Color color,
  }) {
    return Card(
      color: color.withOpacity(0.1),
      child: InkWell(
        onTap: () {
          // Navigate to agent details
        },
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                emoji,
                style: const TextStyle(fontSize: 32),
              ),
              const SizedBox(height: 8),
              Text(
                name,
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 16,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                description,
                style: const TextStyle(
                  fontSize: 12,
                  color: Colors.grey,
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
  
  Widget _buildQuickAction({
    required IconData icon,
    required String title,
    required String description,
    required VoidCallback onTap,
  }) {
    return Card(
      child: ListTile(
        leading: Icon(icon, size: 32),
        title: Text(title),
        subtitle: Text(description),
        trailing: const Icon(Icons.chevron_right),
        onTap: onTap,
      ),
    );
  }
}
