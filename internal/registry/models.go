// Package registry provides data models for the Tokyo-IA agent orchestration system.
package registry

import (
	"database/sql/driver"
	"encoding/json"
	"time"

	"github.com/google/uuid"
	"github.com/lib/pq"
)

// Agent represents an AI agent in the system.
type Agent struct {
	ID                  string         `json:"id" db:"id"`
	Name                string         `json:"name" db:"name"`
	Role                string         `json:"role" db:"role"`
	Model               string         `json:"model" db:"model"`
	Specialties         pq.StringArray `json:"specialties" db:"specialties"`
	Backstory           string         `json:"backstory" db:"backstory"`
	PersonalityEmoji    string         `json:"personality_emoji" db:"personality_emoji"`
	Status              string         `json:"status" db:"status"`
	TotalTasksCompleted int            `json:"total_tasks_completed" db:"total_tasks_completed"`
	TotalTokensUsed     int64          `json:"total_tokens_used" db:"total_tokens_used"`
	AverageLatencyMs    float64        `json:"average_latency_ms" db:"average_latency_ms"`
	SuccessRate         float64        `json:"success_rate" db:"success_rate"`
	CreatedAt           time.Time      `json:"created_at" db:"created_at"`
	UpdatedAt           time.Time      `json:"updated_at" db:"updated_at"`
	Metadata            JSONB          `json:"metadata" db:"metadata"`
}

// Workflow represents a multi-agent workflow execution.
type Workflow struct {
	ID              uuid.UUID  `json:"id" db:"id"`
	Name            string     `json:"name" db:"name"`
	Description     string     `json:"description" db:"description"`
	Status          string     `json:"status" db:"status"`
	WorkflowType    string     `json:"workflow_type" db:"workflow_type"`
	Initiator       string     `json:"initiator" db:"initiator"`
	TotalTasks      int        `json:"total_tasks" db:"total_tasks"`
	CompletedTasks  int        `json:"completed_tasks" db:"completed_tasks"`
	FailedTasks     int        `json:"failed_tasks" db:"failed_tasks"`
	StartedAt       *time.Time `json:"started_at,omitempty" db:"started_at"`
	CompletedAt     *time.Time `json:"completed_at,omitempty" db:"completed_at"`
	DurationMs      *int       `json:"duration_ms,omitempty" db:"duration_ms"`
	TotalTokensUsed int        `json:"total_tokens_used" db:"total_tokens_used"`
	TotalCostUsd    float64    `json:"total_cost_usd" db:"total_cost_usd"`
	CreatedAt       time.Time  `json:"created_at" db:"created_at"`
	UpdatedAt       time.Time  `json:"updated_at" db:"updated_at"`
	Metadata        JSONB      `json:"metadata" db:"metadata"`
}

// AgentTask represents a single task executed by an agent.
type AgentTask struct {
	ID           uuid.UUID  `json:"id" db:"id"`
	AgentID      string     `json:"agent_id" db:"agent_id"`
	WorkflowID   *uuid.UUID `json:"workflow_id,omitempty" db:"workflow_id"`
	TaskType     string     `json:"task_type" db:"task_type"`
	Description  string     `json:"description" db:"description"`
	Status       string     `json:"status" db:"status"`
	InputData    JSONB      `json:"input_data,omitempty" db:"input_data"`
	OutputData   JSONB      `json:"output_data,omitempty" db:"output_data"`
	ErrorMessage *string    `json:"error_message,omitempty" db:"error_message"`
	StartedAt    *time.Time `json:"started_at,omitempty" db:"started_at"`
	CompletedAt  *time.Time `json:"completed_at,omitempty" db:"completed_at"`
	DurationMs   *int       `json:"duration_ms,omitempty" db:"duration_ms"`
	TokensUsed   int        `json:"tokens_used" db:"tokens_used"`
	CostUsd      float64    `json:"cost_usd" db:"cost_usd"`
	RetryCount   int        `json:"retry_count" db:"retry_count"`
	ParentTaskID *uuid.UUID `json:"parent_task_id,omitempty" db:"parent_task_id"`
	CreatedAt    time.Time  `json:"created_at" db:"created_at"`
	Metadata     JSONB      `json:"metadata" db:"metadata"`
}

// AgentMetric represents a performance metric for an agent.
type AgentMetric struct {
	ID          uuid.UUID `json:"id" db:"id"`
	AgentID     string    `json:"agent_id" db:"agent_id"`
	MetricType  string    `json:"metric_type" db:"metric_type"`
	MetricValue float64   `json:"metric_value" db:"metric_value"`
	MetricUnit  string    `json:"metric_unit" db:"metric_unit"`
	RecordedAt  time.Time `json:"recorded_at" db:"recorded_at"`
	Context     JSONB     `json:"context" db:"context"`
}

// AgentInteraction represents communication between agents.
type AgentInteraction struct {
	ID              uuid.UUID  `json:"id" db:"id"`
	WorkflowID      *uuid.UUID `json:"workflow_id,omitempty" db:"workflow_id"`
	FromAgentID     string     `json:"from_agent_id" db:"from_agent_id"`
	ToAgentID       string     `json:"to_agent_id" db:"to_agent_id"`
	InteractionType string     `json:"interaction_type" db:"interaction_type"`
	Message         string     `json:"message" db:"message"`
	Payload         JSONB      `json:"payload,omitempty" db:"payload"`
	CreatedAt       time.Time  `json:"created_at" db:"created_at"`
}

// UserSession represents a user session.
type UserSession struct {
	ID             uuid.UUID  `json:"id" db:"id"`
	UserID         string     `json:"user_id" db:"user_id"`
	SessionToken   string     `json:"session_token" db:"session_token"`
	DeviceInfo     JSONB      `json:"device_info,omitempty" db:"device_info"`
	IPAddress      *string    `json:"ip_address,omitempty" db:"ip_address"`
	StartedAt      time.Time  `json:"started_at" db:"started_at"`
	LastActivityAt time.Time  `json:"last_activity_at" db:"last_activity_at"`
	EndedAt        *time.Time `json:"ended_at,omitempty" db:"ended_at"`
	IsActive       bool       `json:"is_active" db:"is_active"`
	Metadata       JSONB      `json:"metadata" db:"metadata"`
}

// AgentStats represents aggregated statistics for an agent.
type AgentStats struct {
	ID             string  `json:"id" db:"id"`
	Name           string  `json:"name" db:"name"`
	Role           string  `json:"role" db:"role"`
	Status         string  `json:"status" db:"status"`
	TotalTasks     int     `json:"total_tasks" db:"total_tasks"`
	CompletedTasks int     `json:"completed_tasks" db:"completed_tasks"`
	FailedTasks    int     `json:"failed_tasks" db:"failed_tasks"`
	TotalTokens    int64   `json:"total_tokens" db:"total_tokens"`
	TotalCost      float64 `json:"total_cost" db:"total_cost"`
	AvgDurationMs  float64 `json:"avg_duration_ms" db:"avg_duration_ms"`
	SuccessRate    float64 `json:"success_rate" db:"success_rate"`
}

// JSONB is a custom type for PostgreSQL JSONB columns.
type JSONB map[string]interface{}

// Value implements the driver.Valuer interface for JSONB.
func (j JSONB) Value() (driver.Value, error) {
	if j == nil {
		return nil, nil
	}
	return json.Marshal(j)
}

// Scan implements the sql.Scanner interface for JSONB.
func (j *JSONB) Scan(value interface{}) error {
	if value == nil {
		*j = nil
		return nil
	}

	bytes, ok := value.([]byte)
	if !ok {
		return nil
	}

	result := make(map[string]interface{})
	if err := json.Unmarshal(bytes, &result); err != nil {
		return err
	}

	*j = result
	return nil
}

// CreateTaskRequest represents a request to create a new task.
type CreateTaskRequest struct {
	AgentID     string                 `json:"agent_id" binding:"required"`
	WorkflowID  *uuid.UUID             `json:"workflow_id,omitempty"`
	TaskType    string                 `json:"task_type" binding:"required"`
	Description string                 `json:"description" binding:"required"`
	InputData   map[string]interface{} `json:"input_data,omitempty"`
}

// CreateWorkflowRequest represents a request to create a new workflow.
type CreateWorkflowRequest struct {
	Name         string                 `json:"name" binding:"required"`
	Description  string                 `json:"description"`
	WorkflowType string                 `json:"workflow_type"`
	Initiator    string                 `json:"initiator"`
	Metadata     map[string]interface{} `json:"metadata,omitempty"`
}

// UpdateTaskStatusRequest represents a request to update task status.
type UpdateTaskStatusRequest struct {
	Status       string                 `json:"status" binding:"required"`
	OutputData   map[string]interface{} `json:"output_data,omitempty"`
	ErrorMessage *string                `json:"error_message,omitempty"`
	TokensUsed   int                    `json:"tokens_used,omitempty"`
	CostUsd      float64                `json:"cost_usd,omitempty"`
}
