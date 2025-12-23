# Glue Catalog Database
resource "aws_glue_catalog_database" "analytics" {
  name        = local.athena_database_name
  description = "Tokyo-IA Analytics Database for ${var.environment}"

  catalog_id = data.aws_caller_identity.current.account_id

  parameters = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# Glue Crawler IAM Role
resource "aws_iam_role" "glue_crawler" {
  name = "${var.project_name}-glue-crawler-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-glue-crawler-${var.environment}"
      Environment = var.environment
    }
  )
}

# Attach AWS managed policy for Glue Service
resource "aws_iam_role_policy_attachment" "glue_service" {
  role       = aws_iam_role.glue_crawler.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# Custom policy for S3 access
resource "aws_iam_role_policy" "glue_s3_access" {
  name = "${var.project_name}-glue-s3-access-${var.environment}"
  role = aws_iam_role.glue_crawler.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = [
          "${aws_s3_bucket.data_lake.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.data_lake.arn
        ]
      }
    ]
  })
}

# Glue Crawler for automatic schema discovery
resource "aws_glue_crawler" "analytics" {
  name          = "${var.project_name}-analytics-crawler-${var.environment}"
  role          = aws_iam_role.glue_crawler.arn
  database_name = aws_glue_catalog_database.analytics.name

  description = "Crawler for Tokyo-IA analytics data lake"

  s3_target {
    path = "s3://${aws_s3_bucket.data_lake.bucket}/workflows/"
  }

  s3_target {
    path = "s3://${aws_s3_bucket.data_lake.bucket}/agent_tasks/"
  }

  s3_target {
    path = "s3://${aws_s3_bucket.data_lake.bucket}/agent_metrics/"
  }

  s3_target {
    path = "s3://${aws_s3_bucket.data_lake.bucket}/agent_interactions/"
  }

  s3_target {
    path = "s3://${aws_s3_bucket.data_lake.bucket}/user_sessions/"
  }

  schedule = var.environment == "prod" ? "cron(0 3 * * ? *)" : null # Run at 3 AM daily in prod

  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "UPDATE_IN_DATABASE"
  }

  configuration = jsonencode({
    Version = 1.0
    CrawlerOutput = {
      Partitions = {
        AddOrUpdateBehavior = "InheritFromTable"
      }
    }
    Grouping = {
      TableGroupingPolicy = "CombineCompatibleSchemas"
    }
  })

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-analytics-crawler-${var.environment}"
      Environment = var.environment
    }
  )
}

# Glue Classifier for Parquet files
resource "aws_glue_classifier" "parquet" {
  name = "${var.project_name}-parquet-classifier-${var.environment}"

  parquet_classifier {
    compression = "SNAPPY"
  }
}

# Data source for current AWS account
data "aws_caller_identity" "current" {}

# Local values
locals {
  athena_database_name = var.athena_database_name != "" ? var.athena_database_name : "${var.project_name}_billing_${var.environment}"
}
