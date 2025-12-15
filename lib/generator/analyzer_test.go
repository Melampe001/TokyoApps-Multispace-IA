// Package generator provides tests for the analyzer.
package generator

import (
	"testing"
)

func TestSimpleDetection(t *testing.T) {
	analyzer := NewAnalyzer("non-existent-manifest.yaml")

	tests := []struct {
		name         string
		keywords     []string
		expectedType ProjectType
	}{
		{
			name:         "Detect bot",
			keywords:     []string{"telegram", "bot", "messages"},
			expectedType: ProjectTypeBot,
		},
		{
			name:         "Detect e-commerce",
			keywords:     []string{"ecommerce", "shop", "products"},
			expectedType: ProjectTypeEcommerce,
		},
		{
			name:         "Detect AI agent",
			keywords:     []string{"ai", "agent", "crewai"},
			expectedType: ProjectTypeAIAgent,
		},
		{
			name:         "Detect PWA",
			keywords:     []string{"pwa", "progressive", "web"},
			expectedType: ProjectTypePWA,
		},
		{
			name:         "Detect API (default)",
			keywords:     []string{"rest", "endpoint", "server"},
			expectedType: ProjectTypeAPI,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := analyzer.DetectProjectType(tt.keywords)
			if err != nil {
				t.Fatalf("DetectProjectType failed: %v", err)
			}
			if result != tt.expectedType {
				t.Errorf("DetectProjectType(%v) = %v; want %v", tt.keywords, result, tt.expectedType)
			}
		})
	}
}

func TestDefaultStack(t *testing.T) {
	analyzer := NewAnalyzer("non-existent-manifest.yaml")

	tests := []struct {
		name         string
		projectType  ProjectType
		expectedSize int
	}{
		{
			name:         "PWA stack",
			projectType:  ProjectTypePWA,
			expectedSize: 4,
		},
		{
			name:         "Bot stack",
			projectType:  ProjectTypeBot,
			expectedSize: 3,
		},
		{
			name:         "API stack",
			projectType:  ProjectTypeAPI,
			expectedSize: 4,
		},
		{
			name:         "E-commerce stack",
			projectType:  ProjectTypeEcommerce,
			expectedSize: 4,
		},
		{
			name:         "AI Agent stack",
			projectType:  ProjectTypeAIAgent,
			expectedSize: 4,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			stack, err := analyzer.GetOptimalStack(tt.projectType)
			if err != nil {
				t.Fatalf("GetOptimalStack failed: %v", err)
			}
			if len(stack) != tt.expectedSize {
				t.Errorf("GetOptimalStack(%v) returned %d items; want %d. Stack: %v",
					tt.projectType, len(stack), tt.expectedSize, stack)
			}
		})
	}
}
