// Package clients provides real AI model client implementations.
package clients

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"

	"github.com/Melampe001/Tokyo-IA/internal/ai"
)

// AnthropicRequest represents a request to the Anthropic API.
type AnthropicRequest struct {
	Model       string         `json:"model"`
	Messages    []AnthropicMsg `json:"messages"`
	MaxTokens   int            `json:"max_tokens"`
	Temperature float64        `json:"temperature,omitempty"`
	System      string         `json:"system,omitempty"`
}

// AnthropicMsg represents a message in the Anthropic API format.
type AnthropicMsg struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

// AnthropicResponse represents a response from the Anthropic API.
type AnthropicResponse struct {
	ID      string `json:"id"`
	Type    string `json:"type"`
	Role    string `json:"role"`
	Content []struct {
		Type string `json:"type"`
		Text string `json:"text"`
	} `json:"content"`
	Model        string `json:"model"`
	StopReason   string `json:"stop_reason"`
	StopSequence string `json:"stop_sequence"`
	Usage        struct {
		InputTokens  int `json:"input_tokens"`
		OutputTokens int `json:"output_tokens"`
	} `json:"usage"`
}

// RealAnthropicClient is a client for Anthropic Claude models.
type RealAnthropicClient struct {
	apiKey    string
	modelName string
	client    *http.Client
	baseURL   string
}

// NewRealAnthropicClient creates a new Anthropic client with real API integration.
func NewRealAnthropicClient(apiKey, modelName string) *RealAnthropicClient {
	return &RealAnthropicClient{
		apiKey:    apiKey,
		modelName: modelName,
		client:    &http.Client{},
		baseURL:   "https://api.anthropic.com/v1/messages",
	}
}

// Complete implements the ModelClient interface with real Anthropic API calls.
func (c *RealAnthropicClient) Complete(ctx context.Context, req *ai.CompletionRequest) (*ai.CompletionResponse, error) {
	// Set defaults
	maxTokens := req.MaxTokens
	if maxTokens <= 0 {
		maxTokens = 2048
	}

	temperature := req.Temperature
	if temperature <= 0 {
		temperature = 0.7
	}

	// Build request
	anthropicReq := AnthropicRequest{
		Model: c.modelName,
		Messages: []AnthropicMsg{
			{
				Role:    "user",
				Content: req.Prompt,
			},
		},
		MaxTokens:   maxTokens,
		Temperature: temperature,
	}

	// Marshal to JSON
	jsonData, err := json.Marshal(anthropicReq)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %w", err)
	}

	// Create HTTP request
	httpReq, err := http.NewRequestWithContext(ctx, "POST", c.baseURL, bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	// Set headers
	httpReq.Header.Set("Content-Type", "application/json")
	httpReq.Header.Set("x-api-key", c.apiKey)
	httpReq.Header.Set("anthropic-version", "2023-06-01")

	// Make the request
	resp, err := c.client.Do(httpReq)
	if err != nil {
		return nil, fmt.Errorf("anthropic api error: %w", err)
	}
	defer resp.Body.Close()

	// Read response body
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response: %w", err)
	}

	// Check for errors
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("anthropic api error: status %d, body: %s", resp.StatusCode, string(body))
	}

	// Parse response
	var anthropicResp AnthropicResponse
	if err := json.Unmarshal(body, &anthropicResp); err != nil {
		return nil, fmt.Errorf("failed to parse response: %w", err)
	}

	// Extract content
	var content string
	if len(anthropicResp.Content) > 0 {
		content = anthropicResp.Content[0].Text
	}

	// Calculate cost
	tokensUsed := anthropicResp.Usage.InputTokens + anthropicResp.Usage.OutputTokens
	costPerToken := c.GetCostPerToken()
	totalCost := float64(tokensUsed) * costPerToken

	return &ai.CompletionResponse{
		Content:      content,
		Model:        c.modelName,
		Provider:     ai.ProviderAnthropic,
		TokensUsed:   tokensUsed,
		LatencyMs:    0,
		CostUSD:      totalCost,
		CachedResult: false,
	}, nil
}

// GetProvider returns the provider name.
func (c *RealAnthropicClient) GetProvider() ai.ModelProvider {
	return ai.ProviderAnthropic
}

// GetModelName returns the model name.
func (c *RealAnthropicClient) GetModelName() string {
	return c.modelName
}

// IsAvailable checks if the model is available.
func (c *RealAnthropicClient) IsAvailable(ctx context.Context) bool {
	return c.apiKey != ""
}

// GetCostPerToken returns the approximate cost per token.
func (c *RealAnthropicClient) GetCostPerToken() float64 {
	// Approximate pricing for Claude models
	switch c.modelName {
	case "claude-opus-4", "claude-opus-4.1":
		return 0.000015
	case "claude-sonnet-3.5", "claude-sonnet-4", "claude-sonnet-4.5":
		return 0.000003
	case "claude-haiku-3", "claude-haiku-3.5":
		return 0.00000025
	default:
		return 0.000003 // Default to Sonnet pricing
	}
}
