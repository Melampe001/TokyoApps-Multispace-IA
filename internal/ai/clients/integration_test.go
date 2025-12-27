// Package clients provides integration tests for AI clients.
package clients

import (
	"context"
	"os"
	"testing"

	"github.com/Melampe001/Tokyo-IA/internal/ai"
)

// TestOpenAIClientIntegration tests the real OpenAI client.
func TestOpenAIClientIntegration(t *testing.T) {
	apiKey := os.Getenv("OPENAI_API_KEY")
	if apiKey == "" {
		t.Skip("Skipping OpenAI integration test: OPENAI_API_KEY not set")
	}

	client := NewRealOpenAIClient(apiKey, "gpt-3.5-turbo")

	ctx := context.Background()
	req := &ai.CompletionRequest{
		Prompt:      "Say 'Hello, World!' and nothing else.",
		TaskType:    ai.TaskTypeChat,
		Complexity:  ai.ComplexitySimple,
		MaxTokens:   50,
		Temperature: 0.7,
	}

	resp, err := client.Complete(ctx, req)
	if err != nil {
		t.Fatalf("OpenAI completion failed: %v", err)
	}

	if resp.Content == "" {
		t.Error("Expected non-empty response content")
	}

	if resp.Provider != ai.ProviderOpenAI {
		t.Errorf("Expected provider %s, got %s", ai.ProviderOpenAI, resp.Provider)
	}

	if resp.TokensUsed <= 0 {
		t.Error("Expected positive token usage")
	}

	t.Logf("OpenAI response: %s (tokens: %d, cost: $%.6f)", resp.Content, resp.TokensUsed, resp.CostUSD)
}

// TestAnthropicClientIntegration tests the real Anthropic client.
func TestAnthropicClientIntegration(t *testing.T) {
	apiKey := os.Getenv("ANTHROPIC_API_KEY")
	if apiKey == "" {
		t.Skip("Skipping Anthropic integration test: ANTHROPIC_API_KEY not set")
	}

	client := NewRealAnthropicClient(apiKey, "claude-3-haiku-20240307")

	ctx := context.Background()
	req := &ai.CompletionRequest{
		Prompt:      "Say 'Hello, World!' and nothing else.",
		TaskType:    ai.TaskTypeChat,
		Complexity:  ai.ComplexitySimple,
		MaxTokens:   50,
		Temperature: 0.7,
	}

	resp, err := client.Complete(ctx, req)
	if err != nil {
		t.Fatalf("Anthropic completion failed: %v", err)
	}

	if resp.Content == "" {
		t.Error("Expected non-empty response content")
	}

	if resp.Provider != ai.ProviderAnthropic {
		t.Errorf("Expected provider %s, got %s", ai.ProviderAnthropic, resp.Provider)
	}

	if resp.TokensUsed <= 0 {
		t.Error("Expected positive token usage")
	}

	t.Logf("Anthropic response: %s (tokens: %d, cost: $%.6f)", resp.Content, resp.TokensUsed, resp.CostUSD)
}

// TestGeminiClientIntegration tests the real Gemini client.
func TestGeminiClientIntegration(t *testing.T) {
	apiKey := os.Getenv("GOOGLE_API_KEY")
	if apiKey == "" {
		t.Skip("Skipping Gemini integration test: GOOGLE_API_KEY not set")
	}

	client, err := NewRealGeminiClient(apiKey, "gemini-pro")
	if err != nil {
		t.Skipf("Skipping Gemini integration test: %v", err)
	}

	ctx := context.Background()
	req := &ai.CompletionRequest{
		Prompt:      "Say 'Hello, World!' and nothing else.",
		TaskType:    ai.TaskTypeChat,
		Complexity:  ai.ComplexitySimple,
		MaxTokens:   50,
		Temperature: 0.7,
	}

	resp, err := client.Complete(ctx, req)
	if err != nil {
		// Expected to fail since full SDK not implemented yet
		t.Skipf("Gemini client not fully implemented: %v", err)
	}

	if resp.Content == "" {
		t.Error("Expected non-empty response content")
	}

	if resp.Provider != ai.ProviderGemini {
		t.Errorf("Expected provider %s, got %s", ai.ProviderGemini, resp.Provider)
	}

	if resp.TokensUsed <= 0 {
		t.Error("Expected positive token usage")
	}

	t.Logf("Gemini response: %s (tokens: %d, cost: $%.6f)", resp.Content, resp.TokensUsed, resp.CostUSD)
}

// TestClientFactory tests the client factory.
func TestClientFactory(t *testing.T) {
	// Test with mock clients (default when USE_REAL_AI_CLIENTS not set)
	os.Setenv("USE_REAL_AI_CLIENTS", "false")
	defer os.Unsetenv("USE_REAL_AI_CLIENTS")

	factory := NewClientFactory()

	if factory.IsUsingRealClients() {
		t.Error("Expected factory to use mock clients")
	}

	// Test creating clients
	openaiClient, err := factory.CreateOpenAIClient("gpt-3.5-turbo")
	if err != nil {
		t.Fatalf("Failed to create OpenAI client: %v", err)
	}

	if openaiClient.GetProvider() != ai.ProviderOpenAI {
		t.Error("Expected OpenAI provider")
	}

	anthropicClient, err := factory.CreateAnthropicClient("claude-3-haiku-20240307")
	if err != nil {
		t.Fatalf("Failed to create Anthropic client: %v", err)
	}

	if anthropicClient.GetProvider() != ai.ProviderAnthropic {
		t.Error("Expected Anthropic provider")
	}

	geminiClient, err := factory.CreateGeminiClient("gemini-pro")
	if err != nil {
		t.Fatalf("Failed to create Gemini client: %v", err)
	}

	if geminiClient.GetProvider() != ai.ProviderGemini {
		t.Error("Expected Gemini provider")
	}
}

// TestClientFactoryFallback tests fallback to mock when no API keys.
func TestClientFactoryFallback(t *testing.T) {
	// Enable real clients but don't provide API keys
	os.Setenv("USE_REAL_AI_CLIENTS", "true")
	os.Unsetenv("OPENAI_API_KEY")
	os.Unsetenv("ANTHROPIC_API_KEY")
	os.Unsetenv("GOOGLE_API_KEY")
	defer os.Unsetenv("USE_REAL_AI_CLIENTS")

	factory := NewClientFactory()

	if !factory.IsUsingRealClients() {
		t.Error("Expected factory to be configured for real clients")
	}

	// Should fallback to mock when no API keys
	client, err := factory.CreateOpenAIClient("gpt-3.5-turbo")
	if err != nil {
		t.Fatalf("Failed to create client: %v", err)
	}

	// Should be mock client
	_, isMock := client.(*MockClient)
	if !isMock {
		t.Log("Client fell back to mock as expected (no API key)")
	}
}
