# Athena Workgroup
resource "aws_athena_workgroup" "main" {
  name        = local.athena_workgroup_name
  description = "Tokyo-IA Analytics Workgroup for ${var.environment}"

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true

    result_configuration {
      output_location = "s3://${aws_s3_bucket.athena_results.bucket}/query-results/"

      encryption_configuration {
        encryption_option = "SSE_S3"
      }
    }

    engine_version {
      selected_engine_version = "AUTO"
    }
  }

  tags = merge(
    var.tags,
    {
      Name        = local.athena_workgroup_name
      Environment = var.environment
    }
  )
}

# Athena Named Query - Get Monthly Workflow Metrics
resource "aws_athena_named_query" "monthly_workflow_metrics" {
  name        = "monthly_workflow_metrics"
  workgroup   = aws_athena_workgroup.main.name
  database    = aws_glue_catalog_database.analytics.name
  description = "Get workflow metrics aggregated by month"

  query = <<-EOT
    SELECT 
      year,
      month,
      COUNT(*) as total_workflows,
      COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_count,
      COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_count,
      AVG(duration_ms) as avg_duration_ms,
      SUM(total_tokens_used) as total_tokens,
      SUM(total_cost_usd) as total_cost_usd
    FROM workflows
    WHERE year = YEAR(CURRENT_DATE) AND month = MONTH(CURRENT_DATE)
    GROUP BY year, month
    ORDER BY year, month;
  EOT
}

# Athena Named Query - Get Agent Performance
resource "aws_athena_named_query" "agent_performance" {
  name        = "agent_performance"
  workgroup   = aws_athena_workgroup.main.name
  database    = aws_glue_catalog_database.analytics.name
  description = "Get agent performance metrics"

  query = <<-EOT
    SELECT 
      agent_id,
      COUNT(*) as total_tasks,
      COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tasks,
      COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_tasks,
      AVG(duration_ms) as avg_duration_ms,
      SUM(tokens_used) as total_tokens,
      SUM(cost_usd) as total_cost_usd,
      CAST(COUNT(CASE WHEN status = 'completed' THEN 1 END) AS DOUBLE) / COUNT(*) * 100 as success_rate
    FROM agent_tasks
    WHERE year = YEAR(CURRENT_DATE) AND month = MONTH(CURRENT_DATE)
    GROUP BY agent_id
    ORDER BY total_tasks DESC;
  EOT
}

# Athena Named Query - Get Cost Analysis
resource "aws_athena_named_query" "cost_analysis" {
  name        = "cost_analysis"
  workgroup   = aws_athena_workgroup.main.name
  database    = aws_glue_catalog_database.analytics.name
  description = "Get cost breakdown by agent"

  query = <<-EOT
    SELECT 
      agent_id,
      SUM(cost_usd) as total_cost_usd,
      SUM(tokens_used) as total_tokens,
      COUNT(*) as total_tasks,
      CASE WHEN SUM(tokens_used) > 0 THEN SUM(cost_usd) / SUM(tokens_used) ELSE 0 END as cost_per_token,
      CASE WHEN COUNT(*) > 0 THEN SUM(cost_usd) / COUNT(*) ELSE 0 END as cost_per_task
    FROM agent_tasks
    WHERE year = YEAR(CURRENT_DATE) AND month = MONTH(CURRENT_DATE)
    GROUP BY agent_id
    ORDER BY total_cost_usd DESC;
  EOT
}

# Athena Named Query - Get Daily Metrics
resource "aws_athena_named_query" "daily_metrics" {
  name        = "daily_metrics"
  workgroup   = aws_athena_workgroup.main.name
  database    = aws_glue_catalog_database.analytics.name
  description = "Get comprehensive daily metrics"

  query = <<-EOT
    SELECT 
      year,
      month,
      day,
      COUNT(*) as total_workflows,
      AVG(duration_ms) as avg_duration_ms,
      SUM(total_cost_usd) as total_cost_usd,
      SUM(total_tokens_used) as total_tokens
    FROM workflows
    WHERE year = YEAR(CURRENT_DATE) 
      AND month = MONTH(CURRENT_DATE)
      AND day >= DAY(CURRENT_DATE - INTERVAL '7' DAY)
    GROUP BY year, month, day
    ORDER BY year DESC, month DESC, day DESC;
  EOT
}

# Athena Named Query - Get Top Task Types
resource "aws_athena_named_query" "top_task_types" {
  name        = "top_task_types"
  workgroup   = aws_athena_workgroup.main.name
  database    = aws_glue_catalog_database.analytics.name
  description = "Get most common task types and their metrics"

  query = <<-EOT
    SELECT 
      task_type,
      COUNT(*) as total_tasks,
      COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tasks,
      AVG(duration_ms) as avg_duration_ms,
      AVG(tokens_used) as avg_tokens,
      AVG(cost_usd) as avg_cost_usd
    FROM agent_tasks
    WHERE year = YEAR(CURRENT_DATE) AND month = MONTH(CURRENT_DATE)
    GROUP BY task_type
    ORDER BY total_tasks DESC
    LIMIT 20;
  EOT
}

# Local values for Athena
locals {
  athena_workgroup_name = var.athena_workgroup_name != "" ? var.athena_workgroup_name : "${var.project_name}-${var.environment}"
}
