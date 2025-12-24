import React, { useEffect, useState } from 'react';
import './AgentDashboard.css';

interface Agent {
  id: string;
  name: string;
  role: string;
  model: string;
  specialties: string[];
  personality_emoji: string;
  status: string;
  total_tasks_completed: number;
  total_tokens_used: number;
  success_rate: number;
}

interface AgentStats {
  total_tasks: number;
  completed_tasks: number;
  failed_tasks: number;
  total_tokens: number;
  total_cost: number;
  avg_duration_ms: number;
  success_rate: number;
}

/**
 * AgentDashboard - Main dashboard displaying all Tokyo-IA agents
 * 
 * Features:
 * - Real-time agent status
 * - Performance metrics and charts
 * - Task history
 * - Cost tracking
 */
export const AgentDashboard: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080/api';

  useEffect(() => {
    fetchAgents();
    // Refresh every 30 seconds
    const interval = setInterval(fetchAgents, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/agents`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const data = await response.json();
      setAgents(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch agents');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading agents...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <h2>❌ Error</h2>
        <p>{error}</p>
        <button onClick={fetchAgents}>Retry</button>
      </div>
    );
  }

  return (
    <div className="agent-dashboard">
      <header className="dashboard-header">
        <h1>🗼 Tokyo-IA Agent Dashboard</h1>
        <button onClick={fetchAgents} className="refresh-btn">
          🔄 Refresh
        </button>
      </header>

      <div className="dashboard-stats">
        <StatCard
          label="Total Agents"
          value={agents.length}
          icon="🤖"
        />
        <StatCard
          label="Active Agents"
          value={agents.filter(a => a.status === 'active').length}
          icon="✅"
        />
        <StatCard
          label="Total Tasks"
          value={agents.reduce((sum, a) => sum + a.total_tasks_completed, 0)}
          icon="📋"
        />
        <StatCard
          label="Total Tokens"
          value={formatNumber(agents.reduce((sum, a) => sum + a.total_tokens_used, 0))}
          icon="🎫"
        />
      </div>

      <div className="agents-grid">
        {agents.map(agent => (
          <AgentCard key={agent.id} agent={agent} />
        ))}
      </div>
    </div>
  );
};

interface AgentCardProps {
  agent: Agent;
}

const AgentCard: React.FC<AgentCardProps> = ({ agent }) => {
  const [stats, setStats] = useState<AgentStats | null>(null);
  const [expanded, setExpanded] = useState(false);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080/api';

  const loadStats = async () => {
    if (stats) return; // Already loaded
    
    try {
      const response = await fetch(`${API_BASE_URL}/agents/${agent.id}/stats`);
      const data = await response.json();
      setStats(data);
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  };

  const handleToggle = () => {
    if (!expanded) {
      loadStats();
    }
    setExpanded(!expanded);
  };

  return (
    <div className={`agent-card ${agent.status}`}>
      <div className="agent-header" onClick={handleToggle}>
        <div className="agent-info">
          <span className="agent-emoji">{agent.personality_emoji}</span>
          <div>
            <h3>{agent.name}</h3>
            <p className="agent-role">{agent.role}</p>
          </div>
        </div>
        <span className={`status-badge ${agent.status}`}>
          {agent.status.toUpperCase()}
        </span>
      </div>

      <div className="agent-metrics">
        <Metric label="Tasks" value={agent.total_tasks_completed} />
        <Metric label="Tokens" value={formatNumber(agent.total_tokens_used)} />
        <Metric label="Success" value={`${agent.success_rate.toFixed(1)}%`} />
      </div>

      {expanded && (
        <div className="agent-details">
          <div className="agent-model">
            <strong>Model:</strong> {agent.model}
          </div>
          <div className="agent-specialties">
            <strong>Specialties:</strong>
            <div className="specialties-tags">
              {agent.specialties.map(s => (
                <span key={s} className="specialty-tag">{s}</span>
              ))}
            </div>
          </div>
          {stats && (
            <div className="agent-stats">
              <h4>Detailed Statistics</h4>
              <div className="stats-grid">
                <div>Completed: {stats.completed_tasks}</div>
                <div>Failed: {stats.failed_tasks}</div>
                <div>Avg Duration: {stats.avg_duration_ms.toFixed(0)}ms</div>
                <div>Total Cost: ${stats.total_cost.toFixed(4)}</div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

interface StatCardProps {
  label: string;
  value: number | string;
  icon: string;
}

const StatCard: React.FC<StatCardProps> = ({ label, value, icon }) => (
  <div className="stat-card">
    <span className="stat-icon">{icon}</span>
    <div>
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  </div>
);

interface MetricProps {
  label: string;
  value: number | string;
}

const Metric: React.FC<MetricProps> = ({ label, value }) => (
  <div className="metric">
    <div className="metric-value">{value}</div>
    <div className="metric-label">{label}</div>
  </div>
);

function formatNumber(num: number): string {
  if (num >= 1_000_000) return `${(num / 1_000_000).toFixed(1)}M`;
  if (num >= 1_000) return `${(num / 1_000).toFixed(1)}K`;
  return num.toString();
}

export default AgentDashboard;
