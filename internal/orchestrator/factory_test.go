package orchestrator

import (
	"context"
	"testing"
)

func TestNewDefaultOrchestrator(t *testing.T) {
	orch := NewDefaultOrchestrator()

	if orch == nil {
		t.Fatal("NewDefaultOrchestrator should not return nil")
	}

	if len(orch.agents) != 7 {
		t.Errorf("Expected 7 agents, got %d", len(orch.agents))
	}

	// Verify agent order
	expectedOrder := []string{
		"architect.agent",
		"dependency.agent",
		"validator.agent",
		"security.agent",
		"optimization.agent",
		"monetization.agent",
		"build.agent",
	}

	for i, expected := range expectedOrder {
		if i >= len(orch.agents) {
			t.Errorf("Missing agent at position %d: %s", i, expected)
			continue
		}
		actual := orch.agents[i].Name()
		if actual != expected {
			t.Errorf("Agent at position %d: expected '%s', got '%s'", i, expected, actual)
		}
	}
}

func TestDefaultOrchestrator_Execute(t *testing.T) {
	orch := NewDefaultOrchestrator()
	ctx := context.Background()

	results, err := orch.Execute(ctx)

	if err != nil {
		t.Errorf("Default orchestrator should execute without error, got: %v", err)
	}

	if len(results) != 7 {
		t.Errorf("Expected 7 results, got %d", len(results))
	}

	// All results should be successful
	for i, result := range results {
		if !result.Success {
			t.Errorf("Result %d (%s) should be successful", i, result.AgentName)
		}
		if result.Error != nil {
			t.Errorf("Result %d (%s) should have no error, got: %v", i, result.AgentName, result.Error)
		}
	}
}
