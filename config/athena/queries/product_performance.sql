-- Product Performance Report
-- Analyzes performance by workflow/product type

SELECT 
    workflow_type as product_type,
    COUNT(*) as total_workflows,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed,
    CAST(COUNT(CASE WHEN status = 'completed' THEN 1 END) AS DOUBLE) / COUNT(*) * 100 as success_rate,
    AVG(duration_ms) / 1000.0 as avg_duration_sec,
    PERCENTILE(duration_ms, 0.5) / 1000.0 as median_duration_sec,
    PERCENTILE(duration_ms, 0.95) / 1000.0 as p95_duration_sec,
    SUM(total_cost_usd) as total_revenue,
    AVG(total_cost_usd) as avg_revenue,
    SUM(total_tokens_used) as total_tokens,
    AVG(total_tokens_used) as avg_tokens
FROM workflows
WHERE year = YEAR(CURRENT_DATE)
  AND month = MONTH(CURRENT_DATE)
  AND workflow_type IS NOT NULL
GROUP BY workflow_type
ORDER BY total_workflows DESC;
