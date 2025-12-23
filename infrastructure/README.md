# Tokyo-IA Infrastructure
# Hybrid PostgreSQL + AWS Athena Analytics Architecture

This directory contains Terraform configuration for deploying the analytics infrastructure.

## Prerequisites

- Terraform >= 1.5.0
- AWS CLI configured with appropriate credentials
- AWS account with permissions to create S3, Athena, Glue, and IAM resources

## Quick Start

### 1. Initialize Terraform

```bash
cd infrastructure
terraform init
```

### 2. Review Configuration

```bash
# Create a terraform.tfvars file
cat > terraform.tfvars <<EOF
environment  = "dev"
aws_region   = "us-east-1"
project_name = "tokyo-ia"
EOF
```

### 3. Plan Deployment

```bash
terraform plan
```

### 4. Apply Configuration

```bash
terraform apply
```

## Configuration

### Variables

Key variables that can be customized:

- `environment`: Environment name (dev, staging, prod)
- `aws_region`: AWS region for deployment
- `project_name`: Project name for resource naming
- `data_retention_days`: Days before moving data to Glacier
- `data_deletion_days`: Days before permanent deletion

See `variables.tf` for all available options.

### Outputs

After successful deployment, Terraform will output:

- S3 bucket names (data lake, athena results, etl artifacts)
- Athena database and workgroup names
- IAM role ARNs for ETL and Athena users
- Glue crawler name

## Resource Overview

### S3 Buckets

1. **Data Lake** (`tokyo-ia-data-lake-{env}`)
   - Stores historical data in Parquet format
   - Partitioned by year/month/day
   - Lifecycle: Transition to Glacier after 90 days
   - Encryption: AES256
   - Versioning: Enabled

2. **Athena Results** (`tokyo-ia-athena-results-{env}`)
   - Stores query results
   - Auto-cleanup after 7 days
   - Encryption: AES256

3. **ETL Artifacts** (`tokyo-ia-etl-artifacts-{env}`)
   - Stores ETL scripts and logs
   - Log retention: 30 days

### Athena

- **Workgroup**: Configured with result encryption and CloudWatch metrics
- **Named Queries**: Pre-configured queries for common analytics operations
- **Database**: Glue catalog database for table metadata

### Glue

- **Crawler**: Automatic schema discovery from S3 data
- **Database**: Catalog database for table metadata
- **Classifier**: Parquet file classifier with Snappy compression

### IAM

1. **ETL Role**: For GitHub Actions to execute ETL pipeline
2. **Athena User Role**: For Go services to query Athena
3. **Glue Crawler Role**: For automatic schema discovery

## Multi-Environment Setup

To deploy multiple environments:

```bash
# Development
terraform workspace new dev
terraform apply -var="environment=dev"

# Staging
terraform workspace new staging
terraform apply -var="environment=staging"

# Production
terraform workspace new prod
terraform apply -var="environment=prod"
```

## Security

- All S3 buckets have public access blocked
- Encryption at rest enabled for all buckets
- IAM roles follow principle of least privilege
- HTTPS required for all API calls

## Cost Optimization

- Lifecycle policies move old data to Glacier
- Query results are automatically cleaned up
- Parquet format with Snappy compression (~75% size reduction)
- Athena workgroup enforces result caching

## Maintenance

### Update Glue Schema

```bash
aws glue start-crawler --name tokyo-ia-analytics-crawler-dev
```

### View Terraform State

```bash
terraform show
```

### Destroy Resources

```bash
terraform destroy
```

**Warning**: This will delete all data in S3 buckets!

## Troubleshooting

### Issue: Terraform fails to create resources

**Solution**: Verify AWS credentials and permissions

```bash
aws sts get-caller-identity
```

### Issue: S3 bucket already exists

**Solution**: Bucket names must be globally unique. Change `project_name` or `environment` in variables.

### Issue: IAM role assumption fails

**Solution**: Verify OIDC provider is configured for GitHub Actions

## Integration

After deployment, update your application configuration:

```bash
# Get outputs
terraform output -json > ../config/terraform-outputs.json

# Or set environment variables
export S3_DATA_LAKE_BUCKET=$(terraform output -raw data_lake_bucket_name)
export ATHENA_DATABASE=$(terraform output -raw athena_database_name)
export ATHENA_WORKGROUP=$(terraform output -raw athena_workgroup_name)
```

## Next Steps

1. Configure GitHub Actions secrets with IAM role ARN
2. Run initial ETL to populate data lake
3. Verify Glue crawler discovers tables
4. Test Athena queries
5. Set up monitoring and alerts

## Support

For issues or questions, please refer to:
- [AWS Athena Documentation](https://docs.aws.amazon.com/athena/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- Project README.md
