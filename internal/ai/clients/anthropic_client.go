package clients

import (
	"context"
	"fmt"
	"os"

	"github.com/Melampe001/Tokyo-IA/internal/ai"
)

// AnthropicClient is a client for Anthropic Claude API
type AnthropicClient struct {
	apiKey string
	model  string
}

// NewAnthropicClient creates a new Anthropic client
// TODO: Implement real Anthropic client
// This requires ANTHROPIC_API_KEY environment variable
// Implementation guide: docs/guides/ai-model-router-guide.md#api-keys
// Example: Use official Anthropic SDK
func NewAnthropicClient() *AnthropicClient {
	return &AnthropicClient{
		apiKey: os.Getenv("ANTHROPIC_API_KEY"),
		model:  "claude-3-opus-20240229",
	}
}

// Complete sends a completion request to Anthropic
// TODO: Implement actual Anthropic API integration
// For now, returns an error indicating stub implementation
func (c *AnthropicClient) Complete(ctx context.Context, req ai.CompletionRequest) (*ai.CompletionResponse, error) {
	if c.apiKey == "" {
		return nil, fmt.Errorf("ANTHROPIC_API_KEY not set")
	}

	// TODO: Implement real Anthropic API call using official SDK
	// Example integration:
	// 1. Import Anthropic SDK (e.g., "github.com/anthropics/anthropic-sdk-go")
	// 2. Create client with API key
	// 3. Call messages endpoint
	// 4. Map response to CompletionResponse

	return nil, fmt.Errorf("Anthropic client not yet implemented - this is a stub")
}

// Name returns the client name
func (c *AnthropicClient) Name() string {
	return c.model
}

// IsAvailable returns whether the client is available
func (c *AnthropicClient) IsAvailable() bool {
	// Client is available if API key is set
	// TODO: Add connectivity check to Anthropic API
	return c.apiKey != ""
}
