/// Agents Dashboard Screen - Monitor all agents
library;

import 'package:flutter/material.dart';
import '../services/agent_orchestrator.dart';
import '../models/agent_log.dart';
import '../utils/constants.dart';

class AgentsDashboardScreen extends StatefulWidget {
  const AgentsDashboardScreen({super.key});
  
  @override
  State<AgentsDashboardScreen> createState() => _AgentsDashboardScreenState();
}

class _AgentsDashboardScreenState extends State<AgentsDashboardScreen> {
  final AgentOrchestrator _orchestrator = AgentOrchestrator();
  Map<String, AgentHealthStatus>? _healthStatuses;
  bool _isLoadingHealth = false;
  
  @override
  void initState() {
    super.initState();
    _checkHealth();
  }
  
  Future<void> _checkHealth() async {
    setState(() {
      _isLoadingHealth = true;
    });
    
    final statuses = await _orchestrator.checkAllAgentsHealth();
    
    setState(() {
      _healthStatuses = statuses;
      _isLoadingHealth = false;
    });
  }
  
  @override
  Widget build(BuildContext context) {
    final agentsMetadata = _orchestrator.getAllAgentsMetadata();
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('Agents Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _checkHealth,
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _checkHealth,
        child: ListView(
          padding: const EdgeInsets.all(16.0),
          children: [
            // Summary card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'System Overview',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        _buildStatItem(
                          label: 'Total Agents',
                          value: agentsMetadata.length.toString(),
                          icon: Icons.smart_toy,
                        ),
                        _buildStatItem(
                          label: 'Healthy',
                          value: _healthStatuses?.values
                                  .where((s) => s.healthy)
                                  .length
                                  .toString() ??
                              '...',
                          icon: Icons.check_circle,
                          color: Colors.green,
                        ),
                        _buildStatItem(
                          label: 'Issues',
                          value: _healthStatuses?.values
                                  .where((s) => !s.healthy)
                                  .length
                                  .toString() ??
                              '...',
                          icon: Icons.error,
                          color: Colors.red,
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            
            // Agents list
            Text(
              'Agents Status',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 8),
            
            ...agentsMetadata.entries.map((entry) {
              final agentId = entry.key;
              final metadata = entry.value;
              final healthStatus = _healthStatuses?[agentId];
              
              return _buildAgentCard(
                agentId: agentId,
                metadata: metadata,
                healthStatus: healthStatus,
              );
            }).toList(),
            
            const SizedBox(height: 16),
            
            // Logs section
            Text(
              'Recent Logs',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 8),
            _buildLogsSection(),
          ],
        ),
      ),
    );
  }
  
  Widget _buildStatItem({
    required String label,
    required String value,
    required IconData icon,
    Color? color,
  }) {
    return Column(
      children: [
        Icon(icon, size: 32, color: color),
        const SizedBox(height: 8),
        Text(
          value,
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
        Text(
          label,
          style: const TextStyle(
            fontSize: 12,
            color: Colors.grey,
          ),
        ),
      ],
    );
  }
  
  Widget _buildAgentCard({
    required String agentId,
    required Map<String, dynamic> metadata,
    AgentHealthStatus? healthStatus,
  }) {
    final name = metadata['name'] as String? ?? 'Unknown';
    final emoji = metadata['emoji'] as String? ?? '🤖';
    final status = metadata['status'] as String? ?? 'unknown';
    final tasksCompleted = metadata['tasks_completed'] as int? ?? 0;
    final tasksFailed = metadata['tasks_failed'] as int? ?? 0;
    final isHealthy = healthStatus?.healthy ?? false;
    
    return Card(
      child: ExpansionTile(
        leading: Text(emoji, style: const TextStyle(fontSize: 24)),
        title: Text('$emoji $name'),
        subtitle: Text('Status: $status'),
        trailing: Icon(
          isHealthy ? Icons.check_circle : Icons.error,
          color: isHealthy ? Colors.green : Colors.red,
        ),
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildInfoRow('Agent ID', agentId),
                _buildInfoRow('Status', status),
                _buildInfoRow('Tasks Completed', tasksCompleted.toString()),
                _buildInfoRow('Tasks Failed', tasksFailed.toString()),
                if (metadata['last_active'] != null)
                  _buildInfoRow('Last Active', metadata['last_active']),
                if (healthStatus != null)
                  _buildInfoRow(
                    'Health Check',
                    healthStatus.healthy ? 'OK' : healthStatus.message ?? 'Failed',
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: const TextStyle(fontWeight: FontWeight.bold),
          ),
          Text(value),
        ],
      ),
    );
  }
  
  Widget _buildLogsSection() {
    return StreamBuilder<AgentLog>(
      stream: _orchestrator.logsStream,
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const Card(
            child: Padding(
              padding: EdgeInsets.all(16.0),
              child: Text('No logs yet'),
            ),
          );
        }
        
        final log = snapshot.data!;
        return Card(
          child: ListTile(
            leading: _getLogIcon(log.level),
            title: Text(log.message),
            subtitle: Text('${log.agentId} - ${log.timestamp}'),
            trailing: Icon(
              log.verified ? Icons.verified : Icons.warning,
              color: log.verified ? Colors.green : Colors.orange,
            ),
          ),
        );
      },
    );
  }
  
  Icon _getLogIcon(String level) {
    switch (level) {
      case LogLevel.debug:
        return const Icon(Icons.bug_report, color: Colors.grey);
      case LogLevel.info:
        return const Icon(Icons.info, color: Colors.blue);
      case LogLevel.warning:
        return const Icon(Icons.warning, color: Colors.orange);
      case LogLevel.error:
        return const Icon(Icons.error, color: Colors.red);
      case LogLevel.critical:
        return const Icon(Icons.error_outline, color: Colors.red);
      default:
        return const Icon(Icons.circle, color: Colors.grey);
    }
  }
}
