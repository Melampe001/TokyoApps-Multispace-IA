package analytics

import (
	"context"
	"fmt"
	"time"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/athena"
	"github.com/aws/aws-sdk-go-v2/service/athena/types"
)

// AthenaClient provides methods to query AWS Athena
type AthenaClient struct {
	client       *athena.Client
	database     string
	workgroup    string
	outputBucket string
}

// NewAthenaClient creates a new Athena client
func NewAthenaClient(ctx context.Context, database, workgroup, outputBucket string) (*AthenaClient, error) {
	cfg, err := config.LoadDefaultConfig(ctx)
	if err != nil {
		return nil, fmt.Errorf("unable to load SDK config: %w", err)
	}

	return &AthenaClient{
		client:       athena.NewFromConfig(cfg),
		database:     database,
		workgroup:    workgroup,
		outputBucket: outputBucket,
	}, nil
}

// ExecuteQuery executes a query in Athena and waits for results
func (c *AthenaClient) ExecuteQuery(ctx context.Context, query string) (*QueryResult, error) {
	// Start query execution
	startInput := &athena.StartQueryExecutionInput{
		QueryString: &query,
		QueryExecutionContext: &types.QueryExecutionContext{
			Database: &c.database,
		},
		WorkGroup: &c.workgroup,
	}

	startOutput, err := c.client.StartQueryExecution(ctx, startInput)
	if err != nil {
		return nil, fmt.Errorf("failed to start query: %w", err)
	}

	// Wait for query completion
	if err := c.waitForQueryCompletion(ctx, *startOutput.QueryExecutionId); err != nil {
		return nil, err
	}

	// Get query results
	return c.getQueryResults(ctx, *startOutput.QueryExecutionId)
}

// waitForQueryCompletion waits for a query to complete
func (c *AthenaClient) waitForQueryCompletion(ctx context.Context, queryExecutionID string) error {
	maxAttempts := 60 // 60 seconds timeout
	pollInterval := 1 * time.Second

	for i := 0; i < maxAttempts; i++ {
		getInput := &athena.GetQueryExecutionInput{
			QueryExecutionId: &queryExecutionID,
		}

		getOutput, err := c.client.GetQueryExecution(ctx, getInput)
		if err != nil {
			return fmt.Errorf("failed to get query execution status: %w", err)
		}

		state := getOutput.QueryExecution.Status.State

		switch state {
		case types.QueryExecutionStateSucceeded:
			return nil
		case types.QueryExecutionStateFailed:
			reason := ""
			if getOutput.QueryExecution.Status.StateChangeReason != nil {
				reason = *getOutput.QueryExecution.Status.StateChangeReason
			}
			return fmt.Errorf("query failed: %s", reason)
		case types.QueryExecutionStateCancelled:
			return fmt.Errorf("query was cancelled")
		case types.QueryExecutionStateQueued, types.QueryExecutionStateRunning:
			// Continue polling
			time.Sleep(pollInterval)
		}
	}

	return fmt.Errorf("query execution timed out after %d seconds", maxAttempts)
}

// getQueryResults retrieves the results of a completed query
func (c *AthenaClient) getQueryResults(ctx context.Context, queryExecutionID string) (*QueryResult, error) {
	getResultsInput := &athena.GetQueryResultsInput{
		QueryExecutionId: &queryExecutionID,
	}

	getResultsOutput, err := c.client.GetQueryResults(ctx, getResultsInput)
	if err != nil {
		return nil, fmt.Errorf("failed to get query results: %w", err)
	}

	// Parse results
	if len(getResultsOutput.ResultSet.Rows) == 0 {
		return &QueryResult{
			Columns: []string{},
			Rows:    []map[string]interface{}{},
		}, nil
	}

	// Extract column names from first row
	columns := make([]string, 0)
	headerRow := getResultsOutput.ResultSet.Rows[0]
	for _, col := range headerRow.Data {
		if col.VarCharValue != nil {
			columns = append(columns, *col.VarCharValue)
		}
	}

	// Extract data rows
	rows := make([]map[string]interface{}, 0)
	for i := 1; i < len(getResultsOutput.ResultSet.Rows); i++ {
		row := make(map[string]interface{})
		dataRow := getResultsOutput.ResultSet.Rows[i]

		for j, col := range dataRow.Data {
			if j < len(columns) && col.VarCharValue != nil {
				row[columns[j]] = *col.VarCharValue
			}
		}

		rows = append(rows, row)
	}

	return &QueryResult{
		Columns: columns,
		Rows:    rows,
	}, nil
}

// Close closes the Athena client (placeholder for future cleanup)
func (c *AthenaClient) Close() error {
	// AWS SDK v2 clients don't need explicit closing
	return nil
}
