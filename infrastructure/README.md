# Infrastructure

This directory contains Terraform configurations for deploying the hybrid data architecture.

## Overview

The infrastructure includes:
- **S3 Buckets**: Data lake and Athena query results
- **AWS Glue**: Data catalog with tables and partitions
- **AWS Athena**: Workgroup for analytics queries
- **IAM**: Roles and policies for ETL and application access
- **CloudWatch**: Log groups for monitoring

## Prerequisites

- Terraform >= 1.6.0
- AWS CLI configured with credentials
- Appropriate AWS permissions (see IAM requirements below)

## Quick Start

1. **Copy example variables**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Edit terraform.tfvars** with your values:
   ```hcl
   environment = "dev"
   aws_region  = "us-east-1"
   project_name = "tokyo-ia"
   ```

3. **Initialize Terraform**:
   ```bash
   terraform init
   ```

4. **Review the plan**:
   ```bash
   terraform plan
   ```

5. **Apply infrastructure**:
   ```bash
   terraform apply
   ```

6. **Save outputs**:
   ```bash
   terraform output -json > outputs.json
   ```

## Files

- **main.tf**: Provider configuration
- **variables.tf**: Input variables
- **athena.tf**: S3, Glue, and Athena resources
- **iam.tf**: IAM roles and policies
- **outputs.tf**: Output values
- **terraform.tfvars.example**: Example variables file

## Resources Created

### S3 Buckets

1. **Data Lake**: `tokyo-ia-data-lake-{environment}`
   - Versioning enabled
   - SSE-S3 encryption
   - Lifecycle policies for archival

2. **Query Results**: `tokyo-ia-athena-results-{environment}`
   - SSE-S3 encryption
   - 30-day expiration

### AWS Glue

- **Database**: `tokyo_ia_billing_{environment}`
- **Tables**: invoices, transactions, users, subscriptions
- **Partition Projection**: Enabled for all tables

### AWS Athena

- **Workgroup**: `tokyo-ia-analytics-{environment}`
- Result caching enabled
- CloudWatch metrics enabled

### IAM

- **ETL Role**: For data export to S3
- **App Role**: For Athena queries from applications

## IAM Permissions Required

To deploy this infrastructure, your AWS user/role needs:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:CreateBucket",
        "s3:PutBucketPolicy",
        "s3:PutBucketVersioning",
        "s3:PutEncryptionConfiguration",
        "s3:PutLifecycleConfiguration",
        "glue:CreateDatabase",
        "glue:CreateTable",
        "athena:CreateWorkGroup",
        "iam:CreateRole",
        "iam:CreatePolicy",
        "iam:AttachRolePolicy",
        "logs:CreateLogGroup"
      ],
      "Resource": "*"
    }
  ]
}
```

## Environments

The infrastructure supports multiple environments via the `environment` variable:

- `dev`: Development environment
- `staging`: Staging environment
- `prod`: Production environment

Each environment creates separate resources with the environment suffix.

## Cost Estimation

Monthly costs (approximate):

- **S3 Storage**: $0.023/GB (~$2.30 for 100GB)
- **Athena Queries**: $5/TB scanned (depends on usage)
- **Glue Catalog**: Free for first million objects
- **CloudWatch Logs**: $0.50/GB ingested

Total: **~$10-50/month** depending on usage

## State Management

For production, use remote state:

1. Create S3 bucket for state:
   ```bash
   aws s3 mb s3://tokyo-ia-terraform-state
   ```

2. Enable versioning:
   ```bash
   aws s3api put-bucket-versioning \
     --bucket tokyo-ia-terraform-state \
     --versioning-configuration Status=Enabled
   ```

3. Uncomment backend configuration in `main.tf`:
   ```hcl
   backend "s3" {
     bucket = "tokyo-ia-terraform-state"
     key    = "analytics/terraform.tfstate"
     region = "us-east-1"
   }
   ```

4. Re-initialize:
   ```bash
   terraform init -migrate-state
   ```

## Outputs

After applying, Terraform provides these outputs:

- `data_lake_bucket`: S3 bucket name for data
- `athena_results_bucket`: S3 bucket for query results
- `glue_database_name`: Glue database name
- `athena_workgroup_name`: Athena workgroup name
- `etl_role_arn`: IAM role ARN for ETL
- `app_athena_role_arn`: IAM role ARN for app queries

Use these values to configure your applications and ETL pipeline.

## Destroying Infrastructure

To remove all resources:

```bash
terraform destroy
```

**Warning**: This will delete all S3 buckets and data. Make backups first!

## Troubleshooting

### Error: Bucket already exists

The bucket names must be globally unique. Change the `project_name` or `environment` variable.

### Error: Access Denied

Check that your AWS credentials have sufficient permissions.

### State Lock

If you see "Error locking state", someone else is running Terraform. Wait or use:

```bash
terraform force-unlock <LOCK_ID>
```

## Best Practices

1. **Use remote state** for production
2. **Enable state locking** with DynamoDB
3. **Use workspaces** for multiple environments
4. **Tag all resources** for cost tracking
5. **Version control** all Terraform files
6. **Review plans** before applying
7. **Use modules** for reusable components

## Next Steps

After deploying infrastructure:

1. Update `.env` file with outputs
2. Configure GitHub Actions secrets
3. Run ETL pipeline: `./scripts/run_etl.sh`
4. Test Athena queries

See [ATHENA_SETUP.md](../docs/ATHENA_SETUP.md) for detailed setup instructions.
