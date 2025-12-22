output "data_lake_bucket" {
  description = "S3 bucket name for data lake"
  value       = aws_s3_bucket.data_lake.bucket
}

output "athena_results_bucket" {
  description = "S3 bucket name for Athena query results"
  value       = aws_s3_bucket.athena_results.bucket
}

output "glue_database_name" {
  description = "Glue database name"
  value       = aws_glue_catalog_database.tokyo_ia_billing.name
}

output "athena_workgroup_name" {
  description = "Athena workgroup name"
  value       = aws_athena_workgroup.tokyo_ia_analytics.name
}

output "etl_role_arn" {
  description = "IAM role ARN for ETL"
  value       = aws_iam_role.etl_role.arn
}

output "app_athena_role_arn" {
  description = "IAM role ARN for application Athena queries"
  value       = aws_iam_role.app_athena_role.arn
}

output "etl_log_group" {
  description = "CloudWatch log group for ETL"
  value       = aws_cloudwatch_log_group.etl_logs.name
}
