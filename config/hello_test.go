// Package config provides configuration functionality for Tokyo-IA.
package config

import "testing"

// TestHello tests the Hello function in the config package.
func TestHello(t *testing.T) {
	expected := "Hello, Tokyo-IA!"
	actual := Hello()
	if actual != expected {
		t.Errorf("Hello() = %q, want %q", actual, expected)
	}
}
