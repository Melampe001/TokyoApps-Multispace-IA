package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/Melampe001/Tokyo-IA/internal/ai"
)

func main() {
	// Initialize router with configuration
	config := ai.RouterConfig{
		EnableCache:     true,
		CacheTTL:        10 * time.Minute,
		DefaultProvider: ai.ProviderOpenAI,
		TaskRouting: map[ai.TaskType]ai.Provider{
			ai.TaskTypeReasoning:   ai.ProviderAnthropic,
			ai.TaskTypeCreative:    ai.ProviderOpenAI,
			ai.TaskTypeCodeReview:  ai.ProviderAnthropic,
			ai.TaskTypeCodeGen:     ai.ProviderOpenAI,
			ai.TaskTypeTranslation: ai.ProviderGemini,
		},
	}

	router := ai.NewModelRouter(config)

	// Register mock clients for development
	// In production, these would be replaced with real clients
	router.RegisterClient(ai.ProviderOpenAI, ai.NewMockClient(ai.ProviderOpenAI, "gpt-4-mock"))
	router.RegisterClient(ai.ProviderAnthropic, ai.NewMockClient(ai.ProviderAnthropic, "claude-3-mock"))
	router.RegisterClient(ai.ProviderGemini, ai.NewMockClient(ai.ProviderGemini, "gemini-pro-mock"))

	// Setup HTTP server
	mux := http.NewServeMux()

	// Health check endpoint
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
	})

	// AI completion endpoint
	mux.HandleFunc("/ai/complete", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var req struct {
			Prompt      string  `json:"prompt"`
			TaskType    string  `json:"task_type"`
			MaxTokens   int     `json:"max_tokens,omitempty"`
			Temperature float64 `json:"temperature,omitempty"`
		}

		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "Invalid request body", http.StatusBadRequest)
			return
		}

		if req.Prompt == "" {
			http.Error(w, "Prompt is required", http.StatusBadRequest)
			return
		}

		// Set defaults
		if req.MaxTokens == 0 {
			req.MaxTokens = 2048
		}
		if req.Temperature == 0 {
			req.Temperature = 0.7
		}
		if req.TaskType == "" {
			req.TaskType = string(ai.TaskTypeGeneral)
		}

		// Create completion request
		completionReq := ai.CompletionRequest{
			Prompt:      req.Prompt,
			TaskType:    ai.TaskType(req.TaskType),
			MaxTokens:   req.MaxTokens,
			Temperature: req.Temperature,
		}

		// Execute completion
		// TODO: Make timeout configurable via environment variable
		// Default: 30 seconds, adjust based on provider response times
		ctx, cancel := context.WithTimeout(r.Context(), 30*time.Second)
		defer cancel()

		resp, err := router.Complete(ctx, completionReq)
		if err != nil {
			log.Printf("Completion error: %v", err)
			http.Error(w, fmt.Sprintf("Completion failed: %v", err), http.StatusInternalServerError)
			return
		}

		// Return response
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"content":     resp.Content,
			"model":       resp.Model.Name,
			"provider":    resp.Provider,
			"tokens_used": resp.TokensUsed,
			"latency_ms":  resp.Latency.Milliseconds(),
			"cache_hit":   resp.CacheHit,
		})
	})

	// Metrics endpoint
	mux.HandleFunc("/ai/metrics", func(w http.ResponseWriter, r *http.Request) {
		metrics := router.GetMetrics()

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]interface{}{
			"total_requests":   metrics.TotalRequests,
			"success_requests": metrics.SuccessRequests,
			"failed_requests":  metrics.FailedRequests,
			"cache_hits":       metrics.CacheHits,
			"total_tokens":     metrics.TotalTokens,
			"success_rate":     fmt.Sprintf("%.2f%%", metrics.SuccessRate*100),
			"cache_hit_rate":   fmt.Sprintf("%.2f%%", metrics.CacheHitRate*100),
			"average_latency":  metrics.AverageLatency.String(),
			"provider_stats":   metrics.ProviderStats,
		})
	})

	// Cache control endpoint
	mux.HandleFunc("/ai/cache/clear", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		router.ClearCache()
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"status": "cache cleared"})
	})

	// Start server
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	server := &http.Server{
		Addr:         ":" + port,
		Handler:      mux,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 45 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	// Graceful shutdown
	go func() {
		sigint := make(chan os.Signal, 1)
		signal.Notify(sigint, os.Interrupt, syscall.SIGTERM)
		<-sigint

		log.Println("Shutting down server...")
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()

		if err := server.Shutdown(ctx); err != nil {
			log.Printf("Server shutdown error: %v", err)
		}
	}()

	log.Printf("🚀 AI API Server starting on port %s", port)
	log.Printf("Endpoints:")
	log.Printf("  - POST /ai/complete    - AI completion")
	log.Printf("  - GET  /ai/metrics     - Metrics")
	log.Printf("  - POST /ai/cache/clear - Clear cache")
	log.Printf("  - GET  /health         - Health check")

	if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatalf("Server error: %v", err)
	}

	log.Println("Server stopped")
}
