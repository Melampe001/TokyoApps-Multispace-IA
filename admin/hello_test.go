// Package admin provides admin functionality for Tokyo-IA.
package admin

import "testing"

// TestHello tests the Hello function in the admin package.
func TestHello(t *testing.T) {
	expected := "Hello, Tokyo-IA!"
	actual := Hello()
	if actual != expected {
		t.Errorf("Hello() = %q, want %q", actual, expected)
	}
}
