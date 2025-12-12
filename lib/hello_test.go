// Package lib provides library functionality for Tokyo-IA.
package lib

import "testing"

// TestHello tests the Hello function in the lib package.
func TestHello(t *testing.T) {
	expected := "Hello, Tokyo-IA!"
	actual := Hello()
	if actual != expected {
		t.Errorf("Hello() = %q, want %q", actual, expected)
	}
}
