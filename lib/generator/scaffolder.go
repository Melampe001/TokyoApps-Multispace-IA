// Package generator provides scaffolding functionality for project generation.
package generator

import (
	"fmt"
	"os"
	"path/filepath"
)

// Scaffolder handles creation of project directory structures.
type Scaffolder struct{}

// NewScaffolder creates a new Scaffolder instance.
func NewScaffolder() *Scaffolder {
	return &Scaffolder{}
}

// CreateStructure creates the complete directory structure for a project.
func (s *Scaffolder) CreateStructure(config *ProjectConfig) error {
	// Create output directory
	err := os.MkdirAll(config.OutputDir, 0755)
	if err != nil {
		return fmt.Errorf("failed to create output directory: %w", err)
	}
	
	// Get directory structure based on project type
	dirs := s.getDirectories(config.Type)
	
	// Create each directory
	for _, dir := range dirs {
		path := filepath.Join(config.OutputDir, dir)
		err := os.MkdirAll(path, 0755)
		if err != nil {
			return fmt.Errorf("failed to create directory %s: %w", dir, err)
		}
	}
	
	return nil
}

// getDirectories returns the directory structure for a project type.
func (s *Scaffolder) getDirectories(projectType ProjectType) []string {
	switch projectType {
	case ProjectTypePWA:
		return []string{
			"src",
			"src/components",
			"src/pages",
			"src/styles",
			"src/utils",
			"public",
			"tests",
			"tests/unit",
			"tests/e2e",
			"deploy",
			"docs",
		}
	
	case ProjectTypeBot:
		return []string{
			"bot",
			"bot/handlers",
			"bot/commands",
			"handlers",
			"services",
			"utils",
			"tests",
			"tests/unit",
			"tests/integration",
			"deploy",
			"docs",
		}
	
	case ProjectTypeAPI:
		return []string{
			"cmd",
			"cmd/api",
			"internal",
			"internal/handler",
			"internal/service",
			"internal/repository",
			"api",
			"models",
			"config",
			"tests",
			"tests/unit",
			"tests/integration",
			"deploy",
			"docs",
		}
	
	case ProjectTypeEcommerce:
		return []string{
			"app",
			"app/(auth)",
			"app/(shop)",
			"app/admin",
			"components",
			"components/ui",
			"lib",
			"api",
			"prisma",
			"public",
			"tests",
			"tests/unit",
			"tests/e2e",
			"deploy",
			"docs",
		}
	
	case ProjectTypeAIAgent:
		return []string{
			"agents",
			"tools",
			"tasks",
			"config",
			"utils",
			"tests",
			"tests/unit",
			"tests/integration",
			"deploy",
			"docs",
		}
	
	default:
		return []string{
			"src",
			"tests",
			"deploy",
			"docs",
		}
	}
}

// CreateFile creates a file with the given content at the specified path.
func (s *Scaffolder) CreateFile(basePath, relativePath, content string) error {
	fullPath := filepath.Join(basePath, relativePath)
	
	// Ensure directory exists
	dir := filepath.Dir(fullPath)
	err := os.MkdirAll(dir, 0755)
	if err != nil {
		return fmt.Errorf("failed to create directory for file %s: %w", relativePath, err)
	}
	
	// Write file
	err = os.WriteFile(fullPath, []byte(content), 0644)
	if err != nil {
		return fmt.Errorf("failed to write file %s: %w", relativePath, err)
	}
	
	return nil
}

// GetProjectName generates a project name from the description.
func (s *Scaffolder) GetProjectName(description string) string {
	// Simple slug generation
	name := description
	name = filepath.Base(name) // Remove any path separators
	
	// Convert to lowercase and replace spaces with hyphens
	name = filepath.Clean(name)
	
	// If name is too long, truncate
	if len(name) > 50 {
		name = name[:50]
	}
	
	return name
}
