// Package generator provides tests for the scaffolder.
package generator

import (
	"os"
	"path/filepath"
	"testing"
)

func TestCreateStructure(t *testing.T) {
	scaffolder := NewScaffolder()
	
	// Create temporary directory
	tmpDir := t.TempDir()
	
	config := &ProjectConfig{
		Name:        "test-project",
		Description: "Test project",
		Type:        ProjectTypeAPI,
		OutputDir:   filepath.Join(tmpDir, "test-project"),
	}
	
	err := scaffolder.CreateStructure(config)
	if err != nil {
		t.Fatalf("CreateStructure failed: %v", err)
	}
	
	// Verify output directory exists
	if _, err := os.Stat(config.OutputDir); os.IsNotExist(err) {
		t.Errorf("Output directory was not created: %s", config.OutputDir)
	}
	
	// Verify some expected directories exist
	expectedDirs := []string{"cmd", "internal", "tests", "deploy", "docs"}
	for _, dir := range expectedDirs {
		dirPath := filepath.Join(config.OutputDir, dir)
		if _, err := os.Stat(dirPath); os.IsNotExist(err) {
			t.Errorf("Expected directory does not exist: %s", dirPath)
		}
	}
}

func TestGetProjectName(t *testing.T) {
	scaffolder := NewScaffolder()
	
	tests := []struct {
		name        string
		description string
		maxLength   int
	}{
		{
			name:        "Simple description",
			description: "My Test Project",
			maxLength:   50,
		},
		{
			name:        "Long description",
			description: "This is a very long project description that should be truncated to fit within reasonable limits",
			maxLength:   50,
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := scaffolder.GetProjectName(tt.description)
			if result == "" {
				t.Error("GetProjectName returned empty string")
			}
			if len(result) > tt.maxLength {
				t.Errorf("GetProjectName(%q) returned name with length %d; want <= %d",
					tt.description, len(result), tt.maxLength)
			}
		})
	}
}

func TestCreateFile(t *testing.T) {
	scaffolder := NewScaffolder()
	tmpDir := t.TempDir()
	
	content := "test content"
	relativePath := "subdir/test.txt"
	
	err := scaffolder.CreateFile(tmpDir, relativePath, content)
	if err != nil {
		t.Fatalf("CreateFile failed: %v", err)
	}
	
	// Verify file exists
	fullPath := filepath.Join(tmpDir, relativePath)
	if _, err := os.Stat(fullPath); os.IsNotExist(err) {
		t.Errorf("File was not created: %s", fullPath)
	}
	
	// Verify content
	data, err := os.ReadFile(fullPath)
	if err != nil {
		t.Fatalf("Failed to read created file: %v", err)
	}
	
	if string(data) != content {
		t.Errorf("File content = %q; want %q", string(data), content)
	}
}
