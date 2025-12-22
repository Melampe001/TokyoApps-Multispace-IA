# ETL Pipeline Documentation

Comprehensive guide to the Tokyo-IA ETL (Extract, Transform, Load) pipeline that exports PostgreSQL data to S3 for Athena analytics.

## Overview

The ETL pipeline runs daily to export historical data from PostgreSQL to S3 in Parquet format, partitioned by date for efficient querying in Athena.

## Pipeline Architecture

```
PostgreSQL → Python ETL → S3 (Parquet) → Glue Crawler → Athena
     ↓           ↓            ↓              ↓             ↓
 Hot Data    Transform    Partition      Catalog      Analytics
```

## Components

### 1. Configuration (`python/etl/config.py`)

Centralized configuration management using environment variables.

**Key Features**:
- Environment variable validation
- Default values for development
- Support for multiple environments
- Secure credential handling

**Usage**:
```python
from config import config

print(config.database_url)
print(config.s3_data_lake_bucket)
```

### 2. S3 Exporter (`python/etl/export_to_s3.py`)

Main ETL script that exports data from PostgreSQL to S3.

**Features**:
- Batch processing (configurable size)
- Date-based partitioning
- Parquet format with Snappy compression
- Automatic retry logic
- Progress logging
- Error handling

**Usage**:
```bash
# Export yesterday's data (default)
python python/etl/export_to_s3.py

# Export specific date range
python python/etl/export_to_s3.py \
  --start-date 2024-12-01 \
  --end-date 2024-12-31

# Export single table
python python/etl/export_to_s3.py --table workflows
```

### 3. Athena Setup (`python/etl/athena_setup.py`)

Creates and manages Athena tables and partitions.

**Features**:
- Create Glue database
- Define external tables
- Repair partitions (MSCK REPAIR)
- Query execution with retry

**Usage**:
```bash
# Initial setup
python python/etl/athena_setup.py

# Repair partitions only
python -c "from athena_setup import AthenaSetup; \
  s = AthenaSetup(); s.repair_partitions('workflows')"
```

## Data Flow

### Extract Phase

1. Connect to PostgreSQL
2. Query data for date range
3. Stream results to pandas DataFrame

```python
query = """
    SELECT *
    FROM workflows
    WHERE created_at >= %s AND created_at < %s
    ORDER BY created_at
"""
df = pd.read_sql_query(query, conn, params=(start, end))
```

### Transform Phase

1. Convert to Parquet format
2. Apply Snappy compression
3. Add partition columns

```python
df.to_parquet(
    buffer,
    engine='pyarrow',
    compression='snappy',
    index=False,
)
```

**Compression Ratio**: ~75% size reduction

### Load Phase

1. Upload to S3 with partitioning
2. Update Glue catalog
3. Validate upload

**Partition Structure**:
```
s3://bucket/table_name/year=2024/month=12/day=22/data.parquet
```

## Tables Exported

| Table | Date Column | Description |
|-------|-------------|-------------|
| workflows | created_at | Workflow execution records |
| agent_tasks | created_at | Individual task executions |
| agent_metrics | recorded_at | Performance metrics |
| agent_interactions | created_at | Agent communications |
| user_sessions | started_at | User session data |

## Scheduling

### Automated Schedule (GitHub Actions)

**Trigger**: Daily at 2 AM UTC

**Workflow**: `.github/workflows/data-pipeline.yml`

**Steps**:
1. Checkout code
2. Setup Python environment
3. Install dependencies
4. Configure AWS credentials
5. Run ETL export
6. Update Athena partitions
7. Validate data
8. Start Glue crawler
9. Send notifications (on failure)

### Manual Execution

```bash
# Using helper script
./scripts/run_etl.sh --start-date 2024-12-22

# Direct Python
python python/etl/export_to_s3.py --start-date 2024-12-22
```

## Configuration

### Environment Variables

Required:
```env
DB_HOST=localhost
DB_NAME=tokyo_ia
DB_USER=postgres
DB_PASSWORD=your_password
S3_DATA_LAKE_BUCKET=tokyo-ia-data-lake-dev
ATHENA_DATABASE=tokyo_ia_billing_dev
AWS_REGION=us-east-1
```

Optional:
```env
ETL_BATCH_SIZE=10000
ETL_RETENTION_DAYS=90
ENVIRONMENT=dev
```

### Batch Size Configuration

Adjust based on available memory:
- Small datasets (<1M rows): 10,000
- Medium datasets (1M-10M rows): 50,000
- Large datasets (>10M rows): 100,000

## Error Handling

### Retry Logic

ETL automatically retries failed operations:
- **Database queries**: 3 retries with exponential backoff
- **S3 uploads**: 3 retries with exponential backoff
- **Athena queries**: 5 retries with exponential backoff

### Error Scenarios

**1. Database Connection Failure**
```
ERROR: Failed to connect to database: connection refused
```
**Solution**: Check database connectivity and credentials

**2. S3 Upload Failure**
```
ERROR: Failed to upload to S3: Access Denied
```
**Solution**: Verify IAM role permissions

**3. Partition Creation Failure**
```
ERROR: Failed to create partitions: Table not found
```
**Solution**: Run `athena_setup.py` to create tables

## Monitoring

### Logs

ETL logs include:
- Start/end timestamps
- Row counts per table
- File sizes
- Error messages
- Execution duration

**Example**:
```
2024-12-22 02:00:01 - INFO - Starting ETL export
2024-12-22 02:00:05 - INFO - Connected to PostgreSQL
2024-12-22 02:01:23 - INFO - Fetched 15,234 rows from workflows
2024-12-22 02:01:45 - INFO - Uploaded to s3://bucket/workflows/...
2024-12-22 02:05:12 - INFO - ETL completed: 87,456 rows, 5 files
```

### Metrics

Track these metrics:
- **Rows exported**: Total records processed
- **Files created**: Number of Parquet files
- **Data size**: Total bytes uploaded
- **Execution time**: Duration in seconds
- **Success rate**: Percentage of successful exports

### Alerts

Configure alerts for:
- ETL failure (immediate)
- Long execution time (>1 hour)
- Low row count (data quality issue)
- S3 upload failures

## Performance Optimization

### Database Query Optimization

1. **Add indexes** on date columns:
```sql
CREATE INDEX idx_workflows_created_at ON workflows(created_at);
```

2. **Use connection pooling**
3. **Limit concurrent exports**

### S3 Upload Optimization

1. **Use multipart upload** for large files (>100MB)
2. **Compress before upload** (already done with Parquet)
3. **Batch small files** instead of many individual uploads

### Parquet Optimization

1. **Use appropriate compression**:
   - Snappy: Fast, moderate compression (current)
   - GZIP: Slower, better compression
   - ZSTD: Best balance

2. **Optimize row group size**: 128MB (default)

3. **Column pruning**: Only export needed columns

## Backfilling Historical Data

For loading old data, use the backfill script:

```bash
# Backfill last 30 days
python scripts/backfill_data.py \
  --start-date 2024-11-22 \
  --end-date 2024-12-22

# Backfill specific table
python scripts/backfill_data.py \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --table workflows
```

**Warning**: Large backfills can take hours. Use `--dry-run` first.

## Data Validation

### Automated Validation

Run after ETL:
```bash
python scripts/validate_data.py --days 7
```

Checks:
- ✓ Files exist in S3
- ✓ Row counts match PostgreSQL
- ✓ Partitions registered in Glue
- ✓ Data format is valid Parquet

### Manual Validation

```sql
-- Count rows by day
SELECT year, month, day, COUNT(*) as row_count
FROM workflows
GROUP BY year, month, day
ORDER BY year DESC, month DESC, day DESC
LIMIT 10;

-- Check for gaps
SELECT DISTINCT year, month, day
FROM workflows
ORDER BY year, month, day;
```

## Troubleshooting

### Issue: Out of Memory

**Symptoms**: Python process killed during export

**Solutions**:
1. Reduce `ETL_BATCH_SIZE`
2. Increase worker memory
3. Process tables sequentially

### Issue: Slow Exports

**Symptoms**: ETL takes >2 hours

**Solutions**:
1. Add database indexes
2. Increase batch size
3. Use faster storage class
4. Parallel table exports

### Issue: Data Inconsistency

**Symptoms**: Row counts don't match

**Solutions**:
1. Check time zones (UTC vs local)
2. Verify date filters
3. Re-run ETL for affected dates

## Best Practices

1. **Always partition by date** for efficient queries
2. **Run ETL during off-peak hours** (2-4 AM)
3. **Monitor execution times** for performance regression
4. **Keep backups** of ETL scripts
5. **Version control** configuration changes
6. **Test in dev** before prod changes
7. **Document** any custom transformations

## Cost Considerations

### Data Transfer Costs

- **PostgreSQL → EC2**: Free (same region)
- **EC2 → S3**: Free
- **S3 Storage**: $0.023/GB/month (Standard)

### Processing Costs

- **ETL Execution**: GitHub Actions (free for public repos)
- **Glue Crawler**: $0.44/DPU-hour (minimal)
- **Athena Queries**: $5/TB scanned

**Monthly Estimate** (100GB data): ~$2-3

## Security

### Credentials Management

- Use AWS IAM roles (not access keys)
- Store secrets in GitHub Secrets
- Rotate credentials regularly
- Use least privilege principle

### Data Encryption

- **At rest**: S3 AES-256 encryption
- **In transit**: TLS 1.3
- **PostgreSQL**: SSL connections

## Related Documentation

- [Athena Setup Guide](./ATHENA_SETUP.md)
- [Analytics Guide](./ANALYTICS_GUIDE.md)
- [Architecture Overview](./HYBRID_ARCHITECTURE.md)
- [Infrastructure Guide](../infrastructure/README.md)
