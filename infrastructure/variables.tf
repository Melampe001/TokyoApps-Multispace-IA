variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "aws_region" {
  description = "AWS Region for resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "tokyo-ia"
}

variable "data_retention_days" {
  description = "Number of days to retain data in S3 before transitioning to Glacier"
  type        = number
  default     = 90
}

variable "data_deletion_days" {
  description = "Number of days to retain data before permanent deletion"
  type        = number
  default     = 365
}

variable "enable_versioning" {
  description = "Enable versioning for S3 buckets"
  type        = bool
  default     = true
}

variable "enable_encryption" {
  description = "Enable server-side encryption for S3 buckets"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default = {
    Project    = "Tokyo-IA"
    ManagedBy  = "Terraform"
    Component  = "Analytics"
  }
}

variable "athena_workgroup_name" {
  description = "Name for the Athena workgroup"
  type        = string
  default     = ""
}

variable "athena_database_name" {
  description = "Name for the Athena database"
  type        = string
  default     = ""
}

variable "etl_retention_days" {
  description = "Number of days to retain ETL execution history"
  type        = number
  default     = 30
}

variable "query_results_retention_days" {
  description = "Number of days to retain Athena query results"
  type        = number
  default     = 7
}
