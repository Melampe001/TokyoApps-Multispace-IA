// Package ai provides caching functionality for AI model responses.
package ai

import (
	"context"
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"sync"
	"time"
)

// Cache is the interface for caching AI model responses.
type Cache interface {
	Get(ctx context.Context, req *CompletionRequest) (*CompletionResponse, error)
	Set(ctx context.Context, req *CompletionRequest, resp *CompletionResponse) error
	Delete(ctx context.Context, req *CompletionRequest) error
	Clear(ctx context.Context) error
}

// InMemoryCache is a simple in-memory cache implementation.
type InMemoryCache struct {
	store map[string]*cacheEntry
	ttl   time.Duration
	mu    sync.RWMutex
}

type cacheEntry struct {
	response  *CompletionResponse
	expiresAt time.Time
}

// NewInMemoryCache creates a new in-memory cache.
func NewInMemoryCache(ttl time.Duration) *InMemoryCache {
	cache := &InMemoryCache{
		store: make(map[string]*cacheEntry),
		ttl:   ttl,
	}

	// Start cleanup goroutine
	go cache.cleanupExpired()

	return cache
}

// Get retrieves a cached response.
func (c *InMemoryCache) Get(ctx context.Context, req *CompletionRequest) (*CompletionResponse, error) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	key := c.generateKey(req)
	entry, ok := c.store[key]
	if !ok {
		return nil, fmt.Errorf("cache miss")
	}

	// Check if expired
	if time.Now().After(entry.expiresAt) {
		return nil, fmt.Errorf("cache expired")
	}

	return entry.response, nil
}

// Set stores a response in the cache.
func (c *InMemoryCache) Set(ctx context.Context, req *CompletionRequest, resp *CompletionResponse) error {
	c.mu.Lock()
	defer c.mu.Unlock()

	key := c.generateKey(req)
	c.store[key] = &cacheEntry{
		response:  resp,
		expiresAt: time.Now().Add(c.ttl),
	}

	return nil
}

// Delete removes an entry from the cache.
func (c *InMemoryCache) Delete(ctx context.Context, req *CompletionRequest) error {
	c.mu.Lock()
	defer c.mu.Unlock()

	key := c.generateKey(req)
	delete(c.store, key)

	return nil
}

// Clear removes all entries from the cache.
func (c *InMemoryCache) Clear(ctx context.Context) error {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.store = make(map[string]*cacheEntry)
	return nil
}

// generateKey generates a cache key from a request.
func (c *InMemoryCache) generateKey(req *CompletionRequest) string {
	// Create a deterministic key from request properties
	data := fmt.Sprintf("%s|%s|%s|%d|%.2f",
		req.Prompt,
		req.TaskType,
		req.Complexity,
		req.MaxTokens,
		req.Temperature,
	)

	hash := sha256.Sum256([]byte(data))
	return fmt.Sprintf("%x", hash)
}

// cleanupExpired periodically removes expired entries.
func (c *InMemoryCache) cleanupExpired() {
	ticker := time.NewTicker(5 * time.Minute)
	defer ticker.Stop()

	for range ticker.C {
		c.mu.Lock()
		now := time.Now()
		for key, entry := range c.store {
			if now.After(entry.expiresAt) {
				delete(c.store, key)
			}
		}
		c.mu.Unlock()
	}
}

// RedisCache is a Redis-based cache implementation (stub for now).
type RedisCache struct {
	// Redis client would go here
	ttl time.Duration
}

// NewRedisCache creates a new Redis cache (stub implementation).
func NewRedisCache(ttl time.Duration) *RedisCache {
	return &RedisCache{
		ttl: ttl,
	}
}

// Get retrieves a cached response from Redis.
func (c *RedisCache) Get(ctx context.Context, req *CompletionRequest) (*CompletionResponse, error) {
	// TODO: Implement Redis integration
	return nil, fmt.Errorf("redis cache not implemented")
}

// Set stores a response in Redis.
func (c *RedisCache) Set(ctx context.Context, req *CompletionRequest, resp *CompletionResponse) error {
	// TODO: Implement Redis integration
	return fmt.Errorf("redis cache not implemented")
}

// Delete removes an entry from Redis.
func (c *RedisCache) Delete(ctx context.Context, req *CompletionRequest) error {
	// TODO: Implement Redis integration
	return fmt.Errorf("redis cache not implemented")
}

// Clear removes all entries from Redis.
func (c *RedisCache) Clear(ctx context.Context) error {
	// TODO: Implement Redis integration
	return fmt.Errorf("redis cache not implemented")
}

// CacheStats holds statistics about cache usage.
type CacheStats struct {
	Hits        int64
	Misses      int64
	Size        int
	HitRate     float64
	LastCleanup time.Time
}

// GetStats returns cache statistics.
func (c *InMemoryCache) GetStats() *CacheStats {
	c.mu.RLock()
	defer c.mu.RUnlock()

	hits := int64(0)   // Would need to track this
	misses := int64(0) // Would need to track this
	hitRate := 0.0
	if hits+misses > 0 {
		hitRate = float64(hits) / float64(hits+misses)
	}

	return &CacheStats{
		Hits:    hits,
		Misses:  misses,
		Size:    len(c.store),
		HitRate: hitRate,
	}
}

// SerializeResponse serializes a response for storage.
func SerializeResponse(resp *CompletionResponse) ([]byte, error) {
	return json.Marshal(resp)
}

// DeserializeResponse deserializes a response from storage.
func DeserializeResponse(data []byte) (*CompletionResponse, error) {
	var resp CompletionResponse
	err := json.Unmarshal(data, &resp)
	return &resp, err
}
