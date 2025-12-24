// Package orchestrator provides the agent orchestration system.
package orchestrator

import (
	"context"
	"fmt"
)

// Orchestrator manages the execution of agents in a specific order.
type Orchestrator struct {
	agents []Agent
}

// NewOrchestrator creates a new orchestrator with the given agents.
func NewOrchestrator(agents []Agent) *Orchestrator {
	return &Orchestrator{
		agents: agents,
	}
}

// Execute runs all agents in order.
// If any agent fails, execution stops immediately and returns an error.
func (o *Orchestrator) Execute(ctx context.Context) ([]AgentResult, error) {
	results := make([]AgentResult, 0, len(o.agents))

	for i, agent := range o.agents {
		fmt.Printf("🔄 Executing agent %d/%d: %s\n", i+1, len(o.agents), agent.Name())

		err := agent.Execute(ctx)
		result := AgentResult{
			AgentName: agent.Name(),
			Success:   err == nil,
			Error:     err,
		}
		results = append(results, result)

		fmt.Println(result.String())

		if err != nil {
			return results, fmt.Errorf("agent %s failed: %w", agent.Name(), err)
		}
	}

	return results, nil
}
