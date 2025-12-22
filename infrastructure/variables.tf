variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "data_retention_days" {
  description = "Number of days to retain raw data in S3"
  type        = number
  default     = 90
}

variable "archive_retention_days" {
  description = "Number of days before archiving to Glacier"
  type        = number
  default     = 365
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "tokyo-ia"
}
