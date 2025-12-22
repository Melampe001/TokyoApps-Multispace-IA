# Analytics Guide - Using the Go Athena Client

Complete guide to querying historical data using the Tokyo-IA Go analytics client.

## Overview

The `lib/analytics` package provides a Go client for querying historical data in AWS Athena. It offers type-safe methods for common analytics operations with automatic error handling and retries.

## Quick Start

### Installation

The package is included in the Tokyo-IA repository:

```go
import "github.com/Melampe001/Tokyo-IA/lib/analytics"
```

### Basic Usage

```go
package main

import (
    "context"
    "fmt"
    "log"
    
    "github.com/Melampe001/Tokyo-IA/lib/analytics"
)

func main() {
    ctx := context.Background()
    
    // Create client
    cfg := analytics.AthenaConfig{
        Region:       "us-east-1",
        Database:     "tokyo_ia_billing_dev",
        OutputBucket: "tokyo-ia-athena-results-dev",
        Workgroup:    "tokyo-ia-dev",
    }
    
    client, err := analytics.NewAthenaClient(ctx, cfg)
    if err != nil {
        log.Fatal(err)
    }
    
    // Get workflow metrics
    metrics, err := client.GetWorkflowMetrics(ctx, 2024, 12, 1, 31)
    if err != nil {
        log.Fatal(err)
    }
    
    for _, m := range metrics {
        fmt.Printf("%s: %d workflows, $%.2f cost\n",
            m.Date.Format("2006-01-02"),
            m.TotalWorkflows,
            m.TotalCostUSD)
    }
}
```

## Client Configuration

### AthenaConfig

```go
type AthenaConfig struct {
    Region       string // AWS region (e.g., "us-east-1")
    Database     string // Glue database name
    OutputBucket string // S3 bucket for query results
    Workgroup    string // Athena workgroup (optional, default: "primary")
}
```

### Environment-Based Configuration

```go
import "os"

cfg := analytics.AthenaConfig{
    Region:       os.Getenv("AWS_REGION"),
    Database:     os.Getenv("ATHENA_DATABASE"),
    OutputBucket: os.Getenv("S3_ATHENA_RESULTS_BUCKET"),
    Workgroup:    os.Getenv("ATHENA_WORKGROUP"),
}
```

## Common Queries

### 1. Workflow Metrics

Get workflow statistics for a date range:

```go
// Get December 2024 workflow metrics
metrics, err := client.GetWorkflowMetrics(ctx, 2024, 12, 1, 31)

// Access data
for _, m := range metrics {
    fmt.Printf("Date: %v\n", m.Date)
    fmt.Printf("Total Workflows: %d\n", m.TotalWorkflows)
    fmt.Printf("Completed: %d\n", m.CompletedCount)
    fmt.Printf("Failed: %d\n", m.FailedCount)
    fmt.Printf("Avg Duration: %.2f ms\n", m.AvgDurationMs)
    fmt.Printf("Total Cost: $%.2f\n", m.TotalCostUSD)
    fmt.Printf("Tokens Used: %d\n\n", m.TotalTokens)
}
```

### 2. Agent Performance

Analyze agent performance for a month:

```go
// Get December 2024 agent metrics
agents, err := client.GetAgentPerformance(ctx, 2024, 12)

// Find top performing agent
var topAgent analytics.AgentMetric
for _, a := range agents {
    if a.SuccessRate > topAgent.SuccessRate {
        topAgent = a
    }
}

fmt.Printf("Top Agent: %s\n", topAgent.AgentID)
fmt.Printf("Success Rate: %.1f%%\n", topAgent.SuccessRate)
fmt.Printf("Total Tasks: %d\n", topAgent.TotalTasks)
```

### 3. Task Type Analysis

Get metrics by task type:

```go
tasks, err := client.GetTaskTypeMetrics(ctx, 2024, 12)

// Sort by volume
sort.Slice(tasks, func(i, j int) bool {
    return tasks[i].TotalTasks > tasks[j].TotalTasks
})

fmt.Println("Top Task Types:")
for i, t := range tasks {
    if i >= 10 {
        break
    }
    fmt.Printf("%d. %s: %d tasks (%.1f%% success)\n",
        i+1, t.TaskType, t.TotalTasks, t.SuccessRate)
}
```

### 4. Cost Analysis

Analyze costs by agent:

```go
costs, err := client.GetCostAnalysis(ctx, 2024, 12)

// Calculate total cost
var total float64
for _, c := range costs {
    total += c.TotalCostUSD
}

fmt.Printf("Total Cost: $%.2f\n\n", total)
fmt.Println("Cost Breakdown:")
for _, c := range costs {
    pct := (c.TotalCostUSD / total) * 100
    fmt.Printf("%s: $%.2f (%.1f%%)\n",
        c.AgentID, c.TotalCostUSD, pct)
}
```

## Custom Queries

### ExecuteQuery Method

For custom analytics, use `ExecuteQuery`:

```go
query := `
    SELECT 
        workflow_type,
        COUNT(*) as count,
        AVG(duration_ms) as avg_duration
    FROM workflows
    WHERE year = 2024 AND month = 12
    GROUP BY workflow_type
    ORDER BY count DESC
`

result, err := client.ExecuteQuery(ctx, query)
if err != nil {
    log.Fatal(err)
}

// Access results
for _, row := range result.Rows {
    workflowType := row["workflow_type"].(string)
    count := row["count"].(string)
    avgDuration := row["avg_duration"].(string)
    
    fmt.Printf("%s: %s workflows (avg: %s ms)\n",
        workflowType, count, avgDuration)
}
```

### Export to CSV

Save query results to CSV:

```go
result, err := client.ExecuteQuery(ctx, query)
if err != nil {
    log.Fatal(err)
}

err = client.ExportToCSV(result, "report.csv")
if err != nil {
    log.Fatal(err)
}

fmt.Println("Exported to report.csv")
```

## Data Models

### WorkflowMetric

```go
type WorkflowMetric struct {
    Year            int       // Partition year
    Month           int       // Partition month
    Day             int       // Partition day
    TotalWorkflows  int       // Count of workflows
    CompletedCount  int       // Completed workflows
    FailedCount     int       // Failed workflows
    AvgDurationMs   float64   // Average duration
    TotalTokens     int64     // Total tokens used
    TotalCostUSD    float64   // Total cost
    Date            time.Time // Date representation
}
```

### AgentMetric

```go
type AgentMetric struct {
    AgentID         string    // Agent identifier
    AgentName       string    // Agent display name
    Period          string    // "daily", "weekly", "monthly"
    TotalTasks      int       // Total tasks executed
    CompletedTasks  int       // Successfully completed
    FailedTasks     int       // Failed tasks
    AvgDurationMs   float64   // Average duration
    TotalTokens     int64     // Total tokens consumed
    TotalCostUSD    float64   // Total cost
    SuccessRate     float64   // Success percentage
    StartDate       time.Time // Period start
    EndDate         time.Time // Period end
}
```

### TaskTypeMetric

```go
type TaskTypeMetric struct {
    TaskType       string  // Type of task
    TotalTasks     int     // Total count
    CompletedTasks int     // Completed count
    FailedTasks    int     // Failed count
    AvgDurationMs  float64 // Average duration
    AvgTokens      float64 // Average tokens
    AvgCostUSD     float64 // Average cost
    SuccessRate    float64 // Success percentage
}
```

## Best Practices

### 1. Always Use Partition Filters

**Good** (uses partitions):
```go
metrics, err := client.GetWorkflowMetrics(ctx, 2024, 12, 1, 31)
```

**Bad** (scans all data):
```go
query := "SELECT * FROM workflows WHERE created_at >= '2024-12-01'"
```

### 2. Use Context with Timeout

```go
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
defer cancel()

metrics, err := client.GetWorkflowMetrics(ctx, 2024, 12, 1, 31)
```

### 3. Handle Errors Gracefully

```go
metrics, err := client.GetWorkflowMetrics(ctx, 2024, 12, 1, 31)
if err != nil {
    // Log error but continue
    log.Printf("Warning: failed to get metrics: %v", err)
    // Use cached or default data
    metrics = getCachedMetrics()
}
```

### 4. Cache Results

```go
type MetricsCache struct {
    metrics map[string][]analytics.WorkflowMetric
    mu      sync.RWMutex
    ttl     time.Duration
}

func (c *MetricsCache) GetOrFetch(
    ctx context.Context,
    client *analytics.AthenaClient,
    year, month int,
) ([]analytics.WorkflowMetric, error) {
    key := fmt.Sprintf("%d-%d", year, month)
    
    c.mu.RLock()
    if cached, ok := c.metrics[key]; ok {
        c.mu.RUnlock()
        return cached, nil
    }
    c.mu.RUnlock()
    
    // Fetch from Athena
    metrics, err := client.GetWorkflowMetrics(ctx, year, month, 1, 31)
    if err != nil {
        return nil, err
    }
    
    // Cache results
    c.mu.Lock()
    c.metrics[key] = metrics
    c.mu.Unlock()
    
    return metrics, nil
}
```

## Performance Optimization

### 1. Limit Date Ranges

Query smaller date ranges for faster results:

```go
// Instead of full year
metrics, err := client.GetWorkflowMetrics(ctx, 2024, 1, 1, 365)

// Query by month
for month := 1; month <= 12; month++ {
    metrics, err := client.GetWorkflowMetrics(ctx, 2024, month, 1, 31)
    // Process metrics
}
```

### 2. Select Only Needed Columns

```go
// Efficient
query := `
    SELECT agent_id, COUNT(*) as count
    FROM agent_tasks
    WHERE year = 2024 AND month = 12
    GROUP BY agent_id
`

// Inefficient
query := `
    SELECT *
    FROM agent_tasks
    WHERE year = 2024 AND month = 12
`
```

### 3. Use Aggregations in Athena

Let Athena do the heavy lifting:

```go
// Good - aggregate in Athena
query := `
    SELECT agent_id, AVG(cost_usd) as avg_cost
    FROM agent_tasks
    WHERE year = 2024 AND month = 12
    GROUP BY agent_id
`

// Bad - fetch all data and average in Go
query := `
    SELECT agent_id, cost_usd
    FROM agent_tasks
    WHERE year = 2024 AND month = 12
`
```

## Cost Estimation

Athena charges $5 per TB of data scanned.

### Typical Query Costs

| Query Type | Data Scanned | Cost |
|------------|--------------|------|
| Single day metrics | ~10 MB | $0.00005 |
| Monthly metrics | ~300 MB | $0.0015 |
| Yearly metrics | ~3.6 GB | $0.018 |
| Full table scan | ~100 GB | $0.50 |

### Cost Optimization

```go
// Cost: ~$0.0001 (10 MB scanned)
metrics, err := client.GetWorkflowMetrics(ctx, 2024, 12, 22, 22)

// Cost: ~$0.0015 (300 MB scanned)
metrics, err := client.GetWorkflowMetrics(ctx, 2024, 12, 1, 31)

// Cost: ~$0.50 (100 GB scanned) - AVOID!
query := "SELECT * FROM workflows"
```

## Error Handling

### Common Errors

**1. Query Timeout**
```go
if err != nil {
    if strings.Contains(err.Error(), "timeout") {
        // Retry with smaller date range
    }
}
```

**2. Insufficient Permissions**
```go
if err != nil {
    if strings.Contains(err.Error(), "Access Denied") {
        // Check IAM permissions
    }
}
```

**3. Table Not Found**
```go
if err != nil {
    if strings.Contains(err.Error(), "Table not found") {
        // Run athena_setup.py
    }
}
```

## Testing

### Unit Tests

```go
func TestWorkflowMetrics(t *testing.T) {
    // Use test data or mock
    metrics := []analytics.WorkflowMetric{
        {Year: 2024, Month: 12, Day: 22, TotalWorkflows: 100},
    }
    
    if len(metrics) != 1 {
        t.Errorf("Expected 1 metric, got %d", len(metrics))
    }
}
```

### Integration Tests

```go
func TestAthenaQuery(t *testing.T) {
    if testing.Short() {
        t.Skip("Skipping integration test")
    }
    
    cfg := analytics.AthenaConfig{
        Region:       "us-east-1",
        Database:     "tokyo_ia_billing_dev",
        OutputBucket: "tokyo-ia-athena-results-dev",
    }
    
    client, err := analytics.NewAthenaClient(context.Background(), cfg)
    if err != nil {
        t.Fatal(err)
    }
    
    metrics, err := client.GetWorkflowMetrics(
        context.Background(), 2024, 12, 1, 1,
    )
    
    if err != nil {
        t.Fatal(err)
    }
    
    if len(metrics) == 0 {
        t.Error("Expected metrics, got none")
    }
}
```

Run integration tests:
```bash
go test ./lib/analytics/... -v
go test ./lib/analytics/... -v -short=false  # Include integration tests
```

## Examples

See complete examples in:
- `examples/analytics_basic.go` - Basic usage
- `examples/analytics_dashboard.go` - Dashboard metrics
- `examples/analytics_export.go` - CSV export

## Related Documentation

- [Athena Setup Guide](./ATHENA_SETUP.md)
- [ETL Pipeline Documentation](./ETL_PIPELINE.md)
- [Architecture Overview](./HYBRID_ARCHITECTURE.md)
- [Go Package Documentation](https://pkg.go.dev/github.com/Melampe001/Tokyo-IA/lib/analytics)
