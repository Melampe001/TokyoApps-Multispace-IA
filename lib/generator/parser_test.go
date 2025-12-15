// Package generator provides tests for the parser.
package generator

import (
	"testing"
)

func TestParseCommand(t *testing.T) {
	parser := NewParser()

	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{
			name:     "Standard PROYECTO format",
			input:    "// PROYECTO: REST API for tasks",
			expected: "REST API for tasks",
		},
		{
			name:     "Without slashes",
			input:    "PROYECTO: Telegram bot",
			expected: "Telegram bot",
		},
		{
			name:     "Plain description",
			input:    "E-commerce platform",
			expected: "E-commerce platform",
		},
		{
			name:     "Case insensitive",
			input:    "// proyecto: Weather app",
			expected: "Weather app",
		},
		{
			name:     "With extra spaces",
			input:    "//  PROYECTO:  PWA application  ",
			expected: "PWA application",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := parser.ParseCommand(tt.input)
			if result != tt.expected {
				t.Errorf("ParseCommand(%q) = %q; want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func TestExtractKeywords(t *testing.T) {
	parser := NewParser()

	tests := []struct {
		name        string
		description string
		minKeywords int
	}{
		{
			name:        "API description",
			description: "REST API for task management",
			minKeywords: 3,
		},
		{
			name:        "Bot description",
			description: "Telegram bot for weather updates",
			minKeywords: 3,
		},
		{
			name:        "Complex description",
			description: "E-commerce platform with Stripe payments and inventory",
			minKeywords: 4,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			keywords := parser.ExtractKeywords(tt.description)
			if len(keywords) < tt.minKeywords {
				t.Errorf("ExtractKeywords(%q) returned %d keywords; want at least %d. Got: %v",
					tt.description, len(keywords), tt.minKeywords, keywords)
			}
		})
	}
}

func TestExtractKeywordsFiltersStopWords(t *testing.T) {
	parser := NewParser()

	description := "the a an and or"
	keywords := parser.ExtractKeywords(description)

	if len(keywords) > 0 {
		t.Errorf("ExtractKeywords should filter all stop words, but got: %v", keywords)
	}
}
