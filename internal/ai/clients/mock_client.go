// Package clients provides AI model client implementations.
package clients

import (
	"context"
	"errors"
	"fmt"
	"math/rand"
	"time"

	"github.com/Melampe001/Tokyo-IA/internal/ai"
)

// MockClient is a mock implementation of ModelClient for testing and development.
type MockClient struct {
	provider      ai.ModelProvider
	modelName     string
	costPerToken  float64
	baseLatencyMs int
	available     bool
}

// NewMockClient creates a new mock client.
func NewMockClient(provider ai.ModelProvider, modelName string, costPerToken float64) *MockClient {
	return &MockClient{
		provider:      provider,
		modelName:     modelName,
		costPerToken:  costPerToken,
		baseLatencyMs: 100,
		available:     true,
	}
}

// Complete implements the ModelClient interface.
func (c *MockClient) Complete(ctx context.Context, req *ai.CompletionRequest) (*ai.CompletionResponse, error) {
	if !c.available {
		return nil, errors.New("model unavailable")
	}

	// Simulate processing time
	latency := c.baseLatencyMs + rand.Intn(50)
	time.Sleep(time.Duration(latency) * time.Millisecond)

	// Simulate token usage
	tokensUsed := len(req.Prompt)/4 + req.MaxTokens/2

	// Generate mock response based on task type
	content := c.generateMockResponse(req)

	return &ai.CompletionResponse{
		Content:      content,
		Model:        c.modelName,
		Provider:     c.provider,
		TokensUsed:   tokensUsed,
		LatencyMs:    int64(latency),
		CostUSD:      float64(tokensUsed) * c.costPerToken,
		CachedResult: false,
		Timestamp:    time.Now(),
	}, nil
}

// GetProvider returns the provider name.
func (c *MockClient) GetProvider() ai.ModelProvider {
	return c.provider
}

// GetModelName returns the model name.
func (c *MockClient) GetModelName() string {
	return c.modelName
}

// IsAvailable checks if the model is available.
func (c *MockClient) IsAvailable(ctx context.Context) bool {
	return c.available
}

// GetCostPerToken returns the cost per token.
func (c *MockClient) GetCostPerToken() float64 {
	return c.costPerToken
}

// SetAvailable sets the availability status (for testing).
func (c *MockClient) SetAvailable(available bool) {
	c.available = available
}

// generateMockResponse generates a mock response based on the request.
func (c *MockClient) generateMockResponse(req *ai.CompletionRequest) string {
	switch req.TaskType {
	case ai.TaskTypeReasoning:
		return fmt.Sprintf("[%s] Analyzing the problem: %s... After deep reasoning, the solution is...",
			c.modelName, req.Prompt[:min(50, len(req.Prompt))])
	case ai.TaskTypeCodeGen:
		return fmt.Sprintf("[%s] Here's the generated code:\n```go\npackage main\nfunc solution() {}\n```", c.modelName)
	case ai.TaskTypeCodeReview:
		return fmt.Sprintf("[%s] Code review complete. Found 0 issues. Code quality is excellent.", c.modelName)
	case ai.TaskTypeMultimodal:
		return fmt.Sprintf("[%s] Multimodal analysis: Image shows... Text indicates...", c.modelName)
	case ai.TaskTypeDocumentation:
		return fmt.Sprintf("[%s] # Documentation\n\nThis function does...", c.modelName)
	default:
		return fmt.Sprintf("[%s] Response to: %s", c.modelName, req.Prompt[:min(100, len(req.Prompt))])
	}
}

// min returns the minimum of two integers.
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

// OpenAIClient is a client for OpenAI models (stub implementation).
type OpenAIClient struct {
	apiKey    string
	modelName string
}

// NewOpenAIClient creates a new OpenAI client.
func NewOpenAIClient(apiKey, modelName string) *OpenAIClient {
	return &OpenAIClient{
		apiKey:    apiKey,
		modelName: modelName,
	}
}

// Complete implements the ModelClient interface.
func (c *OpenAIClient) Complete(ctx context.Context, req *ai.CompletionRequest) (*ai.CompletionResponse, error) {
	// TODO: Implement actual OpenAI API integration
	// For now, use mock client
	mock := NewMockClient(ai.ProviderOpenAI, c.modelName, 0.00003)
	return mock.Complete(ctx, req)
}

// GetProvider returns the provider name.
func (c *OpenAIClient) GetProvider() ai.ModelProvider {
	return ai.ProviderOpenAI
}

// GetModelName returns the model name.
func (c *OpenAIClient) GetModelName() string {
	return c.modelName
}

// IsAvailable checks if the model is available.
func (c *OpenAIClient) IsAvailable(ctx context.Context) bool {
	return c.apiKey != ""
}

// GetCostPerToken returns the cost per token.
func (c *OpenAIClient) GetCostPerToken() float64 {
	// Approximate cost for o3-mini
	return 0.00003
}

// AnthropicClient is a client for Anthropic Claude models (stub implementation).
type AnthropicClient struct {
	apiKey    string
	modelName string
}

// NewAnthropicClient creates a new Anthropic client.
func NewAnthropicClient(apiKey, modelName string) *AnthropicClient {
	return &AnthropicClient{
		apiKey:    apiKey,
		modelName: modelName,
	}
}

// Complete implements the ModelClient interface.
func (c *AnthropicClient) Complete(ctx context.Context, req *ai.CompletionRequest) (*ai.CompletionResponse, error) {
	// TODO: Implement actual Anthropic API integration
	mock := NewMockClient(ai.ProviderAnthropic, c.modelName, 0.000015)
	return mock.Complete(ctx, req)
}

// GetProvider returns the provider name.
func (c *AnthropicClient) GetProvider() ai.ModelProvider {
	return ai.ProviderAnthropic
}

// GetModelName returns the model name.
func (c *AnthropicClient) GetModelName() string {
	return c.modelName
}

// IsAvailable checks if the model is available.
func (c *AnthropicClient) IsAvailable(ctx context.Context) bool {
	return c.apiKey != ""
}

// GetCostPerToken returns the cost per token.
func (c *AnthropicClient) GetCostPerToken() float64 {
	return 0.000015
}

// GeminiClient is a client for Google Gemini models (stub implementation).
type GeminiClient struct {
	apiKey    string
	modelName string
}

// NewGeminiClient creates a new Gemini client.
func NewGeminiClient(apiKey, modelName string) *GeminiClient {
	return &GeminiClient{
		apiKey:    apiKey,
		modelName: modelName,
	}
}

// Complete implements the ModelClient interface.
func (c *GeminiClient) Complete(ctx context.Context, req *ai.CompletionRequest) (*ai.CompletionResponse, error) {
	// TODO: Implement actual Gemini API integration
	mock := NewMockClient(ai.ProviderGemini, c.modelName, 0.00001)
	return mock.Complete(ctx, req)
}

// GetProvider returns the provider name.
func (c *GeminiClient) GetProvider() ai.ModelProvider {
	return ai.ProviderGemini
}

// GetModelName returns the model name.
func (c *GeminiClient) GetModelName() string {
	return c.modelName
}

// IsAvailable checks if the model is available.
func (c *GeminiClient) IsAvailable(ctx context.Context) bool {
	return c.apiKey != ""
}

// GetCostPerToken returns the cost per token.
func (c *GeminiClient) GetCostPerToken() float64 {
	return 0.00001
}
