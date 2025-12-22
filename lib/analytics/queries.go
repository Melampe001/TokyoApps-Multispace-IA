package analytics

// Predefined SQL queries for common analytics operations

const (
	// QueryWorkflowMetricsByDay gets workflow metrics grouped by day
	QueryWorkflowMetricsByDay = `
		SELECT 
			year,
			month,
			day,
			COUNT(*) as total_workflows,
			COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_count,
			COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_count,
			AVG(duration_ms) as avg_duration_ms,
			SUM(total_tokens_used) as total_tokens,
			SUM(total_cost_usd) as total_cost_usd
		FROM workflows
		WHERE year = %d AND month = %d AND day >= %d AND day <= %d
		GROUP BY year, month, day
		ORDER BY year, month, day
	`

	// QueryAgentPerformance gets agent performance metrics
	QueryAgentPerformance = `
		SELECT 
			at.agent_id,
			COUNT(*) as total_tasks,
			COUNT(CASE WHEN at.status = 'completed' THEN 1 END) as completed_tasks,
			COUNT(CASE WHEN at.status = 'failed' THEN 1 END) as failed_tasks,
			AVG(at.duration_ms) as avg_duration_ms,
			SUM(at.tokens_used) as total_tokens,
			SUM(at.cost_usd) as total_cost_usd,
			CAST(COUNT(CASE WHEN at.status = 'completed' THEN 1 END) AS DOUBLE) / COUNT(*) * 100 as success_rate
		FROM agent_tasks at
		WHERE at.year = %d AND at.month = %d 
		GROUP BY at.agent_id
		ORDER BY total_tasks DESC
	`

	// QueryTaskTypeMetrics gets metrics by task type
	QueryTaskTypeMetrics = `
		SELECT 
			task_type,
			COUNT(*) as total_tasks,
			COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tasks,
			COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_tasks,
			AVG(duration_ms) as avg_duration_ms,
			AVG(tokens_used) as avg_tokens,
			AVG(cost_usd) as avg_cost_usd,
			CAST(COUNT(CASE WHEN status = 'completed' THEN 1 END) AS DOUBLE) / COUNT(*) * 100 as success_rate
		FROM agent_tasks
		WHERE year = %d AND month = %d
		GROUP BY task_type
		ORDER BY total_tasks DESC
	`

	// QueryCostAnalysisByAgent gets cost breakdown by agent
	QueryCostAnalysisByAgent = `
		SELECT 
			agent_id,
			SUM(cost_usd) as total_cost_usd,
			SUM(tokens_used) as total_tokens,
			COUNT(*) as total_tasks,
			CASE WHEN SUM(tokens_used) > 0 THEN SUM(cost_usd) / SUM(tokens_used) ELSE 0 END as cost_per_token,
			CASE WHEN COUNT(*) > 0 THEN SUM(cost_usd) / COUNT(*) ELSE 0 END as cost_per_task
		FROM agent_tasks
		WHERE year = %d AND month = %d
		GROUP BY agent_id
		ORDER BY total_cost_usd DESC
	`

	// QueryUserSessionMetrics gets user session statistics
	QueryUserSessionMetrics = `
		SELECT 
			year,
			month,
			day,
			COUNT(*) as total_sessions,
			COUNT(CASE WHEN is_active = true THEN 1 END) as active_sessions,
			COUNT(DISTINCT user_id) as unique_users,
			AVG(date_diff('millisecond', started_at, COALESCE(ended_at, last_activity_at))) as avg_session_ms
		FROM user_sessions
		WHERE year = %d AND month = %d AND day >= %d AND day <= %d
		GROUP BY year, month, day
		ORDER BY year, month, day
	`

	// QueryPerformanceTrend gets performance trends over time
	QueryPerformanceTrend = `
		SELECT 
			DATE(created_at) as date,
			AVG(duration_ms) as avg_latency_ms,
			CAST(COUNT(CASE WHEN status = 'completed' THEN 1 END) AS DOUBLE) / COUNT(*) * 100 as success_rate,
			COUNT(*) as total_tasks,
			SUM(tokens_used) as total_tokens
		FROM agent_tasks
		WHERE year = %d AND month = %d
		GROUP BY DATE(created_at)
		ORDER BY DATE(created_at)
	`

	// QueryTopPerformingAgents gets top performing agents by success rate
	QueryTopPerformingAgents = `
		SELECT 
			agent_id,
			COUNT(*) as total_tasks,
			COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tasks,
			CAST(COUNT(CASE WHEN status = 'completed' THEN 1 END) AS DOUBLE) / COUNT(*) * 100 as success_rate,
			AVG(duration_ms) as avg_duration_ms
		FROM agent_tasks
		WHERE year = %d AND month = %d
		GROUP BY agent_id
		HAVING COUNT(*) >= 10
		ORDER BY success_rate DESC, total_tasks DESC
		LIMIT 10
	`

	// QueryWorkflowsByStatus gets workflow counts grouped by status
	QueryWorkflowsByStatus = `
		SELECT 
			status,
			COUNT(*) as count,
			AVG(duration_ms) as avg_duration_ms,
			AVG(total_cost_usd) as avg_cost_usd
		FROM workflows
		WHERE year = %d AND month = %d
		GROUP BY status
		ORDER BY count DESC
	`

	// QueryAgentInteractionVolume gets interaction volume between agents
	QueryAgentInteractionVolume = `
		SELECT 
			from_agent_id,
			to_agent_id,
			interaction_type,
			COUNT(*) as interaction_count
		FROM agent_interactions
		WHERE year = %d AND month = %d
		GROUP BY from_agent_id, to_agent_id, interaction_type
		ORDER BY interaction_count DESC
	`

	// QueryDailyMetricsSummary gets comprehensive daily summary
	QueryDailyMetricsSummary = `
		SELECT 
			'workflows' as metric_source,
			year,
			month,
			day,
			COUNT(*) as count,
			SUM(total_cost_usd) as total_cost
		FROM workflows
		WHERE year = %d AND month = %d AND day = %d
		GROUP BY year, month, day
	`
)

// QueryBuilder helps construct dynamic queries
type QueryBuilder struct {
	baseQuery string
	params    []interface{}
}

// NewQueryBuilder creates a new query builder
func NewQueryBuilder(baseQuery string) *QueryBuilder {
	return &QueryBuilder{
		baseQuery: baseQuery,
		params:    make([]interface{}, 0),
	}
}

// AddParam adds a parameter to the query
func (qb *QueryBuilder) AddParam(param interface{}) *QueryBuilder {
	qb.params = append(qb.params, param)
	return qb
}

// Build returns the query string and parameters
func (qb *QueryBuilder) Build() (string, []interface{}) {
	return qb.baseQuery, qb.params
}
