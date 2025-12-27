// Package clients provides client factory for AI providers.
package clients

import (
	"fmt"
	"os"
	"strings"

	"github.com/Melampe001/Tokyo-IA/internal/ai"
)

// ClientFactory creates AI clients based on configuration.
type ClientFactory struct {
	useRealClients bool
}

// NewClientFactory creates a new client factory.
func NewClientFactory() *ClientFactory {
	useReal := strings.ToLower(os.Getenv("USE_REAL_AI_CLIENTS")) == "true"
	return &ClientFactory{
		useRealClients: useReal,
	}
}

// CreateOpenAIClient creates an OpenAI client (real or mock).
func (f *ClientFactory) CreateOpenAIClient(modelName string) (ai.ModelClient, error) {
	if !f.useRealClients {
		// Use mock client for development
		return NewMockClient(ai.ProviderOpenAI, modelName, 0.00003), nil
	}

	apiKey := os.Getenv("OPENAI_API_KEY")
	if apiKey == "" {
		// Fallback to mock if no API key
		return NewMockClient(ai.ProviderOpenAI, modelName, 0.00003), nil
	}

	return NewRealOpenAIClient(apiKey, modelName), nil
}

// CreateAnthropicClient creates an Anthropic client (real or mock).
func (f *ClientFactory) CreateAnthropicClient(modelName string) (ai.ModelClient, error) {
	if !f.useRealClients {
		// Use mock client for development
		return NewMockClient(ai.ProviderAnthropic, modelName, 0.000015), nil
	}

	apiKey := os.Getenv("ANTHROPIC_API_KEY")
	if apiKey == "" {
		// Fallback to mock if no API key
		return NewMockClient(ai.ProviderAnthropic, modelName, 0.000015), nil
	}

	return NewRealAnthropicClient(apiKey, modelName), nil
}

// CreateGeminiClient creates a Gemini client (real or mock).
func (f *ClientFactory) CreateGeminiClient(modelName string) (ai.ModelClient, error) {
	if !f.useRealClients {
		// Use mock client for development
		return NewMockClient(ai.ProviderGemini, modelName, 0.00001), nil
	}

	apiKey := os.Getenv("GOOGLE_API_KEY")
	if apiKey == "" {
		// Fallback to mock if no API key
		return NewMockClient(ai.ProviderGemini, modelName, 0.00001), nil
	}

	// Note: Real Gemini client returns error if SDK not fully implemented
	client, err := NewRealGeminiClient(apiKey, modelName)
	if err != nil {
		// Fallback to mock if real client fails
		return NewMockClient(ai.ProviderGemini, modelName, 0.00001), nil
	}

	return client, nil
}

// CreateClient creates a client for any provider.
func (f *ClientFactory) CreateClient(provider ai.ModelProvider, modelName string) (ai.ModelClient, error) {
	switch provider {
	case ai.ProviderOpenAI:
		return f.CreateOpenAIClient(modelName)
	case ai.ProviderAnthropic:
		return f.CreateAnthropicClient(modelName)
	case ai.ProviderGemini:
		return f.CreateGeminiClient(modelName)
	default:
		return nil, fmt.Errorf("unsupported provider: %s", provider)
	}
}

// IsUsingRealClients returns whether real clients are enabled.
func (f *ClientFactory) IsUsingRealClients() bool {
	return f.useRealClients
}
