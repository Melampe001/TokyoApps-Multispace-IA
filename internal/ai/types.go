// Package ai provides AI model integration and orchestration functionality.
package ai

import (
	"context"
	"time"
)

// ModelProvider represents different AI model providers.
type ModelProvider string

const (
	ProviderOpenAI    ModelProvider = "openai"
	ProviderAnthropic ModelProvider = "anthropic"
	ProviderGemini    ModelProvider = "gemini"
	ProviderGrok      ModelProvider = "grok"
	ProviderLlama     ModelProvider = "llama"
)

// TaskType represents the type of AI task to perform.
type TaskType string

const (
	TaskTypeReasoning     TaskType = "reasoning"
	TaskTypeCodeGen       TaskType = "code_generation"
	TaskTypeCodeReview    TaskType = "code_review"
	TaskTypeMultimodal    TaskType = "multimodal"
	TaskTypeDocumentation TaskType = "documentation"
	TaskTypeChat          TaskType = "chat"
)

// ComplexityLevel represents the complexity of a task.
type ComplexityLevel string

const (
	ComplexitySimple   ComplexityLevel = "simple"
	ComplexityModerate ComplexityLevel = "moderate"
	ComplexityComplex  ComplexityLevel = "complex"
)

// CompletionRequest represents a request to an AI model.
type CompletionRequest struct {
	Prompt          string
	TaskType        TaskType
	Complexity      ComplexityLevel
	MaxTokens       int
	Temperature     float64
	PrivacyRequired bool
	BudgetLimit     float64
	Metadata        map[string]string
}

// CompletionResponse represents a response from an AI model.
type CompletionResponse struct {
	Content      string
	Model        string
	Provider     ModelProvider
	TokensUsed   int
	LatencyMs    int64
	CostUSD      float64
	CachedResult bool
	Timestamp    time.Time
}

// ModelClient is the interface that all AI model clients must implement.
type ModelClient interface {
	Complete(ctx context.Context, req *CompletionRequest) (*CompletionResponse, error)
	GetProvider() ModelProvider
	GetModelName() string
	IsAvailable(ctx context.Context) bool
	GetCostPerToken() float64
}

// ModelMetrics holds performance metrics for a model.
type ModelMetrics struct {
	Provider     ModelProvider
	Model        string
	RequestCount int64
	ErrorCount   int64
	TotalTokens  int64
	TotalCostUSD float64
	AvgLatencyMs float64
	LastUsed     time.Time
}

// RoutingDecision represents the result of the routing decision.
type RoutingDecision struct {
	SelectedProvider ModelProvider
	SelectedModel    string
	Reason           string
	FallbackChain    []ModelProvider
	EstimatedCostUSD float64
}
