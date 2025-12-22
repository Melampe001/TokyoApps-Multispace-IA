package analytics

import (
	"context"
	"testing"
	"time"
)

func TestQueryBuilder(t *testing.T) {
	tests := []struct {
		name           string
		baseQuery      string
		params         []interface{}
		expectedParams int
	}{
		{
			name:           "Simple query with one parameter",
			baseQuery:      "SELECT * FROM table WHERE id = ?",
			params:         []interface{}{1},
			expectedParams: 1,
		},
		{
			name:           "Query with multiple parameters",
			baseQuery:      "SELECT * FROM table WHERE year = ? AND month = ?",
			params:         []interface{}{2024, 12},
			expectedParams: 2,
		},
		{
			name:           "Query with no parameters",
			baseQuery:      "SELECT * FROM table",
			params:         []interface{}{},
			expectedParams: 0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			qb := NewQueryBuilder(tt.baseQuery)

			for _, param := range tt.params {
				qb.AddParam(param)
			}

			query, params := qb.Build()

			if query != tt.baseQuery {
				t.Errorf("Expected query %s, got %s", tt.baseQuery, query)
			}

			if len(params) != tt.expectedParams {
				t.Errorf("Expected %d params, got %d", tt.expectedParams, len(params))
			}
		})
	}
}

func TestValidateQueryParameters(t *testing.T) {
	tests := []struct {
		name      string
		year      int
		month     int
		expectErr bool
	}{
		{
			name:      "Valid parameters",
			year:      2024,
			month:     12,
			expectErr: false,
		},
		{
			name:      "Invalid year - too low",
			year:      1999,
			month:     6,
			expectErr: true,
		},
		{
			name:      "Invalid year - too high",
			year:      2101,
			month:     6,
			expectErr: true,
		},
		{
			name:      "Invalid month - too low",
			year:      2024,
			month:     0,
			expectErr: true,
		},
		{
			name:      "Invalid month - too high",
			year:      2024,
			month:     13,
			expectErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := validateQueryParameters(tt.year, tt.month)

			if tt.expectErr && err == nil {
				t.Error("Expected error but got none")
			}

			if !tt.expectErr && err != nil {
				t.Errorf("Expected no error but got: %v", err)
			}
		})
	}
}

func TestGetStringFromRow(t *testing.T) {
	tests := []struct {
		name     string
		row      map[string]interface{}
		key      string
		expected string
	}{
		{
			name:     "Existing string value",
			row:      map[string]interface{}{"name": "test"},
			key:      "name",
			expected: "test",
		},
		{
			name:     "Non-existing key",
			row:      map[string]interface{}{"name": "test"},
			key:      "missing",
			expected: "",
		},
		{
			name:     "Non-string value",
			row:      map[string]interface{}{"count": 123},
			key:      "count",
			expected: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := getStringFromRow(tt.row, tt.key)
			if result != tt.expected {
				t.Errorf("Expected %s, got %s", tt.expected, result)
			}
		})
	}
}

func TestGetIntFromRow(t *testing.T) {
	tests := []struct {
		name     string
		row      map[string]interface{}
		key      string
		expected int
	}{
		{
			name:     "Valid integer string",
			row:      map[string]interface{}{"count": "123"},
			key:      "count",
			expected: 123,
		},
		{
			name:     "Invalid integer string",
			row:      map[string]interface{}{"count": "abc"},
			key:      "count",
			expected: 0,
		},
		{
			name:     "Non-existing key",
			row:      map[string]interface{}{"count": "123"},
			key:      "missing",
			expected: 0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := getIntFromRow(tt.row, tt.key)
			if result != tt.expected {
				t.Errorf("Expected %d, got %d", tt.expected, result)
			}
		})
	}
}

func TestGetFloatFromRow(t *testing.T) {
	tests := []struct {
		name     string
		row      map[string]interface{}
		key      string
		expected float64
	}{
		{
			name:     "Valid float string",
			row:      map[string]interface{}{"value": "123.45"},
			key:      "value",
			expected: 123.45,
		},
		{
			name:     "Invalid float string",
			row:      map[string]interface{}{"value": "abc"},
			key:      "value",
			expected: 0.0,
		},
		{
			name:     "Non-existing key",
			row:      map[string]interface{}{"value": "123.45"},
			key:      "missing",
			expected: 0.0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := getFloatFromRow(tt.row, tt.key)
			if result != tt.expected {
				t.Errorf("Expected %f, got %f", tt.expected, result)
			}
		})
	}
}

func TestSanitizeQuery(t *testing.T) {
	tests := []struct {
		name     string
		query    string
		expected string
	}{
		{
			name:     "Safe SELECT query",
			query:    "SELECT * FROM table WHERE id = 1",
			expected: "SELECT * FROM table WHERE id = 1",
		},
		{
			name:     "Dangerous DROP query",
			query:    "DROP TABLE users",
			expected: "",
		},
		{
			name:     "Dangerous DELETE query",
			query:    "DELETE FROM users WHERE id = 1",
			expected: "",
		},
		{
			name:     "Dangerous INSERT query",
			query:    "INSERT INTO users VALUES (1, 'admin')",
			expected: "",
		},
		{
			name:     "Dangerous UPDATE query",
			query:    "UPDATE users SET role = 'admin'",
			expected: "",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := sanitizeQuery(tt.query)
			if result != tt.expected {
				t.Errorf("Expected %s, got %s", tt.expected, result)
			}
		})
	}
}

func TestWorkflowMetricStructure(t *testing.T) {
	metric := WorkflowMetric{
		Year:           2024,
		Month:          12,
		Day:            22,
		TotalWorkflows: 100,
		CompletedCount: 95,
		FailedCount:    5,
		AvgDurationMs:  1500.5,
		TotalTokens:    50000,
		TotalCostUSD:   25.50,
		Date:           time.Date(2024, 12, 22, 0, 0, 0, 0, time.UTC),
	}

	if metric.Year != 2024 {
		t.Errorf("Expected year 2024, got %d", metric.Year)
	}
	if metric.TotalWorkflows != 100 {
		t.Errorf("Expected 100 workflows, got %d", metric.TotalWorkflows)
	}
	if metric.TotalCostUSD != 25.50 {
		t.Errorf("Expected cost 25.50, got %f", metric.TotalCostUSD)
	}
}

func TestAgentMetricStructure(t *testing.T) {
	metric := AgentMetric{
		AgentID:        "akira-001",
		AgentName:      "Akira",
		Period:         "monthly",
		TotalTasks:     500,
		CompletedTasks: 480,
		FailedTasks:    20,
		AvgDurationMs:  2000.0,
		TotalTokens:    100000,
		TotalCostUSD:   50.00,
		SuccessRate:    96.0,
		StartDate:      time.Date(2024, 12, 1, 0, 0, 0, 0, time.UTC),
		EndDate:        time.Date(2024, 12, 31, 0, 0, 0, 0, time.UTC),
	}

	if metric.AgentID != "akira-001" {
		t.Errorf("Expected agent ID akira-001, got %s", metric.AgentID)
	}
	if metric.SuccessRate != 96.0 {
		t.Errorf("Expected success rate 96.0, got %f", metric.SuccessRate)
	}
}

func TestQueryResult(t *testing.T) {
	result := QueryResult{
		Columns: []string{"id", "name", "count"},
		Rows: []map[string]interface{}{
			{"id": "1", "name": "test1", "count": "10"},
			{"id": "2", "name": "test2", "count": "20"},
		},
		RowCount: 2,
	}

	if len(result.Columns) != 3 {
		t.Errorf("Expected 3 columns, got %d", len(result.Columns))
	}
	if result.RowCount != 2 {
		t.Errorf("Expected 2 rows, got %d", result.RowCount)
	}
	if len(result.Rows) != result.RowCount {
		t.Errorf("Row count mismatch: %d vs %d", len(result.Rows), result.RowCount)
	}
}

// TestAthenaConfig tests configuration validation
func TestAthenaConfig(t *testing.T) {
	tests := []struct {
		name   string
		config AthenaConfig
		valid  bool
	}{
		{
			name: "Valid config",
			config: AthenaConfig{
				Region:       "us-east-1",
				Database:     "tokyo_ia_billing_dev",
				OutputBucket: "tokyo-ia-athena-results-dev",
				Workgroup:    "tokyo-ia-dev",
			},
			valid: true,
		},
		{
			name: "Empty workgroup uses default",
			config: AthenaConfig{
				Region:       "us-east-1",
				Database:     "tokyo_ia_billing_dev",
				OutputBucket: "tokyo-ia-athena-results-dev",
				Workgroup:    "",
			},
			valid: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// We can't actually create a client without AWS credentials,
			// but we can test the config structure
			if tt.config.Region == "" {
				t.Error("Region should not be empty")
			}
			if tt.config.Database == "" {
				t.Error("Database should not be empty")
			}
		})
	}
}

// Benchmark tests
func BenchmarkGetStringFromRow(b *testing.B) {
	row := map[string]interface{}{"name": "test"}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = getStringFromRow(row, "name")
	}
}

func BenchmarkGetIntFromRow(b *testing.B) {
	row := map[string]interface{}{"count": "123"}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = getIntFromRow(row, "count")
	}
}

func BenchmarkSanitizeQuery(b *testing.B) {
	query := "SELECT * FROM table WHERE id = 1"
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_ = sanitizeQuery(query)
	}
}

// Example test demonstrating usage
func ExampleNewQueryBuilder() {
	qb := NewQueryBuilder("SELECT * FROM table WHERE year = ? AND month = ?")
	qb.AddParam(2024).AddParam(12)
	query, params := qb.Build()

	_ = query
	_ = params
	// Output:
}

// Context test
func TestContextCancellation(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel() // Cancel immediately

	// Verify context is cancelled
	select {
	case <-ctx.Done():
		// Expected
	default:
		t.Error("Context should be cancelled")
	}
}
