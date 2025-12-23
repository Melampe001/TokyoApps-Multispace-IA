// Package orchestrator provides the agent orchestration system.
package orchestrator

import (
	"context"
	"fmt"
)

// Agent represents an executable agent in the orchestration system.
type Agent interface {
	// Name returns the agent's name.
	Name() string

	// Execute runs the agent's logic.
	// Returns an error if the agent fails, which will stop the orchestration.
	Execute(ctx context.Context) error
}

// AgentResult holds the result of an agent execution.
type AgentResult struct {
	AgentName string
	Success   bool
	Error     error
}

// String returns a string representation of the result.
func (r AgentResult) String() string {
	if r.Success {
		return fmt.Sprintf("✅ %s: SUCCESS", r.AgentName)
	}
	return fmt.Sprintf("❌ %s: FAILED - %v", r.AgentName, r.Error)
}
