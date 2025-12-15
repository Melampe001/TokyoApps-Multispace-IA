package clients

import (
	"context"
	"fmt"
	"os"

	"github.com/Melampe001/Tokyo-IA/internal/ai"
)

// GeminiClient is a client for Google Gemini API
type GeminiClient struct {
	apiKey string
	model  string
}

// NewGeminiClient creates a new Gemini client
// TODO: Implement real Gemini client
// This requires GEMINI_API_KEY environment variable
// Implementation guide: docs/guides/ai-model-router-guide.md#api-keys
// Example: Use google.golang.org/api/generativeai/v1beta
func NewGeminiClient() *GeminiClient {
	return &GeminiClient{
		apiKey: os.Getenv("GEMINI_API_KEY"),
		model:  "gemini-pro",
	}
}

// Complete sends a completion request to Gemini
// TODO: Implement actual Gemini API integration
// For now, returns an error indicating stub implementation
func (c *GeminiClient) Complete(ctx context.Context, req ai.CompletionRequest) (*ai.CompletionResponse, error) {
	if c.apiKey == "" {
		return nil, fmt.Errorf("GEMINI_API_KEY not set")
	}

	// TODO: Implement real Gemini API call using official SDK
	// Example integration:
	// 1. Import "google.golang.org/api/generativeai/v1beta"
	// 2. Create client with API key
	// 3. Call generate content endpoint
	// 4. Map response to CompletionResponse

	return nil, fmt.Errorf("Gemini client not yet implemented - this is a stub")
}

// Name returns the client name
func (c *GeminiClient) Name() string {
	return c.model
}

// IsAvailable returns whether the client is available
func (c *GeminiClient) IsAvailable() bool {
	// Client is available if API key is set
	// TODO: Add connectivity check to Gemini API
	return c.apiKey != ""
}
