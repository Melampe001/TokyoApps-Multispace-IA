// Package generator provides the main project generation orchestration.
package generator

import (
	"fmt"
	"path/filepath"
)

// Generator orchestrates the complete project generation process.
type Generator struct {
	parser      *Parser
	analyzer    *Analyzer
	scaffolder  *Scaffolder
	templater   *Templater
	documenter  *Documenter
	deployer    *Deployer
	manifestPath string
}

// NewGenerator creates a new Generator instance.
func NewGenerator(manifestPath string) *Generator {
	return &Generator{
		parser:       NewParser(),
		analyzer:     NewAnalyzer(manifestPath),
		scaffolder:   NewScaffolder(),
		templater:    NewTemplater(),
		documenter:   NewDocumenter(),
		deployer:     NewDeployer(),
		manifestPath: manifestPath,
	}
}

// Generate creates a complete project from a description.
func (g *Generator) Generate(input, outputDir string) (*ProjectConfig, error) {
	// Parse the command
	description := g.parser.ParseCommand(input)
	if description == "" {
		return nil, fmt.Errorf("empty project description")
	}
	
	// Extract keywords
	keywords := g.parser.ExtractKeywords(description)
	
	// Detect project type
	projectType, err := g.analyzer.DetectProjectType(keywords)
	if err != nil {
		return nil, fmt.Errorf("failed to detect project type: %w", err)
	}
	
	// Get optimal stack
	stack, err := g.analyzer.GetOptimalStack(projectType)
	if err != nil {
		return nil, fmt.Errorf("failed to determine stack: %w", err)
	}
	
	// Generate project name
	projectName := GenerateProjectName(description)
	
	// Create config
	config := &ProjectConfig{
		Name:        projectName,
		Description: description,
		Type:        projectType,
		Stack:       stack,
		OutputDir:   filepath.Join(outputDir, projectName),
	}
	
	// Create directory structure
	err = g.scaffolder.CreateStructure(config)
	if err != nil {
		return nil, fmt.Errorf("failed to create structure: %w", err)
	}
	
	// Generate files
	err = g.generateFiles(config)
	if err != nil {
		return nil, fmt.Errorf("failed to generate files: %w", err)
	}
	
	return config, nil
}

// generateFiles creates all necessary files for the project.
func (g *Generator) generateFiles(config *ProjectConfig) error {
	// Generate README
	readme, err := g.templater.RenderREADME(config)
	if err != nil {
		return fmt.Errorf("failed to generate README: %w", err)
	}
	err = g.scaffolder.CreateFile(config.OutputDir, "README.md", readme)
	if err != nil {
		return err
	}
	
	// Generate Dockerfile
	dockerfile, err := g.templater.RenderDockerfile(config)
	if err != nil {
		return fmt.Errorf("failed to generate Dockerfile: %w", err)
	}
	err = g.scaffolder.CreateFile(config.OutputDir, "Dockerfile", dockerfile)
	if err != nil {
		return err
	}
	
	// Generate GitHub workflow
	workflow, err := g.templater.RenderGitHubWorkflow(config)
	if err != nil {
		return fmt.Errorf("failed to generate workflow: %w", err)
	}
	err = g.scaffolder.CreateFile(config.OutputDir, ".github/workflows/ci.yml", workflow)
	if err != nil {
		return err
	}
	
	// Generate docker-compose
	compose, err := g.deployer.GenerateDockerCompose(config)
	if err != nil {
		return fmt.Errorf("failed to generate docker-compose: %w", err)
	}
	err = g.scaffolder.CreateFile(config.OutputDir, "docker-compose.yml", compose)
	if err != nil {
		return err
	}
	
	// Generate deployment README
	deployREADME, err := g.deployer.GenerateDeploymentREADME(config)
	if err != nil {
		return fmt.Errorf("failed to generate deployment README: %w", err)
	}
	err = g.scaffolder.CreateFile(config.OutputDir, "deploy/README.md", deployREADME)
	if err != nil {
		return err
	}
	
	// Generate architecture docs
	archDocs, err := g.documenter.GenerateArchitectureDocs(config)
	if err != nil {
		return fmt.Errorf("failed to generate architecture docs: %w", err)
	}
	err = g.scaffolder.CreateFile(config.OutputDir, "docs/ARCHITECTURE.md", archDocs)
	if err != nil {
		return err
	}
	
	// Generate API docs (if applicable)
	apiDocs, err := g.documenter.GenerateAPIDoc(config)
	if err != nil {
		return fmt.Errorf("failed to generate API docs: %w", err)
	}
	if apiDocs != "" {
		err = g.scaffolder.CreateFile(config.OutputDir, "docs/API.md", apiDocs)
		if err != nil {
			return err
		}
	}
	
	// Generate contributing guide
	contributing, err := g.documenter.GenerateContributingGuide(config)
	if err != nil {
		return fmt.Errorf("failed to generate contributing guide: %w", err)
	}
	err = g.scaffolder.CreateFile(config.OutputDir, "CONTRIBUTING.md", contributing)
	if err != nil {
		return err
	}
	
	// Generate LICENSE
	license := g.documenter.GenerateLicense()
	err = g.scaffolder.CreateFile(config.OutputDir, "LICENSE", license)
	if err != nil {
		return err
	}
	
	// Generate .gitignore
	gitignore := g.generateGitignore(config)
	err = g.scaffolder.CreateFile(config.OutputDir, ".gitignore", gitignore)
	if err != nil {
		return err
	}
	
	// Generate project-specific files
	err = g.generateProjectSpecificFiles(config)
	if err != nil {
		return fmt.Errorf("failed to generate project-specific files: %w", err)
	}
	
	return nil
}

// generateGitignore creates a .gitignore file.
func (g *Generator) generateGitignore(config *ProjectConfig) string {
	var ignore string
	
	switch config.Type {
	case ProjectTypePWA, ProjectTypeEcommerce:
		ignore = `node_modules/
dist/
.env
.env.local
*.log
.DS_Store
coverage/
.next/
out/
build/
`
	
	case ProjectTypeBot, ProjectTypeAIAgent:
		ignore = `__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.env
venv/
env/
*.log
.pytest_cache/
.coverage
htmlcov/
`
	
	case ProjectTypeAPI:
		ignore = `bin/
*.exe
*.dll
*.so
*.dylib
*.test
*.out
.env
.env.local
*.log
coverage.txt
vendor/
`
	}
	
	return ignore
}

// generateProjectSpecificFiles creates files specific to each project type.
func (g *Generator) generateProjectSpecificFiles(config *ProjectConfig) error {
	switch config.Type {
	case ProjectTypePWA:
		return g.generatePWAFiles(config)
	case ProjectTypeBot:
		return g.generateBotFiles(config)
	case ProjectTypeAPI:
		return g.generateAPIFiles(config)
	case ProjectTypeEcommerce:
		return g.generateEcommerceFiles(config)
	case ProjectTypeAIAgent:
		return g.generateAIAgentFiles(config)
	}
	return nil
}

// generatePWAFiles creates PWA-specific files.
func (g *Generator) generatePWAFiles(config *ProjectConfig) error {
	// package.json
	packageJSON := `{
  "name": "` + config.Name + `",
  "version": "1.0.0",
  "description": "` + config.Description + `",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "vitest": "^1.0.0"
  }
}
`
	err := g.scaffolder.CreateFile(config.OutputDir, "package.json", packageJSON)
	if err != nil {
		return err
	}
	
	// vite.config.js
	viteConfig := `import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
`
	err = g.scaffolder.CreateFile(config.OutputDir, "vite.config.js", viteConfig)
	if err != nil {
		return err
	}
	
	// src/main.jsx
	mainJSX := `import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
`
	err = g.scaffolder.CreateFile(config.OutputDir, "src/main.jsx", mainJSX)
	if err != nil {
		return err
	}
	
	// src/App.jsx
	appJSX := `import React from 'react'

function App() {
  return (
    <div>
      <h1>` + config.Name + `</h1>
      <p>` + config.Description + `</p>
    </div>
  )
}

export default App
`
	err = g.scaffolder.CreateFile(config.OutputDir, "src/App.jsx", appJSX)
	if err != nil {
		return err
	}
	
	// index.html
	indexHTML := `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>` + config.Name + `</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
`
	return g.scaffolder.CreateFile(config.OutputDir, "index.html", indexHTML)
}

// generateBotFiles creates bot-specific files.
func (g *Generator) generateBotFiles(config *ProjectConfig) error {
	// requirements.txt
	requirements := `python-telegram-bot>=20.0
python-dotenv>=1.0.0
aiohttp>=3.9.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
`
	err := g.scaffolder.CreateFile(config.OutputDir, "requirements.txt", requirements)
	if err != nil {
		return err
	}
	
	// main.py
	mainPy := `import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hello! I am ` + config.Name + `')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await update.message.reply_text('Help!')

def main():
    """Start the bot."""
    token = os.getenv('BOT_TOKEN')
    if not token:
        raise ValueError('BOT_TOKEN environment variable is not set')
    
    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    application.run_polling()

if __name__ == '__main__':
    main()
`
	err = g.scaffolder.CreateFile(config.OutputDir, "main.py", mainPy)
	if err != nil {
		return err
	}
	
	// .env.example
	envExample := `BOT_TOKEN=your_bot_token_here
`
	return g.scaffolder.CreateFile(config.OutputDir, ".env.example", envExample)
}

// generateAPIFiles creates API-specific files.
func (g *Generator) generateAPIFiles(config *ProjectConfig) error {
	// go.mod
	goMod := `module ` + config.Name + `

go 1.21

require (
	github.com/gin-gonic/gin v1.9.1
	gorm.io/gorm v1.25.5
	gorm.io/driver/postgres v1.5.4
)
`
	err := g.scaffolder.CreateFile(config.OutputDir, "go.mod", goMod)
	if err != nil {
		return err
	}
	
	// cmd/api/main.go
	mainGo := `package main

import (
	"log"
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	
	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"status": "ok",
		})
	})
	
	r.GET("/api/items", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"data": []string{},
		})
	})
	
	if err := r.Run(":8080"); err != nil {
		log.Fatal(err)
	}
}
`
	return g.scaffolder.CreateFile(config.OutputDir, "cmd/api/main.go", mainGo)
}

// generateEcommerceFiles creates e-commerce-specific files.
func (g *Generator) generateEcommerceFiles(config *ProjectConfig) error {
	// package.json
	packageJSON := `{
  "name": "` + config.Name + `",
  "version": "1.0.0",
  "description": "` + config.Description + `",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "test": "jest"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@stripe/stripe-js": "^2.0.0",
    "@prisma/client": "^5.0.0"
  },
  "devDependencies": {
    "prisma": "^5.0.0",
    "typescript": "^5.0.0"
  }
}
`
	err := g.scaffolder.CreateFile(config.OutputDir, "package.json", packageJSON)
	if err != nil {
		return err
	}
	
	// app/page.tsx
	pageTSX := `export default function Home() {
  return (
    <main>
      <h1>` + config.Name + `</h1>
      <p>` + config.Description + `</p>
    </main>
  )
}
`
	err = g.scaffolder.CreateFile(config.OutputDir, "app/page.tsx", pageTSX)
	if err != nil {
		return err
	}
	
	// .env.example
	envExample := `DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
`
	return g.scaffolder.CreateFile(config.OutputDir, ".env.example", envExample)
}

// generateAIAgentFiles creates AI agent-specific files.
func (g *Generator) generateAIAgentFiles(config *ProjectConfig) error {
	// requirements.txt
	requirements := `crewai>=0.1.0
groq>=0.4.0
langchain>=0.1.0
python-dotenv>=1.0.0
pytest>=7.4.0
`
	err := g.scaffolder.CreateFile(config.OutputDir, "requirements.txt", requirements)
	if err != nil {
		return err
	}
	
	// main.py
	mainPy := `import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

load_dotenv()

def main():
    # Define your agent
    agent = Agent(
        role='Assistant',
        goal='Help users with their tasks',
        backstory='An AI assistant powered by ` + config.Name + `',
        verbose=True
    )
    
    # Define a task
    task = Task(
        description='Analyze the given input and provide helpful response',
        agent=agent
    )
    
    # Create crew
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )
    
    # Execute
    result = crew.kickoff()
    print(result)

if __name__ == '__main__':
    main()
`
	err = g.scaffolder.CreateFile(config.OutputDir, "main.py", mainPy)
	if err != nil {
		return err
	}
	
	// .env.example
	envExample := `GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
`
	return g.scaffolder.CreateFile(config.OutputDir, ".env.example", envExample)
}
