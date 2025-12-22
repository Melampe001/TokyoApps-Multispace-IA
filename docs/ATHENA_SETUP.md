# AWS Athena Setup Guide

Complete step-by-step guide for setting up the Athena analytics infrastructure.

## Prerequisites

- AWS Account with admin access
- AWS CLI configured (`aws configure`)
- Terraform >= 1.5.0 (for infrastructure)
- Python 3.11+ (for ETL)
- PostgreSQL database with Tokyo-IA data
- GitHub repository access (for CI/CD)

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA

# 2. Copy environment template
cp .env.example .env

# 3. Edit .env with your configuration
nano .env

# 4. Run setup script
chmod +x scripts/setup_athena.sh
./scripts/setup_athena.sh
```

That's it! The script will:
- Validate AWS credentials
- Create S3 buckets
- Apply Terraform infrastructure
- Set up Athena tables
- Run initial ETL (optional)

### Option 2: Manual Setup

Follow the detailed steps below for manual configuration.

## Step 1: Configure Environment

### 1.1 Create Configuration File

```bash
cp .env.example .env
```

### 1.2 Edit Configuration

```env
# Required fields
DB_HOST=your-postgres-host.com
DB_NAME=tokyo_ia
DB_USER=your_db_user
DB_PASSWORD=your_db_password

AWS_REGION=us-east-1
S3_DATA_LAKE_BUCKET=tokyo-ia-data-lake-dev
S3_ATHENA_RESULTS_BUCKET=tokyo-ia-athena-results-dev
ATHENA_DATABASE=tokyo_ia_billing_dev
```

## Step 2: Deploy Infrastructure with Terraform

### 2.1 Initialize Terraform

```bash
cd infrastructure
terraform init
```

### 2.2 Review Plan

```bash
terraform plan
```

Expected resources:
- 3 S3 buckets (data lake, results, artifacts)
- 1 Glue database
- 1 Glue crawler
- 1 Athena workgroup
- 3 IAM roles (ETL, Athena user, Glue)

### 2.3 Apply Infrastructure

```bash
terraform apply
```

Type `yes` to confirm.

### 2.4 Save Outputs

```bash
terraform output -json > ../config/terraform-outputs.json
```

## Step 3: Install Python Dependencies

```bash
cd ..
pip install -r python/etl/requirements.txt
```

Dependencies:
- psycopg2-binary (PostgreSQL)
- boto3 (AWS SDK)
- pandas (Data processing)
- pyarrow (Parquet format)
- python-dotenv (Configuration)

## Step 4: Create Athena Tables

### 4.1 Using Python Script (Recommended)

```bash
python python/etl/athena_setup.py
```

This creates:
- Glue database
- 5 external tables (workflows, agent_tasks, etc.)
- Partitions setup

### 4.2 Using SQL Directly

Alternative: Run SQL from Athena console:

```bash
# Copy table definitions
cat config/athena/tables.sql
```

Paste into Athena query editor and execute.

## Step 5: Run Initial ETL

### 5.1 Test Connection

```bash
python python/etl/config.py
```

Should print configuration without errors.

### 5.2 Export Yesterday's Data

```bash
python python/etl/export_to_s3.py
```

This exports data from yesterday to S3.

### 5.3 Verify Data in S3

```bash
aws s3 ls s3://tokyo-ia-data-lake-dev/ --recursive
```

Expected structure:
```
workflows/year=2024/month=12/day=22/data.parquet
agent_tasks/year=2024/month=12/day=22/data.parquet
...
```

### 5.4 Update Partitions

```bash
python python/etl/athena_setup.py
```

## Step 6: Verify Setup

### 6.1 Check Tables in Athena

```bash
aws athena list-table-metadata \
  --catalog-name AwsDataCatalog \
  --database-name tokyo_ia_billing_dev
```

Should list 5 tables.

### 6.2 Run Test Query

In Athena console or using AWS CLI:

```sql
SELECT COUNT(*) as total_workflows
FROM workflows
WHERE year = 2024 AND month = 12;
```

### 6.3 Check Glue Crawler

```bash
aws glue get-crawler --name tokyo-ia-analytics-crawler-dev
```

## Step 7: Setup GitHub Actions

### 7.1 Create GitHub Secrets

Go to: Settings → Secrets and variables → Actions

Add these secrets:
```
AWS_ETL_ROLE_ARN=arn:aws:iam::ACCOUNT:role/tokyo-ia-etl-role-dev
DB_HOST=your-db-host
DB_PORT=5432
DB_NAME=tokyo_ia
DB_USER=db_user
DB_PASSWORD=db_password
S3_DATA_LAKE_BUCKET=tokyo-ia-data-lake-dev
S3_ATHENA_RESULTS_BUCKET=tokyo-ia-athena-results-dev
ATHENA_DATABASE=tokyo_ia_billing_dev
ATHENA_WORKGROUP=tokyo-ia-dev
GLUE_CRAWLER_NAME=tokyo-ia-analytics-crawler-dev
```

### 7.2 Enable Workflows

Workflows are in `.github/workflows/`:
- `data-pipeline.yml` - Daily ETL (2 AM UTC)
- `infrastructure.yml` - Terraform management
- `athena-queries.yml` - Query validation

### 7.3 Test Manual Run

Go to: Actions → Data Pipeline - ETL → Run workflow

## Step 8: Go Analytics Client Setup

### 8.1 Update Application Config

```go
import "github.com/Melampe001/Tokyo-IA/lib/analytics"

cfg := analytics.AthenaConfig{
    Region:       "us-east-1",
    Database:     "tokyo_ia_billing_dev",
    OutputBucket: "tokyo-ia-athena-results-dev",
    Workgroup:    "tokyo-ia-dev",
}

client, err := analytics.NewAthenaClient(context.Background(), cfg)
```

### 8.2 Run Test Query

```go
metrics, err := client.GetWorkflowMetrics(ctx, 2024, 12, 1, 31)
if err != nil {
    log.Fatal(err)
}

for _, m := range metrics {
    fmt.Printf("Date: %v, Workflows: %d, Cost: $%.2f\n",
        m.Date, m.TotalWorkflows, m.TotalCostUSD)
}
```

## Troubleshooting

### Issue: AWS Credentials Invalid

```bash
aws sts get-caller-identity
```

If fails, reconfigure:
```bash
aws configure
```

### Issue: S3 Bucket Already Exists

Bucket names must be globally unique. Change in `.env`:
```
S3_DATA_LAKE_BUCKET=tokyo-ia-data-lake-dev-YOURNAME
```

### Issue: Terraform State Lock

```bash
cd infrastructure
terraform force-unlock LOCK_ID
```

### Issue: No Data in Athena

Check partitions:
```sql
SHOW PARTITIONS workflows;
```

Repair if needed:
```sql
MSCK REPAIR TABLE workflows;
```

### Issue: ETL Fails with Database Connection

1. Check PostgreSQL accessibility
2. Verify credentials in `.env`
3. Test connection:
```bash
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT 1"
```

### Issue: Athena Query Times Out

- Reduce date range
- Add partition filters
- Check query complexity

## Cost Management

### Monitor Costs

```bash
# Check S3 storage
aws s3 ls s3://tokyo-ia-data-lake-dev --recursive --summarize

# Check Athena query costs
aws athena list-query-executions --max-results 50
```

### Set Budget Alerts

Create AWS Budget for:
- S3 storage: Alert at $10/month
- Athena queries: Alert at $20/month

### Optimize Queries

Always use partition filters:
```sql
-- Good (uses partitions)
SELECT * FROM workflows
WHERE year = 2024 AND month = 12 AND day = 22;

-- Bad (scans all data)
SELECT * FROM workflows
WHERE created_at >= '2024-12-22';
```

## Next Steps

1. ✅ Setup complete! Now explore:
   - [ETL Pipeline Documentation](./ETL_PIPELINE.md)
   - [Analytics Guide](./ANALYTICS_GUIDE.md)
   - [Architecture Overview](./HYBRID_ARCHITECTURE.md)

2. Schedule regular backfills for historical data:
```bash
python scripts/backfill_data.py --start-date 2024-01-01 --end-date 2024-12-22
```

3. Set up monitoring dashboards

4. Configure QuickSight for business intelligence

## Support

- Issues: [GitHub Issues](https://github.com/Melampe001/Tokyo-IA/issues)
- Documentation: [README.md](../README.md)
- AWS Support: [AWS Console](https://console.aws.amazon.com/support)
