// Package registry provides database operations for the Tokyo-IA agent orchestration system.
package registry

import (
	"context"
	"database/sql"
	"fmt"
	"time"

	"github.com/google/uuid"
	_ "github.com/lib/pq"
)

// Registry manages all database operations for agents, tasks, and workflows.
type Registry struct {
	db *sql.DB
}

// NewRegistry creates a new Registry instance with the given database connection string.
func NewRegistry(dbURL string) (*Registry, error) {
	db, err := sql.Open("postgres", dbURL)
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %w", err)
	}

	// Test connection
	if err := db.Ping(); err != nil {
		return nil, fmt.Errorf("failed to ping database: %w", err)
	}

	// Set connection pool settings
	db.SetMaxOpenConns(25)
	db.SetMaxIdleConns(5)
	db.SetConnMaxLifetime(5 * time.Minute)

	return &Registry{db: db}, nil
}

// Close closes the database connection.
func (r *Registry) Close() error {
	return r.db.Close()
}

// Agent Operations

// GetAllAgents retrieves all agents from the database.
func (r *Registry) GetAllAgents(ctx context.Context) ([]Agent, error) {
	query := `
		SELECT id, name, role, model, specialties, backstory, personality_emoji,
		       status, total_tasks_completed, total_tokens_used, average_latency_ms,
		       success_rate, created_at, updated_at, metadata
		FROM agents
		ORDER BY name
	`

	rows, err := r.db.QueryContext(ctx, query)
	if err != nil {
		return nil, fmt.Errorf("failed to query agents: %w", err)
	}
	defer rows.Close()

	var agents []Agent
	for rows.Next() {
		var agent Agent
		err := rows.Scan(
			&agent.ID, &agent.Name, &agent.Role, &agent.Model, &agent.Specialties,
			&agent.Backstory, &agent.PersonalityEmoji, &agent.Status,
			&agent.TotalTasksCompleted, &agent.TotalTokensUsed, &agent.AverageLatencyMs,
			&agent.SuccessRate, &agent.CreatedAt, &agent.UpdatedAt, &agent.Metadata,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan agent: %w", err)
		}
		agents = append(agents, agent)
	}

	return agents, rows.Err()
}

// GetAgentByID retrieves a single agent by ID.
func (r *Registry) GetAgentByID(ctx context.Context, agentID string) (*Agent, error) {
	query := `
		SELECT id, name, role, model, specialties, backstory, personality_emoji,
		       status, total_tasks_completed, total_tokens_used, average_latency_ms,
		       success_rate, created_at, updated_at, metadata
		FROM agents
		WHERE id = $1
	`

	var agent Agent
	err := r.db.QueryRowContext(ctx, query, agentID).Scan(
		&agent.ID, &agent.Name, &agent.Role, &agent.Model, &agent.Specialties,
		&agent.Backstory, &agent.PersonalityEmoji, &agent.Status,
		&agent.TotalTasksCompleted, &agent.TotalTokensUsed, &agent.AverageLatencyMs,
		&agent.SuccessRate, &agent.CreatedAt, &agent.UpdatedAt, &agent.Metadata,
	)
	if err == sql.ErrNoRows {
		return nil, fmt.Errorf("agent not found: %s", agentID)
	}
	if err != nil {
		return nil, fmt.Errorf("failed to get agent: %w", err)
	}

	return &agent, nil
}

// GetAgentStats retrieves statistics for a specific agent.
func (r *Registry) GetAgentStats(ctx context.Context, agentID string) (*AgentStats, error) {
	query := `
		SELECT id, name, role, status, total_tasks, completed_tasks, failed_tasks,
		       total_tokens, total_cost, avg_duration_ms, success_rate
		FROM agent_stats
		WHERE id = $1
	`

	var stats AgentStats
	err := r.db.QueryRowContext(ctx, query, agentID).Scan(
		&stats.ID, &stats.Name, &stats.Role, &stats.Status,
		&stats.TotalTasks, &stats.CompletedTasks, &stats.FailedTasks,
		&stats.TotalTokens, &stats.TotalCost, &stats.AvgDurationMs,
		&stats.SuccessRate,
	)
	if err == sql.ErrNoRows {
		return nil, fmt.Errorf("agent stats not found: %s", agentID)
	}
	if err != nil {
		return nil, fmt.Errorf("failed to get agent stats: %w", err)
	}

	return &stats, nil
}

// Workflow Operations

// CreateWorkflow creates a new workflow.
func (r *Registry) CreateWorkflow(ctx context.Context, req CreateWorkflowRequest) (*Workflow, error) {
	query := `
		INSERT INTO workflows (name, description, workflow_type, initiator, metadata)
		VALUES ($1, $2, $3, $4, $5)
		RETURNING id, name, description, status, workflow_type, initiator,
		          total_tasks, completed_tasks, failed_tasks, started_at, completed_at,
		          duration_ms, total_tokens_used, total_cost_usd, created_at, updated_at, metadata
	`

	metadata := JSONB(req.Metadata)
	var workflow Workflow
	err := r.db.QueryRowContext(ctx, query,
		req.Name, req.Description, req.WorkflowType, req.Initiator, metadata,
	).Scan(
		&workflow.ID, &workflow.Name, &workflow.Description, &workflow.Status,
		&workflow.WorkflowType, &workflow.Initiator, &workflow.TotalTasks,
		&workflow.CompletedTasks, &workflow.FailedTasks, &workflow.StartedAt,
		&workflow.CompletedAt, &workflow.DurationMs, &workflow.TotalTokensUsed,
		&workflow.TotalCostUsd, &workflow.CreatedAt, &workflow.UpdatedAt, &workflow.Metadata,
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create workflow: %w", err)
	}

	return &workflow, nil
}

// GetAllWorkflows retrieves all workflows.
func (r *Registry) GetAllWorkflows(ctx context.Context, limit int) ([]Workflow, error) {
	if limit <= 0 {
		limit = 50
	}

	query := `
		SELECT id, name, description, status, workflow_type, initiator,
		       total_tasks, completed_tasks, failed_tasks, started_at, completed_at,
		       duration_ms, total_tokens_used, total_cost_usd, created_at, updated_at, metadata
		FROM workflows
		ORDER BY created_at DESC
		LIMIT $1
	`

	rows, err := r.db.QueryContext(ctx, query, limit)
	if err != nil {
		return nil, fmt.Errorf("failed to query workflows: %w", err)
	}
	defer rows.Close()

	var workflows []Workflow
	for rows.Next() {
		var wf Workflow
		err := rows.Scan(
			&wf.ID, &wf.Name, &wf.Description, &wf.Status, &wf.WorkflowType,
			&wf.Initiator, &wf.TotalTasks, &wf.CompletedTasks, &wf.FailedTasks,
			&wf.StartedAt, &wf.CompletedAt, &wf.DurationMs, &wf.TotalTokensUsed,
			&wf.TotalCostUsd, &wf.CreatedAt, &wf.UpdatedAt, &wf.Metadata,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan workflow: %w", err)
		}
		workflows = append(workflows, wf)
	}

	return workflows, rows.Err()
}

// GetWorkflowByID retrieves a specific workflow by ID.
func (r *Registry) GetWorkflowByID(ctx context.Context, workflowID uuid.UUID) (*Workflow, error) {
	query := `
		SELECT id, name, description, status, workflow_type, initiator,
		       total_tasks, completed_tasks, failed_tasks, started_at, completed_at,
		       duration_ms, total_tokens_used, total_cost_usd, created_at, updated_at, metadata
		FROM workflows
		WHERE id = $1
	`

	var wf Workflow
	err := r.db.QueryRowContext(ctx, query, workflowID).Scan(
		&wf.ID, &wf.Name, &wf.Description, &wf.Status, &wf.WorkflowType,
		&wf.Initiator, &wf.TotalTasks, &wf.CompletedTasks, &wf.FailedTasks,
		&wf.StartedAt, &wf.CompletedAt, &wf.DurationMs, &wf.TotalTokensUsed,
		&wf.TotalCostUsd, &wf.CreatedAt, &wf.UpdatedAt, &wf.Metadata,
	)
	if err == sql.ErrNoRows {
		return nil, fmt.Errorf("workflow not found: %s", workflowID)
	}
	if err != nil {
		return nil, fmt.Errorf("failed to get workflow: %w", err)
	}

	return &wf, nil
}

// Task Operations

// CreateTask creates a new agent task.
func (r *Registry) CreateTask(ctx context.Context, req CreateTaskRequest) (*AgentTask, error) {
	query := `
		INSERT INTO agent_tasks (agent_id, workflow_id, task_type, description, input_data)
		VALUES ($1, $2, $3, $4, $5)
		RETURNING id, agent_id, workflow_id, task_type, description, status,
		          input_data, output_data, error_message, started_at, completed_at,
		          duration_ms, tokens_used, cost_usd, retry_count, parent_task_id,
		          created_at, metadata
	`

	inputData := JSONB(req.InputData)
	var task AgentTask
	err := r.db.QueryRowContext(ctx, query,
		req.AgentID, req.WorkflowID, req.TaskType, req.Description, inputData,
	).Scan(
		&task.ID, &task.AgentID, &task.WorkflowID, &task.TaskType, &task.Description,
		&task.Status, &task.InputData, &task.OutputData, &task.ErrorMessage,
		&task.StartedAt, &task.CompletedAt, &task.DurationMs, &task.TokensUsed,
		&task.CostUsd, &task.RetryCount, &task.ParentTaskID, &task.CreatedAt, &task.Metadata,
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create task: %w", err)
	}

	return &task, nil
}

// UpdateTaskStatus updates the status and results of a task.
func (r *Registry) UpdateTaskStatus(ctx context.Context, taskID uuid.UUID, req UpdateTaskStatusRequest) error {
	now := time.Now()

	query := `
		UPDATE agent_tasks
		SET status = $1,
		    output_data = $2,
		    error_message = $3,
		    tokens_used = $4,
		    cost_usd = $5,
		    completed_at = $6
		WHERE id = $7
	`

	outputData := JSONB(req.OutputData)
	var completedAt *time.Time
	if req.Status == "completed" || req.Status == "failed" {
		completedAt = &now
	}

	_, err := r.db.ExecContext(ctx, query,
		req.Status, outputData, req.ErrorMessage, req.TokensUsed, req.CostUsd,
		completedAt, taskID,
	)
	if err != nil {
		return fmt.Errorf("failed to update task status: %w", err)
	}

	return nil
}

// GetTasksByAgent retrieves all tasks for a specific agent.
func (r *Registry) GetTasksByAgent(ctx context.Context, agentID string, limit int) ([]AgentTask, error) {
	if limit <= 0 {
		limit = 50
	}

	query := `
		SELECT id, agent_id, workflow_id, task_type, description, status,
		       input_data, output_data, error_message, started_at, completed_at,
		       duration_ms, tokens_used, cost_usd, retry_count, parent_task_id,
		       created_at, metadata
		FROM agent_tasks
		WHERE agent_id = $1
		ORDER BY created_at DESC
		LIMIT $2
	`

	rows, err := r.db.QueryContext(ctx, query, agentID, limit)
	if err != nil {
		return nil, fmt.Errorf("failed to query tasks: %w", err)
	}
	defer rows.Close()

	var tasks []AgentTask
	for rows.Next() {
		var task AgentTask
		err := rows.Scan(
			&task.ID, &task.AgentID, &task.WorkflowID, &task.TaskType, &task.Description,
			&task.Status, &task.InputData, &task.OutputData, &task.ErrorMessage,
			&task.StartedAt, &task.CompletedAt, &task.DurationMs, &task.TokensUsed,
			&task.CostUsd, &task.RetryCount, &task.ParentTaskID, &task.CreatedAt, &task.Metadata,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan task: %w", err)
		}
		tasks = append(tasks, task)
	}

	return tasks, rows.Err()
}

// GetTasksByWorkflow retrieves all tasks in a workflow.
func (r *Registry) GetTasksByWorkflow(ctx context.Context, workflowID uuid.UUID) ([]AgentTask, error) {
	query := `
		SELECT id, agent_id, workflow_id, task_type, description, status,
		       input_data, output_data, error_message, started_at, completed_at,
		       duration_ms, tokens_used, cost_usd, retry_count, parent_task_id,
		       created_at, metadata
		FROM agent_tasks
		WHERE workflow_id = $1
		ORDER BY created_at ASC
	`

	rows, err := r.db.QueryContext(ctx, query, workflowID)
	if err != nil {
		return nil, fmt.Errorf("failed to query workflow tasks: %w", err)
	}
	defer rows.Close()

	var tasks []AgentTask
	for rows.Next() {
		var task AgentTask
		err := rows.Scan(
			&task.ID, &task.AgentID, &task.WorkflowID, &task.TaskType, &task.Description,
			&task.Status, &task.InputData, &task.OutputData, &task.ErrorMessage,
			&task.StartedAt, &task.CompletedAt, &task.DurationMs, &task.TokensUsed,
			&task.CostUsd, &task.RetryCount, &task.ParentTaskID, &task.CreatedAt, &task.Metadata,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan task: %w", err)
		}
		tasks = append(tasks, task)
	}

	return tasks, rows.Err()
}

// RecordMetric records a performance metric for an agent.
func (r *Registry) RecordMetric(ctx context.Context, agentID string, metricType string, value float64, unit string, context map[string]interface{}) error {
	query := `
		INSERT INTO agent_metrics (agent_id, metric_type, metric_value, metric_unit, context)
		VALUES ($1, $2, $3, $4, $5)
	`

	ctx2 := JSONB(context)
	_, err := r.db.ExecContext(ctx, query, agentID, metricType, value, unit, ctx2)
	if err != nil {
		return fmt.Errorf("failed to record metric: %w", err)
	}

	return nil
}

// GetMetrics retrieves metrics for an agent within a time range.
func (r *Registry) GetMetrics(ctx context.Context, agentID string, metricType string, limit int) ([]AgentMetric, error) {
	if limit <= 0 {
		limit = 100
	}

	query := `
		SELECT id, agent_id, metric_type, metric_value, metric_unit, recorded_at, context
		FROM agent_metrics
		WHERE agent_id = $1 AND metric_type = $2
		ORDER BY recorded_at DESC
		LIMIT $3
	`

	rows, err := r.db.QueryContext(ctx, query, agentID, metricType, limit)
	if err != nil {
		return nil, fmt.Errorf("failed to query metrics: %w", err)
	}
	defer rows.Close()

	var metrics []AgentMetric
	for rows.Next() {
		var metric AgentMetric
		err := rows.Scan(
			&metric.ID, &metric.AgentID, &metric.MetricType, &metric.MetricValue,
			&metric.MetricUnit, &metric.RecordedAt, &metric.Context,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan metric: %w", err)
		}
		metrics = append(metrics, metric)
	}

	return metrics, rows.Err()
}
