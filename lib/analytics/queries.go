package analytics

import (
	"context"
	"fmt"
	"strconv"
	"time"
)

// GetMonthlyRevenue retrieves total revenue for a specific month
func (c *AthenaClient) GetMonthlyRevenue(ctx context.Context, year, month int) (float64, error) {
	query := fmt.Sprintf(`
		SELECT SUM(amount) as total_revenue
		FROM invoices
		WHERE year = %d 
		  AND month = %d 
		  AND status = 'paid'
	`, year, month)

	result, err := c.ExecuteQuery(ctx, query)
	if err != nil {
		return 0, fmt.Errorf("failed to execute query: %w", err)
	}

	if len(result.Rows) == 0 {
		return 0, nil
	}

	// Parse revenue from result
	revenueStr, ok := result.Rows[0]["total_revenue"].(string)
	if !ok || revenueStr == "" {
		return 0, nil
	}

	revenue, err := strconv.ParseFloat(revenueStr, 64)
	if err != nil {
		return 0, fmt.Errorf("invalid revenue value: %w", err)
	}

	return revenue, nil
}

// GetTopCustomers retrieves the top N customers by revenue
func (c *AthenaClient) GetTopCustomers(ctx context.Context, startDate, endDate time.Time, limit int) ([]CustomerMetric, error) {
	query := fmt.Sprintf(`
		SELECT 
			user_id,
			COUNT(DISTINCT invoice_id) as invoice_count,
			SUM(amount) as total_spent,
			AVG(amount) as avg_invoice_amount,
			MAX(created_at) as last_invoice_date
		FROM invoices
		WHERE created_at BETWEEN TIMESTAMP '%s' AND TIMESTAMP '%s'
		  AND status = 'paid'
		GROUP BY user_id
		ORDER BY total_spent DESC
		LIMIT %d
	`, startDate.Format("2006-01-02 15:04:05"), endDate.Format("2006-01-02 15:04:05"), limit)

	result, err := c.ExecuteQuery(ctx, query)
	if err != nil {
		return nil, fmt.Errorf("failed to execute query: %w", err)
	}

	return c.parseCustomerMetrics(result)
}

// GetRevenueByProduct retrieves revenue breakdown by product
func (c *AthenaClient) GetRevenueByProduct(ctx context.Context, startDate, endDate time.Time) ([]ProductRevenue, error) {
	query := fmt.Sprintf(`
		SELECT 
			product_id,
			product_name,
			COUNT(*) as sales_count,
			SUM(amount) as total_revenue,
			AVG(amount) as avg_price
		FROM invoices
		WHERE created_at BETWEEN TIMESTAMP '%s' AND TIMESTAMP '%s'
		  AND status = 'paid'
		GROUP BY product_id, product_name
		ORDER BY total_revenue DESC
	`, startDate.Format("2006-01-02"), endDate.Format("2006-01-02"))

	result, err := c.ExecuteQuery(ctx, query)
	if err != nil {
		return nil, fmt.Errorf("failed to execute query: %w", err)
	}

	return c.parseProductRevenue(result)
}

// parseCustomerMetrics parses customer metrics from query results
func (c *AthenaClient) parseCustomerMetrics(result *QueryResult) ([]CustomerMetric, error) {
	metrics := make([]CustomerMetric, 0, len(result.Rows))

	for _, row := range result.Rows {
		metric := CustomerMetric{}

		// Parse user_id
		if userID, ok := row["user_id"].(string); ok {
			metric.UserID = userID
		}

		// Parse invoice_count
		if countStr, ok := row["invoice_count"].(string); ok {
			if count, err := strconv.ParseInt(countStr, 10, 64); err == nil {
				metric.InvoiceCount = count
			}
		}

		// Parse total_spent
		if spentStr, ok := row["total_spent"].(string); ok {
			if spent, err := strconv.ParseFloat(spentStr, 64); err == nil {
				metric.TotalSpent = spent
			}
		}

		// Parse avg_invoice_amount
		if avgStr, ok := row["avg_invoice_amount"].(string); ok {
			if avg, err := strconv.ParseFloat(avgStr, 64); err == nil {
				metric.AvgInvoiceAmount = avg
			}
		}

		// Parse last_invoice_date
		if dateStr, ok := row["last_invoice_date"].(string); ok {
			if date, err := time.Parse("2006-01-02 15:04:05", dateStr); err == nil {
				metric.LastInvoiceDate = date
			}
		}

		metrics = append(metrics, metric)
	}

	return metrics, nil
}

// parseProductRevenue parses product revenue from query results
func (c *AthenaClient) parseProductRevenue(result *QueryResult) ([]ProductRevenue, error) {
	revenues := make([]ProductRevenue, 0, len(result.Rows))

	for _, row := range result.Rows {
		revenue := ProductRevenue{}

		// Parse product_id
		if productID, ok := row["product_id"].(string); ok {
			revenue.ProductID = productID
		}

		// Parse product_name
		if productName, ok := row["product_name"].(string); ok {
			revenue.ProductName = productName
		}

		// Parse sales_count
		if countStr, ok := row["sales_count"].(string); ok {
			if count, err := strconv.ParseInt(countStr, 10, 64); err == nil {
				revenue.SalesCount = count
			}
		}

		// Parse total_revenue
		if revenueStr, ok := row["total_revenue"].(string); ok {
			if rev, err := strconv.ParseFloat(revenueStr, 64); err == nil {
				revenue.TotalRevenue = rev
			}
		}

		// Parse avg_price
		if avgStr, ok := row["avg_price"].(string); ok {
			if avg, err := strconv.ParseFloat(avgStr, 64); err == nil {
				revenue.AvgPrice = avg
			}
		}

		revenues = append(revenues, revenue)
	}

	return revenues, nil
}
