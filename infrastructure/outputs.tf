output "data_lake_bucket_name" {
  description = "Name of the S3 data lake bucket"
  value       = aws_s3_bucket.data_lake.bucket
}

output "data_lake_bucket_arn" {
  description = "ARN of the S3 data lake bucket"
  value       = aws_s3_bucket.data_lake.arn
}

output "athena_results_bucket_name" {
  description = "Name of the Athena results bucket"
  value       = aws_s3_bucket.athena_results.bucket
}

output "athena_results_bucket_arn" {
  description = "ARN of the Athena results bucket"
  value       = aws_s3_bucket.athena_results.arn
}

output "etl_artifacts_bucket_name" {
  description = "Name of the ETL artifacts bucket"
  value       = aws_s3_bucket.etl_artifacts.bucket
}

output "athena_database_name" {
  description = "Name of the Athena/Glue database"
  value       = aws_glue_catalog_database.analytics.name
}

output "athena_workgroup_name" {
  description = "Name of the Athena workgroup"
  value       = aws_athena_workgroup.main.name
}

output "athena_workgroup_arn" {
  description = "ARN of the Athena workgroup"
  value       = aws_athena_workgroup.main.arn
}

output "glue_crawler_name" {
  description = "Name of the Glue crawler"
  value       = aws_glue_crawler.analytics.name
}

output "etl_role_arn" {
  description = "ARN of the IAM role for ETL execution"
  value       = aws_iam_role.etl_role.arn
}

output "athena_user_role_arn" {
  description = "ARN of the IAM role for Athena users"
  value       = aws_iam_role.athena_user_role.arn
}

output "athena_user_instance_profile_name" {
  description = "Name of the instance profile for Athena users"
  value       = aws_iam_instance_profile.athena_user.name
}

output "glue_crawler_role_arn" {
  description = "ARN of the IAM role for Glue crawler"
  value       = aws_iam_role.glue_crawler.arn
}

output "region" {
  description = "AWS region where resources are deployed"
  value       = var.aws_region
}

output "environment" {
  description = "Environment name"
  value       = var.environment
}

# Output for easy integration with application configuration
output "config_summary" {
  description = "Configuration summary for application integration"
  value = {
    region               = var.aws_region
    environment          = var.environment
    data_lake_bucket     = aws_s3_bucket.data_lake.bucket
    athena_results_bucket = aws_s3_bucket.athena_results.bucket
    athena_database      = aws_glue_catalog_database.analytics.name
    athena_workgroup     = aws_athena_workgroup.main.name
  }
}
