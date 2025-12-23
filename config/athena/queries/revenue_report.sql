-- Monthly Revenue Report
-- Shows revenue metrics aggregated by month

SELECT 
    year,
    month,
    COUNT(DISTINCT id) as total_workflows,
    COUNT(DISTINCT CASE WHEN status = 'completed' THEN id END) as completed_workflows,
    SUM(total_cost_usd) as total_revenue,
    AVG(total_cost_usd) as avg_revenue_per_workflow,
    SUM(total_tokens_used) as total_tokens,
    AVG(total_tokens_used) as avg_tokens_per_workflow,
    AVG(duration_ms) / 1000.0 as avg_duration_seconds,
    MIN(created_at) as period_start,
    MAX(created_at) as period_end
FROM workflows
WHERE year = YEAR(CURRENT_DATE)
GROUP BY year, month
ORDER BY year DESC, month DESC;
