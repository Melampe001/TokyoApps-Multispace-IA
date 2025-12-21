# Tokyo-IA Database

This directory contains the PostgreSQL database schema for the Tokyo-IA Agent Orchestration System.

## Quick Start

### Prerequisites
- PostgreSQL 14 or higher
- psql CLI tool

### Setup Database

```bash
# Create database
createdb tokyoia

# Run schema
psql tokyoia < db/schema.sql
```

### Environment Variables

Set the following environment variable to connect:

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/tokyoia"
```

## Schema Overview

### Core Tables

#### `agents`
Stores information about the 5 specialized AI agents:
- **akira-001**: Code Review Master (侍)
- **yuki-002**: Test Engineering Specialist (❄️)
- **hiro-003**: SRE & DevOps Guardian (🛡️)
- **sakura-004**: Documentation Artist (🌸)
- **kenji-005**: Architecture Visionary (🏗️)

#### `workflows`
Multi-agent workflow orchestration tracking:
- Workflow execution status
- Task coordination
- Performance metrics
- Cost tracking

#### `agent_tasks`
Individual task execution records:
- Task status and results
- Token usage and costs
- Parent-child task relationships
- Error tracking and retries

#### `agent_metrics`
Time-series performance data:
- Latency measurements
- Token consumption
- Success rates
- Custom metrics

#### `agent_interactions`
Inter-agent communication logs:
- Message passing
- Workflow coordination
- Collaboration patterns

#### `user_sessions`
User authentication and activity tracking:
- Session management
- Device information
- Activity timestamps

### Views

#### `agent_stats`
Aggregated statistics per agent:
- Total/completed/failed tasks
- Token usage and costs
- Average duration
- Success rates

## Example Queries

### Get all agents with their stats
```sql
SELECT * FROM agent_stats ORDER BY total_tasks DESC;
```

### Get active workflows
```sql
SELECT * FROM workflows 
WHERE status = 'running' 
ORDER BY started_at DESC;
```

### Get recent tasks for an agent
```sql
SELECT * FROM agent_tasks 
WHERE agent_id = 'akira-001' 
ORDER BY created_at DESC 
LIMIT 10;
```

### Get agent interactions in a workflow
```sql
SELECT 
    ai.*,
    a1.name as from_agent,
    a2.name as to_agent
FROM agent_interactions ai
JOIN agents a1 ON ai.from_agent_id = a1.id
JOIN agents a2 ON ai.to_agent_id = a2.id
WHERE workflow_id = 'your-workflow-id'
ORDER BY created_at;
```

## Migrations

Future schema changes should be added to `db/migrations/` with timestamp prefixes:
```
db/migrations/
  001_initial_schema.sql
  002_add_agent_tags.sql
  003_add_workflow_templates.sql
```

## Backup & Restore

### Backup
```bash
pg_dump tokyoia > backup_$(date +%Y%m%d).sql
```

### Restore
```bash
psql tokyoia < backup_20231215.sql
```

## Performance Tuning

The schema includes indexes on frequently queried columns:
- Task lookups by agent, workflow, and status
- Time-based queries on metrics
- Active session filtering

For production deployments, consider:
- Partitioning `agent_metrics` by time
- Archiving old `agent_tasks` data
- Setting up read replicas for analytics
