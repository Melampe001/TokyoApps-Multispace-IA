package orchestrator

import (
	"context"
	"errors"
	"testing"
)

// mockAgent is a mock agent for testing.
type mockAgent struct {
	name       string
	shouldFail bool
	executed   bool
}

func (m *mockAgent) Name() string {
	return m.name
}

func (m *mockAgent) Execute(ctx context.Context) error {
	m.executed = true
	if m.shouldFail {
		return errors.New("mock agent failed")
	}
	return nil
}

func TestOrchestrator_Execute_AllSuccess(t *testing.T) {
	agent1 := &mockAgent{name: "agent1", shouldFail: false}
	agent2 := &mockAgent{name: "agent2", shouldFail: false}
	agent3 := &mockAgent{name: "agent3", shouldFail: false}

	orch := NewOrchestrator([]Agent{agent1, agent2, agent3})
	ctx := context.Background()

	results, err := orch.Execute(ctx)

	if err != nil {
		t.Errorf("Expected no error, got: %v", err)
	}

	if len(results) != 3 {
		t.Errorf("Expected 3 results, got: %d", len(results))
	}

	// Check all agents were executed
	if !agent1.executed || !agent2.executed || !agent3.executed {
		t.Error("Not all agents were executed")
	}

	// Check all results are successful
	for i, result := range results {
		if !result.Success {
			t.Errorf("Result %d should be successful", i)
		}
		if result.Error != nil {
			t.Errorf("Result %d should have no error, got: %v", i, result.Error)
		}
	}
}

func TestOrchestrator_Execute_StopsOnFailure(t *testing.T) {
	agent1 := &mockAgent{name: "agent1", shouldFail: false}
	agent2 := &mockAgent{name: "agent2", shouldFail: true} // This one fails
	agent3 := &mockAgent{name: "agent3", shouldFail: false}

	orch := NewOrchestrator([]Agent{agent1, agent2, agent3})
	ctx := context.Background()

	results, err := orch.Execute(ctx)

	// Should return an error
	if err == nil {
		t.Error("Expected an error when agent fails")
	}

	// Should have 2 results (agent1 success, agent2 failure)
	if len(results) != 2 {
		t.Errorf("Expected 2 results, got: %d", len(results))
	}

	// Agent1 should be executed and successful
	if !agent1.executed {
		t.Error("Agent1 should have been executed")
	}
	if !results[0].Success {
		t.Error("Agent1 result should be successful")
	}

	// Agent2 should be executed and failed
	if !agent2.executed {
		t.Error("Agent2 should have been executed")
	}
	if results[1].Success {
		t.Error("Agent2 result should not be successful")
	}

	// Agent3 should NOT be executed (stopped after agent2 failed)
	if agent3.executed {
		t.Error("Agent3 should NOT have been executed")
	}
}

func TestOrchestrator_Execute_FirstAgentFails(t *testing.T) {
	agent1 := &mockAgent{name: "agent1", shouldFail: true} // First one fails
	agent2 := &mockAgent{name: "agent2", shouldFail: false}
	agent3 := &mockAgent{name: "agent3", shouldFail: false}

	orch := NewOrchestrator([]Agent{agent1, agent2, agent3})
	ctx := context.Background()

	results, err := orch.Execute(ctx)

	if err == nil {
		t.Error("Expected an error when first agent fails")
	}

	// Should have only 1 result (agent1 failure)
	if len(results) != 1 {
		t.Errorf("Expected 1 result, got: %d", len(results))
	}

	// Agent1 should be executed and failed
	if !agent1.executed {
		t.Error("Agent1 should have been executed")
	}
	if results[0].Success {
		t.Error("Agent1 result should not be successful")
	}

	// Subsequent agents should NOT be executed
	if agent2.executed || agent3.executed {
		t.Error("Subsequent agents should NOT have been executed")
	}
}

func TestOrchestrator_Execute_EmptyAgentList(t *testing.T) {
	orch := NewOrchestrator([]Agent{})
	ctx := context.Background()

	results, err := orch.Execute(ctx)

	if err != nil {
		t.Errorf("Expected no error for empty agent list, got: %v", err)
	}

	if len(results) != 0 {
		t.Errorf("Expected 0 results for empty agent list, got: %d", len(results))
	}
}

func TestAgentResult_String(t *testing.T) {
	// Test success case
	result := AgentResult{
		AgentName: "test-agent",
		Success:   true,
		Error:     nil,
	}
	expected := "✅ test-agent: SUCCESS"
	if result.String() != expected {
		t.Errorf("Expected %q, got %q", expected, result.String())
	}

	// Test failure case
	result = AgentResult{
		AgentName: "test-agent",
		Success:   false,
		Error:     errors.New("test error"),
	}
	if result.Success {
		t.Error("Result should not be successful")
	}
	strResult := result.String()
	if strResult[:len("❌ test-agent: FAILED")] != "❌ test-agent: FAILED" {
		t.Errorf("Unexpected string format: %q", strResult)
	}
}
