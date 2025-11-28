// Package agents provides AI agent interfaces and implementations for Tokyo-IA.
package agents

// Agent defines the minimal interface that all agents must implement.
// It provides common functionality for agent identification and execution.
type Agent interface {
	// Name returns the unique name identifier of the agent.
	Name() string

	// Execute performs the agent's main functionality and returns a result or error.
	Execute(input string) (string, error)
}
