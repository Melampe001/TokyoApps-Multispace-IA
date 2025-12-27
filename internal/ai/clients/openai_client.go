// Package clients provides real AI model client implementations.
package clients

import (
	"context"
	"fmt"

	"github.com/Melampe001/Tokyo-IA/internal/ai"
	"github.com/sashabaranov/go-openai"
)

// RealOpenAIClient is a client for OpenAI models using the official SDK.
type RealOpenAIClient struct {
	client    *openai.Client
	modelName string
}

// NewRealOpenAIClient creates a new OpenAI client with real API integration.
func NewRealOpenAIClient(apiKey, modelName string) *RealOpenAIClient {
	return &RealOpenAIClient{
		client:    openai.NewClient(apiKey),
		modelName: modelName,
	}
}

// Complete implements the ModelClient interface with real OpenAI API calls.
func (c *RealOpenAIClient) Complete(ctx context.Context, req *ai.CompletionRequest) (*ai.CompletionResponse, error) {
	// Build the chat completion request
	messages := []openai.ChatCompletionMessage{
		{
			Role:    openai.ChatMessageRoleUser,
			Content: req.Prompt,
		},
	}

	// Set defaults if not provided
	maxTokens := req.MaxTokens
	if maxTokens <= 0 {
		maxTokens = 2048
	}

	temperature := float32(req.Temperature)
	if temperature <= 0 {
		temperature = 0.7
	}

	// Make the API call
	resp, err := c.client.CreateChatCompletion(ctx, openai.ChatCompletionRequest{
		Model:       c.modelName,
		Messages:    messages,
		MaxTokens:   maxTokens,
		Temperature: temperature,
	})
	if err != nil {
		return nil, fmt.Errorf("openai api error: %w", err)
	}

	if len(resp.Choices) == 0 {
		return nil, fmt.Errorf("no response choices returned from openai")
	}

	// Calculate cost (approximate - adjust based on actual model pricing)
	tokensUsed := resp.Usage.TotalTokens
	costPerToken := c.GetCostPerToken()
	totalCost := float64(tokensUsed) * costPerToken

	return &ai.CompletionResponse{
		Content:      resp.Choices[0].Message.Content,
		Model:        c.modelName,
		Provider:     ai.ProviderOpenAI,
		TokensUsed:   tokensUsed,
		LatencyMs:    0, // Could be calculated if we track timing
		CostUSD:      totalCost,
		CachedResult: false,
	}, nil
}

// GetProvider returns the provider name.
func (c *RealOpenAIClient) GetProvider() ai.ModelProvider {
	return ai.ProviderOpenAI
}

// GetModelName returns the model name.
func (c *RealOpenAIClient) GetModelName() string {
	return c.modelName
}

// IsAvailable checks if the model is available.
func (c *RealOpenAIClient) IsAvailable(ctx context.Context) bool {
	// Simple check - could be enhanced with actual API ping
	return c.client != nil
}

// GetCostPerToken returns the approximate cost per token.
func (c *RealOpenAIClient) GetCostPerToken() float64 {
	// Approximate pricing - adjust based on model
	// o3: ~$0.0001/token, gpt-4: ~$0.00003/token
	switch c.modelName {
	case "o3", "o3-mini":
		return 0.0001
	case "gpt-4-turbo", "gpt-4":
		return 0.00003
	case "gpt-3.5-turbo":
		return 0.000002
	default:
		return 0.00003 // Default to gpt-4 pricing
	}
}
