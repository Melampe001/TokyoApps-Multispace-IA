# Athena Setup Guide

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
3. **Terraform** >= 1.6.0 installed
4. **Python** 3.11+ installed
5. **Go** 1.23+ installed (for application integration)

## Step 1: Configure AWS Credentials

### Option A: Using AWS CLI

```bash
aws configure
```

Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `us-east-1`)
- Output format (e.g., `json`)

### Option B: Using Environment Variables

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"
```

### Option C: Using IAM Roles (Recommended for EC2/ECS)

If running on AWS infrastructure, attach an IAM role with the required permissions.

## Step 2: Create Configuration File

Create a `.env` file in the project root:

```bash
# PostgreSQL Configuration
DB_HOST=your-postgres-host.rds.amazonaws.com
DB_NAME=tokyo_ia
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_PORT=5432

# AWS S3 Configuration
S3_DATA_LAKE_BUCKET=tokyo-ia-data-lake-dev
AWS_REGION=us-east-1

# Athena Configuration
ATHENA_DATABASE=tokyo_ia_billing_dev
ATHENA_WORKGROUP=tokyo-ia-analytics-dev
ATHENA_OUTPUT_LOCATION=s3://tokyo-ia-athena-results-dev/
```

**⚠️ Important**: Never commit `.env` to git. It's already in `.gitignore`.

## Step 3: Deploy Infrastructure with Terraform

### Initialize Terraform

```bash
cd infrastructure
terraform init
```

### Review the Plan

```bash
terraform plan
```

This will show you all resources that will be created:
- 2 S3 buckets (data lake + query results)
- AWS Glue database and tables
- Athena workgroup
- IAM roles and policies
- CloudWatch log group

### Apply Infrastructure

```bash
terraform apply
```

Type `yes` to confirm.

### Save Outputs

```bash
terraform output -json > outputs.json
```

Update your `.env` file with the output values:

```bash
# Get bucket names from terraform output
export S3_DATA_LAKE_BUCKET=$(terraform output -raw data_lake_bucket)
export ATHENA_DATABASE=$(terraform output -raw glue_database_name)
export ATHENA_WORKGROUP=$(terraform output -raw athena_workgroup_name)
```

## Step 4: Install Python Dependencies

```bash
cd python/etl
pip install -r requirements.txt
```

Or using a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 5: Setup Athena Tables

Run the setup script to create Athena tables:

```bash
cd python/etl
python athena_setup.py
```

This will:
- Create the Glue database (if not exists)
- Create all tables: `invoices`, `transactions`, `users`, `subscriptions`
- Configure partition projection
- Validate table accessibility

## Step 6: Verify Installation

### Test Athena Connectivity

```bash
# Using AWS CLI
aws athena list-work-groups --region us-east-1
aws athena list-databases --catalog-name AwsDataCatalog --region us-east-1
```

### Run Test Query

```bash
cd python/etl
python -c "
from athena_setup import AthenaSetup
setup = AthenaSetup()
setup.validate_table('invoices')
"
```

### Test Go Client

```bash
cd lib/analytics
go test -v
```

## Step 7: Configure GitHub Actions Secrets

In your GitHub repository, go to Settings > Secrets > Actions and add:

```
AWS_ACCESS_KEY_ID=<your-access-key>
AWS_SECRET_ACCESS_KEY=<your-secret-key>
AWS_REGION=us-east-1

DB_HOST=<your-postgres-host>
DB_NAME=tokyo_ia
DB_USER=postgres
DB_PASSWORD=<your-db-password>

S3_DATA_LAKE_BUCKET=<from-terraform-output>
ATHENA_DATABASE=<from-terraform-output>
ATHENA_WORKGROUP=<from-terraform-output>
ATHENA_OUTPUT_LOCATION=s3://<athena-results-bucket>/
```

## Step 8: Run First ETL Export (Optional)

To test the ETL pipeline manually:

```bash
./scripts/run_etl.sh 2025-12-22 full
```

This will:
- Connect to PostgreSQL
- Export all tables for the specified date
- Upload to S3 in Parquet format
- Create partitions automatically

## Verification Checklist

- [ ] AWS credentials configured
- [ ] Terraform infrastructure deployed
- [ ] S3 buckets created and accessible
- [ ] Glue database and tables created
- [ ] Athena workgroup configured
- [ ] Python dependencies installed
- [ ] Athena tables validated
- [ ] Go tests passing
- [ ] GitHub Actions secrets configured
- [ ] First ETL run successful (optional)

## Troubleshooting

### Problem: "Access Denied" errors

**Solution**: Check IAM permissions. Ensure your user/role has:
- `s3:PutObject`, `s3:GetObject` on data lake bucket
- `athena:StartQueryExecution` on workgroup
- `glue:GetDatabase`, `glue:GetTable` permissions

### Problem: Terraform fails with "bucket already exists"

**Solution**: Either:
1. Change `project_name` or `environment` in `terraform.tfvars`
2. Import existing bucket: `terraform import aws_s3_bucket.data_lake bucket-name`

### Problem: Python import errors

**Solution**: Make sure you're in the right directory and dependencies are installed:
```bash
cd python/etl
pip install -r requirements.txt
```

### Problem: "No module named 'psycopg2'"

**Solution**: Install the binary package:
```bash
pip install psycopg2-binary
```

### Problem: Athena query returns no data

**Solution**: 
1. Check that data exists in S3: `aws s3 ls s3://your-bucket/billing-data/invoices/`
2. Run partition repair: See ETL_PIPELINE.md
3. Check partition projection configuration

## Next Steps

1. Read [ETL_PIPELINE.md](ETL_PIPELINE.md) to understand the data pipeline
2. Review [QUERIES_EXAMPLES.md](QUERIES_EXAMPLES.md) for query examples
3. Integrate the Go Athena client in your application
4. Set up monitoring and alerts

## Additional Resources

- [Terraform AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Athena Best Practices](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning.html)
- [Partition Projection](https://docs.aws.amazon.com/athena/latest/ug/partition-projection.html)
