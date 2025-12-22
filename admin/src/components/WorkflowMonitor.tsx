import React, { useEffect, useState } from 'react';
import './WorkflowMonitor.css';

interface Workflow {
  id: string;
  name: string;
  description: string;
  status: string;
  workflow_type: string;
  initiator: string;
  total_tasks: number;
  completed_tasks: number;
  failed_tasks: number;
  started_at?: string;
  completed_at?: string;
  duration_ms?: number;
  total_tokens_used: number;
  total_cost_usd: number;
  created_at: string;
}

interface Task {
  id: string;
  agent_id: string;
  task_type: string;
  description: string;
  status: string;
  started_at?: string;
  completed_at?: string;
  duration_ms?: number;
  tokens_used: number;
  cost_usd: number;
}

/**
 * WorkflowMonitor - Real-time workflow execution monitoring
 * 
 * Features:
 * - Active workflow tracking
 * - Task progress visualization
 * - Timeline view
 * - Performance metrics
 */
export const WorkflowMonitor: React.FC = () => {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState<string | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080/api';

  useEffect(() => {
    fetchWorkflows();
    const interval = setInterval(fetchWorkflows, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (selectedWorkflow) {
      fetchWorkflowTasks(selectedWorkflow);
    }
  }, [selectedWorkflow]);

  const fetchWorkflows = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/workflows?limit=20`);
      const data = await response.json();
      setWorkflows(data);
      setLoading(false);
    } catch (err) {
      console.error('Failed to fetch workflows:', err);
      setLoading(false);
    }
  };

  const fetchWorkflowTasks = async (workflowId: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/workflows/${workflowId}/tasks`);
      const data = await response.json();
      setTasks(data);
    } catch (err) {
      console.error('Failed to fetch tasks:', err);
    }
  };

  if (loading) {
    return <div className="monitor-loading">Loading workflows...</div>;
  }

  const activeWorkflows = workflows.filter(w => w.status === 'running');
  const recentWorkflows = workflows.filter(w => w.status !== 'running').slice(0, 10);

  return (
    <div className="workflow-monitor">
      <header className="monitor-header">
        <h1>🔄 Workflow Monitor</h1>
        <button onClick={fetchWorkflows}>🔄 Refresh</button>
      </header>

      {activeWorkflows.length > 0 && (
        <section className="active-workflows">
          <h2>🟢 Active Workflows ({activeWorkflows.length})</h2>
          <div className="workflows-list">
            {activeWorkflows.map(workflow => (
              <WorkflowCard
                key={workflow.id}
                workflow={workflow}
                isSelected={selectedWorkflow === workflow.id}
                onClick={() => setSelectedWorkflow(workflow.id)}
              />
            ))}
          </div>
        </section>
      )}

      <section className="recent-workflows">
        <h2>📋 Recent Workflows</h2>
        <div className="workflows-list">
          {recentWorkflows.map(workflow => (
            <WorkflowCard
              key={workflow.id}
              workflow={workflow}
              isSelected={selectedWorkflow === workflow.id}
              onClick={() => setSelectedWorkflow(workflow.id)}
            />
          ))}
        </div>
      </section>

      {selectedWorkflow && (
        <section className="workflow-details">
          <h2>Tasks Timeline</h2>
          <div className="tasks-timeline">
            {tasks.map(task => (
              <TaskItem key={task.id} task={task} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
};

interface WorkflowCardProps {
  workflow: Workflow;
  isSelected: boolean;
  onClick: () => void;
}

const WorkflowCard: React.FC<WorkflowCardProps> = ({ workflow, isSelected, onClick }) => {
  const progress = workflow.total_tasks > 0
    ? (workflow.completed_tasks / workflow.total_tasks) * 100
    : 0;

  return (
    <div 
      className={`workflow-card ${workflow.status} ${isSelected ? 'selected' : ''}`}
      onClick={onClick}
    >
      <div className="workflow-header">
        <h3>{workflow.name}</h3>
        <span className={`status-badge ${workflow.status}`}>
          {workflow.status}
        </span>
      </div>

      <p className="workflow-description">{workflow.description}</p>

      <div className="workflow-progress">
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        <span className="progress-text">
          {workflow.completed_tasks} / {workflow.total_tasks} tasks
        </span>
      </div>

      <div className="workflow-metrics">
        <span>⏱️ {workflow.duration_ms ? `${(workflow.duration_ms / 1000).toFixed(1)}s` : 'In progress'}</span>
        <span>🎫 {workflow.total_tokens_used} tokens</span>
        <span>💰 ${workflow.total_cost_usd.toFixed(4)}</span>
      </div>

      <div className="workflow-footer">
        <span className="workflow-type">{workflow.workflow_type}</span>
        <span className="workflow-initiator">by {workflow.initiator}</span>
      </div>
    </div>
  );
};

interface TaskItemProps {
  task: Task;
}

const TaskItem: React.FC<TaskItemProps> = ({ task }) => {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return '✅';
      case 'running': return '⏳';
      case 'failed': return '❌';
      case 'pending': return '⏸️';
      default: return '📋';
    }
  };

  return (
    <div className={`task-item ${task.status}`}>
      <div className="task-status-icon">
        {getStatusIcon(task.status)}
      </div>
      <div className="task-content">
        <div className="task-header">
          <strong>{task.task_type}</strong>
          <span className="task-agent">{task.agent_id}</span>
        </div>
        <p className="task-description">{task.description}</p>
        <div className="task-metrics">
          {task.duration_ms && (
            <span>⏱️ {task.duration_ms}ms</span>
          )}
          {task.tokens_used > 0 && (
            <span>🎫 {task.tokens_used} tokens</span>
          )}
          {task.cost_usd > 0 && (
            <span>💰 ${task.cost_usd.toFixed(4)}</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default WorkflowMonitor;
