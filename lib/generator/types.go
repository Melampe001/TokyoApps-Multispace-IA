// Package generator provides types and interfaces for the Elite Framework.
package generator

// ProjectType represents the type of project to generate.
type ProjectType string

const (
	ProjectTypePWA       ProjectType = "pwa"
	ProjectTypeBot       ProjectType = "bot"
	ProjectTypeAPI       ProjectType = "api"
	ProjectTypeEcommerce ProjectType = "ecommerce"
	ProjectTypeAIAgent   ProjectType = "ai-agent"
)

// ProjectConfig holds the configuration for a project generation.
type ProjectConfig struct {
	Name        string
	Description string
	Type        ProjectType
	Stack       []string
	OutputDir   string
}

// Template represents a project template definition.
type Template struct {
	Name        string
	Description string
	Stack       []string
	Structure   []string
	Files       []string
}

// TemplateManifest represents the complete templates manifest.
type TemplateManifest struct {
	Templates map[string]Template `yaml:"templates"`
}
