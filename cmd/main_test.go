// Package main provides the entry point for Tokyo-IA.
package main

import (
	"bytes"
	"io"
	"os"
	"testing"
)

// TestMain tests the main function output.
func TestMain(t *testing.T) {
	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Run main
	main()

	// Restore stdout
	w.Close()
	os.Stdout = oldStdout

	// Read captured output
	var buf bytes.Buffer
	io.Copy(&buf, r)
	output := buf.String()

	expected := "Hello, Tokyo-IA!\n"
	if output != expected {
		t.Errorf("main() output = %q, want %q", output, expected)
	}
}
