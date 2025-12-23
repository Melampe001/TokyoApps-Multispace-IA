-- User Analytics Report
-- Comprehensive user activity and engagement metrics

SELECT 
    user_id,
    COUNT(DISTINCT id) as total_sessions,
    COUNT(DISTINCT CASE WHEN is_active = true THEN id END) as active_sessions,
    AVG(CAST(date_diff('second', started_at, COALESCE(ended_at, last_activity_at)) AS DOUBLE)) as avg_session_duration_sec,
    MIN(started_at) as first_session,
    MAX(last_activity_at) as last_activity,
    COUNT(DISTINCT DATE(started_at)) as active_days,
    -- Engagement score (0-100)
    LEAST(100, 
        (COUNT(DISTINCT id) * 10) + 
        (COUNT(DISTINCT DATE(started_at)) * 5)
    ) as engagement_score
FROM user_sessions
WHERE year = YEAR(CURRENT_DATE)
  AND month = MONTH(CURRENT_DATE)
GROUP BY user_id
ORDER BY engagement_score DESC, total_sessions DESC
LIMIT 100;
