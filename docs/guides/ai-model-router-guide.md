# AI Model Router Guide

## Overview

The AI Model Router is the intelligent orchestration layer that routes requests to the most appropriate AI model based on task type, complexity, privacy requirements, and budget constraints.

## Quick Start

### Basic Usage

```go
package main

import (
    "context"
    "fmt"
    "time"
    
    "github.com/Melampe001/Tokyo-IA/internal/ai"
    "github.com/Melampe001/Tokyo-IA/internal/ai/clients"
)

func main() {
    // Create router with configuration
    config := &ai.RouterConfig{
        EnableCaching:      true,
        CacheTTL:           time.Hour,
        EnableFallback:     true,
        MaxRetries:         3,
        BudgetLimitDaily:   500.0,
        BudgetAlertPercent: 80.0,
    }
    
    router := ai.NewModelRouter(config)
    
    // Register clients (use real API keys in production)
    router.RegisterClient(clients.NewOpenAIClient(apiKey, "o3-mini"))
    router.RegisterClient(clients.NewAnthropicClient(apiKey, "claude-sonnet-4.5"))
    
    // Setup caching and metrics
    cache := ai.NewInMemoryCache(time.Hour)
    router.SetCache(cache)
    
    metrics := ai.NewMetricsCollector()
    router.SetMetrics(metrics)
    
    // Make a request
    req := &ai.CompletionRequest{
        Prompt:      "Explain quantum computing in simple terms",
        TaskType:    ai.TaskTypeReasoning,
        Complexity:  ai.ComplexityModerate,
        MaxTokens:   500,
        Temperature: 0.7,
    }
    
    ctx := context.Background()
    resp, err := router.Complete(ctx, req)
    if err != nil {
        panic(err)
    }
    
    fmt.Printf("Response: %s\n", resp.Content)
    fmt.Printf("Model: %s\n", resp.Model)
    fmt.Printf("Cost: $%.4f\n", resp.CostUSD)
}
```

## Routing Rules

The router uses intelligent rules to select the best model for each request:

### Task Type Routing

#### Reasoning Tasks
- **Complex**: OpenAI o3 → Claude Opus → Gemini
- **Moderate**: Claude Sonnet → o3-mini → Gemini
- **Simple**: Claude Sonnet → Llama 4

#### Code Generation/Review
- **Privacy Required**: Llama 4 (local)
- **Default**: Claude Opus → o3-mini → Llama 4

#### Multimodal Tasks
- **Primary**: Gemini 3.0 Ultra → Grok 4

#### Documentation
- **Primary**: Gemini 3.0 → Claude Sonnet

### Complexity Levels

```go
// Use these constants for complexity
ai.ComplexitySimple    // Simple tasks, fast models
ai.ComplexityModerate  // Balanced performance
ai.ComplexityComplex   // Most capable models
```

### Task Types

```go
ai.TaskTypeReasoning     // Complex reasoning and analysis
ai.TaskTypeCodeGen       // Code generation
ai.TaskTypeCodeReview    // Code review and analysis
ai.TaskTypeMultimodal    // Image/video analysis
ai.TaskTypeDocumentation // Documentation generation
ai.TaskTypeChat          // General chat
```

## Advanced Features

### Privacy-Aware Routing

For sensitive data that shouldn't leave your infrastructure:

```go
req := &ai.CompletionRequest{
    Prompt:          "Analyze this confidential code...",
    TaskType:        ai.TaskTypeCodeReview,
    PrivacyRequired: true,  // Forces local Llama 4
}
```

### Budget Management

Set per-request budget limits:

```go
req := &ai.CompletionRequest{
    Prompt:      "Long analysis task...",
    BudgetLimit: 1.0,  // Max $1.00 for this request
}
```

Check current budget usage:

```go
metrics := router.GetMetrics()
for provider, metric := range metrics {
    fmt.Printf("%s: $%.2f\n", provider, metric.TotalCostUSD)
}
```

### Caching

Enable caching to reduce costs and improve latency:

```go
config := &ai.RouterConfig{
    EnableCaching: true,
    CacheTTL:      time.Hour,  // Cache for 1 hour
}

cache := ai.NewInMemoryCache(config.CacheTTL)
router.SetCache(cache)
```

Responses are automatically cached based on:
- Prompt content
- Task type
- Complexity
- Model parameters

### Fallback Chains

Automatic fallback to alternative models if primary fails:

```go
config := &ai.RouterConfig{
    EnableFallback: true,
    MaxRetries:     3,
}
```

Fallback order is defined by the routing rules. For example:
- Reasoning task: o3 → Claude Opus → Gemini
- If o3 fails, automatically tries Claude Opus
- If Claude Opus fails, tries Gemini

### Metrics Collection

Track usage across all models:

```go
metrics := ai.NewMetricsCollector()
router.SetMetrics(metrics)

// Later, get summary
summary := metrics.GetSummary()
fmt.Printf("Total Requests: %d\n", summary.TotalRequests)
fmt.Printf("Total Cost: $%.2f\n", summary.TotalCost)

for provider, stats := range summary.ProviderBreakdown {
    fmt.Printf("\n%s:\n", provider)
    fmt.Printf("  Requests: %d\n", stats.Requests)
    fmt.Printf("  Cost: $%.2f\n", stats.Cost)
    fmt.Printf("  Avg Latency: %.0fms\n", stats.AvgLatency)
}
```

## Configuration File

Use YAML configuration for production deployments:

```yaml
# config/ai_models.yaml
models:
  openai:
    models:
      - name: o3-mini
        max_tokens: 128000
        cost_per_1k_tokens: 0.015

routing_rules:
  reasoning:
    complex:
      primary: openai/o3
      fallback: [anthropic/claude-opus-4.1]

budget:
  daily_limit_usd: 500.0
  alert_threshold_percent: 80.0

cache:
  enabled: true
  ttl_seconds: 3600
```

Load configuration:

```go
import "github.com/Melampe001/Tokyo-IA/internal/config"

cfg, err := config.LoadAIConfig("config/ai_models.yaml")
if err != nil {
    log.Fatal(err)
}
```

## Cost Optimization

### Tips for Reducing Costs

1. **Enable Caching**: Can achieve 40%+ cache hit rate
   ```go
   config.EnableCaching = true
   ```

2. **Use Appropriate Complexity**: Don't use `ComplexityComplex` for simple tasks
   ```go
   req.Complexity = ai.ComplexitySimple  // Uses cheaper models
   ```

3. **Set Budget Limits**: Prevent runaway costs
   ```go
   config.BudgetLimitDaily = 100.0  // $100/day max
   ```

4. **Use Local Models**: For high-volume or privacy-sensitive workloads
   ```go
   req.PrivacyRequired = true  // Uses local Llama 4 (free)
   ```

5. **Monitor Usage**: Track costs in real-time
   ```go
   metrics := router.GetMetrics()
   totalCost := metrics.GetTotalCost()
   ```

### Cost Examples

Typical costs per 1K tokens:
- OpenAI o3: $0.03
- OpenAI o3-mini: $0.015
- Claude Opus 4.1: $0.015
- Claude Sonnet 4.5: $0.008
- Gemini 3.0: $0.01
- Llama 4 (local): $0.00 (infrastructure only)

Example request costs:
- Simple chat (100 tokens): $0.0008 - $0.003
- Code review (2000 tokens): $0.016 - $0.06
- Complex analysis (5000 tokens): $0.04 - $0.15

## Error Handling

The router handles various error scenarios:

```go
resp, err := router.Complete(ctx, req)
if err != nil {
    switch err {
    case ai.ErrBudgetExceeded:
        log.Println("Daily budget limit reached")
    case ai.ErrNoAvailableModel:
        log.Println("No models available for this request")
    case ai.ErrInvalidRequest:
        log.Println("Invalid request parameters")
    default:
        log.Printf("Request failed: %v", err)
    }
    return
}
```

## Best Practices

1. **Always set MaxTokens**: Prevents unexpectedly large responses
   ```go
   req.MaxTokens = 1000  // Limit response size
   ```

2. **Use appropriate task types**: Helps router make better decisions
   ```go
   req.TaskType = ai.TaskTypeCodeReview  // Not ai.TaskTypeChat
   ```

3. **Enable metrics**: Track usage and costs
   ```go
   router.SetMetrics(ai.NewMetricsCollector())
   ```

4. **Set timeouts**: Prevent hanging requests
   ```go
   ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
   defer cancel()
   ```

5. **Handle errors gracefully**: Always check error returns
   ```go
   if err != nil {
       // Handle error appropriately
   }
   ```

## Troubleshooting

### High Costs

**Problem**: Daily budget limit being exceeded

**Solutions**:
1. Enable caching to reduce duplicate requests
2. Use appropriate complexity levels
3. Set per-request budget limits
4. Consider using local Llama 4 for high-volume tasks

### Slow Responses

**Problem**: High latency on requests

**Solutions**:
1. Check network connectivity to API providers
2. Enable caching for repeated queries
3. Use faster models for simple tasks
4. Consider deploying local Llama 4

### Model Unavailability

**Problem**: Models returning unavailable

**Solutions**:
1. Verify API keys are set correctly
2. Check API rate limits with providers
3. Enable fallback chains
4. Monitor provider status pages

### Budget Exceeded Errors

**Problem**: Getting `ErrBudgetExceeded` errors

**Solutions**:
1. Increase daily budget limit
2. Optimize prompt lengths
3. Use cheaper models where appropriate
4. Implement request queuing for off-peak hours

## API Integration

See the HTTP API service for REST endpoint usage:

```bash
# Make a completion request
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain Docker containers",
    "task_type": "documentation",
    "max_tokens": 500
  }'

# Get metrics
curl http://localhost:8080/ai/metrics
```

## Additional Resources

- [Architecture Documentation](../architecture/ai-models-integration-architecture.md)
- [Agent Workflows Guide](./agent-workflows-guide.md)
- [API Reference](../api/ai-api-reference.md)
- [Operations Runbook](../runbooks/ai-operations-runbook.md)
