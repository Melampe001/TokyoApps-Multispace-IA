# IAM Role for ETL
resource "aws_iam_role" "etl_role" {
  name = "${var.project_name}-etl-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-etl-role"
    Environment = var.environment
  }
}

# Policy for ETL to write to S3 Data Lake
resource "aws_iam_policy" "etl_s3_write" {
  name        = "${var.project_name}-etl-s3-write-${var.environment}"
  description = "Policy for ETL to write to S3 Data Lake"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.data_lake.arn,
          "${aws_s3_bucket.data_lake.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "glue:GetDatabase",
          "glue:GetTable",
          "glue:CreatePartition",
          "glue:BatchCreatePartition",
          "glue:UpdatePartition"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "${aws_cloudwatch_log_group.etl_logs.arn}:*"
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-etl-s3-policy"
    Environment = var.environment
  }
}

# Attach ETL policy to role
resource "aws_iam_role_policy_attachment" "etl_s3_write" {
  role       = aws_iam_role.etl_role.name
  policy_arn = aws_iam_policy.etl_s3_write.arn
}

# IAM Role for Application to query Athena
resource "aws_iam_role" "app_athena_role" {
  name = "${var.project_name}-app-athena-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-app-athena-role"
    Environment = var.environment
  }
}

# Policy for Athena queries
resource "aws_iam_policy" "athena_query" {
  name        = "${var.project_name}-athena-query-${var.environment}"
  description = "Policy for querying Athena"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "athena:StartQueryExecution",
          "athena:GetQueryExecution",
          "athena:GetQueryResults",
          "athena:StopQueryExecution",
          "athena:GetWorkGroup"
        ]
        Resource = [
          aws_athena_workgroup.tokyo_ia_analytics.arn,
          "arn:aws:athena:${var.aws_region}:*:workgroup/${aws_athena_workgroup.tokyo_ia_analytics.name}"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.data_lake.arn,
          "${aws_s3_bucket.data_lake.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject"
        ]
        Resource = [
          "${aws_s3_bucket.athena_results.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "glue:GetDatabase",
          "glue:GetTable",
          "glue:GetPartitions"
        ]
        Resource = [
          "arn:aws:glue:${var.aws_region}:*:catalog",
          "arn:aws:glue:${var.aws_region}:*:database/${aws_glue_catalog_database.tokyo_ia_billing.name}",
          "arn:aws:glue:${var.aws_region}:*:table/${aws_glue_catalog_database.tokyo_ia_billing.name}/*"
        ]
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-athena-query-policy"
    Environment = var.environment
  }
}

# Attach Athena query policy to app role
resource "aws_iam_role_policy_attachment" "athena_query" {
  role       = aws_iam_role.app_athena_role.name
  policy_arn = aws_iam_policy.athena_query.arn
}
