// Package agents provides agent implementations for Tokyo-IA.
//
// This file contains tests for all agent implementations.
package agents

import "testing"

// TestAgentCreation tests the creation of all agents using table-driven tests.
func TestAgentCreation(t *testing.T) {
	tests := []struct {
		name     string
		createFn func() interface{}
		wantNil  bool
	}{
		{
			name:     "CodeMasterAgent creation",
			createFn: func() interface{} { return NewCodeMasterAgent() },
			wantNil:  false,
		},
		{
			name:     "GenAIAgent creation",
			createFn: func() interface{} { return NewGenAIAgent() },
			wantNil:  false,
		},
		{
			name:     "KnowledgeAgent creation",
			createFn: func() interface{} { return NewKnowledgeAgent() },
			wantNil:  false,
		},
		{
			name:     "SentimentAgent creation",
			createFn: func() interface{} { return NewSentimentAgent() },
			wantNil:  false,
		},
		{
			name:     "UnrestrictedAgent creation",
			createFn: func() interface{} { return NewUnrestrictedAgent() },
			wantNil:  false,
		},
		{
			name:     "QAAgent creation",
			createFn: func() interface{} { return NewQAAgent() },
			wantNil:  false,
		},
		{
			name:     "DeployAgent creation",
			createFn: func() interface{} { return NewDeployAgent() },
			wantNil:  false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := tt.createFn()
			if (got == nil) != tt.wantNil {
				t.Errorf("%s = %v, wantNil = %v", tt.name, got, tt.wantNil)
			}
		})
	}
}

// TestCodeMasterAgentAnalyze tests the CodeMasterAgent Analyze method.
func TestCodeMasterAgentAnalyze(t *testing.T) {
	agent := NewCodeMasterAgent()
	result, err := agent.Analyze("test input")
	if err != nil {
		t.Errorf("Analyze() error = %v", err)
	}
	if result == "" {
		t.Error("Analyze() returned empty result")
	}
}

// TestGenAIAgentGenerate tests the GenAIAgent Generate method.
func TestGenAIAgentGenerate(t *testing.T) {
	agent := NewGenAIAgent()
	result, err := agent.Generate("test prompt")
	if err != nil {
		t.Errorf("Generate() error = %v", err)
	}
	if result == "" {
		t.Error("Generate() returned empty result")
	}
}

// TestKnowledgeAgentQuery tests the KnowledgeAgent Query method.
func TestKnowledgeAgentQuery(t *testing.T) {
	agent := NewKnowledgeAgent()
	result, err := agent.Query("test query")
	if err != nil {
		t.Errorf("Query() error = %v", err)
	}
	if result == "" {
		t.Error("Query() returned empty result")
	}
}

// TestSentimentAgentAnalyze tests the SentimentAgent Analyze method.
func TestSentimentAgentAnalyze(t *testing.T) {
	agent := NewSentimentAgent()
	result, err := agent.Analyze("test text")
	if err != nil {
		t.Errorf("Analyze() error = %v", err)
	}
	if result == "" {
		t.Error("Analyze() returned empty result")
	}
}

// TestUnrestrictedAgentProcess tests the UnrestrictedAgent Process method.
func TestUnrestrictedAgentProcess(t *testing.T) {
	agent := NewUnrestrictedAgent()
	result, err := agent.Process("test input")
	if err != nil {
		t.Errorf("Process() error = %v", err)
	}
	if result == "" {
		t.Error("Process() returned empty result")
	}
}

// TestQAAgentValidate tests the QAAgent Validate method.
func TestQAAgentValidate(t *testing.T) {
	agent := NewQAAgent()
	result, err := agent.Validate("test input")
	if err != nil {
		t.Errorf("Validate() error = %v", err)
	}
	if result == "" {
		t.Error("Validate() returned empty result")
	}
}

// TestDeployAgentExecute tests the DeployAgent Execute method.
func TestDeployAgentExecute(t *testing.T) {
	agent := NewDeployAgent()
	result, err := agent.Execute("test config")
	if err != nil {
		t.Errorf("Execute() error = %v", err)
	}
	if result == "" {
		t.Error("Execute() returned empty result")
	}
}
