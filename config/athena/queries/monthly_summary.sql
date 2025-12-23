-- Monthly Summary Dashboard
-- Executive summary of key metrics

WITH monthly_workflows AS (
    SELECT 
        year,
        month,
        COUNT(*) as total_workflows,
        COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
        SUM(total_cost_usd) as revenue,
        SUM(total_tokens_used) as tokens
    FROM workflows
    WHERE year = YEAR(CURRENT_DATE)
    GROUP BY year, month
),
monthly_tasks AS (
    SELECT 
        year,
        month,
        COUNT(*) as total_tasks,
        COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tasks,
        COUNT(DISTINCT agent_id) as active_agents
    FROM agent_tasks
    WHERE year = YEAR(CURRENT_DATE)
    GROUP BY year, month
),
monthly_sessions AS (
    SELECT 
        year,
        month,
        COUNT(*) as total_sessions,
        COUNT(DISTINCT user_id) as unique_users
    FROM user_sessions
    WHERE year = YEAR(CURRENT_DATE)
    GROUP BY year, month
)
SELECT 
    w.year,
    w.month,
    -- Workflow Metrics
    w.total_workflows,
    w.completed as completed_workflows,
    CAST(w.completed AS DOUBLE) / w.total_workflows * 100 as workflow_success_rate,
    -- Task Metrics
    t.total_tasks,
    t.completed_tasks,
    t.active_agents,
    -- Financial Metrics
    w.revenue as total_revenue_usd,
    w.revenue / w.total_workflows as avg_revenue_per_workflow,
    w.tokens as total_tokens,
    CASE WHEN w.tokens > 0 THEN w.revenue / w.tokens * 1000000 ELSE 0 END as cost_per_million_tokens,
    -- User Metrics
    s.total_sessions,
    s.unique_users,
    CAST(s.total_sessions AS DOUBLE) / s.unique_users as avg_sessions_per_user
FROM monthly_workflows w
LEFT JOIN monthly_tasks t ON w.year = t.year AND w.month = t.month
LEFT JOIN monthly_sessions s ON w.year = s.year AND w.month = s.month
ORDER BY w.year DESC, w.month DESC;
