# AWS Athena Query Guide

This guide explains how to use AWS Athena to query the Tokyo-IA data lake for analytics and billing insights.

## Overview

AWS Athena allows you to query data stored in S3 using standard SQL. The Tokyo-IA data lake stores:
- Invoices
- Transactions
- Users
- Subscriptions

Data is partitioned by date (year/month/day) and stored in Parquet format for efficient querying.

## Prerequisites

- AWS account with Athena access
- Data lake set up (see [AWS Setup Guide](../deployment/AWS_SETUP.md))
- AWS CLI or Console access

## Quick Start

### 1. Access Athena Console

1. Log in to [AWS Console](https://console.aws.amazon.com/)
2. Navigate to Athena service
3. Select the workgroup: `tokyo-ia-production`
4. Choose database: `tokyo_ia_billing_production`

### 2. Run Your First Query

```sql
SELECT 
    COUNT(*) as invoice_count,
    SUM(amount) as total_revenue
FROM invoices
WHERE status = 'paid'
AND year = 2025
AND month = 1;
```

## Common Queries

### Revenue Queries

#### Monthly Revenue
```sql
SELECT 
    year,
    month,
    COUNT(*) as invoice_count,
    SUM(amount) as total_revenue,
    AVG(amount) as avg_invoice
FROM invoices
WHERE status = 'paid'
GROUP BY year, month
ORDER BY year DESC, month DESC
LIMIT 12;
```

#### Daily Revenue Trend
```sql
SELECT 
    CONCAT(year, '-', LPAD(CAST(month AS VARCHAR), 2, '0'), '-', LPAD(CAST(day AS VARCHAR), 2, '0')) as date,
    SUM(amount) as revenue
FROM invoices
WHERE status = 'paid'
AND year = 2025
AND month = 1
GROUP BY year, month, day
ORDER BY year, month, day;
```

#### Revenue by Currency
```sql
SELECT 
    currency,
    COUNT(*) as invoice_count,
    SUM(amount) as total
FROM invoices
WHERE status = 'paid'
AND year = 2025
GROUP BY currency
ORDER BY total DESC;
```

### Subscription Queries

#### Active Subscriptions by Plan
```sql
SELECT 
    plan_name,
    COUNT(*) as subscriber_count
FROM subscriptions
WHERE status = 'active'
GROUP BY plan_name
ORDER BY subscriber_count DESC;
```

#### New Subscriptions by Month
```sql
SELECT 
    year,
    month,
    plan_name,
    COUNT(*) as new_subscriptions
FROM subscriptions
WHERE year = 2025
GROUP BY year, month, plan_name
ORDER BY year DESC, month DESC, plan_name;
```

#### Churn Analysis
```sql
SELECT 
    year,
    month,
    COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as churned,
    COUNT(CASE WHEN status = 'active' THEN 1 END) as active,
    CAST(COUNT(CASE WHEN status = 'cancelled' THEN 1 END) AS DOUBLE) / 
        CAST(COUNT(*) AS DOUBLE) * 100 as churn_rate
FROM subscriptions
GROUP BY year, month
ORDER BY year DESC, month DESC;
```

### Transaction Queries

#### Transaction Volume
```sql
SELECT 
    year,
    month,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount
FROM transactions
WHERE status = 'completed'
GROUP BY year, month
ORDER BY year DESC, month DESC;
```

#### Failed Transactions
```sql
SELECT 
    year,
    month,
    day,
    COUNT(*) as failed_count,
    SUM(amount) as failed_amount
FROM transactions
WHERE status = 'failed'
GROUP BY year, month, day
ORDER BY year DESC, month DESC, day DESC;
```

### Customer Queries

#### Top Customers by Revenue
```sql
SELECT 
    u.name,
    u.email,
    SUM(i.amount) as total_spent,
    COUNT(i.id) as invoice_count
FROM users u
JOIN subscriptions s ON u.id = s.user_id
JOIN invoices i ON s.id = i.subscription_id
WHERE i.status = 'paid'
GROUP BY u.name, u.email
ORDER BY total_spent DESC
LIMIT 20;
```

#### Customer Lifetime Value (CLV)
```sql
SELECT 
    s.plan_name,
    AVG(revenue_per_customer) as avg_clv
FROM (
    SELECT 
        s.plan_name,
        u.id as user_id,
        SUM(i.amount) as revenue_per_customer
    FROM users u
    JOIN subscriptions s ON u.id = s.user_id
    JOIN invoices i ON s.id = i.subscription_id
    WHERE i.status = 'paid'
    GROUP BY s.plan_name, u.id
) subquery
GROUP BY subquery.plan_name
ORDER BY avg_clv DESC;
```

## Advanced Queries

### Revenue Growth Rate
```sql
WITH monthly_revenue AS (
    SELECT 
        year,
        month,
        SUM(amount) as revenue
    FROM invoices
    WHERE status = 'paid'
    GROUP BY year, month
),
revenue_with_prev AS (
    SELECT 
        year,
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY year, month) as prev_revenue
    FROM monthly_revenue
)
SELECT 
    year,
    month,
    revenue,
    prev_revenue,
    CASE 
        WHEN prev_revenue > 0 THEN 
            ((revenue - prev_revenue) / prev_revenue) * 100 
        ELSE 0 
    END as growth_rate
FROM revenue_with_prev
ORDER BY year DESC, month DESC;
```

### Cohort Analysis
```sql
SELECT 
    DATE_FORMAT(s.created_at, '%Y-%m') as cohort_month,
    COUNT(DISTINCT s.user_id) as cohort_size,
    COUNT(DISTINCT CASE WHEN s.status = 'active' THEN s.user_id END) as still_active,
    CAST(COUNT(DISTINCT CASE WHEN s.status = 'active' THEN s.user_id END) AS DOUBLE) / 
        CAST(COUNT(DISTINCT s.user_id) AS DOUBLE) * 100 as retention_rate
FROM subscriptions s
GROUP BY DATE_FORMAT(s.created_at, '%Y-%m')
ORDER BY cohort_month DESC;
```

### MRR (Monthly Recurring Revenue)
```sql
SELECT 
    year,
    month,
    SUM(CASE 
        WHEN plan_name = 'Pro' THEN 29.99
        WHEN plan_name = 'Business' THEN 99.99
        WHEN plan_name = 'Enterprise' THEN 299.99
        ELSE 0 
    END) as mrr
FROM subscriptions
WHERE status = 'active'
GROUP BY year, month
ORDER BY year DESC, month DESC;
```

## Using the Go Athena Client

### Basic Query
```go
import (
    "context"
    "fmt"
    "github.com/Melampe001/Tokyo-IA/lib/analytics"
)

func main() {
    client := analytics.NewAthenaClient(
        "tokyo_ia_billing_production",
        "tokyo-ia-production",
        "us-east-1",
    )
    
    revenue, err := client.GetMonthlyRevenue(context.Background(), 2025, 1)
    if err != nil {
        panic(err)
    }
    
    fmt.Printf("January 2025 Revenue: $%.2f\n", revenue)
}
```

### Top Users
```go
users, err := client.GetTopUsers(context.Background(), 10)
if err != nil {
    panic(err)
}

for _, user := range users {
    fmt.Printf("%s: $%.2f (%d invoices)\n", 
        user.Email, user.TotalRevenue, user.InvoiceCount)
}
```

## Query Optimization

### Use Partitions
Always filter by partition keys (year, month, day) to reduce data scanned:

```sql
-- Good: Uses partition pruning
SELECT * FROM invoices 
WHERE year = 2025 AND month = 1 AND status = 'paid';

-- Bad: Scans all partitions
SELECT * FROM invoices 
WHERE status = 'paid';
```

### Limit Results
Use LIMIT to reduce data returned:

```sql
SELECT * FROM invoices 
WHERE year = 2025 
LIMIT 100;
```

### Use Appropriate Data Types
Cast columns to appropriate types for better performance:

```sql
SELECT 
    CAST(amount AS DECIMAL(10,2)) as amount,
    CAST(created_at AS TIMESTAMP) as created_at
FROM invoices;
```

### Avoid SELECT *
Select only needed columns:

```sql
-- Good
SELECT id, amount, status FROM invoices;

-- Bad
SELECT * FROM invoices;
```

## Cost Management

### Monitor Query Costs
Athena charges based on data scanned. View query costs:

1. Go to Athena console
2. Click "Recent queries"
3. View "Data scanned" column

### Use Columnar Formats
Parquet format (already used) reduces costs significantly compared to CSV/JSON.

### Partition Effectively
Proper partitioning reduces data scanned per query by up to 95%.

### Create Views
Create views for commonly used queries:

```sql
CREATE VIEW monthly_revenue AS
SELECT 
    year,
    month,
    SUM(amount) as revenue
FROM invoices
WHERE status = 'paid'
GROUP BY year, month;
```

## Troubleshooting

### Issue: "Table not found"

**Solutions:**
1. Verify database name: `tokyo_ia_billing_production`
2. Check table name spelling
3. Ensure ETL has run at least once

### Issue: "No data returned"

**Solutions:**
1. Check partition filters
2. Verify data exists in S3: `s3://tokyo-ia-data-lake/data/invoices/`
3. Run ETL export if needed

### Issue: "Permission denied"

**Solutions:**
1. Check IAM permissions for S3 bucket
2. Verify Athena execution role
3. Ensure workgroup has correct permissions

### Issue: "Query timeout"

**Solutions:**
1. Add partition filters
2. Reduce time range
3. Use LIMIT clause
4. Create materialized views

## Best Practices

1. **Always use partition filters** to reduce costs and improve performance
2. **Test queries on small datasets** before running on full data
3. **Use CTEs (Common Table Expressions)** for complex queries
4. **Cache frequent queries** in your application
5. **Monitor query costs** regularly
6. **Create views** for commonly used aggregations
7. **Use EXPLAIN** to understand query plans
8. **Schedule heavy queries** during off-peak hours

## Scheduling Queries

### Using AWS EventBridge + Lambda

Create a Lambda function to run Athena queries on schedule:

```python
import boto3

def lambda_handler(event, context):
    athena = boto3.client('athena')
    
    query = """
        SELECT year, month, SUM(amount) as revenue
        FROM invoices
        WHERE status = 'paid'
        GROUP BY year, month
    """
    
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': 'tokyo_ia_billing_production'},
        ResultConfiguration={
            'OutputLocation': 's3://tokyo-ia-athena-results/scheduled/'
        },
        WorkGroup='tokyo-ia-production'
    )
    
    return {'queryExecutionId': response['QueryExecutionId']}
```

## Security

### IAM Policies
Minimum permissions for querying:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "athena:StartQueryExecution",
        "athena:GetQueryExecution",
        "athena:GetQueryResults",
        "athena:StopQueryExecution"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::tokyo-ia-data-lake/*",
        "arn:aws:s3:::tokyo-ia-athena-results/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "glue:GetTable",
        "glue:GetDatabase",
        "glue:GetPartitions"
      ],
      "Resource": "*"
    }
  ]
}
```

## Support

For issues or questions:
1. Check [troubleshooting section](#troubleshooting)
2. Review [AWS Athena documentation](https://docs.aws.amazon.com/athena/)
3. Check query execution history for errors
4. Open an issue in the Tokyo-IA repository

## Related Documentation

- [AWS Setup Guide](../deployment/AWS_SETUP.md)
- [ETL Pipeline](../../python/etl/export_to_s3.py)
- [Terraform Infrastructure](../../infrastructure/athena.tf)
- [Go Athena Client](../../lib/analytics/athena_client.go)
