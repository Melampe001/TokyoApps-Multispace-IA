// Package ai provides tests for the model router.
package ai

import (
	"context"
	"testing"
	"time"
)

func TestNewModelRouter(t *testing.T) {
	config := &RouterConfig{
		EnableCaching:      true,
		CacheTTL:           time.Hour,
		EnableFallback:     true,
		MaxRetries:         3,
		BudgetLimitDaily:   100.0,
		BudgetAlertPercent: 80.0,
	}

	router := NewModelRouter(config)
	if router == nil {
		t.Fatal("expected router to be created")
	}

	if router.config.BudgetLimitDaily != 100.0 {
		t.Errorf("expected budget limit 100.0, got %f", router.config.BudgetLimitDaily)
	}
}

func TestModelRouterRegisterClient(t *testing.T) {
	router := NewModelRouter(&RouterConfig{})

	// Create mock client
	client := &mockTestClient{
		provider:  ProviderOpenAI,
		modelName: "test-model",
		available: true,
	}

	router.RegisterClient(client)

	if len(router.clients) != 1 {
		t.Errorf("expected 1 client, got %d", len(router.clients))
	}

	if _, ok := router.clients[ProviderOpenAI]; !ok {
		t.Error("expected OpenAI client to be registered")
	}
}

func TestModelRouterComplete(t *testing.T) {
	tests := []struct {
		name      string
		request   *CompletionRequest
		wantError bool
		errorType error
	}{
		{
			name: "valid reasoning request",
			request: &CompletionRequest{
				Prompt:      "What is 2+2?",
				TaskType:    TaskTypeReasoning,
				Complexity:  ComplexitySimple,
				MaxTokens:   100,
				Temperature: 0.7,
			},
			wantError: false,
		},
		{
			name: "empty prompt",
			request: &CompletionRequest{
				Prompt:     "",
				TaskType:   TaskTypeReasoning,
				Complexity: ComplexitySimple,
			},
			wantError: true,
			errorType: ErrInvalidRequest,
		},
		{
			name: "valid code generation request",
			request: &CompletionRequest{
				Prompt:      "Write a hello world function",
				TaskType:    TaskTypeCodeGen,
				Complexity:  ComplexityModerate,
				MaxTokens:   500,
				Temperature: 0.5,
			},
			wantError: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			router := setupTestRouter()
			ctx := context.Background()

			resp, err := router.Complete(ctx, tt.request)

			if tt.wantError {
				if err == nil {
					t.Error("expected error but got none")
				}
				return
			}

			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}

			if resp == nil {
				t.Fatal("expected response but got nil")
			}

			if resp.Content == "" {
				t.Error("expected non-empty content")
			}

			if resp.TokensUsed <= 0 {
				t.Error("expected positive token count")
			}
		})
	}
}

func TestMakeRoutingDecision(t *testing.T) {
	tests := []struct {
		name             string
		request          *CompletionRequest
		expectedProvider ModelProvider
		expectedReason   string
	}{
		{
			name: "complex reasoning to OpenAI o3",
			request: &CompletionRequest{
				TaskType:   TaskTypeReasoning,
				Complexity: ComplexityComplex,
			},
			expectedProvider: ProviderOpenAI,
		},
		{
			name: "code generation with privacy",
			request: &CompletionRequest{
				TaskType:        TaskTypeCodeGen,
				PrivacyRequired: true,
			},
			expectedProvider: ProviderLlama,
		},
		{
			name: "multimodal task",
			request: &CompletionRequest{
				TaskType: TaskTypeMultimodal,
			},
			expectedProvider: ProviderGemini,
		},
		{
			name: "code review task",
			request: &CompletionRequest{
				TaskType: TaskTypeCodeReview,
			},
			expectedProvider: ProviderAnthropic,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			router := setupTestRouter()
			decision := router.makeRoutingDecision(tt.request)

			if decision.SelectedProvider != tt.expectedProvider {
				t.Errorf("expected provider %s, got %s", tt.expectedProvider, decision.SelectedProvider)
			}

			if decision.SelectedModel == "" {
				t.Error("expected non-empty model name")
			}

			if decision.Reason == "" {
				t.Error("expected non-empty reason")
			}
		})
	}
}

func TestBudgetTracker(t *testing.T) {
	tracker := NewBudgetTracker(100.0)

	// Test initial state
	if !tracker.CanSpend(50.0) {
		t.Error("should be able to spend 50.0")
	}

	// Record spending
	tracker.RecordSpending(40.0)
	if tracker.GetCurrentSpend() != 40.0 {
		t.Errorf("expected current spend 40.0, got %f", tracker.GetCurrentSpend())
	}

	// Test percentage
	pct := tracker.GetBudgetPercent()
	if pct != 40.0 {
		t.Errorf("expected 40%% budget used, got %f%%", pct)
	}

	// Test spending over budget
	if tracker.CanSpend(70.0) {
		t.Error("should not be able to spend 70.0 (total would be 110.0)")
	}

	// Can still spend within budget
	if !tracker.CanSpend(50.0) {
		t.Error("should be able to spend 50.0 (total would be 90.0)")
	}
}

func TestBudgetExceeded(t *testing.T) {
	config := &RouterConfig{
		BudgetLimitDaily: 1.0,
	}
	router := setupTestRouterWithConfig(config)

	request := &CompletionRequest{
		Prompt:      "test",
		TaskType:    TaskTypeReasoning,
		Complexity:  ComplexitySimple,
		BudgetLimit: 2.0, // Exceeds daily limit
	}

	ctx := context.Background()
	_, err := router.Complete(ctx, request)

	if err != ErrBudgetExceeded {
		t.Errorf("expected ErrBudgetExceeded, got %v", err)
	}
}

func TestCachingEnabled(t *testing.T) {
	router := setupTestRouter()
	cache := NewInMemoryCache(time.Hour)
	router.SetCache(cache)

	request := &CompletionRequest{
		Prompt:      "test prompt",
		TaskType:    TaskTypeReasoning,
		Complexity:  ComplexitySimple,
		MaxTokens:   100,
		Temperature: 0.7,
	}

	ctx := context.Background()

	// First request - should hit model
	resp1, err := router.Complete(ctx, request)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if resp1.CachedResult {
		t.Error("first request should not be cached")
	}

	// Second request - should hit cache
	resp2, err := router.Complete(ctx, request)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !resp2.CachedResult {
		t.Error("second request should be cached")
	}
}

func TestFallbackChain(t *testing.T) {
	router := setupTestRouter()

	// Make primary provider unavailable
	if client, ok := router.clients[ProviderOpenAI]; ok {
		if mc, ok := client.(*mockTestClient); ok {
			mc.available = false
		}
	}

	request := &CompletionRequest{
		Prompt:      "test",
		TaskType:    TaskTypeReasoning,
		Complexity:  ComplexityComplex,
		MaxTokens:   100,
		Temperature: 0.7,
	}

	ctx := context.Background()
	resp, err := router.Complete(ctx, request)

	if err != nil {
		t.Fatalf("expected fallback to work, got error: %v", err)
	}

	// Should have fallen back to Anthropic
	if resp.Provider != ProviderAnthropic {
		t.Errorf("expected fallback to Anthropic, got %s", resp.Provider)
	}
}

// Helper functions

func setupTestRouter() *ModelRouter {
	config := &RouterConfig{
		EnableCaching:      true,
		CacheTTL:           time.Hour,
		EnableFallback:     true,
		MaxRetries:         3,
		BudgetLimitDaily:   1000.0,
		BudgetAlertPercent: 80.0,
	}
	return setupTestRouterWithConfig(config)
}

func setupTestRouterWithConfig(config *RouterConfig) *ModelRouter {
	router := NewModelRouter(config)

	// Register mock clients for all providers
	router.RegisterClient(&mockTestClient{
		provider:  ProviderOpenAI,
		modelName: "o3",
		available: true,
	})
	router.RegisterClient(&mockTestClient{
		provider:  ProviderAnthropic,
		modelName: "claude-opus-4.1",
		available: true,
	})
	router.RegisterClient(&mockTestClient{
		provider:  ProviderGemini,
		modelName: "gemini-3.0-ultra",
		available: true,
	})
	router.RegisterClient(&mockTestClient{
		provider:  ProviderGrok,
		modelName: "grok-4",
		available: true,
	})
	router.RegisterClient(&mockTestClient{
		provider:  ProviderLlama,
		modelName: "llama-4-405b",
		available: true,
	})

	// Set up metrics
	router.SetMetrics(NewMetricsCollector())

	return router
}

// mockTestClient is a simple mock for testing
type mockTestClient struct {
	provider  ModelProvider
	modelName string
	available bool
}

func (m *mockTestClient) Complete(ctx context.Context, req *CompletionRequest) (*CompletionResponse, error) {
	if !m.available {
		return nil, ErrNoAvailableModel
	}

	return &CompletionResponse{
		Content:      "Mock response to: " + req.Prompt,
		Model:        m.modelName,
		Provider:     m.provider,
		TokensUsed:   100,
		LatencyMs:    50,
		CostUSD:      0.001,
		CachedResult: false,
		Timestamp:    time.Now(),
	}, nil
}

func (m *mockTestClient) GetProvider() ModelProvider {
	return m.provider
}

func (m *mockTestClient) GetModelName() string {
	return m.modelName
}

func (m *mockTestClient) IsAvailable(ctx context.Context) bool {
	return m.available
}

func (m *mockTestClient) GetCostPerToken() float64 {
	return 0.00001
}
