package analytics

import (
	"context"
	"testing"
	"time"
)

func TestAthenaClient_GetMonthlyRevenue(t *testing.T) {
	tests := []struct {
		name    string
		year    int
		month   int
		want    float64
		wantErr bool
	}{
		{
			name:    "valid month",
			year:    2025,
			month:   12,
			want:    150000.50,
			wantErr: false,
		},
		{
			name:    "no data month",
			year:    2020,
			month:   1,
			want:    0,
			wantErr: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Skip in CI/CD environments without AWS credentials
			t.Skip("Skipping Athena integration test - requires AWS credentials")

			ctx := context.Background()
			client, err := NewAthenaClient(ctx, "test_db", "test_workgroup", "s3://test-bucket/")
			if err != nil {
				t.Fatalf("Failed to create client: %v", err)
			}
			defer client.Close()

			got, err := client.GetMonthlyRevenue(ctx, tt.year, tt.month)
			if (err != nil) != tt.wantErr {
				t.Errorf("GetMonthlyRevenue() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if got != tt.want {
				t.Errorf("GetMonthlyRevenue() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestAthenaClient_GetTopCustomers(t *testing.T) {
	tests := []struct {
		name      string
		startDate time.Time
		endDate   time.Time
		limit     int
		wantErr   bool
	}{
		{
			name:      "valid date range",
			startDate: time.Date(2025, 1, 1, 0, 0, 0, 0, time.UTC),
			endDate:   time.Date(2025, 12, 31, 23, 59, 59, 0, time.UTC),
			limit:     10,
			wantErr:   false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Skip in CI/CD environments without AWS credentials
			t.Skip("Skipping Athena integration test - requires AWS credentials")

			ctx := context.Background()
			client, err := NewAthenaClient(ctx, "test_db", "test_workgroup", "s3://test-bucket/")
			if err != nil {
				t.Fatalf("Failed to create client: %v", err)
			}
			defer client.Close()

			_, err = client.GetTopCustomers(ctx, tt.startDate, tt.endDate, tt.limit)
			if (err != nil) != tt.wantErr {
				t.Errorf("GetTopCustomers() error = %v, wantErr %v", err, tt.wantErr)
			}
		})
	}
}

func TestAthenaClient_GetRevenueByProduct(t *testing.T) {
	tests := []struct {
		name      string
		startDate time.Time
		endDate   time.Time
		wantErr   bool
	}{
		{
			name:      "valid date range",
			startDate: time.Date(2025, 1, 1, 0, 0, 0, 0, time.UTC),
			endDate:   time.Date(2025, 12, 31, 23, 59, 59, 0, time.UTC),
			wantErr:   false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Skip in CI/CD environments without AWS credentials
			t.Skip("Skipping Athena integration test - requires AWS credentials")

			ctx := context.Background()
			client, err := NewAthenaClient(ctx, "test_db", "test_workgroup", "s3://test-bucket/")
			if err != nil {
				t.Fatalf("Failed to create client: %v", err)
			}
			defer client.Close()

			_, err = client.GetRevenueByProduct(ctx, tt.startDate, tt.endDate)
			if (err != nil) != tt.wantErr {
				t.Errorf("GetRevenueByProduct() error = %v, wantErr %v", err, tt.wantErr)
			}
		})
	}
}

func TestParseCustomerMetrics(t *testing.T) {
	client := &AthenaClient{}

	result := &QueryResult{
		Columns: []string{"user_id", "invoice_count", "total_spent", "avg_invoice_amount", "last_invoice_date"},
		Rows: []map[string]interface{}{
			{
				"user_id":            "user123",
				"invoice_count":      "5",
				"total_spent":        "1000.50",
				"avg_invoice_amount": "200.10",
				"last_invoice_date":  "2025-12-22 10:30:00",
			},
		},
	}

	metrics, err := client.parseCustomerMetrics(result)
	if err != nil {
		t.Fatalf("parseCustomerMetrics() error = %v", err)
	}

	if len(metrics) != 1 {
		t.Errorf("Expected 1 metric, got %d", len(metrics))
	}

	if metrics[0].UserID != "user123" {
		t.Errorf("Expected user_id 'user123', got '%s'", metrics[0].UserID)
	}

	if metrics[0].InvoiceCount != 5 {
		t.Errorf("Expected invoice_count 5, got %d", metrics[0].InvoiceCount)
	}

	if metrics[0].TotalSpent != 1000.50 {
		t.Errorf("Expected total_spent 1000.50, got %f", metrics[0].TotalSpent)
	}
}

func TestParseProductRevenue(t *testing.T) {
	client := &AthenaClient{}

	result := &QueryResult{
		Columns: []string{"product_id", "product_name", "sales_count", "total_revenue", "avg_price"},
		Rows: []map[string]interface{}{
			{
				"product_id":    "prod123",
				"product_name":  "Premium Plan",
				"sales_count":   "100",
				"total_revenue": "10000.00",
				"avg_price":     "100.00",
			},
		},
	}

	revenues, err := client.parseProductRevenue(result)
	if err != nil {
		t.Fatalf("parseProductRevenue() error = %v", err)
	}

	if len(revenues) != 1 {
		t.Errorf("Expected 1 revenue entry, got %d", len(revenues))
	}

	if revenues[0].ProductID != "prod123" {
		t.Errorf("Expected product_id 'prod123', got '%s'", revenues[0].ProductID)
	}

	if revenues[0].ProductName != "Premium Plan" {
		t.Errorf("Expected product_name 'Premium Plan', got '%s'", revenues[0].ProductName)
	}

	if revenues[0].SalesCount != 100 {
		t.Errorf("Expected sales_count 100, got %d", revenues[0].SalesCount)
	}

	if revenues[0].TotalRevenue != 10000.00 {
		t.Errorf("Expected total_revenue 10000.00, got %f", revenues[0].TotalRevenue)
	}
}
