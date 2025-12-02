// Package ai provides tests for the AI module.
package ai

import "testing"

func TestGreet(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{
			name:     "greet user",
			input:    "Usuario",
			expected: "¡Hola, Usuario! Bienvenido a Tokyo-IA.",
		},
		{
			name:     "greet empty string",
			input:    "",
			expected: "¡Hola, ! Bienvenido a Tokyo-IA.",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Greet(tt.input)
			if result != tt.expected {
				t.Errorf("Greet(%q) = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func TestProcess(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{
			name:     "process valid input",
			input:    "test input",
			expected: "Procesando entrada: test input",
		},
		{
			name:     "process empty input",
			input:    "",
			expected: "No se recibió entrada para procesar.",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Process(tt.input)
			if result != tt.expected {
				t.Errorf("Process(%q) = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}

func TestVersion(t *testing.T) {
	expected := "0.1.0"
	result := Version()
	if result != expected {
		t.Errorf("Version() = %q, want %q", result, expected)
	}
}
