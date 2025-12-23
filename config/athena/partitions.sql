-- Partition Management Scripts for Athena Tables
-- Use these scripts to manually manage partitions when needed

-- ============================================================================
-- REPAIR ALL TABLES (Discover new partitions automatically)
-- ============================================================================
-- This is the recommended approach as it discovers all partitions at once

MSCK REPAIR TABLE workflows;
MSCK REPAIR TABLE agent_tasks;
MSCK REPAIR TABLE agent_metrics;
MSCK REPAIR TABLE agent_interactions;
MSCK REPAIR TABLE user_sessions;

-- ============================================================================
-- ADD SPECIFIC PARTITIONS MANUALLY
-- ============================================================================
-- Use these if MSCK REPAIR doesn't work or for specific partition management

-- Add workflows partition for a specific date
ALTER TABLE workflows ADD IF NOT EXISTS
PARTITION (year=2024, month=12, day=22)
LOCATION 's3://tokyo-ia-data-lake-dev/workflows/year=2024/month=12/day=22/';

-- Add agent_tasks partition for a specific date
ALTER TABLE agent_tasks ADD IF NOT EXISTS
PARTITION (year=2024, month=12, day=22)
LOCATION 's3://tokyo-ia-data-lake-dev/agent_tasks/year=2024/month=12/day=22/';

-- Add agent_metrics partition for a specific date
ALTER TABLE agent_metrics ADD IF NOT EXISTS
PARTITION (year=2024, month=12, day=22)
LOCATION 's3://tokyo-ia-data-lake-dev/agent_metrics/year=2024/month=12/day=22/';

-- Add agent_interactions partition for a specific date
ALTER TABLE agent_interactions ADD IF NOT EXISTS
PARTITION (year=2024, month=12, day=22)
LOCATION 's3://tokyo-ia-data-lake-dev/agent_interactions/year=2024/month=12/day=22/';

-- Add user_sessions partition for a specific date
ALTER TABLE user_sessions ADD IF NOT EXISTS
PARTITION (year=2024, month=12, day=22)
LOCATION 's3://tokyo-ia-data-lake-dev/user_sessions/year=2024/month=12/day=22/';

-- ============================================================================
-- DROP SPECIFIC PARTITIONS
-- ============================================================================
-- Use these to remove old or incorrect partitions

-- Drop workflows partition
ALTER TABLE workflows DROP IF EXISTS
PARTITION (year=2024, month=12, day=22);

-- Drop agent_tasks partition
ALTER TABLE agent_tasks DROP IF EXISTS
PARTITION (year=2024, month=12, day=22);

-- ============================================================================
-- SHOW PARTITIONS
-- ============================================================================
-- Use these to view existing partitions for each table

SHOW PARTITIONS workflows;
SHOW PARTITIONS agent_tasks;
SHOW PARTITIONS agent_metrics;
SHOW PARTITIONS agent_interactions;
SHOW PARTITIONS user_sessions;

-- ============================================================================
-- ADD MULTIPLE PARTITIONS (Example: for a week)
-- ============================================================================
-- Example of adding partitions for multiple days at once

-- Workflows partitions for Dec 22-28, 2024
ALTER TABLE workflows ADD IF NOT EXISTS
PARTITION (year=2024, month=12, day=22) LOCATION 's3://tokyo-ia-data-lake-dev/workflows/year=2024/month=12/day=22/'
PARTITION (year=2024, month=12, day=23) LOCATION 's3://tokyo-ia-data-lake-dev/workflows/year=2024/month=12/day=23/'
PARTITION (year=2024, month=12, day=24) LOCATION 's3://tokyo-ia-data-lake-dev/workflows/year=2024/month=12/day=24/'
PARTITION (year=2024, month=12, day=25) LOCATION 's3://tokyo-ia-data-lake-dev/workflows/year=2024/month=12/day=25/'
PARTITION (year=2024, month=12, day=26) LOCATION 's3://tokyo-ia-data-lake-dev/workflows/year=2024/month=12/day=26/'
PARTITION (year=2024, month=12, day=27) LOCATION 's3://tokyo-ia-data-lake-dev/workflows/year=2024/month=12/day=27/'
PARTITION (year=2024, month=12, day=28) LOCATION 's3://tokyo-ia-data-lake-dev/workflows/year=2024/month=12/day=28/';

-- ============================================================================
-- VERIFY PARTITION DATA
-- ============================================================================
-- Check if partitions contain data

SELECT year, month, day, COUNT(*) as row_count
FROM workflows
GROUP BY year, month, day
ORDER BY year DESC, month DESC, day DESC
LIMIT 10;

SELECT year, month, day, COUNT(*) as row_count
FROM agent_tasks
GROUP BY year, month, day
ORDER BY year DESC, month DESC, day DESC
LIMIT 10;

-- ============================================================================
-- NOTES
-- ============================================================================
-- 1. MSCK REPAIR TABLE is usually sufficient for discovering partitions
-- 2. Manual partition addition is useful for immediate needs or troubleshooting
-- 3. Always verify S3 paths match your environment (dev/staging/prod)
-- 4. Partition format must match: year=YYYY/month=MM/day=DD
-- 5. Run SHOW PARTITIONS to verify partitions were added successfully
