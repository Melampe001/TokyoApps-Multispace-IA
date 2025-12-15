package ai

import (
	"context"
	"time"
)

// TaskType represents different types of AI tasks
type TaskType string

const (
	TaskTypeReasoning   TaskType = "reasoning"
	TaskTypeCreative    TaskType = "creative"
	TaskTypeCodeReview  TaskType = "code_review"
	TaskTypeCodeGen     TaskType = "code_generation"
	TaskTypeTranslation TaskType = "translation"
	TaskTypeGeneral     TaskType = "general"
)

// Provider represents an AI model provider
type Provider string

const (
	ProviderOpenAI    Provider = "openai"
	ProviderAnthropic Provider = "anthropic"
	ProviderGemini    Provider = "gemini"
)

// Model represents a specific AI model
type Model struct {
	Provider  Provider
	Name      string
	MaxTokens int
}

// CompletionRequest represents a request for AI completion
type CompletionRequest struct {
	Prompt      string
	TaskType    TaskType
	MaxTokens   int
	Temperature float64
	Model       *Model // Optional: force specific model
}

// CompletionResponse represents an AI completion response
type CompletionResponse struct {
	Content    string
	Model      Model
	TokensUsed int
	Latency    time.Duration
	CacheHit   bool
	Provider   Provider
}

// AIClient is the interface that all AI provider clients must implement
type AIClient interface {
	Complete(ctx context.Context, req CompletionRequest) (*CompletionResponse, error)
	Name() string
	IsAvailable() bool
}

// RoutingDecision contains information about how a request was routed
type RoutingDecision struct {
	SelectedProvider Provider
	SelectedModel    Model
	Reason           string
	Confidence       float64
}
