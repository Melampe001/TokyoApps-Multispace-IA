// Package main provides the AI API service for Tokyo-IA.
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/Melampe001/Tokyo-IA/internal/ai"
	"github.com/Melampe001/Tokyo-IA/internal/ai/clients"
	"github.com/Melampe001/Tokyo-IA/internal/config"
)

// Server represents the AI API server.
type Server struct {
	router    *ai.ModelRouter
	aiConfig  *config.AIConfig
	startTime time.Time
}

// NewServer creates a new AI API server.
func NewServer(configPath string) (*Server, error) {
	// Load configuration
	cfg, err := config.LoadAIConfig(configPath)
	if err != nil {
		// Use default config if file not found
		cfg = getDefaultConfig()
	}

	// Initialize router
	routerConfig := &ai.RouterConfig{
		EnableCaching:      cfg.Cache.Enabled,
		CacheTTL:           time.Duration(cfg.Cache.TTLSeconds) * time.Second,
		EnableFallback:     cfg.Performance.EnableFallback,
		MaxRetries:         cfg.Performance.MaxRetries,
		BudgetLimitDaily:   cfg.Budget.DailyLimitUSD,
		BudgetAlertPercent: cfg.Budget.AlertThresholdPct,
	}

	router := ai.NewModelRouter(routerConfig)

	// Register mock clients (in production, use real clients)
	router.RegisterClient(clients.NewMockClient(ai.ProviderOpenAI, "o3-mini", 0.00003))
	router.RegisterClient(clients.NewMockClient(ai.ProviderAnthropic, "claude-sonnet-4.5", 0.000015))
	router.RegisterClient(clients.NewMockClient(ai.ProviderGemini, "gemini-3.0-ultra", 0.00001))
	router.RegisterClient(clients.NewMockClient(ai.ProviderGrok, "grok-4", 0.000012))
	router.RegisterClient(clients.NewMockClient(ai.ProviderLlama, "llama-4-405b", 0.0))

	// Setup cache
	if routerConfig.EnableCaching {
		cache := ai.NewInMemoryCache(routerConfig.CacheTTL)
		router.SetCache(cache)
	}

	// Setup metrics
	metrics := ai.NewMetricsCollector()
	router.SetMetrics(metrics)

	return &Server{
		router:    router,
		aiConfig:  cfg,
		startTime: time.Now(),
	}, nil
}

// CompletionRequest is the API request format.
type CompletionRequest struct {
	Prompt          string  `json:"prompt"`
	TaskType        string  `json:"task_type"`
	Complexity      string  `json:"complexity,omitempty"`
	MaxTokens       int     `json:"max_tokens,omitempty"`
	Temperature     float64 `json:"temperature,omitempty"`
	PrivacyRequired bool    `json:"privacy_required,omitempty"`
}

// CompletionResponse is the API response format.
type CompletionResponse struct {
	Content      string  `json:"content"`
	Model        string  `json:"model"`
	Provider     string  `json:"provider"`
	TokensUsed   int     `json:"tokens_used"`
	LatencyMs    int64   `json:"latency_ms"`
	CostUSD      float64 `json:"cost_usd"`
	CachedResult bool    `json:"cached_result"`
}

// HealthResponse is the health check response.
type HealthResponse struct {
	Status  string `json:"status"`
	Uptime  string `json:"uptime"`
	Version string `json:"version"`
}

// MetricsResponse is the metrics endpoint response.
type MetricsResponse struct {
	TotalRequests int64                      `json:"total_requests"`
	TotalCost     float64                    `json:"total_cost_usd"`
	Providers     map[string]ProviderMetrics `json:"providers"`
	Budget        BudgetMetrics              `json:"budget"`
}

// ProviderMetrics holds metrics for a provider.
type ProviderMetrics struct {
	Requests   int64   `json:"requests"`
	Tokens     int64   `json:"tokens"`
	Cost       float64 `json:"cost_usd"`
	AvgLatency float64 `json:"avg_latency_ms"`
	ErrorRate  float64 `json:"error_rate"`
}

// BudgetMetrics holds budget information.
type BudgetMetrics struct {
	DailyLimit      float64 `json:"daily_limit_usd"`
	CurrentSpend    float64 `json:"current_spend_usd"`
	PercentUsed     float64 `json:"percent_used"`
	RemainingBudget float64 `json:"remaining_usd"`
}

// handleComplete handles completion requests.
func (s *Server) handleComplete(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req CompletionRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, fmt.Sprintf("Invalid request: %v", err), http.StatusBadRequest)
		return
	}

	// Convert to internal request format
	aiReq := &ai.CompletionRequest{
		Prompt:          req.Prompt,
		TaskType:        mapTaskType(req.TaskType),
		Complexity:      mapComplexity(req.Complexity),
		MaxTokens:       req.MaxTokens,
		Temperature:     req.Temperature,
		PrivacyRequired: req.PrivacyRequired,
		BudgetLimit:     10.0, // Per-request limit
	}

	// Execute request
	ctx := context.Background()
	_ = ctx // Use ctx when needed
	resp, err := s.router.Complete(r.Context(), aiReq)
	if err != nil {
		http.Error(w, fmt.Sprintf("Request failed: %v", err), http.StatusInternalServerError)
		return
	}

	// Convert to API response
	apiResp := CompletionResponse{
		Content:      resp.Content,
		Model:        resp.Model,
		Provider:     string(resp.Provider),
		TokensUsed:   resp.TokensUsed,
		LatencyMs:    resp.LatencyMs,
		CostUSD:      resp.CostUSD,
		CachedResult: resp.CachedResult,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(apiResp)
}

// handleHealth handles health check requests.
func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	uptime := time.Since(s.startTime)
	resp := HealthResponse{
		Status:  "healthy",
		Uptime:  uptime.String(),
		Version: "0.1.0",
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

// handleMetrics handles metrics requests.
func (s *Server) handleMetrics(w http.ResponseWriter, r *http.Request) {
	metrics := s.router.GetMetrics()

	providers := make(map[string]ProviderMetrics)
	totalRequests := int64(0)
	totalCost := 0.0

	for provider, metric := range metrics {
		errorRate := 0.0
		if metric.RequestCount > 0 {
			errorRate = float64(metric.ErrorCount) / float64(metric.RequestCount)
		}
		providers[string(provider)] = ProviderMetrics{
			Requests:   metric.RequestCount,
			Tokens:     metric.TotalTokens,
			Cost:       metric.TotalCostUSD,
			AvgLatency: metric.AvgLatencyMs,
			ErrorRate:  errorRate,
		}
		totalRequests += metric.RequestCount
		totalCost += metric.TotalCostUSD
	}

	// Get budget info
	budgetPercent := 0.0
	dailyLimit := 500.0
	if s.aiConfig != nil {
		dailyLimit = s.aiConfig.Budget.DailyLimitUSD
		if dailyLimit > 0 {
			budgetPercent = (totalCost / dailyLimit) * 100
		}
	}

	resp := MetricsResponse{
		TotalRequests: totalRequests,
		TotalCost:     totalCost,
		Providers:     providers,
		Budget: BudgetMetrics{
			DailyLimit:      dailyLimit,
			CurrentSpend:    totalCost,
			PercentUsed:     budgetPercent,
			RemainingBudget: dailyLimit - totalCost,
		},
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

// mapTaskType maps string task type to internal type.
func mapTaskType(taskType string) ai.TaskType {
	switch taskType {
	case "reasoning":
		return ai.TaskTypeReasoning
	case "code_generation":
		return ai.TaskTypeCodeGen
	case "code_review":
		return ai.TaskTypeCodeReview
	case "multimodal":
		return ai.TaskTypeMultimodal
	case "documentation":
		return ai.TaskTypeDocumentation
	default:
		return ai.TaskTypeChat
	}
}

// mapComplexity maps string complexity to internal type.
func mapComplexity(complexity string) ai.ComplexityLevel {
	switch complexity {
	case "simple":
		return ai.ComplexitySimple
	case "moderate":
		return ai.ComplexityModerate
	case "complex":
		return ai.ComplexityComplex
	default:
		return ai.ComplexityModerate
	}
}

// getDefaultConfig returns a default configuration.
func getDefaultConfig() *config.AIConfig {
	return &config.AIConfig{
		Budget: config.BudgetConfig{
			DailyLimitUSD:     500.0,
			AlertThresholdPct: 80.0,
		},
		Cache: config.CacheConfig{
			Enabled:    true,
			TTLSeconds: 3600,
			Backend:    "memory",
		},
		Performance: config.PerformanceConfig{
			MaxRetries:     3,
			TimeoutSeconds: 30,
			EnableFallback: true,
		},
	}
}

func main() {
	// Create server
	server, err := NewServer("config/ai_models.yaml")
	if err != nil {
		log.Printf("Warning: failed to load config: %v, using defaults", err)
	}

	// Setup routes
	http.HandleFunc("/health", server.handleHealth)
	http.HandleFunc("/ai/complete", server.handleComplete)
	http.HandleFunc("/ai/metrics", server.handleMetrics)

	// Start server
	port := ":8080"
	log.Printf("Starting AI API server on %s", port)
	log.Printf("Endpoints:")
	log.Printf("  - POST /ai/complete  - AI completion requests")
	log.Printf("  - GET  /ai/metrics   - Usage metrics")
	log.Printf("  - GET  /health       - Health check")

	if err := http.ListenAndServe(port, nil); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}
