// Package agents provides AI agent interfaces and implementations for Tokyo-IA.
package agents

import "testing"

// TestAgentCreation verifies that all agent constructors return valid Agent implementations.
// This test uses table-driven testing to ensure each agent can be created and provides
// expected Name() and Execute() functionality.
func TestAgentCreation(t *testing.T) {
	testCases := []struct {
		name        string
		constructor func() Agent
		expected    string
	}{
		{
			name:        "AgentCodeMaster",
			constructor: NewAgentCodeMaster,
			expected:    "CodeMaster",
		},
		{
			name:        "AgentGenAI",
			constructor: NewAgentGenAI,
			expected:    "GenAI",
		},
		{
			name:        "AgentKnowledge",
			constructor: NewAgentKnowledge,
			expected:    "Knowledge",
		},
		{
			name:        "AgentSentiment",
			constructor: NewAgentSentiment,
			expected:    "Sentiment",
		},
		{
			name:        "AgentUnrestricted",
			constructor: NewAgentUnrestricted,
			expected:    "Unrestricted",
		},
		{
			name:        "AgentQA",
			constructor: NewAgentQA,
			expected:    "QA",
		},
		{
			name:        "AgentDeploy",
			constructor: NewAgentDeploy,
			expected:    "Deploy",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			agent := tc.constructor()
			if agent == nil {
				t.Fatalf("expected non-nil agent, got nil")
			}

			actualName := agent.Name()
			if actualName != tc.expected {
				t.Errorf("expected Name() to return %q, got %q", tc.expected, actualName)
			}
		})
	}
}

// TestAgentExecute verifies that all agents can execute with valid input and return expected results.
func TestAgentExecute(t *testing.T) {
	testCases := []struct {
		name        string
		constructor func() Agent
		input       string
		wantPrefix  string
	}{
		{
			name:        "AgentCodeMaster",
			constructor: NewAgentCodeMaster,
			input:       "test input",
			wantPrefix:  "CodeMaster processed: test input",
		},
		{
			name:        "AgentGenAI",
			constructor: NewAgentGenAI,
			input:       "test input",
			wantPrefix:  "GenAI processed: test input",
		},
		{
			name:        "AgentKnowledge",
			constructor: NewAgentKnowledge,
			input:       "test input",
			wantPrefix:  "Knowledge processed: test input",
		},
		{
			name:        "AgentSentiment",
			constructor: NewAgentSentiment,
			input:       "test input",
			wantPrefix:  "Sentiment processed: test input",
		},
		{
			name:        "AgentUnrestricted",
			constructor: NewAgentUnrestricted,
			input:       "test input",
			wantPrefix:  "Unrestricted processed: test input",
		},
		{
			name:        "AgentQA",
			constructor: NewAgentQA,
			input:       "test input",
			wantPrefix:  "QA processed: test input",
		},
		{
			name:        "AgentDeploy",
			constructor: NewAgentDeploy,
			input:       "test input",
			wantPrefix:  "Deploy processed: test input",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			agent := tc.constructor()
			result, err := agent.Execute(tc.input)
			if err != nil {
				t.Fatalf("expected no error, got %v", err)
			}

			if result != tc.wantPrefix {
				t.Errorf("expected Execute() to return %q, got %q", tc.wantPrefix, result)
			}
		})
	}
}
