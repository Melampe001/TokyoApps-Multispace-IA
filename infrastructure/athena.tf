# S3 Bucket for Data Lake
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-data-lake-${var.environment}"

  tags = {
    Name        = "${var.project_name}-data-lake"
    Environment = var.environment
  }
}

# Enable versioning for data lake
resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Encryption for data lake
resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Lifecycle rules for data lake
resource "aws_s3_bucket_lifecycle_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    transition {
      days          = var.data_retention_days
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = var.archive_retention_days
      storage_class = "GLACIER"
    }
  }
}

# S3 Bucket for Athena Query Results
resource "aws_s3_bucket" "athena_results" {
  bucket = "${var.project_name}-athena-results-${var.environment}"

  tags = {
    Name        = "${var.project_name}-athena-results"
    Environment = var.environment
  }
}

# Encryption for Athena results
resource "aws_s3_bucket_server_side_encryption_configuration" "athena_results" {
  bucket = aws_s3_bucket.athena_results.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Lifecycle rules for Athena results (clean up after 30 days)
resource "aws_s3_bucket_lifecycle_configuration" "athena_results" {
  bucket = aws_s3_bucket.athena_results.id

  rule {
    id     = "cleanup-query-results"
    status = "Enabled"

    expiration {
      days = 30
    }
  }
}

# AWS Glue Database
resource "aws_glue_catalog_database" "tokyo_ia_billing" {
  name        = "${var.project_name}_billing_${var.environment}"
  description = "Tokyo-IA Billing Analytics Database"

  location_uri = "s3://${aws_s3_bucket.data_lake.bucket}/billing-data"
}

# Glue Table: Invoices
resource "aws_glue_catalog_table" "invoices" {
  database_name = aws_glue_catalog_database.tokyo_ia_billing.name
  name          = "invoices"

  table_type = "EXTERNAL_TABLE"

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.data_lake.bucket}/billing-data/invoices/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "serialization.format" = "1"
      }
    }

    columns {
      name = "invoice_id"
      type = "string"
    }

    columns {
      name = "user_id"
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
      name = "product_id"
      type = "string"
    }

    columns {
      name = "product_name"
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

    columns {
      name = "metadata"
      type = "string"
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

  parameters = {
    "parquet.compression"                  = "SNAPPY"
    "projection.enabled"                   = "true"
    "projection.year.type"                 = "integer"
    "projection.year.range"                = "2020,2030"
    "projection.month.type"                = "integer"
    "projection.month.range"               = "1,12"
    "projection.day.type"                  = "integer"
    "projection.day.range"                 = "1,31"
    "storage.location.template"            = "s3://${aws_s3_bucket.data_lake.bucket}/billing-data/invoices/year=$${year}/month=$${month}/day=$${day}"
  }
}

# Glue Table: Transactions
resource "aws_glue_catalog_table" "transactions" {
  database_name = aws_glue_catalog_database.tokyo_ia_billing.name
  name          = "transactions"

  table_type = "EXTERNAL_TABLE"

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.data_lake.bucket}/billing-data/transactions/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "serialization.format" = "1"
      }
    }

    columns {
      name = "transaction_id"
      type = "string"
    }

    columns {
      name = "invoice_id"
      type = "string"
    }

    columns {
      name = "user_id"
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
      name = "payment_method"
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
      name = "metadata"
      type = "string"
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

  parameters = {
    "parquet.compression"                  = "SNAPPY"
    "projection.enabled"                   = "true"
    "projection.year.type"                 = "integer"
    "projection.year.range"                = "2020,2030"
    "projection.month.type"                = "integer"
    "projection.month.range"               = "1,12"
    "projection.day.type"                  = "integer"
    "projection.day.range"                 = "1,31"
    "storage.location.template"            = "s3://${aws_s3_bucket.data_lake.bucket}/billing-data/transactions/year=$${year}/month=$${month}/day=$${day}"
  }
}

# Athena Workgroup
resource "aws_athena_workgroup" "tokyo_ia_analytics" {
  name        = "${var.project_name}-analytics-${var.environment}"
  description = "Workgroup for Tokyo-IA analytics queries"

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true

    result_configuration {
      output_location = "s3://${aws_s3_bucket.athena_results.bucket}/"

      encryption_configuration {
        encryption_option = "SSE_S3"
      }
    }

    engine_version {
      selected_engine_version = "AUTO"
    }
  }

  tags = {
    Name        = "${var.project_name}-analytics-workgroup"
    Environment = var.environment
  }
}

# CloudWatch Log Group for ETL
resource "aws_cloudwatch_log_group" "etl_logs" {
  name              = "/aws/${var.project_name}/etl/${var.environment}"
  retention_in_days = 30

  tags = {
    Name        = "${var.project_name}-etl-logs"
    Environment = var.environment
  }
}
