-- Tokyo-IA Athena Tables DDL
-- Complete table definitions for analytics data lake

-- ============================================================================
-- WORKFLOWS TABLE
-- ============================================================================
CREATE EXTERNAL TABLE IF NOT EXISTS workflows (
    id STRING COMMENT 'Workflow UUID',
    name STRING COMMENT 'Workflow name',
    description STRING COMMENT 'Workflow description',
    status STRING COMMENT 'Status: pending, running, completed, failed, cancelled',
    workflow_type STRING COMMENT 'Type of workflow',
    initiator STRING COMMENT 'User or system that initiated the workflow',
    total_tasks INT COMMENT 'Total number of tasks in workflow',
    completed_tasks INT COMMENT 'Number of completed tasks',
    failed_tasks INT COMMENT 'Number of failed tasks',
    started_at TIMESTAMP COMMENT 'Workflow start timestamp',
    completed_at TIMESTAMP COMMENT 'Workflow completion timestamp',
    duration_ms INT COMMENT 'Duration in milliseconds',
    total_tokens_used INT COMMENT 'Total tokens consumed',
    total_cost_usd DECIMAL(10,6) COMMENT 'Total cost in USD',
    created_at TIMESTAMP COMMENT 'Record creation timestamp',
    updated_at TIMESTAMP COMMENT 'Record update timestamp',
    metadata STRING COMMENT 'Additional metadata as JSON'
)
COMMENT 'Multi-agent workflow orchestration records'
PARTITIONED BY (
    year INT COMMENT 'Year partition',
    month INT COMMENT 'Month partition (1-12)',
    day INT COMMENT 'Day partition (1-31)'
)
STORED AS PARQUET
LOCATION 's3://tokyo-ia-data-lake-dev/workflows/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'classification'='parquet',
    'compressionType'='none',
    'typeOfData'='file'
);

-- ============================================================================
-- AGENT TASKS TABLE
-- ============================================================================
CREATE EXTERNAL TABLE IF NOT EXISTS agent_tasks (
    id STRING COMMENT 'Task UUID',
    agent_id STRING COMMENT 'Agent identifier',
    workflow_id STRING COMMENT 'Parent workflow UUID',
    task_type STRING COMMENT 'Type of task',
    description STRING COMMENT 'Task description',
    status STRING COMMENT 'Status: pending, running, completed, failed, cancelled',
    input_data STRING COMMENT 'Input data as JSON',
    output_data STRING COMMENT 'Output data as JSON',
    error_message STRING COMMENT 'Error message if failed',
    started_at TIMESTAMP COMMENT 'Task start timestamp',
    completed_at TIMESTAMP COMMENT 'Task completion timestamp',
    duration_ms INT COMMENT 'Duration in milliseconds',
    tokens_used INT COMMENT 'Tokens consumed',
    cost_usd DECIMAL(10,6) COMMENT 'Cost in USD',
    retry_count INT COMMENT 'Number of retry attempts',
    parent_task_id STRING COMMENT 'Parent task UUID if subtask',
    created_at TIMESTAMP COMMENT 'Record creation timestamp',
    metadata STRING COMMENT 'Additional metadata as JSON'
)
COMMENT 'Individual agent task execution records'
PARTITIONED BY (
    year INT COMMENT 'Year partition',
    month INT COMMENT 'Month partition (1-12)',
    day INT COMMENT 'Day partition (1-31)'
)
STORED AS PARQUET
LOCATION 's3://tokyo-ia-data-lake-dev/agent_tasks/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'classification'='parquet',
    'compressionType'='none',
    'typeOfData'='file'
);

-- ============================================================================
-- AGENT METRICS TABLE
-- ============================================================================
CREATE EXTERNAL TABLE IF NOT EXISTS agent_metrics (
    id STRING COMMENT 'Metric UUID',
    agent_id STRING COMMENT 'Agent identifier',
    metric_type STRING COMMENT 'Type of metric',
    metric_value DOUBLE COMMENT 'Metric value',
    metric_unit STRING COMMENT 'Unit of measurement',
    recorded_at TIMESTAMP COMMENT 'Metric recording timestamp',
    context STRING COMMENT 'Additional context as JSON'
)
COMMENT 'Time-series performance metrics for agents'
PARTITIONED BY (
    year INT COMMENT 'Year partition',
    month INT COMMENT 'Month partition (1-12)',
    day INT COMMENT 'Day partition (1-31)'
)
STORED AS PARQUET
LOCATION 's3://tokyo-ia-data-lake-dev/agent_metrics/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'classification'='parquet',
    'compressionType'='none',
    'typeOfData'='file'
);

-- ============================================================================
-- AGENT INTERACTIONS TABLE
-- ============================================================================
CREATE EXTERNAL TABLE IF NOT EXISTS agent_interactions (
    id STRING COMMENT 'Interaction UUID',
    workflow_id STRING COMMENT 'Parent workflow UUID',
    from_agent_id STRING COMMENT 'Source agent identifier',
    to_agent_id STRING COMMENT 'Target agent identifier',
    interaction_type STRING COMMENT 'Type of interaction',
    message STRING COMMENT 'Interaction message',
    payload STRING COMMENT 'Interaction payload as JSON',
    created_at TIMESTAMP COMMENT 'Interaction timestamp'
)
COMMENT 'Communication records between agents'
PARTITIONED BY (
    year INT COMMENT 'Year partition',
    month INT COMMENT 'Month partition (1-12)',
    day INT COMMENT 'Day partition (1-31)'
)
STORED AS PARQUET
LOCATION 's3://tokyo-ia-data-lake-dev/agent_interactions/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'classification'='parquet',
    'compressionType'='none',
    'typeOfData'='file'
);

-- ============================================================================
-- USER SESSIONS TABLE
-- ============================================================================
CREATE EXTERNAL TABLE IF NOT EXISTS user_sessions (
    id STRING COMMENT 'Session UUID',
    user_id STRING COMMENT 'User identifier',
    session_token STRING COMMENT 'Session token',
    device_info STRING COMMENT 'Device information as JSON',
    ip_address STRING COMMENT 'IP address',
    started_at TIMESTAMP COMMENT 'Session start timestamp',
    last_activity_at TIMESTAMP COMMENT 'Last activity timestamp',
    ended_at TIMESTAMP COMMENT 'Session end timestamp',
    is_active BOOLEAN COMMENT 'Session active status',
    metadata STRING COMMENT 'Additional metadata as JSON'
)
COMMENT 'User session tracking records'
PARTITIONED BY (
    year INT COMMENT 'Year partition',
    month INT COMMENT 'Month partition (1-12)',
    day INT COMMENT 'Day partition (1-31)'
)
STORED AS PARQUET
LOCATION 's3://tokyo-ia-data-lake-dev/user_sessions/'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'classification'='parquet',
    'compressionType'='none',
    'typeOfData'='file'
);

-- ============================================================================
-- NOTES
-- ============================================================================
-- 1. Update S3 locations to match your environment (dev/staging/prod)
-- 2. Run MSCK REPAIR TABLE after loading data to discover partitions
-- 3. All tables use Parquet format with Snappy compression for efficiency
-- 4. Partition pruning is automatic when querying with year/month/day filters
