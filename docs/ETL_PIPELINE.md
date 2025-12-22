# ETL Pipeline Documentation

## Overview

The ETL (Extract, Transform, Load) pipeline exports data from PostgreSQL to AWS S3 in Parquet format for analytics with Athena.

## Pipeline Architecture

```
PostgreSQL → Python Script → Parquet Files → S3 Data Lake → Athena
```

## Components

### 1. Export Script (`export_to_s3.py`)

Main script that handles data extraction and upload.

**Features**:
- Incremental and full export modes
- Automatic partitioning by date
- Parquet format with Snappy compression
- Retry logic for S3 uploads
- Detailed logging
- Error handling

**Usage**:

```bash
# Export yesterday's data (incremental)
python export_to_s3.py

# Export specific date
python export_to_s3.py --date 2025-12-22

# Full export (all data)
python export_to_s3.py --mode full

# Export specific table
python export_to_s3.py --table invoices --date 2025-12-22
```

### 2. Athena Setup (`athena_setup.py`)

Script to initialize Athena tables and validate setup.

**Features**:
- Create Glue database
- Create all tables with partition projection
- Validate table accessibility
- Repair partitions if needed

**Usage**:

```bash
# Setup all tables
python athena_setup.py

# Repair partitions for a specific table
python -c "
from athena_setup import AthenaSetup
setup = AthenaSetup()
setup.repair_partitions('invoices')
"
```

## Export Modes

### Incremental Export (Default)

Exports only data created on the specified date.

**Pros**:
- Fast execution
- Minimal database load
- Cost-effective

**Cons**:
- Doesn't capture updates
- Requires daily execution

**SQL Query**:
```sql
SELECT * FROM invoices
WHERE DATE(created_at) = '2025-12-22'
```

### Full Export

Exports all data in the table.

**Pros**:
- Complete dataset
- Captures all updates
- Good for initial load

**Cons**:
- Slow execution
- High database load
- More expensive

**SQL Query**:
```sql
SELECT * FROM invoices
```

## Data Partitioning

Data is partitioned by date for query performance:

```
s3://bucket/billing-data/invoices/
  ├── year=2025/
  │   ├── month=01/
  │   │   ├── day=01/
  │   │   │   └── invoices_20250101.parquet
  │   │   ├── day=02/
  │   │   └── day=03/
  │   └── month=02/
  └── year=2024/
```

**Benefits**:
- **Query performance**: Only scan relevant partitions
- **Cost reduction**: Athena charges by data scanned
- **Organization**: Clear data structure

## Schedule

The ETL pipeline runs automatically via GitHub Actions:

- **Schedule**: Daily at 2:00 AM UTC
- **Trigger**: GitHub Actions workflow
- **Data**: Previous day's data
- **Mode**: Incremental

### Manual Execution

Use the convenience script:

```bash
# Run for yesterday
./scripts/run_etl.sh

# Run for specific date
./scripts/run_etl.sh 2025-12-22

# Full export for a date
./scripts/run_etl.sh 2025-12-22 full
```

## Error Handling

### Database Connection Errors

**Error**: `psycopg2.OperationalError: could not connect`

**Solutions**:
1. Check database host and credentials
2. Verify network connectivity
3. Check firewall rules
4. Verify database is running

### S3 Upload Errors

**Error**: `ClientError: Access Denied`

**Solutions**:
1. Verify AWS credentials
2. Check IAM permissions
3. Verify bucket exists
4. Check bucket region

**Retry Logic**:
- Automatic retry: 3 attempts
- Exponential backoff
- Detailed error logging

### Out of Memory

**Error**: `MemoryError` when exporting large tables

**Solutions**:
1. Use incremental mode instead of full
2. Increase system memory
3. Export in smaller batches
4. Consider streaming approach

## Monitoring

### CloudWatch Metrics

The pipeline sends metrics to CloudWatch:

- `DataExportSuccess`: 1 when successful
- `DataExportFailure`: 1 when failed
- Namespace: `Tokyo-IA/ETL`

### Logs

Logs are available in:
- **Local**: Console output with timestamps
- **GitHub Actions**: Workflow run logs
- **CloudWatch**: `/aws/tokyo-ia/etl/dev`

### Log Levels

```python
# INFO: Normal operations
logger.info("Successfully exported 1000 rows")

# WARNING: Non-fatal issues
logger.warning("No data found for date")

# ERROR: Failures
logger.error("Failed to upload to S3")
```

## Validation

After each ETL run, validate the export:

```bash
python scripts/validate_data.py
```

This checks:
- Files exist in S3
- File sizes are reasonable
- All tables have data
- Athena connectivity

## Performance

### Typical Performance

| Table | Rows | Export Time | File Size |
|-------|------|-------------|-----------|
| invoices | 10,000 | 30s | 2 MB |
| transactions | 20,000 | 45s | 3 MB |
| users | 5,000 | 15s | 1 MB |
| subscriptions | 1,000 | 10s | 500 KB |

**Total**: ~100s for all tables

### Optimization Tips

1. **Incremental exports**: Much faster than full
2. **Parallel exports**: Export tables in parallel (future)
3. **Batch size**: Adjust row_group_size in config
4. **Compression**: Snappy is fast, Gzip is smaller
5. **Partitioning**: Always partition by date

## Data Quality

### Schema Validation

Tables have defined schemas in `athena_setup.py`. Data is validated during upload:

- Correct data types
- Required columns present
- Timestamp formats

### Null Handling

- PostgreSQL NULLs → Parquet NULLs
- Empty strings → Empty strings (not NULL)
- Missing columns → NULL

## Troubleshooting

### No Data Exported

**Symptoms**: "No data found for table X on date Y"

**Causes**:
1. No data created on that date
2. Wrong date format
3. Wrong timestamp column

**Solutions**:
1. Check database: `SELECT COUNT(*) FROM invoices WHERE DATE(created_at) = '2025-12-22'`
2. Verify date format: YYYY-MM-DD
3. Check `created_at` column exists

### Partition Not Found

**Symptoms**: Athena query returns no results

**Causes**:
1. Partitions not created
2. Wrong S3 path
3. Partition projection misconfigured

**Solutions**:
1. Run partition repair: `python athena_setup.py`
2. Verify S3 path structure
3. Check table properties in Glue

### Slow Exports

**Symptoms**: Exports take &gt;5 minutes

**Causes**:
1. Large dataset
2. Full export mode
3. Database performance

**Solutions**:
1. Use incremental mode
2. Add indexes on `created_at`
3. Optimize database queries
4. Consider parallel exports

## Best Practices

1. **Always use incremental mode** for daily runs
2. **Run full exports** only for initial load or recovery
3. **Validate data** after each run
4. **Monitor CloudWatch** for failures
5. **Keep export history** for audit purposes
6. **Test locally** before deploying changes
7. **Use partitioning** in all queries
8. **Document schema changes**

## Future Improvements

1. **Real-time streaming**: Use AWS DMS or Debezium
2. **Parallel processing**: Export tables concurrently
3. **Delta updates**: Track and export only changes
4. **Data quality checks**: Automated validation
5. **Compression optimization**: Test different algorithms
6. **Incremental partitioning**: Handle late-arriving data
7. **Schema evolution**: Handle schema changes gracefully

## References

- [Pandas to Parquet](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_parquet.html)
- [PyArrow Documentation](https://arrow.apache.org/docs/python/)
- [AWS S3 Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html)
- [Parquet Format Spec](https://parquet.apache.org/docs/)
