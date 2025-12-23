// Package agents provides AI agent interfaces and implementations for Tokyo-IA.
//
// This package contains the Agent interface definition and implementations for
// various specialized AI agents including CodeMaster, GenAI, Knowledge, Sentiment,
// Unrestricted, QA, and Deploy agents.
//
// # Usage
//
// To create and use an agent:
//
//	agent := agents.NewAgentCodeMaster()
//	fmt.Println(agent.Name())           // "CodeMaster"
//	fmt.Println(agent.Description())    // "Specialized in code analysis..."
//	result, err := agent.Execute("foo") // "CodeMaster processed: foo", nil
package agents

// Agent defines the minimal interface that all agents must implement.
// It provides common functionality for agent identification and execution.
type Agent interface {
	// Name returns the unique name identifier of the agent.
	Name() string

	// Description returns a brief description of the agent's capabilities.
	Description() string

	// Execute performs the agent's main functionality and returns a result or error.
	Execute(input string) (string, error)
}
