package agents

import (
	"context"
	"testing"
)

func TestArchitectAgent(t *testing.T) {
	agent := NewArchitectAgent()

	if agent.Name() != "architect.agent" {
		t.Errorf("Expected name 'architect.agent', got '%s'", agent.Name())
	}

	ctx := context.Background()
	err := agent.Execute(ctx)
	if err != nil {
		t.Errorf("Execute should not return error, got: %v", err)
	}
}

func TestDependencyAgent(t *testing.T) {
	agent := NewDependencyAgent()

	if agent.Name() != "dependency.agent" {
		t.Errorf("Expected name 'dependency.agent', got '%s'", agent.Name())
	}

	ctx := context.Background()
	err := agent.Execute(ctx)
	if err != nil {
		t.Errorf("Execute should not return error, got: %v", err)
	}
}

func TestValidatorAgent(t *testing.T) {
	agent := NewValidatorAgent()

	if agent.Name() != "validator.agent" {
		t.Errorf("Expected name 'validator.agent', got '%s'", agent.Name())
	}

	ctx := context.Background()
	err := agent.Execute(ctx)
	if err != nil {
		t.Errorf("Execute should not return error, got: %v", err)
	}
}

func TestSecurityAgent(t *testing.T) {
	agent := NewSecurityAgent()

	if agent.Name() != "security.agent" {
		t.Errorf("Expected name 'security.agent', got '%s'", agent.Name())
	}

	ctx := context.Background()
	err := agent.Execute(ctx)
	if err != nil {
		t.Errorf("Execute should not return error, got: %v", err)
	}
}

func TestOptimizationAgent(t *testing.T) {
	agent := NewOptimizationAgent()

	if agent.Name() != "optimization.agent" {
		t.Errorf("Expected name 'optimization.agent', got '%s'", agent.Name())
	}

	ctx := context.Background()
	err := agent.Execute(ctx)
	if err != nil {
		t.Errorf("Execute should not return error, got: %v", err)
	}
}

func TestMonetizationAgent(t *testing.T) {
	agent := NewMonetizationAgent()

	if agent.Name() != "monetization.agent" {
		t.Errorf("Expected name 'monetization.agent', got '%s'", agent.Name())
	}

	ctx := context.Background()
	err := agent.Execute(ctx)
	if err != nil {
		t.Errorf("Execute should not return error, got: %v", err)
	}
}

func TestBuildAgent(t *testing.T) {
	agent := NewBuildAgent()

	if agent.Name() != "build.agent" {
		t.Errorf("Expected name 'build.agent', got '%s'", agent.Name())
	}

	ctx := context.Background()
	err := agent.Execute(ctx)
	if err != nil {
		t.Errorf("Execute should not return error, got: %v", err)
	}
}
