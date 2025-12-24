// Package config provides configuration management for AI models.
package config

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
)

// AIConfig represents the complete AI configuration.
type AIConfig struct {
	Models      map[string]ProviderConfig `yaml:"models"`
	Routing     RoutingConfig             `yaml:"routing_rules"`
	Budget      BudgetConfig              `yaml:"budget"`
	Cache       CacheConfig               `yaml:"cache"`
	Performance PerformanceConfig         `yaml:"performance"`
	Monitoring  MonitoringConfig          `yaml:"monitoring"`
	Features    FeaturesConfig            `yaml:"features"`
}

// ProviderConfig holds configuration for a model provider.
type ProviderConfig struct {
	Provider string        `yaml:"provider"`
	Models   []ModelConfig `yaml:"models"`
}

// ModelConfig holds configuration for a specific model.
type ModelConfig struct {
	Name            string   `yaml:"name"`
	MaxTokens       int      `yaml:"max_tokens"`
	CostPer1KTokens float64  `yaml:"cost_per_1k_tokens"`
	UseCases        []string `yaml:"use_cases"`
	LatencyTargetMs int      `yaml:"latency_target_ms"`
}

// RoutingConfig holds routing rules for different task types.
type RoutingConfig struct {
	Reasoning      map[string]RouteConfig `yaml:"reasoning"`
	CodeGeneration map[string]RouteConfig `yaml:"code_generation"`
	CodeReview     RouteConfig            `yaml:"code_review"`
	Multimodal     RouteConfig            `yaml:"multimodal"`
	Documentation  RouteConfig            `yaml:"documentation"`
	Chat           RouteConfig            `yaml:"chat"`
}

// RouteConfig defines primary and fallback models for a route.
type RouteConfig struct {
	Primary  string   `yaml:"primary"`
	Fallback []string `yaml:"fallback"`
}

// BudgetConfig holds budget-related configuration.
type BudgetConfig struct {
	DailyLimitUSD      float64            `yaml:"daily_limit_usd"`
	AlertThresholdPct  float64            `yaml:"alert_threshold_percent"`
	PerRequestLimitUSD float64            `yaml:"per_request_limit_usd"`
	Allocation         map[string]float64 `yaml:"allocation"`
}

// CacheConfig holds caching configuration.
type CacheConfig struct {
	Enabled    bool   `yaml:"enabled"`
	TTLSeconds int    `yaml:"ttl_seconds"`
	MaxSizeMB  int    `yaml:"max_size_mb"`
	Backend    string `yaml:"backend"`
}

// PerformanceConfig holds performance-related settings.
type PerformanceConfig struct {
	MaxRetries         int  `yaml:"max_retries"`
	TimeoutSeconds     int  `yaml:"timeout_seconds"`
	EnableFallback     bool `yaml:"enable_fallback"`
	ConcurrentRequests int  `yaml:"concurrent_requests"`
	RateLimitPerMinute int  `yaml:"rate_limit_per_minute"`
}

// MonitoringConfig holds monitoring configuration.
type MonitoringConfig struct {
	Prometheus PrometheusConfig `yaml:"prometheus"`
	Langfuse   LangfuseConfig   `yaml:"langfuse"`
}

// PrometheusConfig holds Prometheus configuration.
type PrometheusConfig struct {
	Enabled bool   `yaml:"enabled"`
	Port    int    `yaml:"port"`
	Path    string `yaml:"path"`
}

// LangfuseConfig holds Langfuse configuration.
type LangfuseConfig struct {
	Enabled   bool   `yaml:"enabled"`
	PublicKey string `yaml:"public_key"`
	SecretKey string `yaml:"secret_key"`
	Host      string `yaml:"host"`
}

// FeaturesConfig holds feature flags.
type FeaturesConfig struct {
	EnableStreaming       bool `yaml:"enable_streaming"`
	EnableFunctionCalling bool `yaml:"enable_function_calling"`
	EnableVision          bool `yaml:"enable_vision"`
	EnableMultimodal      bool `yaml:"enable_multimodal"`
}

// LoadAIConfig loads AI configuration from a YAML file.
func LoadAIConfig(path string) (*AIConfig, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("failed to read config file: %w", err)
	}

	var config AIConfig
	if err := yaml.Unmarshal(data, &config); err != nil {
		return nil, fmt.Errorf("failed to parse config: %w", err)
	}

	// Validate configuration
	if err := config.Validate(); err != nil {
		return nil, fmt.Errorf("invalid configuration: %w", err)
	}

	// Load API keys from environment
	config.LoadAPIKeys()

	return &config, nil
}

// Validate checks if the configuration is valid.
func (c *AIConfig) Validate() error {
	if len(c.Models) == 0 {
		return fmt.Errorf("no models configured")
	}

	if c.Budget.DailyLimitUSD <= 0 {
		return fmt.Errorf("daily budget limit must be positive")
	}

	if c.Performance.MaxRetries < 0 {
		return fmt.Errorf("max retries cannot be negative")
	}

	return nil
}

// LoadAPIKeys loads API keys from environment variables.
func (c *AIConfig) LoadAPIKeys() {
	// API keys should be loaded from environment variables
	// This is a placeholder for actual implementation
	_ = os.Getenv("OPENAI_API_KEY")
	_ = os.Getenv("ANTHROPIC_API_KEY")
	_ = os.Getenv("GEMINI_API_KEY")
	_ = os.Getenv("GROK_API_KEY")
}

// GetModelConfig returns configuration for a specific model.
func (c *AIConfig) GetModelConfig(provider, model string) (*ModelConfig, error) {
	providerConfig, ok := c.Models[provider]
	if !ok {
		return nil, fmt.Errorf("provider %s not found", provider)
	}

	for _, m := range providerConfig.Models {
		if m.Name == model {
			return &m, nil
		}
	}

	return nil, fmt.Errorf("model %s not found for provider %s", model, provider)
}

// GetRoutingRule returns the routing rule for a task type and complexity.
func (c *AIConfig) GetRoutingRule(taskType string, complexity string) *RouteConfig {
	switch taskType {
	case "reasoning":
		if route, ok := c.Routing.Reasoning[complexity]; ok {
			return &route
		}
		return nil
	case "code_generation":
		if route, ok := c.Routing.CodeGeneration[complexity]; ok {
			return &route
		}
		if route, ok := c.Routing.CodeGeneration["default"]; ok {
			return &route
		}
		return nil
	case "code_review":
		return &c.Routing.CodeReview
	case "multimodal":
		return &c.Routing.Multimodal
	case "documentation":
		return &c.Routing.Documentation
	case "chat":
		return &c.Routing.Chat
	default:
		return nil
	}
}
