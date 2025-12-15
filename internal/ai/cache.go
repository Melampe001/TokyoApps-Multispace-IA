package ai

import (
	"crypto/sha256"
	"fmt"
	"sync"
	"time"
)

// CacheEntry represents a cached AI response
type CacheEntry struct {
	Response  *CompletionResponse
	ExpiresAt time.Time
}

// Cache provides in-memory caching for AI responses
type Cache struct {
	mu      sync.RWMutex
	entries map[string]*CacheEntry
	ttl     time.Duration
}

// NewCache creates a new cache with the specified TTL
func NewCache(ttl time.Duration) *Cache {
	cache := &Cache{
		entries: make(map[string]*CacheEntry),
		ttl:     ttl,
	}
	// Start cleanup goroutine
	go cache.cleanup()
	return cache
}

// Get retrieves a cached response
func (c *Cache) Get(req CompletionRequest) (*CompletionResponse, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	key := c.generateKey(req)
	entry, exists := c.entries[key]
	if !exists {
		return nil, false
	}

	if time.Now().After(entry.ExpiresAt) {
		return nil, false
	}

	// Create a copy with CacheHit set to true
	response := *entry.Response
	response.CacheHit = true
	return &response, true
}

// Set stores a response in the cache
func (c *Cache) Set(req CompletionRequest, resp *CompletionResponse) {
	c.mu.Lock()
	defer c.mu.Unlock()

	key := c.generateKey(req)
	c.entries[key] = &CacheEntry{
		Response:  resp,
		ExpiresAt: time.Now().Add(c.ttl),
	}
}

// Clear removes all entries from the cache
func (c *Cache) Clear() {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.entries = make(map[string]*CacheEntry)
}

// Size returns the number of entries in the cache
func (c *Cache) Size() int {
	c.mu.RLock()
	defer c.mu.RUnlock()
	return len(c.entries)
}

// generateKey creates a cache key from a request
func (c *Cache) generateKey(req CompletionRequest) string {
	// Create a deterministic key from request parameters
	data := fmt.Sprintf("%s|%s|%d|%.2f",
		req.Prompt,
		req.TaskType,
		req.MaxTokens,
		req.Temperature,
	)
	hash := sha256.Sum256([]byte(data))
	return fmt.Sprintf("%x", hash)
}

// cleanup periodically removes expired entries
func (c *Cache) cleanup() {
	ticker := time.NewTicker(5 * time.Minute)
	defer ticker.Stop()

	for range ticker.C {
		c.mu.Lock()
		now := time.Now()
		for key, entry := range c.entries {
			if now.After(entry.ExpiresAt) {
				delete(c.entries, key)
			}
		}
		c.mu.Unlock()
	}
}
