package analytics

import (
	"time"
)

// CustomerMetric represents customer analytics data
type CustomerMetric struct {
	UserID           string    `json:"user_id"`
	InvoiceCount     int64     `json:"invoice_count"`
	TotalSpent       float64   `json:"total_spent"`
	AvgInvoiceAmount float64   `json:"avg_invoice_amount"`
	LastInvoiceDate  time.Time `json:"last_invoice_date"`
}

// ProductRevenue represents product revenue analytics
type ProductRevenue struct {
	ProductID    string  `json:"product_id"`
	ProductName  string  `json:"product_name"`
	SalesCount   int64   `json:"sales_count"`
	TotalRevenue float64 `json:"total_revenue"`
	AvgPrice     float64 `json:"avg_price"`
}

// QueryResult represents generic query results from Athena
type QueryResult struct {
	Columns []string                 `json:"columns"`
	Rows    []map[string]interface{} `json:"rows"`
}
