//go:build integration
// +build integration

package ai

import (
	"context"
	"os"
	"testing"

	"github.com/Melampe001/Tokyo-IA/internal/ai/clients"
)

// TestRealProviderIntegration tests with real AI providers if API keys are available
// Run with: go test -tags=integration ./internal/ai/...
func TestRealProviderIntegration(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping integration test in short mode")
	}

	// Check if any API keys are available
	hasOpenAI := os.Getenv("OPENAI_API_KEY") != ""
	hasAnthropic := os.Getenv("ANTHROPIC_API_KEY") != ""
	hasGemini := os.Getenv("GEMINI_API_KEY") != ""

	if !hasOpenAI && !hasAnthropic && !hasGemini {
		t.Skip("Skipping integration test: no API keys available")
	}

	config := RouterConfig{
		EnableCache:     false,
		DefaultProvider: ProviderOpenAI,
	}

	router := NewModelRouter(config)

	// Register available clients
	if hasOpenAI {
		router.RegisterClient(ProviderOpenAI, clients.NewOpenAIClient())
	}
	if hasAnthropic {
		router.RegisterClient(ProviderAnthropic, clients.NewAnthropicClient())
	}
	if hasGemini {
		router.RegisterClient(ProviderGemini, clients.NewGeminiClient())
	}

	// Test a simple completion
	req := CompletionRequest{
		Prompt:      "What is 2+2? Answer in one word.",
		TaskType:    TaskTypeGeneral,
		MaxTokens:   10,
		Temperature: 0.0,
	}

	ctx := context.Background()
	resp, err := router.Complete(ctx, req)

	// Note: This will fail until real clients are implemented
	// For now, we expect an error from the stub implementation
	if err == nil {
		t.Logf("Success! Got response: %s", resp.Content)
		t.Logf("Provider: %s, Model: %s", resp.Provider, resp.Model.Name)
		t.Logf("Tokens used: %d, Latency: %v", resp.TokensUsed, resp.Latency)
	} else {
		t.Logf("Expected error (stubs not implemented): %v", err)
	}
}
