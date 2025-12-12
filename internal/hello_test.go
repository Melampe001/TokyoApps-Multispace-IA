// Package internal provides internal functionality for Tokyo-IA.
package internal

import "testing"

// TestHello tests the Hello function in the internal package.
func TestHello(t *testing.T) {
	expected := "Hello, Tokyo-IA!"
	actual := Hello()
	if actual != expected {
		t.Errorf("Hello() = %q, want %q", actual, expected)
	}
}
