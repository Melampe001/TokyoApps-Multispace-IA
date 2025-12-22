# S3 Bucket for Data Lake
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-data-lake-${var.environment}"

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-data-lake-${var.environment}"
      Environment = var.environment
      Purpose     = "Data Lake for historical analytics"
    }
  )
}

# Enable versioning for data lake
resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Disabled"
  }
}

# Enable encryption for data lake
resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}

# Block public access for data lake
resource "aws_s3_bucket_public_access_block" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Lifecycle policy for data lake
resource "aws_s3_bucket_lifecycle_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    id     = "transition-to-glacier"
    status = "Enabled"

    transition {
      days          = var.data_retention_days
      storage_class = "GLACIER"
    }

    expiration {
      days = var.data_deletion_days
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "GLACIER"
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}

# S3 Bucket for Athena query results
resource "aws_s3_bucket" "athena_results" {
  bucket = "${var.project_name}-athena-results-${var.environment}"

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-athena-results-${var.environment}"
      Environment = var.environment
      Purpose     = "Athena query results"
    }
  )
}

# Enable versioning for Athena results
resource "aws_s3_bucket_versioning" "athena_results" {
  bucket = aws_s3_bucket.athena_results.id

  versioning_configuration {
    status = "Disabled"
  }
}

# Enable encryption for Athena results
resource "aws_s3_bucket_server_side_encryption_configuration" "athena_results" {
  bucket = aws_s3_bucket.athena_results.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}

# Block public access for Athena results
resource "aws_s3_bucket_public_access_block" "athena_results" {
  bucket = aws_s3_bucket.athena_results.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Lifecycle policy for Athena results - clean up old query results
resource "aws_s3_bucket_lifecycle_configuration" "athena_results" {
  bucket = aws_s3_bucket.athena_results.id

  rule {
    id     = "cleanup-query-results"
    status = "Enabled"

    expiration {
      days = var.query_results_retention_days
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 1
    }
  }
}

# S3 Bucket for ETL scripts and logs (optional)
resource "aws_s3_bucket" "etl_artifacts" {
  bucket = "${var.project_name}-etl-artifacts-${var.environment}"

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-etl-artifacts-${var.environment}"
      Environment = var.environment
      Purpose     = "ETL scripts and execution logs"
    }
  )
}

# Enable encryption for ETL artifacts
resource "aws_s3_bucket_server_side_encryption_configuration" "etl_artifacts" {
  bucket = aws_s3_bucket.etl_artifacts.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}

# Block public access for ETL artifacts
resource "aws_s3_bucket_public_access_block" "etl_artifacts" {
  bucket = aws_s3_bucket.etl_artifacts.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Lifecycle policy for ETL artifacts
resource "aws_s3_bucket_lifecycle_configuration" "etl_artifacts" {
  bucket = aws_s3_bucket.etl_artifacts.id

  rule {
    id     = "cleanup-old-logs"
    status = "Enabled"

    filter {
      prefix = "logs/"
    }

    expiration {
      days = var.etl_retention_days
    }
  }
}
