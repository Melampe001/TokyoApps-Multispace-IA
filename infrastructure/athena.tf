# AWS Athena Infrastructure for Tokyo-IA Data Lake
# This Terraform configuration creates the necessary AWS resources for querying
# data in S3 using Athena.

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Variables
variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "tokyo-ia"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

# S3 Bucket for Data Lake
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-data-lake-${var.environment}"
  
  tags = {
    Name        = "${var.project_name}-data-lake"
    Environment = var.environment
    Project     = var.project_name
  }
}

# S3 Bucket versioning
resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# S3 Bucket for Athena query results
resource "aws_s3_bucket" "athena_results" {
  bucket = "${var.project_name}-athena-results-${var.environment}"
  
  tags = {
    Name        = "${var.project_name}-athena-results"
    Environment = var.environment
    Project     = var.project_name
  }
}

# Lifecycle policy for query results (delete after 30 days)
resource "aws_s3_bucket_lifecycle_configuration" "athena_results" {
  bucket = aws_s3_bucket.athena_results.id
  
  rule {
    id     = "delete-old-results"
    status = "Enabled"
    
    expiration {
      days = 30
    }
  }
}

# Glue Catalog Database
resource "aws_glue_catalog_database" "tokyo_ia" {
  name = "${var.project_name}_billing_${var.environment}"
  
  description = "Tokyo-IA billing and analytics data"
}

# Glue Catalog Table: Invoices
resource "aws_glue_catalog_table" "invoices" {
  name          = "invoices"
  database_name = aws_glue_catalog_database.tokyo_ia.name
  
  table_type = "EXTERNAL_TABLE"
  
  parameters = {
    "classification"        = "parquet"
    "compressionType"       = "snappy"
    "typeOfData"           = "file"
    "parquet.compression"  = "SNAPPY"
  }
  
  storage_descriptor {
    location      = "s3://${aws_s3_bucket.data_lake.bucket}/data/invoices/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"
    
    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
      
      parameters = {
        "serialization.format" = "1"
      }
    }
    
    columns {
      name = "id"
      type = "string"
    }
    
    columns {
      name = "subscription_id"
      type = "string"
    }
    
    columns {
      name = "amount"
      type = "decimal(10,2)"
    }
    
    columns {
      name = "currency"
      type = "string"
    }
    
    columns {
      name = "status"
      type = "string"
    }
    
    columns {
      name = "created_at"
      type = "timestamp"
    }
    
    columns {
      name = "updated_at"
      type = "timestamp"
    }
  }
  
  partition_keys {
    name = "year"
    type = "int"
  }
  
  partition_keys {
    name = "month"
    type = "int"
  }
  
  partition_keys {
    name = "day"
    type = "int"
  }
}

# Glue Catalog Table: Transactions
resource "aws_glue_catalog_table" "transactions" {
  name          = "transactions"
  database_name = aws_glue_catalog_database.tokyo_ia.name
  
  table_type = "EXTERNAL_TABLE"
  
  parameters = {
    "classification"       = "parquet"
    "compressionType"      = "snappy"
    "parquet.compression" = "SNAPPY"
  }
  
  storage_descriptor {
    location      = "s3://${aws_s3_bucket.data_lake.bucket}/data/transactions/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"
    
    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }
    
    columns {
      name = "id"
      type = "string"
    }
    
    columns {
      name = "invoice_id"
      type = "string"
    }
    
    columns {
      name = "amount"
      type = "decimal(10,2)"
    }
    
    columns {
      name = "type"
      type = "string"
    }
    
    columns {
      name = "status"
      type = "string"
    }
    
    columns {
      name = "created_at"
      type = "timestamp"
    }
  }
  
  partition_keys {
    name = "year"
    type = "int"
  }
  
  partition_keys {
    name = "month"
    type = "int"
  }
  
  partition_keys {
    name = "day"
    type = "int"
  }
}

# Glue Catalog Table: Subscriptions
resource "aws_glue_catalog_table" "subscriptions" {
  name          = "subscriptions"
  database_name = aws_glue_catalog_database.tokyo_ia.name
  
  table_type = "EXTERNAL_TABLE"
  
  parameters = {
    "classification"       = "parquet"
    "compressionType"      = "snappy"
    "parquet.compression" = "SNAPPY"
  }
  
  storage_descriptor {
    location      = "s3://${aws_s3_bucket.data_lake.bucket}/data/subscriptions/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"
    
    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }
    
    columns {
      name = "id"
      type = "string"
    }
    
    columns {
      name = "user_id"
      type = "string"
    }
    
    columns {
      name = "plan_name"
      type = "string"
    }
    
    columns {
      name = "status"
      type = "string"
    }
    
    columns {
      name = "created_at"
      type = "timestamp"
    }
    
    columns {
      name = "updated_at"
      type = "timestamp"
    }
  }
  
  partition_keys {
    name = "year"
    type = "int"
  }
  
  partition_keys {
    name = "month"
    type = "int"
  }
  
  partition_keys {
    name = "day"
    type = "int"
  }
}

# Athena Workgroup
resource "aws_athena_workgroup" "main" {
  name = "${var.project_name}-${var.environment}"
  
  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true
    
    result_configuration {
      output_location = "s3://${aws_s3_bucket.athena_results.bucket}/output/"
      
      encryption_configuration {
        encryption_option = "SSE_S3"
      }
    }
  }
  
  tags = {
    Name        = "${var.project_name}-workgroup"
    Environment = var.environment
    Project     = var.project_name
  }
}

# Outputs
output "data_lake_bucket" {
  description = "Data lake S3 bucket name"
  value       = aws_s3_bucket.data_lake.bucket
}

output "athena_results_bucket" {
  description = "Athena results S3 bucket name"
  value       = aws_s3_bucket.athena_results.bucket
}

output "glue_database_name" {
  description = "Glue catalog database name"
  value       = aws_glue_catalog_database.tokyo_ia.name
}

output "athena_workgroup_name" {
  description = "Athena workgroup name"
  value       = aws_athena_workgroup.main.name
}

output "data_lake_bucket_arn" {
  description = "Data lake S3 bucket ARN"
  value       = aws_s3_bucket.data_lake.arn
}
