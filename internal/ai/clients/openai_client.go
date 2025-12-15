package clients

import (
	"context"
	"fmt"
	"os"

	"github.com/Melampe001/Tokyo-IA/internal/ai"
)

// OpenAIClient is a client for OpenAI API
type OpenAIClient struct {
	apiKey string
	model  string
}

// NewOpenAIClient creates a new OpenAI client
// TODO: Implement real OpenAI client
// This requires OPENAI_API_KEY environment variable
// Implementation guide: docs/guides/ai-model-router-guide.md#api-keys
// Example: Use github.com/openai/openai-go SDK
func NewOpenAIClient() *OpenAIClient {
	return &OpenAIClient{
		apiKey: os.Getenv("OPENAI_API_KEY"),
		model:  "gpt-4",
	}
}

// Complete sends a completion request to OpenAI
// TODO: Implement actual OpenAI API integration
// For now, returns an error indicating stub implementation
func (c *OpenAIClient) Complete(ctx context.Context, req ai.CompletionRequest) (*ai.CompletionResponse, error) {
	if c.apiKey == "" {
		return nil, fmt.Errorf("OPENAI_API_KEY not set")
	}

	// TODO: Implement real OpenAI API call using official SDK
	// Example integration:
	// 1. Import "github.com/openai/openai-go"
	// 2. Create client with API key
	// 3. Call chat completion endpoint
	// 4. Map response to CompletionResponse

	return nil, fmt.Errorf("OpenAI client not yet implemented - this is a stub")
}

// Name returns the client name
func (c *OpenAIClient) Name() string {
	return c.model
}

// IsAvailable returns whether the client is available
func (c *OpenAIClient) IsAvailable() bool {
	// Client is available if API key is set
	// TODO: Add connectivity check to OpenAI API
	return c.apiKey != ""
}
