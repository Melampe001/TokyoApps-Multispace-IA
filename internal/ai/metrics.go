package ai

import (
	"sync"
	"sync/atomic"
	"time"
)

// Metrics tracks usage statistics for AI operations
type Metrics struct {
	mu sync.RWMutex

	// Request counters
	totalRequests   atomic.Int64
	successRequests atomic.Int64
	failedRequests  atomic.Int64
	cacheHits       atomic.Int64

	// Per-provider counters
	providerRequests map[Provider]*atomic.Int64
	providerLatency  map[Provider]*LatencyStats

	// Token usage
	totalTokens atomic.Int64

	// Latency tracking
	totalLatency atomic.Int64
}

// LatencyStats tracks latency statistics
type LatencyStats struct {
	mu    sync.RWMutex
	sum   time.Duration
	count int64
	min   time.Duration
	max   time.Duration
}

// NewMetrics creates a new metrics instance
func NewMetrics() *Metrics {
	return &Metrics{
		providerRequests: make(map[Provider]*atomic.Int64),
		providerLatency:  make(map[Provider]*LatencyStats),
	}
}

// RecordRequest records a successful request
func (m *Metrics) RecordRequest(resp *CompletionResponse) {
	m.totalRequests.Add(1)
	m.successRequests.Add(1)
	m.totalTokens.Add(int64(resp.TokensUsed))
	m.totalLatency.Add(int64(resp.Latency))

	if resp.CacheHit {
		m.cacheHits.Add(1)
	}

	// Track per-provider metrics
	m.mu.Lock()
	if _, exists := m.providerRequests[resp.Provider]; !exists {
		m.providerRequests[resp.Provider] = &atomic.Int64{}
		m.providerLatency[resp.Provider] = &LatencyStats{
			min: time.Duration(1<<63 - 1), // Max int64
		}
	}
	m.mu.Unlock()

	m.providerRequests[resp.Provider].Add(1)
	m.providerLatency[resp.Provider].Record(resp.Latency)
}

// RecordError records a failed request
func (m *Metrics) RecordError() {
	m.totalRequests.Add(1)
	m.failedRequests.Add(1)
}

// GetStats returns current statistics
func (m *Metrics) GetStats() MetricsSnapshot {
	m.mu.RLock()
	defer m.mu.RUnlock()

	providerStats := make(map[Provider]ProviderMetrics)
	for provider, counter := range m.providerRequests {
		stats := m.providerLatency[provider]
		providerStats[provider] = ProviderMetrics{
			Requests:       counter.Load(),
			AverageLatency: stats.Average(),
			MinLatency:     stats.Min(),
			MaxLatency:     stats.Max(),
		}
	}

	total := m.totalRequests.Load()
	var successRate float64
	if total > 0 {
		successRate = float64(m.successRequests.Load()) / float64(total)
	}

	var cacheHitRate float64
	success := m.successRequests.Load()
	if success > 0 {
		cacheHitRate = float64(m.cacheHits.Load()) / float64(success)
	}

	var avgLatency time.Duration
	if success > 0 {
		avgLatency = time.Duration(m.totalLatency.Load() / success)
	}

	return MetricsSnapshot{
		TotalRequests:   total,
		SuccessRequests: m.successRequests.Load(),
		FailedRequests:  m.failedRequests.Load(),
		CacheHits:       m.cacheHits.Load(),
		TotalTokens:     m.totalTokens.Load(),
		SuccessRate:     successRate,
		CacheHitRate:    cacheHitRate,
		AverageLatency:  avgLatency,
		ProviderStats:   providerStats,
	}
}

// MetricsSnapshot represents a point-in-time view of metrics
type MetricsSnapshot struct {
	TotalRequests   int64
	SuccessRequests int64
	FailedRequests  int64
	CacheHits       int64
	TotalTokens     int64
	SuccessRate     float64
	CacheHitRate    float64
	AverageLatency  time.Duration
	ProviderStats   map[Provider]ProviderMetrics
}

// ProviderMetrics tracks per-provider statistics
type ProviderMetrics struct {
	Requests       int64
	AverageLatency time.Duration
	MinLatency     time.Duration
	MaxLatency     time.Duration
}

// Record adds a latency measurement
func (ls *LatencyStats) Record(latency time.Duration) {
	ls.mu.Lock()
	defer ls.mu.Unlock()

	ls.sum += latency
	ls.count++

	if latency < ls.min {
		ls.min = latency
	}
	if latency > ls.max {
		ls.max = latency
	}
}

// Average returns the average latency
func (ls *LatencyStats) Average() time.Duration {
	ls.mu.RLock()
	defer ls.mu.RUnlock()

	if ls.count == 0 {
		return 0
	}
	return ls.sum / time.Duration(ls.count)
}

// Min returns the minimum latency
func (ls *LatencyStats) Min() time.Duration {
	ls.mu.RLock()
	defer ls.mu.RUnlock()
	return ls.min
}

// Max returns the maximum latency
func (ls *LatencyStats) Max() time.Duration {
	ls.mu.RLock()
	defer ls.mu.RUnlock()
	return ls.max
}
