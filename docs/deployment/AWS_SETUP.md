# AWS Setup Guide

This guide explains how to set up the AWS infrastructure for Tokyo-IA's data lake and analytics.

## Overview

The AWS infrastructure includes:
- S3 buckets for data lake and query results
- AWS Glue Catalog for table metadata
- AWS Athena for SQL queries
- IAM roles and policies

## Prerequisites

- AWS account
- AWS CLI installed and configured
- Terraform installed (v1.0+)
- Appropriate AWS permissions

## Setup Methods

Choose one of the following methods:

### Method 1: Terraform (Recommended)

Automated infrastructure provisioning using Infrastructure as Code.

### Method 2: Manual Console Setup

Step-by-step setup through AWS Console.

### Method 3: AWS CLI

Command-line setup using AWS CLI.

---

## Method 1: Terraform Setup

### Step 1: Install Terraform

```bash
# macOS
brew install terraform

# Linux
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verify installation
terraform version
```

### Step 2: Configure AWS Credentials

```bash
# Set environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"

# Or configure AWS CLI
aws configure
```

### Step 3: Initialize Terraform

```bash
cd infrastructure/
terraform init
```

### Step 4: Review Plan

```bash
terraform plan
```

Review the resources that will be created:
- 2 S3 buckets
- 1 Glue database
- 4 Glue tables (invoices, transactions, users, subscriptions)
- 1 Athena workgroup

### Step 5: Apply Configuration

```bash
terraform apply
```

Type `yes` when prompted.

### Step 6: Save Outputs

```bash
terraform output > ../config/aws-outputs.txt
```

Save these values for later use:
- `data_lake_bucket`
- `athena_results_bucket`
- `glue_database_name`
- `athena_workgroup_name`

---

## Method 2: Manual Console Setup

### Step 1: Create S3 Buckets

#### Data Lake Bucket

1. Go to [S3 Console](https://s3.console.aws.amazon.com/)
2. Click "Create bucket"
3. Bucket name: `tokyo-ia-data-lake-production`
4. Region: `us-east-1` (or your preferred region)
5. Enable "Bucket Versioning"
6. Enable "Default encryption" (SSE-S3)
7. Click "Create bucket"

#### Athena Results Bucket

1. Click "Create bucket"
2. Bucket name: `tokyo-ia-athena-results-production`
3. Same region as data lake
4. Enable "Default encryption"
5. Under "Lifecycle rules":
   - Create rule to delete objects after 30 days
6. Click "Create bucket"

### Step 2: Create Glue Database

1. Go to [AWS Glue Console](https://console.aws.amazon.com/glue/)
2. Click "Databases" in left sidebar
3. Click "Add database"
4. Database name: `tokyo_ia_billing_production`
5. Description: "Tokyo-IA billing and analytics data"
6. Click "Create"

### Step 3: Create Glue Tables

For each table (invoices, transactions, subscriptions, users):

1. Click "Tables" in left sidebar
2. Click "Add table"
3. Table name: e.g., `invoices`
4. Database: `tokyo_ia_billing_production`
5. Data location: `s3://tokyo-ia-data-lake-production/data/invoices/`
6. Data format: Parquet
7. Add columns:

**Invoices Table:**
- `id` - string
- `subscription_id` - string
- `amount` - decimal(10,2)
- `currency` - string
- `status` - string
- `created_at` - timestamp
- `updated_at` - timestamp

8. Add partition keys:
- `year` - int
- `month` - int
- `day` - int

9. Click "Create"

Repeat for other tables with appropriate columns.

### Step 4: Create Athena Workgroup

1. Go to [Athena Console](https://console.aws.amazon.com/athena/)
2. Click "Workgroups" in left sidebar
3. Click "Create workgroup"
4. Name: `tokyo-ia-production`
5. Query result location: `s3://tokyo-ia-athena-results-production/output/`
6. Enable "Override client-side settings"
7. Enable "Publish metrics to CloudWatch"
8. Encryption: SSE-S3
9. Click "Create workgroup"

### Step 5: Configure IAM Permissions

See [IAM Permissions](#iam-permissions) section below.

---

## Method 3: AWS CLI Setup

### Step 1: Create S3 Buckets

```bash
# Set variables
REGION="us-east-1"
DATA_BUCKET="tokyo-ia-data-lake-production"
RESULTS_BUCKET="tokyo-ia-athena-results-production"

# Create data lake bucket
aws s3 mb s3://$DATA_BUCKET --region $REGION

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket $DATA_BUCKET \
  --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket $DATA_BUCKET \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Create results bucket
aws s3 mb s3://$RESULTS_BUCKET --region $REGION

# Set lifecycle policy for results bucket
cat > lifecycle.json << EOF
{
  "Rules": [{
    "Id": "DeleteOldResults",
    "Status": "Enabled",
    "Expiration": { "Days": 30 }
  }]
}
EOF

aws s3api put-bucket-lifecycle-configuration \
  --bucket $RESULTS_BUCKET \
  --lifecycle-configuration file://lifecycle.json
```

### Step 2: Create Glue Database

```bash
aws glue create-database \
  --database-input '{
    "Name": "tokyo_ia_billing_production",
    "Description": "Tokyo-IA billing and analytics data"
  }'
```

### Step 3: Create Glue Tables

```bash
# Create invoices table
cat > invoices-table.json << EOF
{
  "Name": "invoices",
  "StorageDescriptor": {
    "Columns": [
      {"Name": "id", "Type": "string"},
      {"Name": "subscription_id", "Type": "string"},
      {"Name": "amount", "Type": "decimal(10,2)"},
      {"Name": "currency", "Type": "string"},
      {"Name": "status", "Type": "string"},
      {"Name": "created_at", "Type": "timestamp"},
      {"Name": "updated_at", "Type": "timestamp"}
    ],
    "Location": "s3://tokyo-ia-data-lake-production/data/invoices/",
    "InputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
    "OutputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
    "SerdeInfo": {
      "SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }
  },
  "PartitionKeys": [
    {"Name": "year", "Type": "int"},
    {"Name": "month", "Type": "int"},
    {"Name": "day", "Type": "int"}
  ]
}
EOF

aws glue create-table \
  --database-name tokyo_ia_billing_production \
  --table-input file://invoices-table.json
```

Repeat for other tables.

### Step 4: Create Athena Workgroup

```bash
aws athena create-work-group \
  --name tokyo-ia-production \
  --configuration '{
    "ResultConfigurationUpdates": {
      "OutputLocation": "s3://tokyo-ia-athena-results-production/output/",
      "EncryptionConfiguration": {
        "EncryptionOption": "SSE_S3"
      }
    },
    "EnforceWorkGroupConfiguration": true,
    "PublishCloudWatchMetricsEnabled": true
  }'
```

---

## IAM Permissions

### For ETL Export

Create IAM user or role with this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::tokyo-ia-data-lake-production",
        "arn:aws:s3:::tokyo-ia-data-lake-production/*"
      ]
    }
  ]
}
```

### For Athena Queries

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "athena:StartQueryExecution",
        "athena:GetQueryExecution",
        "athena:GetQueryResults",
        "athena:StopQueryExecution",
        "athena:GetWorkGroup"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::tokyo-ia-data-lake-production/*",
        "arn:aws:s3:::tokyo-ia-athena-results-production/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "glue:GetDatabase",
        "glue:GetTable",
        "glue:GetPartitions"
      ],
      "Resource": "*"
    }
  ]
}
```

## Environment Configuration

After setup, configure your environment:

```bash
# Add to .env or environment variables
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_REGION="us-east-1"
export S3_DATA_LAKE_BUCKET="tokyo-ia-data-lake-production"
export ATHENA_DATABASE="tokyo_ia_billing_production"
export ATHENA_WORKGROUP="tokyo-ia-production"
```

For GitHub Actions, add these as secrets:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `S3_DATA_LAKE_BUCKET`
- `ATHENA_DATABASE`

## Running the ETL Pipeline

### Manual Run

```bash
cd python/etl/
python3 export_to_s3.py
```

### Scheduled Run (Cron)

```bash
# Add to crontab
0 2 * * * cd /path/to/tokyo-ia && python3 python/etl/export_to_s3.py >> /var/log/etl.log 2>&1
```

### GitHub Actions

Create `.github/workflows/etl-export.yml`:

```yaml
name: ETL Export

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:

jobs:
  export:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install psycopg2-binary boto3 pandas pyarrow
      
      - name: Run ETL
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: ${{ secrets.AWS_REGION }}
          S3_DATA_LAKE_BUCKET: ${{ secrets.S3_DATA_LAKE_BUCKET }}
        run: python python/etl/export_to_s3.py
```

## Cost Estimation

### S3 Storage
- Data lake: ~$0.023/GB per month (Standard storage)
- Estimate: 100GB = $2.30/month

### Athena Queries
- $5 per TB of data scanned
- With Parquet + partitioning: ~$0.05-0.50 per query

### Glue Catalog
- First 1 million objects: Free
- Beyond that: $1 per 100,000 objects/month

**Estimated monthly cost:** $10-50 depending on usage

## Monitoring

### CloudWatch Metrics

View Athena metrics:
1. Go to CloudWatch Console
2. Select "Metrics"
3. Choose "Athena"
4. View:
   - DataScannedInBytes
   - EngineExecutionTime
   - QueryPlanningTime

### Cost Alerts

Create billing alert:
1. Go to CloudWatch Console
2. Create alarm for "EstimatedCharges"
3. Set threshold (e.g., $100/month)
4. Configure SNS notification

## Troubleshooting

### Issue: Insufficient Permissions

**Error:** "Access Denied" when exporting to S3

**Solution:**
1. Verify IAM policy includes s3:PutObject
2. Check bucket policy doesn't deny access
3. Ensure AWS credentials are correct

### Issue: Athena Query Fails

**Error:** "Table not found"

**Solution:**
1. Verify Glue database and tables exist
2. Check table location in S3 matches data
3. Run `MSCK REPAIR TABLE tablename` to discover partitions

### Issue: ETL Export Slow

**Solution:**
1. Check database query performance
2. Add indexes to PostgreSQL tables
3. Increase instance size if needed
4. Run export during off-peak hours

## Security Best Practices

1. **Enable encryption** on all S3 buckets
2. **Use IAM roles** instead of access keys when possible
3. **Enable S3 versioning** for data protection
4. **Restrict bucket access** using bucket policies
5. **Enable CloudTrail** for audit logging
6. **Rotate credentials** regularly
7. **Use VPC endpoints** for S3 access from EC2/ECS

## Cleanup (Destroy Infrastructure)

### Terraform

```bash
cd infrastructure/
terraform destroy
```

### Manual

1. Empty and delete S3 buckets
2. Delete Glue tables
3. Delete Glue database
4. Delete Athena workgroup
5. Delete IAM policies/roles

## Support

For issues or questions:
1. Check [troubleshooting section](#troubleshooting)
2. Review AWS documentation
3. Check CloudWatch logs
4. Open an issue in the Tokyo-IA repository

## Related Documentation

- [Athena Query Guide](../analytics/ATHENA_GUIDE.md)
- [ETL Pipeline](../../python/etl/export_to_s3.py)
- [Terraform Configuration](../../infrastructure/athena.tf)
