package analytics

import "time"

// WorkflowMetric represents workflow analytics data
type WorkflowMetric struct {
	Year           int       `json:"year"`
	Month          int       `json:"month"`
	Day            int       `json:"day"`
	TotalWorkflows int       `json:"total_workflows"`
	CompletedCount int       `json:"completed_count"`
	FailedCount    int       `json:"failed_count"`
	AvgDurationMs  float64   `json:"avg_duration_ms"`
	TotalTokens    int64     `json:"total_tokens"`
	TotalCostUSD   float64   `json:"total_cost_usd"`
	Date           time.Time `json:"date"`
}

// AgentMetric represents agent performance metrics
type AgentMetric struct {
	AgentID        string    `json:"agent_id"`
	AgentName      string    `json:"agent_name"`
	Period         string    `json:"period"` // daily, weekly, monthly
	TotalTasks     int       `json:"total_tasks"`
	CompletedTasks int       `json:"completed_tasks"`
	FailedTasks    int       `json:"failed_tasks"`
	AvgDurationMs  float64   `json:"avg_duration_ms"`
	TotalTokens    int64     `json:"total_tokens"`
	TotalCostUSD   float64   `json:"total_cost_usd"`
	SuccessRate    float64   `json:"success_rate"`
	StartDate      time.Time `json:"start_date"`
	EndDate        time.Time `json:"end_date"`
}

// TaskTypeMetric represents metrics aggregated by task type
type TaskTypeMetric struct {
	TaskType       string  `json:"task_type"`
	TotalTasks     int     `json:"total_tasks"`
	CompletedTasks int     `json:"completed_tasks"`
	FailedTasks    int     `json:"failed_tasks"`
	AvgDurationMs  float64 `json:"avg_duration_ms"`
	AvgTokens      float64 `json:"avg_tokens"`
	AvgCostUSD     float64 `json:"avg_cost_usd"`
	SuccessRate    float64 `json:"success_rate"`
}

// UserSessionMetric represents user activity metrics
type UserSessionMetric struct {
	Date           time.Time `json:"date"`
	TotalSessions  int       `json:"total_sessions"`
	ActiveSessions int       `json:"active_sessions"`
	UniqueUsers    int       `json:"unique_users"`
	AvgSessionMs   float64   `json:"avg_session_ms"`
}

// CostAnalysis represents cost breakdown by agent and period
type CostAnalysis struct {
	AgentID      string    `json:"agent_id"`
	AgentName    string    `json:"agent_name"`
	Period       string    `json:"period"`
	TotalCostUSD float64   `json:"total_cost_usd"`
	TotalTokens  int64     `json:"total_tokens"`
	CostPerToken float64   `json:"cost_per_token"`
	TotalTasks   int       `json:"total_tasks"`
	CostPerTask  float64   `json:"cost_per_task"`
	StartDate    time.Time `json:"start_date"`
	EndDate      time.Time `json:"end_date"`
}

// QueryResult represents a generic Athena query result
type QueryResult struct {
	Columns  []string                 `json:"columns"`
	Rows     []map[string]interface{} `json:"rows"`
	RowCount int                      `json:"row_count"`
}

// PerformanceTrend represents performance trends over time
type PerformanceTrend struct {
	Date         time.Time `json:"date"`
	AvgLatencyMs float64   `json:"avg_latency_ms"`
	SuccessRate  float64   `json:"success_rate"`
	TotalTasks   int       `json:"total_tasks"`
	TotalTokens  int64     `json:"total_tokens"`
}
