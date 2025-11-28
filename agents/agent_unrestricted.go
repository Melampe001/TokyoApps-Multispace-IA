// Package agents provides AI agent interfaces and implementations for Tokyo-IA.
package agents

// AgentUnrestricted is an agent with unrestricted capabilities.
// It provides functionality for open-ended AI interactions.
type AgentUnrestricted struct{}

// NewAgentUnrestricted creates a new instance of AgentUnrestricted.
// It returns an Agent interface implementation for unrestricted tasks.
func NewAgentUnrestricted() Agent {
	return &AgentUnrestricted{}
}

// Name returns the unique name identifier of the Unrestricted agent.
func (a *AgentUnrestricted) Name() string {
	return "Unrestricted"
}

// Description returns a brief description of the Unrestricted agent's capabilities.
func (a *AgentUnrestricted) Description() string {
	return "Provides open-ended AI interactions without restrictions"
}

// Execute performs unrestricted processing on the given input and returns the result.
func (a *AgentUnrestricted) Execute(input string) (string, error) {
	return "Unrestricted processed: " + input, nil
}
