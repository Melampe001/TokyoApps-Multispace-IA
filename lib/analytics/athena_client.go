package analytics

import (
	"context"
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/athena"
	"github.com/aws/aws-sdk-go-v2/service/athena/types"
	"github.com/aws/aws-sdk-go-v2/service/s3"
)

// AthenaClient provides access to AWS Athena for analytics queries
type AthenaClient struct {
	client       *athena.Client
	s3Client     *s3.Client
	database     string
	outputBucket string
	workgroup    string
}

// AthenaConfig holds configuration for the Athena client
type AthenaConfig struct {
	Region       string
	Database     string
	OutputBucket string
	Workgroup    string
}

// NewAthenaClient creates a new Athena client instance
func NewAthenaClient(ctx context.Context, cfg AthenaConfig) (*AthenaClient, error) {
	// Load AWS configuration
	awsCfg, err := config.LoadDefaultConfig(ctx, config.WithRegion(cfg.Region))
	if err != nil {
		return nil, fmt.Errorf("failed to load AWS config: %w", err)
	}

	// Create Athena client
	athenaClient := athena.NewFromConfig(awsCfg)
	s3Client := s3.NewFromConfig(awsCfg)

	// Set defaults
	if cfg.Workgroup == "" {
		cfg.Workgroup = "primary"
	}

	return &AthenaClient{
		client:       athenaClient,
		s3Client:     s3Client,
		database:     cfg.Database,
		outputBucket: cfg.OutputBucket,
		workgroup:    cfg.Workgroup,
	}, nil
}

// ExecuteQuery executes an Athena query and waits for results
func (ac *AthenaClient) ExecuteQuery(ctx context.Context, query string) (*QueryResult, error) {
	// Start query execution
	startInput := &athena.StartQueryExecutionInput{
		QueryString: aws.String(query),
		QueryExecutionContext: &types.QueryExecutionContext{
			Database: aws.String(ac.database),
		},
		ResultConfiguration: &types.ResultConfiguration{
			OutputLocation: aws.String(fmt.Sprintf("s3://%s/query-results/", ac.outputBucket)),
		},
		WorkGroup: aws.String(ac.workgroup),
	}

	startOutput, err := ac.client.StartQueryExecution(ctx, startInput)
	if err != nil {
		return nil, fmt.Errorf("failed to start query execution: %w", err)
	}

	queryExecutionID := *startOutput.QueryExecutionId

	// Wait for query to complete
	if err := ac.waitForQuery(ctx, queryExecutionID); err != nil {
		return nil, fmt.Errorf("query execution failed: %w", err)
	}

	// Get query results
	return ac.getQueryResults(ctx, queryExecutionID)
}

// waitForQuery waits for a query to complete with exponential backoff
func (ac *AthenaClient) waitForQuery(ctx context.Context, queryExecutionID string) error {
	maxAttempts := 60
	backoff := time.Second

	for attempt := 0; attempt < maxAttempts; attempt++ {
		select {
		case <-ctx.Done():
			return ctx.Err()
		default:
		}

		input := &athena.GetQueryExecutionInput{
			QueryExecutionId: aws.String(queryExecutionID),
		}

		output, err := ac.client.GetQueryExecution(ctx, input)
		if err != nil {
			return fmt.Errorf("failed to get query execution status: %w", err)
		}

		status := output.QueryExecution.Status.State

		switch status {
		case types.QueryExecutionStateSucceeded:
			return nil
		case types.QueryExecutionStateFailed:
			reason := ""
			if output.QueryExecution.Status.StateChangeReason != nil {
				reason = *output.QueryExecution.Status.StateChangeReason
			}
			return fmt.Errorf("query failed: %s", reason)
		case types.QueryExecutionStateCancelled:
			return fmt.Errorf("query was cancelled")
		}

		// Exponential backoff with max of 5 seconds
		time.Sleep(backoff)
		if backoff < 5*time.Second {
			backoff *= 2
		}
	}

	return fmt.Errorf("query execution timed out after %d attempts", maxAttempts)
}

// getQueryResults retrieves the results of a completed query
func (ac *AthenaClient) getQueryResults(ctx context.Context, queryExecutionID string) (*QueryResult, error) {
	input := &athena.GetQueryResultsInput{
		QueryExecutionId: aws.String(queryExecutionID),
		MaxResults:       aws.Int32(1000),
	}

	output, err := ac.client.GetQueryResults(ctx, input)
	if err != nil {
		return nil, fmt.Errorf("failed to get query results: %w", err)
	}

	if len(output.ResultSet.Rows) == 0 {
		return &QueryResult{
			Columns:  []string{},
			Rows:     []map[string]interface{}{},
			RowCount: 0,
		}, nil
	}

	// Extract column names from first row
	columns := make([]string, 0)
	for _, col := range output.ResultSet.Rows[0].Data {
		if col.VarCharValue != nil {
			columns = append(columns, *col.VarCharValue)
		}
	}

	// Extract data rows (skip header row)
	rows := make([]map[string]interface{}, 0)
	for i := 1; i < len(output.ResultSet.Rows); i++ {
		row := make(map[string]interface{})
		for j, cell := range output.ResultSet.Rows[i].Data {
			if j < len(columns) && cell.VarCharValue != nil {
				row[columns[j]] = *cell.VarCharValue
			}
		}
		rows = append(rows, row)
	}

	return &QueryResult{
		Columns:  columns,
		Rows:     rows,
		RowCount: len(rows),
	}, nil
}

// GetWorkflowMetrics retrieves workflow metrics for a specific date range
func (ac *AthenaClient) GetWorkflowMetrics(ctx context.Context, year, month, startDay, endDay int) ([]WorkflowMetric, error) {
	query := fmt.Sprintf(QueryWorkflowMetricsByDay, year, month, startDay, endDay)

	result, err := ac.ExecuteQuery(ctx, query)
	if err != nil {
		return nil, err
	}

	metrics := make([]WorkflowMetric, 0, result.RowCount)
	for _, row := range result.Rows {
		metric := WorkflowMetric{}

		if v, ok := row["year"].(string); ok {
			metric.Year, _ = strconv.Atoi(v)
		}
		if v, ok := row["month"].(string); ok {
			metric.Month, _ = strconv.Atoi(v)
		}
		if v, ok := row["day"].(string); ok {
			metric.Day, _ = strconv.Atoi(v)
		}
		if v, ok := row["total_workflows"].(string); ok {
			metric.TotalWorkflows, _ = strconv.Atoi(v)
		}
		if v, ok := row["completed_count"].(string); ok {
			metric.CompletedCount, _ = strconv.Atoi(v)
		}
		if v, ok := row["failed_count"].(string); ok {
			metric.FailedCount, _ = strconv.Atoi(v)
		}
		if v, ok := row["avg_duration_ms"].(string); ok {
			metric.AvgDurationMs, _ = strconv.ParseFloat(v, 64)
		}
		if v, ok := row["total_tokens"].(string); ok {
			tokens, _ := strconv.ParseInt(v, 10, 64)
			metric.TotalTokens = tokens
		}
		if v, ok := row["total_cost_usd"].(string); ok {
			metric.TotalCostUSD, _ = strconv.ParseFloat(v, 64)
		}

		metric.Date = time.Date(metric.Year, time.Month(metric.Month), metric.Day, 0, 0, 0, 0, time.UTC)
		metrics = append(metrics, metric)
	}

	return metrics, nil
}

// GetAgentPerformance retrieves agent performance metrics for a specific month
func (ac *AthenaClient) GetAgentPerformance(ctx context.Context, year, month int) ([]AgentMetric, error) {
	query := fmt.Sprintf(QueryAgentPerformance, year, month)

	result, err := ac.ExecuteQuery(ctx, query)
	if err != nil {
		return nil, err
	}

	metrics := make([]AgentMetric, 0, result.RowCount)
	for _, row := range result.Rows {
		metric := AgentMetric{
			Period:    "monthly",
			StartDate: time.Date(year, time.Month(month), 1, 0, 0, 0, 0, time.UTC),
			EndDate:   time.Date(year, time.Month(month+1), 1, 0, 0, 0, 0, time.UTC).AddDate(0, 0, -1),
		}

		if v, ok := row["agent_id"].(string); ok {
			metric.AgentID = v
		}
		if v, ok := row["total_tasks"].(string); ok {
			metric.TotalTasks, _ = strconv.Atoi(v)
		}
		if v, ok := row["completed_tasks"].(string); ok {
			metric.CompletedTasks, _ = strconv.Atoi(v)
		}
		if v, ok := row["failed_tasks"].(string); ok {
			metric.FailedTasks, _ = strconv.Atoi(v)
		}
		if v, ok := row["avg_duration_ms"].(string); ok {
			metric.AvgDurationMs, _ = strconv.ParseFloat(v, 64)
		}
		if v, ok := row["total_tokens"].(string); ok {
			tokens, _ := strconv.ParseInt(v, 10, 64)
			metric.TotalTokens = tokens
		}
		if v, ok := row["total_cost_usd"].(string); ok {
			metric.TotalCostUSD, _ = strconv.ParseFloat(v, 64)
		}
		if v, ok := row["success_rate"].(string); ok {
			metric.SuccessRate, _ = strconv.ParseFloat(v, 64)
		}

		metrics = append(metrics, metric)
	}

	return metrics, nil
}

// GetTaskTypeMetrics retrieves metrics grouped by task type
func (ac *AthenaClient) GetTaskTypeMetrics(ctx context.Context, year, month int) ([]TaskTypeMetric, error) {
	query := fmt.Sprintf(QueryTaskTypeMetrics, year, month)

	result, err := ac.ExecuteQuery(ctx, query)
	if err != nil {
		return nil, err
	}

	metrics := make([]TaskTypeMetric, 0, result.RowCount)
	for _, row := range result.Rows {
		metric := TaskTypeMetric{}

		if v, ok := row["task_type"].(string); ok {
			metric.TaskType = v
		}
		if v, ok := row["total_tasks"].(string); ok {
			metric.TotalTasks, _ = strconv.Atoi(v)
		}
		if v, ok := row["completed_tasks"].(string); ok {
			metric.CompletedTasks, _ = strconv.Atoi(v)
		}
		if v, ok := row["failed_tasks"].(string); ok {
			metric.FailedTasks, _ = strconv.Atoi(v)
		}
		if v, ok := row["avg_duration_ms"].(string); ok {
			metric.AvgDurationMs, _ = strconv.ParseFloat(v, 64)
		}
		if v, ok := row["avg_tokens"].(string); ok {
			metric.AvgTokens, _ = strconv.ParseFloat(v, 64)
		}
		if v, ok := row["avg_cost_usd"].(string); ok {
			metric.AvgCostUSD, _ = strconv.ParseFloat(v, 64)
		}
		if v, ok := row["success_rate"].(string); ok {
			metric.SuccessRate, _ = strconv.ParseFloat(v, 64)
		}

		metrics = append(metrics, metric)
	}

	return metrics, nil
}

// ExportToCSV exports query results to a CSV file
func (ac *AthenaClient) ExportToCSV(result *QueryResult, filename string) error {
	file, err := os.Create(filename)
	if err != nil {
		return fmt.Errorf("failed to create CSV file: %w", err)
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Write header
	if err := writer.Write(result.Columns); err != nil {
		return fmt.Errorf("failed to write CSV header: %w", err)
	}

	// Write rows
	for _, row := range result.Rows {
		record := make([]string, len(result.Columns))
		for i, col := range result.Columns {
			if val, ok := row[col]; ok {
				record[i] = fmt.Sprintf("%v", val)
			}
		}
		if err := writer.Write(record); err != nil {
			return fmt.Errorf("failed to write CSV row: %w", err)
		}
	}

	return nil
}

// GetCostAnalysis retrieves cost breakdown by agent
func (ac *AthenaClient) GetCostAnalysis(ctx context.Context, year, month int) ([]CostAnalysis, error) {
	query := fmt.Sprintf(QueryCostAnalysisByAgent, year, month)

	result, err := ac.ExecuteQuery(ctx, query)
	if err != nil {
		return nil, err
	}

	analyses := make([]CostAnalysis, 0, result.RowCount)
	for _, row := range result.Rows {
		analysis := CostAnalysis{
			Period:    "monthly",
			StartDate: time.Date(year, time.Month(month), 1, 0, 0, 0, 0, time.UTC),
			EndDate:   time.Date(year, time.Month(month+1), 1, 0, 0, 0, 0, time.UTC).AddDate(0, 0, -1),
		}

		if v, ok := row["agent_id"].(string); ok {
			analysis.AgentID = v
		}
		if v, ok := row["total_cost_usd"].(string); ok {
			analysis.TotalCostUSD, _ = strconv.ParseFloat(v, 64)
		}
		if v, ok := row["total_tokens"].(string); ok {
			tokens, _ := strconv.ParseInt(v, 10, 64)
			analysis.TotalTokens = tokens
		}
		if v, ok := row["total_tasks"].(string); ok {
			analysis.TotalTasks, _ = strconv.Atoi(v)
		}
		if v, ok := row["cost_per_token"].(string); ok {
			analysis.CostPerToken, _ = strconv.ParseFloat(v, 64)
		}
		if v, ok := row["cost_per_task"].(string); ok {
			analysis.CostPerTask, _ = strconv.ParseFloat(v, 64)
		}

		analyses = append(analyses, analysis)
	}

	return analyses, nil
}

// validateQueryParameters validates common query parameters
func validateQueryParameters(year, month int) error {
	if year < 2000 || year > 2100 {
		return fmt.Errorf("invalid year: %d", year)
	}
	if month < 1 || month > 12 {
		return fmt.Errorf("invalid month: %d", month)
	}
	return nil
}

// Helper function to safely get string from map
func getStringFromRow(row map[string]interface{}, key string) string {
	if v, ok := row[key].(string); ok {
		return v
	}
	return ""
}

// Helper function to safely get int from map
func getIntFromRow(row map[string]interface{}, key string) int {
	if v, ok := row[key].(string); ok {
		val, _ := strconv.Atoi(v)
		return val
	}
	return 0
}

// Helper function to safely get float from map
func getFloatFromRow(row map[string]interface{}, key string) float64 {
	if v, ok := row[key].(string); ok {
		val, _ := strconv.ParseFloat(v, 64)
		return val
	}
	return 0.0
}

// sanitizeQuery provides basic query validation
// NOTE: This is NOT the primary security mechanism. Security is enforced by:
// 1. IAM permissions (read-only access to specific tables)
// 2. Athena workgroup policies
// 3. S3 bucket policies
// This function is defense-in-depth only.
func sanitizeQuery(query string) string {
	// Basic validation - check for write operations
	// Real security comes from IAM permissions
	dangerous := []string{"DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE", "INSERT", "UPDATE"}
	upperQuery := strings.ToUpper(query)

	for _, cmd := range dangerous {
		if strings.Contains(upperQuery, cmd) {
			return ""
		}
	}

	return query
}
