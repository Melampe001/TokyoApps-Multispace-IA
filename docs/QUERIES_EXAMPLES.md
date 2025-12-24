# Athena Query Examples

This document provides SQL query examples for common analytics use cases.

## Table of Contents

- [Revenue Analysis](#revenue-analysis)
- [Customer Analytics](#customer-analytics)
- [Product Performance](#product-performance)
- [Retention Analysis](#retention-analysis)
- [Time-based Analysis](#time-based-analysis)
- [Advanced Queries](#advanced-queries)

## Revenue Analysis

### Monthly Revenue

Get total revenue by month:

```sql
SELECT 
    year,
    month,
    SUM(amount) as total_revenue,
    COUNT(*) as invoice_count,
    AVG(amount) as avg_invoice_amount
FROM invoices
WHERE status = 'paid'
GROUP BY year, month
ORDER BY year DESC, month DESC;
```

### Revenue by Currency

```sql
SELECT 
    currency,
    SUM(amount) as total_revenue,
    COUNT(*) as invoice_count
FROM invoices
WHERE status = 'paid'
  AND year = 2025
GROUP BY currency
ORDER BY total_revenue DESC;
```

### Daily Revenue Trend (Last 30 Days)

```sql
SELECT 
    year,
    month,
    day,
    SUM(amount) as daily_revenue,
    COUNT(*) as invoice_count
FROM invoices
WHERE status = 'paid'
  AND year = 2025
  AND month = 12
GROUP BY year, month, day
ORDER BY year, month, day;
```

### Year-over-Year Growth

```sql
WITH monthly_revenue AS (
    SELECT 
        year,
        month,
        SUM(amount) as revenue
    FROM invoices
    WHERE status = 'paid'
    GROUP BY year, month
)
SELECT 
    a.year,
    a.month,
    a.revenue as current_revenue,
    b.revenue as previous_year_revenue,
    ((a.revenue - b.revenue) / b.revenue * 100) as yoy_growth_percent
FROM monthly_revenue a
LEFT JOIN monthly_revenue b 
    ON a.year = b.year + 1 
    AND a.month = b.month
ORDER BY a.year DESC, a.month DESC;
```

## Customer Analytics

### Top 10 Customers by Lifetime Value

```sql
SELECT 
    user_id,
    COUNT(DISTINCT invoice_id) as purchase_count,
    SUM(amount) as lifetime_value,
    AVG(amount) as avg_purchase_amount,
    MIN(created_at) as first_purchase,
    MAX(created_at) as last_purchase
FROM invoices
WHERE status = 'paid'
GROUP BY user_id
ORDER BY lifetime_value DESC
LIMIT 10;
```

### Customer Segmentation by Spend

```sql
SELECT 
    CASE 
        WHEN total_spent >= 1000 THEN 'High Value'
        WHEN total_spent >= 500 THEN 'Medium Value'
        ELSE 'Low Value'
    END as customer_segment,
    COUNT(*) as customer_count,
    AVG(total_spent) as avg_spent,
    SUM(total_spent) as segment_revenue
FROM (
    SELECT 
        user_id,
        SUM(amount) as total_spent
    FROM invoices
    WHERE status = 'paid'
    GROUP BY user_id
) customer_totals
GROUP BY 
    CASE 
        WHEN total_spent >= 1000 THEN 'High Value'
        WHEN total_spent >= 500 THEN 'Medium Value'
        ELSE 'Low Value'
    END
ORDER BY segment_revenue DESC;
```

### New vs Returning Customers

```sql
WITH customer_first_purchase AS (
    SELECT 
        user_id,
        MIN(DATE(created_at)) as first_purchase_date
    FROM invoices
    WHERE status = 'paid'
    GROUP BY user_id
)
SELECT 
    i.year,
    i.month,
    COUNT(DISTINCT CASE WHEN DATE(i.created_at) = cfp.first_purchase_date THEN i.user_id END) as new_customers,
    COUNT(DISTINCT CASE WHEN DATE(i.created_at) > cfp.first_purchase_date THEN i.user_id END) as returning_customers
FROM invoices i
JOIN customer_first_purchase cfp ON i.user_id = cfp.user_id
WHERE i.status = 'paid'
GROUP BY i.year, i.month
ORDER BY i.year DESC, i.month DESC;
```

## Product Performance

### Top Products by Revenue

```sql
SELECT 
    product_id,
    product_name,
    COUNT(*) as sales_count,
    SUM(amount) as total_revenue,
    AVG(amount) as avg_price
FROM invoices
WHERE status = 'paid'
  AND year = 2025
GROUP BY product_id, product_name
ORDER BY total_revenue DESC
LIMIT 20;
```

### Product Revenue Trend

```sql
SELECT 
    product_name,
    year,
    month,
    SUM(amount) as monthly_revenue,
    COUNT(*) as sales_count
FROM invoices
WHERE status = 'paid'
  AND product_id IN ('prod1', 'prod2', 'prod3')
GROUP BY product_name, year, month
ORDER BY product_name, year DESC, month DESC;
```

### Product Mix Analysis

```sql
WITH total_revenue AS (
    SELECT SUM(amount) as total
    FROM invoices
    WHERE status = 'paid' AND year = 2025
)
SELECT 
    product_name,
    SUM(amount) as product_revenue,
    COUNT(*) as sales_count,
    (SUM(amount) / (SELECT total FROM total_revenue) * 100) as revenue_percentage
FROM invoices
WHERE status = 'paid' AND year = 2025
GROUP BY product_name
ORDER BY product_revenue DESC;
```

## Retention Analysis

### Monthly Active Users

```sql
SELECT 
    year,
    month,
    COUNT(DISTINCT user_id) as active_users
FROM invoices
WHERE status = 'paid'
GROUP BY year, month
ORDER BY year DESC, month DESC;
```

### Customer Cohort Analysis

```sql
WITH cohorts AS (
    SELECT 
        user_id,
        DATE_TRUNC('month', MIN(created_at)) as cohort_month
    FROM invoices
    WHERE status = 'paid'
    GROUP BY user_id
),
user_activities AS (
    SELECT 
        i.user_id,
        c.cohort_month,
        DATE_TRUNC('month', i.created_at) as activity_month
    FROM invoices i
    JOIN cohorts c ON i.user_id = c.user_id
    WHERE i.status = 'paid'
)
SELECT 
    cohort_month,
    COUNT(DISTINCT CASE WHEN activity_month = cohort_month THEN user_id END) as month_0,
    COUNT(DISTINCT CASE WHEN activity_month = cohort_month + INTERVAL '1' MONTH THEN user_id END) as month_1,
    COUNT(DISTINCT CASE WHEN activity_month = cohort_month + INTERVAL '2' MONTH THEN user_id END) as month_2,
    COUNT(DISTINCT CASE WHEN activity_month = cohort_month + INTERVAL '3' MONTH THEN user_id END) as month_3
FROM user_activities
GROUP BY cohort_month
ORDER BY cohort_month DESC;
```

### Churn Rate

```sql
WITH monthly_users AS (
    SELECT 
        year,
        month,
        user_id
    FROM invoices
    WHERE status = 'paid'
    GROUP BY year, month, user_id
)
SELECT 
    a.year,
    a.month,
    COUNT(DISTINCT a.user_id) as current_month_users,
    COUNT(DISTINCT b.user_id) as previous_month_users,
    COUNT(DISTINCT a.user_id) - COUNT(DISTINCT b.user_id) as net_change,
    ((COUNT(DISTINCT a.user_id) - COUNT(DISTINCT b.user_id)) / 
     CAST(COUNT(DISTINCT b.user_id) AS DOUBLE) * 100) as growth_rate
FROM monthly_users a
LEFT JOIN monthly_users b 
    ON b.year = CASE WHEN a.month = 1 THEN a.year - 1 ELSE a.year END
    AND b.month = CASE WHEN a.month = 1 THEN 12 ELSE a.month - 1 END
GROUP BY a.year, a.month
ORDER BY a.year DESC, a.month DESC;
```

## Time-based Analysis

### Revenue by Day of Week

```sql
SELECT 
    EXTRACT(DOW FROM created_at) as day_of_week,
    CASE EXTRACT(DOW FROM created_at)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END as day_name,
    COUNT(*) as invoice_count,
    SUM(amount) as total_revenue,
    AVG(amount) as avg_amount
FROM invoices
WHERE status = 'paid'
  AND year = 2025
GROUP BY EXTRACT(DOW FROM created_at)
ORDER BY day_of_week;
```

### Peak Hours Analysis

```sql
SELECT 
    EXTRACT(HOUR FROM created_at) as hour_of_day,
    COUNT(*) as invoice_count,
    SUM(amount) as total_revenue
FROM invoices
WHERE status = 'paid'
  AND year = 2025
  AND month = 12
GROUP BY EXTRACT(HOUR FROM created_at)
ORDER BY hour_of_day;
```

## Advanced Queries

### Customer Lifetime Value Prediction

```sql
WITH customer_metrics AS (
    SELECT 
        user_id,
        COUNT(*) as purchase_count,
        SUM(amount) as total_spent,
        AVG(amount) as avg_order_value,
        DATE_DIFF('day', MIN(created_at), MAX(created_at)) as customer_lifespan_days,
        MIN(created_at) as first_purchase,
        MAX(created_at) as last_purchase
    FROM invoices
    WHERE status = 'paid'
    GROUP BY user_id
)
SELECT 
    user_id,
    purchase_count,
    total_spent,
    avg_order_value,
    customer_lifespan_days,
    CASE 
        WHEN customer_lifespan_days > 0 
        THEN (purchase_count / CAST(customer_lifespan_days AS DOUBLE)) * 365
        ELSE purchase_count
    END as annual_purchase_frequency,
    CASE 
        WHEN customer_lifespan_days > 0 
        THEN ((purchase_count / CAST(customer_lifespan_days AS DOUBLE)) * 365) * avg_order_value
        ELSE total_spent
    END as predicted_annual_value
FROM customer_metrics
WHERE purchase_count >= 2
ORDER BY predicted_annual_value DESC
LIMIT 100;
```

### RFM Analysis (Recency, Frequency, Monetary)

```sql
WITH customer_rfm AS (
    SELECT 
        user_id,
        DATE_DIFF('day', MAX(created_at), CURRENT_DATE) as recency,
        COUNT(*) as frequency,
        SUM(amount) as monetary
    FROM invoices
    WHERE status = 'paid'
    GROUP BY user_id
),
rfm_scores AS (
    SELECT 
        user_id,
        recency,
        frequency,
        monetary,
        NTILE(5) OVER (ORDER BY recency DESC) as r_score,
        NTILE(5) OVER (ORDER BY frequency) as f_score,
        NTILE(5) OVER (ORDER BY monetary) as m_score
    FROM customer_rfm
)
SELECT 
    user_id,
    recency,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    (r_score + f_score + m_score) as rfm_total,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'Promising'
        WHEN r_score <= 2 AND f_score >= 4 THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
        ELSE 'Others'
    END as customer_segment
FROM rfm_scores
ORDER BY rfm_total DESC;
```

## Query Optimization Tips

1. **Always filter by partition columns**:
   ```sql
   WHERE year = 2025 AND month = 12
   ```

2. **Use LIMIT for exploratory queries**:
   ```sql
   SELECT * FROM invoices LIMIT 100;
   ```

3. **Leverage result caching**:
   - Identical queries return cached results (free)
   - Cache valid for 24 hours

4. **Use columnar projections**:
   ```sql
   SELECT user_id, amount  -- Only select needed columns
   FROM invoices;
   ```

5. **Partition pruning with date ranges**:
   ```sql
   WHERE year = 2025 
     AND month BETWEEN 1 AND 3
     AND day >= 15
   ```

## Cost Estimation

| Query Type | Data Scanned | Cost Estimate |
|------------|--------------|---------------|
| Single day | ~100 MB | $0.0005 |
| Single month | ~3 GB | $0.015 |
| Full year | ~36 GB | $0.18 |
| Full table scan | ~200 GB | $1.00 |

**Note**: Use partitioning to minimize scanned data and reduce costs.

## Using Queries in Go

Example of using the Go Athena client:

```go
import (
    "context"
    "time"
    "github.com/Melampe001/Tokyo-IA/lib/analytics"
)

// Initialize client
client, err := analytics.NewAthenaClient(
    ctx,
    "tokyo_ia_billing",
    "tokyo-ia-analytics",
    "s3://tokyo-ia-athena-results/",
)

// Get monthly revenue
revenue, err := client.GetMonthlyRevenue(ctx, 2025, 12)

// Get top customers
startDate := time.Date(2025, 1, 1, 0, 0, 0, 0, time.UTC)
endDate := time.Date(2025, 12, 31, 23, 59, 59, 0, time.UTC)
customers, err := client.GetTopCustomers(ctx, startDate, endDate, 10)

// Custom query
result, err := client.ExecuteQuery(ctx, "SELECT COUNT(*) FROM invoices WHERE year = 2025")
```

## References

- [Athena SQL Reference](https://docs.aws.amazon.com/athena/latest/ug/ddl-sql-reference.html)
- [Presto SQL Functions](https://prestodb.io/docs/current/functions.html)
- [Partition Projection](https://docs.aws.amazon.com/athena/latest/ug/partition-projection.html)
