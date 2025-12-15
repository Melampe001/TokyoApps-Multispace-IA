// Package generator provides template rendering functionality.
package generator

import (
	"bytes"
	"fmt"
	"text/template"
	"time"
)

// Templater handles rendering of project templates.
type Templater struct{}

// NewTemplater creates a new Templater instance.
func NewTemplater() *Templater {
	return &Templater{}
}

// TemplateData holds data for template rendering.
type TemplateData struct {
	ProjectName string
	Description string
	Type        string
	Stack       []string
	Year        int
}

// RenderREADME generates a README.md file for the project.
func (t *Templater) RenderREADME(config *ProjectConfig) (string, error) {
	tmpl := `# {{.ProjectName}}

{{.Description}}

## Technology Stack

{{range .Stack}}- {{.}}
{{end}}

## Getting Started

### Prerequisites

{{if eq .Type "pwa"}}
- Node.js 18+
- npm or yarn
{{else if eq .Type "bot"}}
- Python 3.9+
- pip
{{else if eq .Type "api"}}
- Go 1.21+
{{else if eq .Type "ecommerce"}}
- Node.js 18+
- PostgreSQL
- npm or yarn
{{else if eq .Type "ai-agent"}}
- Python 3.9+
- pip
- API keys (OpenAI, Groq, etc.)
{{end}}

### Installation

{{if eq .Type "pwa"}}
` + "```bash" + `
npm install
npm run dev
` + "```" + `
{{else if eq .Type "bot"}}
` + "```bash" + `
pip install -r requirements.txt
python main.py
` + "```" + `
{{else if eq .Type "api"}}
` + "```bash" + `
go mod download
go run cmd/api/main.go
` + "```" + `
{{else if eq .Type "ecommerce"}}
` + "```bash" + `
npm install
npm run dev
` + "```" + `
{{else if eq .Type "ai-agent"}}
` + "```bash" + `
pip install -r requirements.txt
python main.py
` + "```" + `
{{end}}

## Project Structure

Generated with Tokyo-IA Elite Framework.

## Testing

{{if eq .Type "pwa"}}
` + "```bash" + `
npm test
npm run test:e2e
` + "```" + `
{{else if eq .Type "bot"}}
` + "```bash" + `
pytest
` + "```" + `
{{else if eq .Type "api"}}
` + "```bash" + `
go test ./...
` + "```" + `
{{else if eq .Type "ecommerce"}}
` + "```bash" + `
npm test
npm run test:e2e
` + "```" + `
{{else if eq .Type "ai-agent"}}
` + "```bash" + `
pytest
` + "```" + `
{{end}}

## Deployment

See [deploy/README.md](deploy/README.md) for deployment instructions.

## License

MIT License - Copyright (c) {{.Year}}
`

	data := TemplateData{
		ProjectName: config.Name,
		Description: config.Description,
		Type:        string(config.Type),
		Stack:       config.Stack,
		Year:        time.Now().Year(),
	}

	return t.render(tmpl, data)
}

// RenderDockerfile generates a Dockerfile for the project.
func (t *Templater) RenderDockerfile(config *ProjectConfig) (string, error) {
	var tmpl string
	
	switch config.Type {
	case ProjectTypePWA:
		tmpl = `FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
`
	
	case ProjectTypeBot, ProjectTypeAIAgent:
		tmpl = `FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
`
	
	case ProjectTypeAPI:
		tmpl = `FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app/server ./cmd/api

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/server .
EXPOSE 8080
CMD ["./server"]
`
	
	case ProjectTypeEcommerce:
		tmpl = `FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
EXPOSE 3000
CMD ["npm", "start"]
`
	}
	
	return tmpl, nil
}

// RenderGitHubWorkflow generates a CI/CD workflow file.
func (t *Templater) RenderGitHubWorkflow(config *ProjectConfig) (string, error) {
	tmpl := `name: CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
{{if eq .Type "pwa" "ecommerce"}}
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm test
    
    - name: Build
      run: npm run build
{{else if eq .Type "bot" "ai-agent"}}
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest
    
    - name: Run tests
      run: pytest
{{else if eq .Type "api"}}
    - name: Setup Go
      uses: actions/setup-go@v4
      with:
        go-version: '1.21'
    
    - name: Install dependencies
      run: go mod download
    
    - name: Run tests
      run: go test ./...
    
    - name: Build
      run: go build ./cmd/api
{{end}}
`

	data := TemplateData{
		Type: string(config.Type),
	}

	return t.render(tmpl, data)
}

// render executes a template with the given data.
func (t *Templater) render(tmplStr string, data interface{}) (string, error) {
	tmpl, err := template.New("template").Parse(tmplStr)
	if err != nil {
		return "", fmt.Errorf("failed to parse template: %w", err)
	}
	
	var buf bytes.Buffer
	err = tmpl.Execute(&buf, data)
	if err != nil {
		return "", fmt.Errorf("failed to execute template: %w", err)
	}
	
	return buf.String(), nil
}
