package ai

import (
	"testing"
	"time"
)

func TestCache_GetSet(t *testing.T) {
	cache := NewCache(5 * time.Minute)

	req := CompletionRequest{
		Prompt:      "Test prompt",
		TaskType:    TaskTypeGeneral,
		MaxTokens:   100,
		Temperature: 0.7,
	}

	resp := &CompletionResponse{
		Content:    "Test response",
		TokensUsed: 10,
		Model: Model{
			Provider: ProviderOpenAI,
			Name:     "gpt-4",
		},
	}

	// Cache should be empty initially
	if _, hit := cache.Get(req); hit {
		t.Error("Expected cache miss for new request")
	}

	// Set cache entry
	cache.Set(req, resp)

	// Should now be cached
	cached, hit := cache.Get(req)
	if !hit {
		t.Error("Expected cache hit after setting")
	}

	if !cached.CacheHit {
		t.Error("Cached response should have CacheHit set to true")
	}

	if cached.Content != resp.Content {
		t.Errorf("Cached content = %v, want %v", cached.Content, resp.Content)
	}
}

func TestCache_Expiration(t *testing.T) {
	cache := NewCache(100 * time.Millisecond)

	req := CompletionRequest{
		Prompt:      "Test prompt",
		TaskType:    TaskTypeGeneral,
		MaxTokens:   100,
		Temperature: 0.7,
	}

	resp := &CompletionResponse{
		Content:    "Test response",
		TokensUsed: 10,
	}

	cache.Set(req, resp)

	// Should be cached immediately
	if _, hit := cache.Get(req); !hit {
		t.Error("Expected cache hit immediately after setting")
	}

	// Wait for expiration
	time.Sleep(150 * time.Millisecond)

	// Should now be expired
	if _, hit := cache.Get(req); hit {
		t.Error("Expected cache miss after expiration")
	}
}

func TestCache_Clear(t *testing.T) {
	cache := NewCache(5 * time.Minute)

	req := CompletionRequest{
		Prompt:      "Test prompt",
		TaskType:    TaskTypeGeneral,
		MaxTokens:   100,
		Temperature: 0.7,
	}

	resp := &CompletionResponse{
		Content:    "Test response",
		TokensUsed: 10,
	}

	cache.Set(req, resp)

	if cache.Size() != 1 {
		t.Errorf("Expected size 1, got %d", cache.Size())
	}

	cache.Clear()

	if cache.Size() != 0 {
		t.Errorf("Expected size 0 after clear, got %d", cache.Size())
	}

	if _, hit := cache.Get(req); hit {
		t.Error("Expected cache miss after clear")
	}
}

func TestCache_DifferentRequests(t *testing.T) {
	cache := NewCache(5 * time.Minute)

	req1 := CompletionRequest{
		Prompt:      "Test prompt 1",
		TaskType:    TaskTypeGeneral,
		MaxTokens:   100,
		Temperature: 0.7,
	}

	req2 := CompletionRequest{
		Prompt:      "Test prompt 2",
		TaskType:    TaskTypeGeneral,
		MaxTokens:   100,
		Temperature: 0.7,
	}

	resp1 := &CompletionResponse{Content: "Response 1"}
	resp2 := &CompletionResponse{Content: "Response 2"}

	cache.Set(req1, resp1)
	cache.Set(req2, resp2)

	// Each request should get its own response
	cached1, hit1 := cache.Get(req1)
	cached2, hit2 := cache.Get(req2)

	if !hit1 || !hit2 {
		t.Error("Expected cache hits for both requests")
	}

	if cached1.Content != "Response 1" {
		t.Errorf("Wrong content for req1: %v", cached1.Content)
	}

	if cached2.Content != "Response 2" {
		t.Errorf("Wrong content for req2: %v", cached2.Content)
	}
}
