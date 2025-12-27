// Package ai provides the model router for intelligent AI model selection.
package ai

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"time"
)

var (
	// ErrNoAvailableModel indicates no model is available for the request.
	ErrNoAvailableModel = errors.New("no available model for request")
	// ErrBudgetExceeded indicates the budget limit has been exceeded.
	ErrBudgetExceeded = errors.New("budget limit exceeded")
	// ErrInvalidRequest indicates the request is invalid.
	ErrInvalidRequest = errors.New("invalid request")
)

// ModelRouter handles intelligent routing of AI requests to appropriate models.
type ModelRouter struct {
	clients       map[ModelProvider]ModelClient
	cache         Cache
	metrics       *MetricsCollector
	config        *RouterConfig
	budgetTracker *BudgetTracker
	mu            sync.RWMutex
}

// RouterConfig holds configuration for the model router.
type RouterConfig struct {
	EnableCaching      bool
	CacheTTL           time.Duration
	EnableFallback     bool
	MaxRetries         int
	BudgetLimitDaily   float64
	BudgetAlertPercent float64
}

// NewModelRouter creates a new ModelRouter instance.
func NewModelRouter(config *RouterConfig) *ModelRouter {
	return &ModelRouter{
		clients:       make(map[ModelProvider]ModelClient),
		config:        config,
		budgetTracker: NewBudgetTracker(config.BudgetLimitDaily),
	}
}

// RegisterClient registers a model client with the router.
func (r *ModelRouter) RegisterClient(client ModelClient) {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.clients[client.GetProvider()] = client
}

// SetCache sets the cache implementation for the router.
func (r *ModelRouter) SetCache(cache Cache) {
	r.cache = cache
}

// SetMetrics sets the metrics collector for the router.
func (r *ModelRouter) SetMetrics(metrics *MetricsCollector) {
	r.metrics = metrics
}

// Complete routes a completion request to the most appropriate model.
func (r *ModelRouter) Complete(ctx context.Context, req *CompletionRequest) (*CompletionResponse, error) {
	startTime := time.Now()

	// Validate request
	if err := r.validateRequest(req); err != nil {
		return nil, fmt.Errorf("%w: %v", ErrInvalidRequest, err)
	}

	// Check budget
	if !r.budgetTracker.CanSpend(req.BudgetLimit) {
		return nil, ErrBudgetExceeded
	}

	// Try cache if enabled
	if r.config.EnableCaching && r.cache != nil {
		if cached, err := r.cache.Get(ctx, req); err == nil && cached != nil {
			cached.CachedResult = true
			r.recordMetrics(cached, time.Since(startTime))
			return cached, nil
		}
	}

	// Make routing decision
	decision := r.makeRoutingDecision(req)
	if decision.SelectedProvider == "" {
		return nil, ErrNoAvailableModel
	}

	// Execute request with fallback
	resp, err := r.executeWithFallback(ctx, req, decision)
	if err != nil {
		return nil, err
	}

	// Record budget usage
	r.budgetTracker.RecordSpending(resp.CostUSD)

	// Cache result if enabled
	if r.config.EnableCaching && r.cache != nil {
		_ = r.cache.Set(ctx, req, resp)
	}

	// Record metrics
	r.recordMetrics(resp, time.Since(startTime))

	return resp, nil
}

// makeRoutingDecision determines which model to use for a request.
func (r *ModelRouter) makeRoutingDecision(req *CompletionRequest) *RoutingDecision {
	r.mu.RLock()
	defer r.mu.RUnlock()

	decision := &RoutingDecision{
		FallbackChain: []ModelProvider{},
	}

	// Routing logic based on task type and complexity
	switch req.TaskType {
	case TaskTypeReasoning:
		if req.Complexity == ComplexityComplex {
			// Use most capable reasoning models
			decision.SelectedProvider = ProviderOpenAI
			decision.SelectedModel = "o3"
			decision.FallbackChain = []ModelProvider{ProviderAnthropic, ProviderGemini}
			decision.Reason = "Complex reasoning task requires o3"
		} else {
			decision.SelectedProvider = ProviderAnthropic
			decision.SelectedModel = "claude-sonnet-4.5"
			decision.FallbackChain = []ModelProvider{ProviderOpenAI, ProviderGemini}
			decision.Reason = "Moderate reasoning with Claude Sonnet"
		}

	case TaskTypeCodeGen, TaskTypeCodeReview:
		if req.PrivacyRequired {
			// Use local model for privacy
			decision.SelectedProvider = ProviderLlama
			decision.SelectedModel = "llama-4-405b"
			decision.Reason = "Privacy required - using local Llama 4"
		} else {
			decision.SelectedProvider = ProviderAnthropic
			decision.SelectedModel = "claude-opus-4.1"
			decision.FallbackChain = []ModelProvider{ProviderOpenAI, ProviderLlama}
			decision.Reason = "Code task with Claude Opus for quality"
		}

	case TaskTypeMultimodal:
		decision.SelectedProvider = ProviderGemini
		decision.SelectedModel = "gemini-3.0-ultra"
		decision.FallbackChain = []ModelProvider{ProviderGrok}
		decision.Reason = "Multimodal task with Gemini 3.0"

	case TaskTypeDocumentation:
		decision.SelectedProvider = ProviderGemini
		decision.SelectedModel = "gemini-3.0-ultra"
		decision.FallbackChain = []ModelProvider{ProviderAnthropic}
		decision.Reason = "Documentation generation with Gemini"

	default:
		// Default to most available/cost-effective
		decision.SelectedProvider = ProviderAnthropic
		decision.SelectedModel = "claude-sonnet-4.5"
		decision.FallbackChain = []ModelProvider{ProviderOpenAI, ProviderLlama}
		decision.Reason = "Default routing to Claude Sonnet"
	}

	// Verify selected provider is available
	if client, ok := r.clients[decision.SelectedProvider]; ok {
		if !client.IsAvailable(context.Background()) && len(decision.FallbackChain) > 0 {
			// Use first fallback
			decision.SelectedProvider = decision.FallbackChain[0]
			decision.FallbackChain = decision.FallbackChain[1:]
			decision.Reason = fmt.Sprintf("%s (fallback)", decision.Reason)
		}
	}

	return decision
}

// executeWithFallback executes the request with fallback logic.
func (r *ModelRouter) executeWithFallback(ctx context.Context, req *CompletionRequest, decision *RoutingDecision) (*CompletionResponse, error) {
	r.mu.RLock()
	client, ok := r.clients[decision.SelectedProvider]
	r.mu.RUnlock()

	if !ok {
		return nil, fmt.Errorf("client not found for provider: %s", decision.SelectedProvider)
	}

	// Try primary client
	resp, err := client.Complete(ctx, req)
	if err == nil {
		return resp, nil
	}

	// Try fallback chain if enabled
	if r.config.EnableFallback {
		for _, fallbackProvider := range decision.FallbackChain {
			r.mu.RLock()
			fallbackClient, ok := r.clients[fallbackProvider]
			r.mu.RUnlock()

			if !ok {
				continue
			}

			resp, err := fallbackClient.Complete(ctx, req)
			if err == nil {
				return resp, nil
			}
		}
	}

	return nil, fmt.Errorf("all providers failed: %w", err)
}

// validateRequest validates a completion request.
func (r *ModelRouter) validateRequest(req *CompletionRequest) error {
	if req.Prompt == "" {
		return errors.New("prompt cannot be empty")
	}
	if req.MaxTokens <= 0 {
		req.MaxTokens = 2048 // Default
	}
	if req.Temperature < 0 || req.Temperature > 2 {
		req.Temperature = 0.7 // Default
	}
	return nil
}

// recordMetrics records performance metrics for a request.
func (r *ModelRouter) recordMetrics(resp *CompletionResponse, duration time.Duration) {
	if r.metrics == nil {
		return
	}

	r.metrics.RecordRequest(resp.Provider, resp.Model, duration, resp.TokensUsed, resp.CostUSD, resp.CachedResult)
}

// GetMetrics returns current metrics for all models.
func (r *ModelRouter) GetMetrics() map[ModelProvider]*ModelMetrics {
	if r.metrics == nil {
		return nil
	}
	return r.metrics.GetAllMetrics()
}

// BudgetTracker tracks spending against budget limits.
type BudgetTracker struct {
	dailyLimit   float64
	currentSpend float64
	resetTime    time.Time
	mu           sync.Mutex
}

// NewBudgetTracker creates a new budget tracker.
func NewBudgetTracker(dailyLimit float64) *BudgetTracker {
	return &BudgetTracker{
		dailyLimit: dailyLimit,
		resetTime:  time.Now().Add(24 * time.Hour),
	}
}

// CanSpend checks if spending amount is within budget.
func (b *BudgetTracker) CanSpend(amount float64) bool {
	b.mu.Lock()
	defer b.mu.Unlock()

	// Reset if past reset time
	if time.Now().After(b.resetTime) {
		b.currentSpend = 0
		b.resetTime = time.Now().Add(24 * time.Hour)
	}

	return (b.currentSpend + amount) <= b.dailyLimit
}

// RecordSpending records actual spending.
func (b *BudgetTracker) RecordSpending(amount float64) {
	b.mu.Lock()
	defer b.mu.Unlock()
	b.currentSpend += amount
}

// GetCurrentSpend returns current spending.
func (b *BudgetTracker) GetCurrentSpend() float64 {
	b.mu.Lock()
	defer b.mu.Unlock()
	return b.currentSpend
}

// GetBudgetPercent returns percentage of budget used.
func (b *BudgetTracker) GetBudgetPercent() float64 {
	b.mu.Lock()
	defer b.mu.Unlock()
	if b.dailyLimit == 0 {
		return 0
	}
	return (b.currentSpend / b.dailyLimit) * 100
}

// RouteWithAgent routes a request using the Python AI Router Agent for intelligent decision making.
// This integrates with the Python agent system for enhanced routing logic.
func (r *ModelRouter) RouteWithAgent(ctx context.Context, req *CompletionRequest) (*CompletionResponse, error) {
	// Try to use Python agent for intelligent routing
	agentDecision, err := r.callPythonRouterAgent(ctx, req)
	if err != nil {
		// Fallback to standard Go routing if agent fails
		return r.Complete(ctx, req)
	}

	// Use the provider suggested by the agent
	if agentDecision.SelectedProvider != "" {
		r.mu.RLock()
		client, ok := r.clients[agentDecision.SelectedProvider]
		r.mu.RUnlock()

		if ok {
			return client.Complete(ctx, req)
		}
	}

	// Fallback to standard routing
	return r.Complete(ctx, req)
}

// callPythonRouterAgent calls the Python AI Router Agent for routing decisions.
func (r *ModelRouter) callPythonRouterAgent(ctx context.Context, req *CompletionRequest) (*RoutingDecision, error) {
	// This is a placeholder for Python agent integration
	// In real implementation, this would execute Python code or call a service

	// For now, return nil to trigger fallback to standard routing
	return nil, fmt.Errorf("python agent integration not yet implemented")
}
