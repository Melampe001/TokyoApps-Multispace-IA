// Package generator provides documentation generation functionality.
package generator

import (
	"fmt"
	"strings"
	"time"
)

// Documenter handles generation of project documentation.
type Documenter struct{}

// NewDocumenter creates a new Documenter instance.
func NewDocumenter() *Documenter {
	return &Documenter{}
}

// GenerateArchitectureDocs creates architecture documentation with Mermaid diagrams.
func (d *Documenter) GenerateArchitectureDocs(config *ProjectConfig) (string, error) {
	var diagram string

	switch config.Type {
	case ProjectTypePWA:
		diagram = `# Architecture

## System Overview

` + "```mermaid" + `
graph TD
    A[User Browser] --> B[React App]
    B --> C[Service Worker]
    C --> D[Cache Storage]
    B --> E[API Backend]
    E --> F[Database]
` + "```" + `

## Components

- **React App**: Main application interface
- **Service Worker**: Offline support and caching
- **API Backend**: RESTful API services
- **Cache Storage**: Local data persistence
`

	case ProjectTypeBot:
		diagram = `# Architecture

## System Overview

` + "```mermaid" + `
graph TD
    A[Bot Platform] --> B[Bot Handler]
    B --> C[Command Router]
    C --> D[Service Layer]
    D --> E[External APIs]
    D --> F[Database]
` + "```" + `

## Components

- **Bot Handler**: Manages incoming messages
- **Command Router**: Dispatches commands to handlers
- **Service Layer**: Business logic
- **External APIs**: Third-party integrations
`

	case ProjectTypeAPI:
		diagram = `# Architecture

## System Overview

` + "```mermaid" + `
graph TD
    A[Client] --> B[API Gateway]
    B --> C[Handler Layer]
    C --> D[Service Layer]
    D --> E[Repository Layer]
    E --> F[Database]
` + "```" + `

## Components

- **API Gateway**: Request routing and middleware
- **Handler Layer**: HTTP request handling
- **Service Layer**: Business logic
- **Repository Layer**: Data access
`

	case ProjectTypeEcommerce:
		diagram = `# Architecture

## System Overview

` + "```mermaid" + `
graph TD
    A[User] --> B[Next.js Frontend]
    B --> C[API Routes]
    C --> D[Payment Gateway]
    C --> E[Database]
    C --> F[Email Service]
` + "```" + `

## Components

- **Next.js Frontend**: Server-side rendered UI
- **API Routes**: Backend API endpoints
- **Payment Gateway**: Stripe integration
- **Database**: Product and order data
- **Email Service**: Order notifications
`

	case ProjectTypeAIAgent:
		diagram = `# Architecture

## System Overview

` + "```mermaid" + `
graph TD
    A[User Input] --> B[Agent Orchestrator]
    B --> C[Task Planner]
    C --> D[Tool Executor]
    D --> E[LLM API]
    D --> F[Custom Tools]
    B --> G[Memory Store]
` + "```" + `

## Components

- **Agent Orchestrator**: Manages agent lifecycle
- **Task Planner**: Breaks down tasks
- **Tool Executor**: Runs tools and actions
- **LLM API**: Language model integration
- **Custom Tools**: Domain-specific utilities
`
	}

	return diagram, nil
}

// GenerateAPIDoc creates API documentation.
func (d *Documenter) GenerateAPIDoc(config *ProjectConfig) (string, error) {
	if config.Type != ProjectTypeAPI && config.Type != ProjectTypeEcommerce {
		return "", nil
	}

	doc := `# API Documentation

## Base URL

` + "```" + `
http://localhost:8080
` + "```" + `

## Authentication

All API requests require authentication using Bearer tokens.

` + "```http" + `
Authorization: Bearer <token>
` + "```" + `

## Endpoints

### Health Check

` + "```http" + `
GET /health
` + "```" + `

**Response:**
` + "```json" + `
{
  "status": "ok",
  "timestamp": "2024-01-01T00:00:00Z"
}
` + "```" + `

### List Items

` + "```http" + `
GET /api/items
` + "```" + `

**Parameters:**
- ` + "`page`" + ` (optional): Page number
- ` + "`limit`" + ` (optional): Items per page

**Response:**
` + "```json" + `
{
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100
  }
}
` + "```" + `

### Create Item

` + "```http" + `
POST /api/items
` + "```" + `

**Request Body:**
` + "```json" + `
{
  "name": "Item name",
  "description": "Item description"
}
` + "```" + `

**Response:**
` + "```json" + `
{
  "id": "123",
  "name": "Item name",
  "description": "Item description",
  "createdAt": "2024-01-01T00:00:00Z"
}
` + "```" + `

## Error Handling

All errors follow this format:

` + "```json" + `
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message"
  }
}
` + "```" + `

## Rate Limiting

- 100 requests per minute per IP
- 1000 requests per hour per user
`

	return doc, nil
}

// GenerateContributingGuide creates contributing guidelines.
func (d *Documenter) GenerateContributingGuide(config *ProjectConfig) (string, error) {
	guide := fmt.Sprintf(`# Contributing to %s

Thank you for your interest in contributing!

## Development Setup

1. Clone the repository
2. Follow the installation instructions in README.md
3. Create a new branch for your feature

## Code Style

`, config.Name)

	// Add language-specific style guidelines
	if contains(config.Stack, "go") {
		guide += `### Go
- Follow the official Go style guide
- Run ` + "`go fmt`" + ` before committing
- Ensure all tests pass with ` + "`go test ./...`" + `

`
	}

	if contains(config.Stack, "python") {
		guide += `### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Run ` + "`black`" + ` formatter before committing
- Ensure all tests pass with ` + "`pytest`" + `

`
	}

	if contains(config.Stack, "typescript") || contains(config.Stack, "javascript") {
		guide += `### TypeScript/JavaScript
- Follow ESLint rules
- Use Prettier for formatting
- Ensure all tests pass with ` + "`npm test`" + `

`
	}

	guide += `## Pull Request Process

1. Update documentation for any changed functionality
2. Add tests for new features
3. Ensure all tests pass
4. Update the README.md if needed
5. Submit a pull request with a clear description

## Testing

- Write unit tests for new code
- Maintain test coverage above 80%
- Include integration tests for API endpoints

## Documentation

- Update API documentation for endpoint changes
- Add code comments for complex logic
- Update README for new features

## Questions?

Feel free to open an issue for any questions or concerns.
`

	return guide, nil
}

// GenerateLicense creates a MIT license file.
func (d *Documenter) GenerateLicense() string {
	year := time.Now().Year()
	return fmt.Sprintf(`MIT License

Copyright (c) %d

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
`, year)
}

// contains checks if a slice contains a string.
func contains(slice []string, item string) bool {
	for _, s := range slice {
		if strings.EqualFold(s, item) {
			return true
		}
	}
	return false
}
