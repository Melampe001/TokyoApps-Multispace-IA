package ai

import (
	"context"
	"fmt"
	"time"
)

// ModelRouter routes requests to appropriate AI models
type ModelRouter struct {
	clients map[Provider]AIClient
	cache   *Cache
	metrics *Metrics
	config  RouterConfig
}

// RouterConfig contains configuration for the router
type RouterConfig struct {
	EnableCache     bool
	CacheTTL        time.Duration
	DefaultProvider Provider
	TaskRouting     map[TaskType]Provider
}

// NewModelRouter creates a new model router
func NewModelRouter(config RouterConfig) *ModelRouter {
	router := &ModelRouter{
		clients: make(map[Provider]AIClient),
		metrics: NewMetrics(),
		config:  config,
	}

	if config.EnableCache {
		router.cache = NewCache(config.CacheTTL)
	}

	return router
}

// RegisterClient registers an AI client for a provider
func (r *ModelRouter) RegisterClient(provider Provider, client AIClient) {
	r.clients[provider] = client
}

// Complete handles an AI completion request
func (r *ModelRouter) Complete(ctx context.Context, req CompletionRequest) (*CompletionResponse, error) {
	startTime := time.Now()

	// Check cache first
	if r.cache != nil {
		if cached, hit := r.cache.Get(req); hit {
			r.metrics.RecordRequest(cached)
			return cached, nil
		}
	}

	// Route to appropriate provider
	provider := r.routeRequest(req)
	client, exists := r.clients[provider]
	if !exists {
		r.metrics.RecordError()
		return nil, fmt.Errorf("no client available for provider: %s", provider)
	}

	if !client.IsAvailable() {
		r.metrics.RecordError()
		return nil, fmt.Errorf("client %s is not available", provider)
	}

	// Execute request
	resp, err := client.Complete(ctx, req)
	if err != nil {
		r.metrics.RecordError()
		return nil, fmt.Errorf("completion failed: %w", err)
	}

	// Set latency
	resp.Latency = time.Since(startTime)
	resp.Provider = provider

	// Cache the response
	if r.cache != nil {
		r.cache.Set(req, resp)
	}

	// Record metrics
	r.metrics.RecordRequest(resp)

	return resp, nil
}

// routeRequest determines which provider should handle the request
func (r *ModelRouter) routeRequest(req CompletionRequest) Provider {
	// If a specific model is requested, use its provider
	if req.Model != nil {
		return req.Model.Provider
	}

	// Use task-specific routing if configured
	if provider, exists := r.config.TaskRouting[req.TaskType]; exists {
		if _, hasClient := r.clients[provider]; hasClient {
			return provider
		}
	}

	// Fall back to default provider
	if _, exists := r.clients[r.config.DefaultProvider]; exists {
		return r.config.DefaultProvider
	}

	// Return first available provider
	for provider := range r.clients {
		return provider
	}

	// This should not happen if clients are properly registered
	return r.config.DefaultProvider
}

// GetRoutingDecision returns information about how a request would be routed
func (r *ModelRouter) GetRoutingDecision(req CompletionRequest) RoutingDecision {
	provider := r.routeRequest(req)
	client := r.clients[provider]

	reason := "default routing"
	if req.Model != nil {
		reason = "explicit model selection"
	} else if _, exists := r.config.TaskRouting[req.TaskType]; exists {
		reason = fmt.Sprintf("task-specific routing for %s", req.TaskType)
	}

	modelName := "unknown"
	if client != nil {
		modelName = client.Name()
	}

	model := Model{
		Provider: provider,
		Name:     modelName,
	}

	return RoutingDecision{
		SelectedProvider: provider,
		SelectedModel:    model,
		Reason:           reason,
		Confidence:       1.0,
	}
}

// GetMetrics returns current metrics
func (r *ModelRouter) GetMetrics() MetricsSnapshot {
	return r.metrics.GetStats()
}

// ClearCache clears the response cache
func (r *ModelRouter) ClearCache() {
	if r.cache != nil {
		r.cache.Clear()
	}
}
