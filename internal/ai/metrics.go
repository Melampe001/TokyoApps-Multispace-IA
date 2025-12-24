// Package ai provides metrics collection for AI model usage.
package ai

import (
	"sync"
	"time"
)

// MetricsCollector collects and aggregates metrics for AI model usage.
type MetricsCollector struct {
	metrics map[ModelProvider]*ModelMetrics
	mu      sync.RWMutex
}

// NewMetricsCollector creates a new metrics collector.
func NewMetricsCollector() *MetricsCollector {
	return &MetricsCollector{
		metrics: make(map[ModelProvider]*ModelMetrics),
	}
}

// RecordRequest records metrics for a completed request.
func (m *MetricsCollector) RecordRequest(provider ModelProvider, model string, duration time.Duration, tokens int, cost float64, cached bool) {
	m.mu.Lock()
	defer m.mu.Unlock()

	if _, ok := m.metrics[provider]; !ok {
		m.metrics[provider] = &ModelMetrics{
			Provider: provider,
			Model:    model,
		}
	}

	metric := m.metrics[provider]
	metric.RequestCount++
	metric.TotalTokens += int64(tokens)
	metric.TotalCostUSD += cost
	metric.LastUsed = time.Now()

	// Calculate running average latency
	if metric.AvgLatencyMs == 0 {
		metric.AvgLatencyMs = float64(duration.Milliseconds())
	} else {
		// Exponential moving average
		alpha := 0.1
		metric.AvgLatencyMs = alpha*float64(duration.Milliseconds()) + (1-alpha)*metric.AvgLatencyMs
	}
}

// RecordError records an error for a provider.
func (m *MetricsCollector) RecordError(provider ModelProvider) {
	m.mu.Lock()
	defer m.mu.Unlock()

	if _, ok := m.metrics[provider]; !ok {
		m.metrics[provider] = &ModelMetrics{
			Provider: provider,
		}
	}

	m.metrics[provider].ErrorCount++
}

// GetMetrics returns metrics for a specific provider.
func (m *MetricsCollector) GetMetrics(provider ModelProvider) *ModelMetrics {
	m.mu.RLock()
	defer m.mu.RUnlock()

	metric, ok := m.metrics[provider]
	if !ok {
		return nil
	}

	// Return a copy to avoid race conditions
	return &ModelMetrics{
		Provider:     metric.Provider,
		Model:        metric.Model,
		RequestCount: metric.RequestCount,
		ErrorCount:   metric.ErrorCount,
		TotalTokens:  metric.TotalTokens,
		TotalCostUSD: metric.TotalCostUSD,
		AvgLatencyMs: metric.AvgLatencyMs,
		LastUsed:     metric.LastUsed,
	}
}

// GetAllMetrics returns metrics for all providers.
func (m *MetricsCollector) GetAllMetrics() map[ModelProvider]*ModelMetrics {
	m.mu.RLock()
	defer m.mu.RUnlock()

	result := make(map[ModelProvider]*ModelMetrics)
	for provider, metric := range m.metrics {
		result[provider] = &ModelMetrics{
			Provider:     metric.Provider,
			Model:        metric.Model,
			RequestCount: metric.RequestCount,
			ErrorCount:   metric.ErrorCount,
			TotalTokens:  metric.TotalTokens,
			TotalCostUSD: metric.TotalCostUSD,
			AvgLatencyMs: metric.AvgLatencyMs,
			LastUsed:     metric.LastUsed,
		}
	}

	return result
}

// GetTotalCost returns the total cost across all providers.
func (m *MetricsCollector) GetTotalCost() float64 {
	m.mu.RLock()
	defer m.mu.RUnlock()

	total := 0.0
	for _, metric := range m.metrics {
		total += metric.TotalCostUSD
	}
	return total
}

// GetTotalRequests returns the total request count across all providers.
func (m *MetricsCollector) GetTotalRequests() int64 {
	m.mu.RLock()
	defer m.mu.RUnlock()

	total := int64(0)
	for _, metric := range m.metrics {
		total += metric.RequestCount
	}
	return total
}

// GetErrorRate returns the error rate for a provider.
func (m *MetricsCollector) GetErrorRate(provider ModelProvider) float64 {
	m.mu.RLock()
	defer m.mu.RUnlock()

	metric, ok := m.metrics[provider]
	if !ok || metric.RequestCount == 0 {
		return 0.0
	}

	return float64(metric.ErrorCount) / float64(metric.RequestCount)
}

// Reset resets all metrics.
func (m *MetricsCollector) Reset() {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.metrics = make(map[ModelProvider]*ModelMetrics)
}

// Summary returns a human-readable summary of metrics.
type MetricsSummary struct {
	TotalRequests     int64
	TotalCost         float64
	TotalTokens       int64
	ProviderBreakdown map[ModelProvider]ProviderSummary
}

// ProviderSummary holds summary data for a provider.
type ProviderSummary struct {
	Requests   int64
	Cost       float64
	Tokens     int64
	AvgLatency float64
	ErrorRate  float64
}

// GetSummary returns a summary of all metrics.
func (m *MetricsCollector) GetSummary() *MetricsSummary {
	m.mu.RLock()
	defer m.mu.RUnlock()

	summary := &MetricsSummary{
		ProviderBreakdown: make(map[ModelProvider]ProviderSummary),
	}

	for provider, metric := range m.metrics {
		summary.TotalRequests += metric.RequestCount
		summary.TotalCost += metric.TotalCostUSD
		summary.TotalTokens += metric.TotalTokens

		errorRate := 0.0
		if metric.RequestCount > 0 {
			errorRate = float64(metric.ErrorCount) / float64(metric.RequestCount)
		}

		summary.ProviderBreakdown[provider] = ProviderSummary{
			Requests:   metric.RequestCount,
			Cost:       metric.TotalCostUSD,
			Tokens:     metric.TotalTokens,
			AvgLatency: metric.AvgLatencyMs,
			ErrorRate:  errorRate,
		}
	}

	return summary
}
