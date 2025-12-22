# IAM Role for ETL (GitHub Actions)
resource "aws_iam_role" "etl_role" {
  name = "${var.project_name}-etl-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:Melampe001/Tokyo-IA:*"
          }
        }
      }
    ]
  })

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-etl-role-${var.environment}"
      Environment = var.environment
      Purpose     = "ETL execution from GitHub Actions"
    }
  )
}

# IAM Policy for ETL role
resource "aws_iam_policy" "etl_policy" {
  name        = "${var.project_name}-etl-policy-${var.environment}"
  description = "Policy for ETL to access S3, Athena, and Glue"

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
          "${aws_s3_bucket.data_lake.arn}/*",
          aws_s3_bucket.etl_artifacts.arn,
          "${aws_s3_bucket.etl_artifacts.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "athena:StartQueryExecution",
          "athena:GetQueryExecution",
          "athena:GetQueryResults",
          "athena:StopQueryExecution"
        ]
        Resource = [
          aws_athena_workgroup.main.arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "glue:GetDatabase",
          "glue:GetTable",
          "glue:GetPartitions",
          "glue:CreatePartition",
          "glue:UpdatePartition",
          "glue:BatchCreatePartition",
          "glue:StartCrawler",
          "glue:GetCrawler"
        ]
        Resource = [
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:catalog",
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:database/${aws_glue_catalog_database.analytics.name}",
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:table/${aws_glue_catalog_database.analytics.name}/*",
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:crawler/${aws_glue_crawler.analytics.name}"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.athena_results.arn,
          "${aws_s3_bucket.athena_results.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject"
        ]
        Resource = [
          "${aws_s3_bucket.athena_results.arn}/query-results/*"
        ]
      }
    ]
  })

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-etl-policy-${var.environment}"
      Environment = var.environment
    }
  )
}

# Attach ETL policy to ETL role
resource "aws_iam_role_policy_attachment" "etl_policy_attachment" {
  role       = aws_iam_role.etl_role.name
  policy_arn = aws_iam_policy.etl_policy.arn
}

# IAM Role for Athena users (Go services)
resource "aws_iam_role" "athena_user_role" {
  name = "${var.project_name}-athena-user-${var.environment}"

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

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-athena-user-${var.environment}"
      Environment = var.environment
      Purpose     = "Read-only access to Athena for analytics queries"
    }
  )
}

# IAM Policy for Athena users (read-only)
resource "aws_iam_policy" "athena_user_policy" {
  name        = "${var.project_name}-athena-user-policy-${var.environment}"
  description = "Read-only policy for querying Athena"

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
          "athena:ListQueryExecutions",
          "athena:GetWorkGroup"
        ]
        Resource = [
          aws_athena_workgroup.main.arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "glue:GetDatabase",
          "glue:GetTable",
          "glue:GetPartitions",
          "glue:GetTables"
        ]
        Resource = [
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:catalog",
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:database/${aws_glue_catalog_database.analytics.name}",
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:table/${aws_glue_catalog_database.analytics.name}/*"
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
          "${aws_s3_bucket.data_lake.arn}/*",
          aws_s3_bucket.athena_results.arn,
          "${aws_s3_bucket.athena_results.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject"
        ]
        Resource = [
          "${aws_s3_bucket.athena_results.arn}/query-results/*"
        ]
      }
    ]
  })

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-athena-user-policy-${var.environment}"
      Environment = var.environment
    }
  )
}

# Attach Athena user policy to role
resource "aws_iam_role_policy_attachment" "athena_user_policy_attachment" {
  role       = aws_iam_role.athena_user_role.name
  policy_arn = aws_iam_policy.athena_user_policy.arn
}

# Instance profile for EC2 instances running Go services
resource "aws_iam_instance_profile" "athena_user" {
  name = "${var.project_name}-athena-user-${var.environment}"
  role = aws_iam_role.athena_user_role.name

  tags = merge(
    var.tags,
    {
      Name        = "${var.project_name}-athena-user-${var.environment}"
      Environment = var.environment
    }
  )
}
