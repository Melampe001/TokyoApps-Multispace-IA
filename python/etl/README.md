# ETL Pipeline

Python-based ETL pipeline for exporting PostgreSQL data to AWS S3/Athena.

## Overview

This ETL pipeline extracts data from PostgreSQL, transforms it to Parquet format, and loads it to S3 for analytics with Athena.

## Components

- **config.py**: Configuration management
- **export_to_s3.py**: Main export script
- **athena_setup.py**: Athena table setup
- **requirements.txt**: Python dependencies

## Installation

### Using pip

```bash
pip install -r requirements.txt
```

### Using virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Set these environment variables:

```bash
# PostgreSQL
export DB_HOST="localhost"
export DB_NAME="tokyo_ia"
export DB_USER="postgres"
export DB_PASSWORD="password"
export DB_PORT="5432"

# AWS
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_REGION="us-east-1"

# S3
export S3_DATA_LAKE_BUCKET="tokyo-ia-data-lake"

# Athena
export ATHENA_DATABASE="tokyo_ia_billing"
export ATHENA_WORKGROUP="tokyo-ia-analytics"
export ATHENA_OUTPUT_LOCATION="s3://tokyo-ia-athena-results/"
```

Or create a `.env` file (recommended).

## Usage

### Export Data

```bash
# Export yesterday's data (default)
python export_to_s3.py

# Export specific date
python export_to_s3.py --date 2025-12-22

# Full export
python export_to_s3.py --mode full

# Export specific table
python export_to_s3.py --table invoices --date 2025-12-22
```

### Setup Athena

```bash
# Create all tables
python athena_setup.py
```

## Export Modes

### Incremental (Default)

Exports only data created on the specified date:

```bash
python export_to_s3.py --date 2025-12-22 --mode incremental
```

- ✅ Fast
- ✅ Low database load
- ❌ Doesn't capture updates

### Full

Exports all data in the table:

```bash
python export_to_s3.py --date 2025-12-22 --mode full
```

- ✅ Complete dataset
- ✅ Captures updates
- ❌ Slow
- ❌ High database load

## Tables

The pipeline exports these tables:

1. **invoices**: Customer invoices
2. **transactions**: Payment transactions
3. **users**: User accounts
4. **subscriptions**: Subscription plans

## Output Format

Data is exported as Parquet files with:

- **Compression**: Snappy (fast, good compression)
- **Partitioning**: year/month/day
- **Schema**: Preserved from PostgreSQL

Example S3 structure:

```
s3://tokyo-ia-data-lake/
└── billing-data/
    ├── invoices/
    │   ├── year=2025/
    │   │   ├── month=12/
    │   │   │   ├── day=22/
    │   │   │   │   └── invoices_20251222.parquet
    │   │   │   └── day=23/
    │   │   └── month=11/
    │   └── year=2024/
    ├── transactions/
    ├── users/
    └── subscriptions/
```

## Logging

The scripts log to stdout with timestamps:

```
2025-12-22 10:30:00 - INFO - Starting export of table 'invoices'
2025-12-22 10:30:05 - INFO - Successfully exported 1000 rows
2025-12-22 10:30:10 - INFO - Uploaded to s3://bucket/path/file.parquet
```

## Error Handling

The pipeline includes:

- **Retry logic**: 3 attempts for S3 uploads
- **Connection pooling**: Efficient DB connections
- **Error logging**: Detailed error messages
- **Graceful failures**: Continue with other tables

## Performance

Typical performance:

| Table | Rows | Time | Size |
|-------|------|------|------|
| invoices | 10k | 30s | 2 MB |
| transactions | 20k | 45s | 3 MB |
| users | 5k | 15s | 1 MB |
| subscriptions | 1k | 10s | 500 KB |

## Testing

### Dry Run

Test without uploading:

```python
from export_to_s3 import PostgresToS3Exporter
from datetime import datetime

exporter = PostgresToS3Exporter(datetime(2025, 12, 22))
# Comment out upload in code for testing
```

### Validate Export

```bash
# Check if files exist
aws s3 ls s3://tokyo-ia-data-lake/billing-data/invoices/year=2025/month=12/day=22/

# Count rows in exported file
# (requires pandas and pyarrow)
python -c "
import pandas as pd
df = pd.read_parquet('s3://tokyo-ia-data-lake/billing-data/invoices/year=2025/month=12/day=22/invoices_20251222.parquet')
print(f'Rows: {len(df)}')
"
```

## Troubleshooting

### Connection Errors

```
psycopg2.OperationalError: could not connect to server
```

**Solutions**:
- Check DB_HOST and credentials
- Verify network connectivity
- Check firewall rules

### Memory Errors

```
MemoryError: Unable to allocate array
```

**Solutions**:
- Use incremental mode
- Process smaller date ranges
- Increase system memory

### S3 Upload Errors

```
botocore.exceptions.ClientError: Access Denied
```

**Solutions**:
- Check AWS credentials
- Verify IAM permissions
- Check bucket exists and region

### No Data Exported

```
WARNING - No data found for table 'invoices'
```

**Causes**:
- No data for that date
- Wrong timestamp column
- Incorrect date format

## Monitoring

Monitor ETL pipeline:

1. **CloudWatch Logs**: `/aws/tokyo-ia/etl/dev`
2. **CloudWatch Metrics**: `Tokyo-IA/ETL` namespace
3. **S3 Events**: Configure bucket notifications

## Automation

The ETL runs automatically via GitHub Actions:

- **Schedule**: Daily at 2 AM UTC
- **Trigger**: Push to main branch
- **Manual**: workflow_dispatch

See `.github/workflows/data-pipeline.yml`

## Best Practices

1. ✅ Use incremental mode for daily runs
2. ✅ Run full exports only for initial load
3. ✅ Monitor CloudWatch logs
4. ✅ Validate exports after each run
5. ✅ Keep export history for audit
6. ✅ Use connection pooling
7. ✅ Set appropriate timeouts

## Development

### Adding New Tables

1. Add table name to `TABLES_TO_EXPORT` in `config.py`
2. Add schema to `_get_table_schema()` in `athena_setup.py`
3. Test export: `python export_to_s3.py --table new_table`
4. Create Athena table: `python athena_setup.py`

### Modifying Schemas

1. Update schema in `athena_setup.py`
2. Drop and recreate table in Athena
3. Re-export data

## Security

- ⚠️ Never commit `.env` files
- ✅ Use IAM roles on AWS infrastructure
- ✅ Rotate credentials regularly
- ✅ Use least privilege permissions
- ✅ Enable encryption at rest

## Support

For issues or questions:

1. Check [ETL_PIPELINE.md](../../docs/ETL_PIPELINE.md) documentation
2. Review logs in CloudWatch
3. Check GitHub Issues
4. Contact the team

## References

- [Pandas Documentation](https://pandas.pydata.org/)
- [PyArrow Documentation](https://arrow.apache.org/docs/python/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
