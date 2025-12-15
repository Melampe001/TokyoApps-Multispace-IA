package ai

import (
	"context"
	"testing"
	"time"
)

func TestModelRouter_Complete(t *testing.T) {
	config := RouterConfig{
		EnableCache:     true,
		CacheTTL:        5 * time.Minute,
		DefaultProvider: ProviderOpenAI,
		TaskRouting: map[TaskType]Provider{
			TaskTypeReasoning: ProviderAnthropic,
			TaskTypeCreative:  ProviderOpenAI,
		},
	}

	router := NewModelRouter(config)
	router.RegisterClient(ProviderOpenAI, NewMockClient(ProviderOpenAI, "gpt-4-mock"))
	router.RegisterClient(ProviderAnthropic, NewMockClient(ProviderAnthropic, "claude-mock"))

	tests := []struct {
		name     string
		req      CompletionRequest
		wantErr  bool
		provider Provider
	}{
		{
			name: "reasoning task routes to Anthropic",
			req: CompletionRequest{
				Prompt:      "What is the meaning of life?",
				TaskType:    TaskTypeReasoning,
				MaxTokens:   100,
				Temperature: 0.7,
			},
			wantErr:  false,
			provider: ProviderAnthropic,
		},
		{
			name: "creative task routes to OpenAI",
			req: CompletionRequest{
				Prompt:      "Write a poem about the moon",
				TaskType:    TaskTypeCreative,
				MaxTokens:   100,
				Temperature: 0.9,
			},
			wantErr:  false,
			provider: ProviderOpenAI,
		},
		{
			name: "general task uses default provider",
			req: CompletionRequest{
				Prompt:      "Hello world",
				TaskType:    TaskTypeGeneral,
				MaxTokens:   50,
				Temperature: 0.7,
			},
			wantErr:  false,
			provider: ProviderOpenAI,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			ctx := context.Background()
			resp, err := router.Complete(ctx, tt.req)

			if (err != nil) != tt.wantErr {
				t.Errorf("Complete() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			if err != nil {
				return
			}

			if resp.Provider != tt.provider {
				t.Errorf("Complete() provider = %v, want %v", resp.Provider, tt.provider)
			}

			if resp.Content == "" {
				t.Error("Complete() returned empty content")
			}

			if resp.TokensUsed == 0 {
				t.Error("Complete() returned zero tokens used")
			}
		})
	}
}

func TestModelRouter_Cache(t *testing.T) {
	config := RouterConfig{
		EnableCache:     true,
		CacheTTL:        1 * time.Second,
		DefaultProvider: ProviderOpenAI,
	}

	router := NewModelRouter(config)
	mockClient := NewMockClient(ProviderOpenAI, "gpt-4-mock")
	router.RegisterClient(ProviderOpenAI, mockClient)

	req := CompletionRequest{
		Prompt:      "Test prompt",
		TaskType:    TaskTypeGeneral,
		MaxTokens:   100,
		Temperature: 0.7,
	}

	ctx := context.Background()

	// First request should not be cached
	resp1, err := router.Complete(ctx, req)
	if err != nil {
		t.Fatalf("Complete() error = %v", err)
	}

	if resp1.CacheHit {
		t.Error("First request should not be a cache hit")
	}

	// Second request should be cached
	resp2, err := router.Complete(ctx, req)
	if err != nil {
		t.Fatalf("Complete() error = %v", err)
	}

	if !resp2.CacheHit {
		t.Error("Second request should be a cache hit")
	}

	// Content should match
	if resp1.Content != resp2.Content {
		t.Error("Cached response content should match original")
	}
}

func TestModelRouter_Metrics(t *testing.T) {
	config := RouterConfig{
		EnableCache:     false,
		DefaultProvider: ProviderOpenAI,
	}

	router := NewModelRouter(config)
	router.RegisterClient(ProviderOpenAI, NewMockClient(ProviderOpenAI, "gpt-4-mock"))

	req := CompletionRequest{
		Prompt:      "Test",
		TaskType:    TaskTypeGeneral,
		MaxTokens:   100,
		Temperature: 0.7,
	}

	ctx := context.Background()

	// Make several requests
	for i := 0; i < 5; i++ {
		_, err := router.Complete(ctx, req)
		if err != nil {
			t.Fatalf("Complete() error = %v", err)
		}
	}

	metrics := router.GetMetrics()

	if metrics.TotalRequests != 5 {
		t.Errorf("Expected 5 total requests, got %d", metrics.TotalRequests)
	}

	if metrics.SuccessRequests != 5 {
		t.Errorf("Expected 5 successful requests, got %d", metrics.SuccessRequests)
	}

	if metrics.SuccessRate != 1.0 {
		t.Errorf("Expected success rate of 1.0, got %f", metrics.SuccessRate)
	}
}

func TestModelRouter_GetRoutingDecision(t *testing.T) {
	config := RouterConfig{
		DefaultProvider: ProviderOpenAI,
		TaskRouting: map[TaskType]Provider{
			TaskTypeReasoning: ProviderAnthropic,
		},
	}

	router := NewModelRouter(config)
	router.RegisterClient(ProviderOpenAI, NewMockClient(ProviderOpenAI, "gpt-4-mock"))
	router.RegisterClient(ProviderAnthropic, NewMockClient(ProviderAnthropic, "claude-mock"))

	tests := []struct {
		name         string
		req          CompletionRequest
		wantProvider Provider
		reasonSubstr string
	}{
		{
			name: "explicit model selection",
			req: CompletionRequest{
				Prompt: "Test",
				Model: &Model{
					Provider: ProviderGemini,
					Name:     "gemini-pro",
				},
			},
			wantProvider: ProviderGemini,
			reasonSubstr: "explicit",
		},
		{
			name: "task-specific routing",
			req: CompletionRequest{
				Prompt:   "What is the meaning of life?",
				TaskType: TaskTypeReasoning,
			},
			wantProvider: ProviderAnthropic,
			reasonSubstr: "task-specific",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			decision := router.GetRoutingDecision(tt.req)

			if decision.SelectedProvider != tt.wantProvider {
				t.Errorf("Expected provider %v, got %v", tt.wantProvider, decision.SelectedProvider)
			}

			if decision.Confidence != 1.0 {
				t.Errorf("Expected confidence 1.0, got %f", decision.Confidence)
			}
		})
	}
}
