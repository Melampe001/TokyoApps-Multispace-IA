// Package orchestrator provides the agent orchestration system.
package orchestrator

import (
	"github.com/Melampe001/Tokyo-IA/internal/orchestrator/agents"
)

// NewDefaultOrchestrator creates an orchestrator with all agents in the correct order.
// Order: architect → dependency → validator → security → optimization → monetization → build
func NewDefaultOrchestrator() *Orchestrator {
	agentList := []Agent{
		agents.NewArchitectAgent(),    // 1
		agents.NewDependencyAgent(),   // 2
		agents.NewValidatorAgent(),    // 3
		agents.NewSecurityAgent(),     // 4
		agents.NewOptimizationAgent(), // 5
		agents.NewMonetizationAgent(), // 6
		agents.NewBuildAgent(),        // 7
	}
	return NewOrchestrator(agentList)
}
