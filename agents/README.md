# Agents Package

The `agents` package provides AI agent interfaces and implementations for Tokyo-IA.

## Overview

This package contains the `Agent` interface definition and implementations for various specialized AI agents. Each agent is designed for specific tasks and can be extended or customized as needed.

## Agent Interface

All agents implement the following interface:

```go
type Agent interface {
    // Name returns the unique name identifier of the agent.
    Name() string

    // Description returns a brief description of the agent's capabilities.
    Description() string

    // Execute performs the agent's main functionality and returns a result or error.
    Execute(input string) (string, error)
}
```

## Available Agents

| Agent | Constructor | Description |
|-------|-------------|-------------|
| **CodeMaster** | `NewAgentCodeMaster()` | Specialized in code analysis, generation, and review |
| **GenAI** | `NewAgentGenAI()` | Specialized in general AI tasks and content generation |
| **Knowledge** | `NewAgentKnowledge()` | Specialized in knowledge retrieval and information management |
| **Sentiment** | `NewAgentSentiment()` | Specialized in sentiment analysis and emotional tone detection |
| **Unrestricted** | `NewAgentUnrestricted()` | Provides open-ended AI interactions without restrictions |
| **QA** | `NewAgentQA()` | Specialized in quality assurance and testing automation |
| **Deploy** | `NewAgentDeploy()` | Specialized in deployment and release management automation |

## Usage

### Basic Usage

```go
package main

import (
    "fmt"
    "github.com/Melampe001/Tokyo-IA/agents"
)

func main() {
    // Create an agent
    agent := agents.NewAgentCodeMaster()
    
    // Get agent information
    fmt.Println("Name:", agent.Name())           // "CodeMaster"
    fmt.Println("Desc:", agent.Description())    // "Specialized in code analysis..."
    
    // Execute the agent
    result, err := agent.Execute("analyze this code")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    fmt.Println("Result:", result)
}
```

### Working with Multiple Agents

```go
func processWithAgents(input string) {
    agentList := []agents.Agent{
        agents.NewAgentCodeMaster(),
        agents.NewAgentGenAI(),
        agents.NewAgentSentiment(),
    }
    
    for _, agent := range agentList {
        result, err := agent.Execute(input)
        if err != nil {
            fmt.Printf("%s error: %v\n", agent.Name(), err)
            continue
        }
        fmt.Printf("%s: %s\n", agent.Name(), result)
    }
}
```

## Testing

Run the tests with:

```bash
make test
# or
go test ./agents/...
```

Run tests with verbose output:

```bash
go test -v ./agents/...
```

## Test Coverage

The test suite includes:

- **TestAgentCreation**: Verifies all agent constructors return valid implementations
- **TestAgentDescription**: Verifies all agents return non-empty descriptions
- **TestAgentExecute**: Verifies Execute() returns expected results
- **TestAgentExecuteEmptyInput**: Verifies agents handle empty input gracefully
- **TestAgentInterfaceCompliance**: Compile-time interface compliance verification

## File Structure

```
agents/
├── agent.go              # Agent interface definition
├── agent_codemaster.go   # CodeMaster agent implementation
├── agent_genai.go        # GenAI agent implementation
├── agent_knowledge.go    # Knowledge agent implementation
├── agent_sentiment.go    # Sentiment agent implementation
├── agent_unrestricted.go # Unrestricted agent implementation
├── agent_qa.go           # QA agent implementation
├── agent_deploy.go       # Deploy agent implementation
├── agents_test.go        # Unit tests
└── README.md             # This file
```

## Contributing

When adding a new agent:

1. Create a new file `agent_<name>.go`
2. Implement the `Agent` interface with all three methods
3. Add a public constructor `NewAgent<Name>() Agent`
4. Add test cases to `agents_test.go`
5. Update this README with the new agent information
