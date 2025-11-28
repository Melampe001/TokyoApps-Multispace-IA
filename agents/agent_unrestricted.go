// Package agents provides AI agent interfaces and implementations for Tokyo-IA.
package agents

// AgentUnrestricted is an agent with unrestricted capabilities.
// It provides functionality for open-ended AI interactions.
type AgentUnrestricted struct {
	name string
}

// NewAgentUnrestricted creates a new instance of AgentUnrestricted.
// It returns an Agent interface implementation for unrestricted tasks.
func NewAgentUnrestricted() Agent {
	return &AgentUnrestricted{
		name: "Unrestricted",
	}
}

// Name returns the unique name identifier of the Unrestricted agent.
func (a *AgentUnrestricted) Name() string {
	return a.name
}

// Execute performs unrestricted processing on the given input and returns the result.
func (a *AgentUnrestricted) Execute(input string) (string, error) {
	return "Unrestricted processed: " + input, nil
}
