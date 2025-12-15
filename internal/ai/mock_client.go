package ai

import (
	"context"
	"fmt"
	"strings"
	"time"
)

// MockClient is a mock AI client for testing and development
type MockClient struct {
	name      string
	provider  Provider
	available bool
	delay     time.Duration
}

// NewMockClient creates a new mock client
func NewMockClient(provider Provider, name string) *MockClient {
	return &MockClient{
		name:      name,
		provider:  provider,
		available: true,
		delay:     100 * time.Millisecond,
	}
}

// Complete generates a mock response
func (m *MockClient) Complete(ctx context.Context, req CompletionRequest) (*CompletionResponse, error) {
	// Simulate processing delay
	select {
	case <-time.After(m.delay):
	case <-ctx.Done():
		return nil, ctx.Err()
	}

	// Generate mock response based on task type
	content := m.generateMockResponse(req)

	return &CompletionResponse{
		Content: content,
		Model: Model{
			Provider:  m.provider,
			Name:      m.name,
			MaxTokens: 4096,
		},
		TokensUsed: len(strings.Split(content, " ")),
		CacheHit:   false,
	}, nil
}

// Name returns the client name
func (m *MockClient) Name() string {
	return m.name
}

// IsAvailable returns whether the client is available
func (m *MockClient) IsAvailable() bool {
	return m.available
}

// SetAvailable sets the availability status
func (m *MockClient) SetAvailable(available bool) {
	m.available = available
}

// SetDelay sets the processing delay
func (m *MockClient) SetDelay(delay time.Duration) {
	m.delay = delay
}

// generateMockResponse generates appropriate mock responses based on task type
func (m *MockClient) generateMockResponse(req CompletionRequest) string {
	switch req.TaskType {
	case TaskTypeReasoning:
		return fmt.Sprintf("Mock reasoning response from %s: After careful analysis of '%s', the logical conclusion is that this demonstrates complex reasoning patterns.", m.name, truncate(req.Prompt, 50))

	case TaskTypeCreative:
		return fmt.Sprintf("Mock creative response from %s: Inspired by '%s', here's a creative interpretation that blends imagination with insight.", m.name, truncate(req.Prompt, 50))

	case TaskTypeCodeReview:
		return fmt.Sprintf("Mock code review from %s: The code snippet looks good overall. Consider adding error handling and documentation. Task: '%s'", m.name, truncate(req.Prompt, 50))

	case TaskTypeCodeGen:
		return fmt.Sprintf("Mock code generation from %s:\n```go\nfunc Example() {\n    // Generated based on: %s\n    fmt.Println(\"Mock implementation\")\n}\n```", m.name, truncate(req.Prompt, 50))

	case TaskTypeTranslation:
		return fmt.Sprintf("Mock translation from %s: This is a translated version of '%s'.", m.name, truncate(req.Prompt, 50))

	default:
		return fmt.Sprintf("Mock response from %s for prompt: '%s'", m.name, truncate(req.Prompt, 100))
	}
}

// truncate truncates a string to the specified length
func truncate(s string, maxLen int) string {
	if len(s) <= maxLen {
		return s
	}
	return s[:maxLen] + "..."
}
