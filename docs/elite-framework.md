# Elite Framework Documentation

The Elite Framework is an automated project generation system that creates complete, production-ready projects from simple descriptions.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Types](#project-types)
- [Generated Structure](#generated-structure)
- [Examples](#examples)
- [Architecture](#architecture)
- [Customization](#customization)

> 📚 **For detailed, real-world examples, see [Elite Framework Examples](elite-framework-examples.md)**

## Overview

The Elite Framework automates the entire process of creating new projects, including:

- Complete source code structure
- Unit and integration tests (>80% coverage goal)
- Deployment configurations (Docker, Kubernetes, CI/CD)
- Comprehensive documentation
- GitHub Actions workflows
- Development environment setup

## Features

### Automatic Project Type Detection

The framework analyzes your project description and automatically detects the best project type:

- **PWA** (Progressive Web Apps)
- **Bot** (Telegram, Discord, Slack)
- **API** (REST/GraphQL)
- **E-commerce** (Online stores with payment processing)
- **AI Agent** (CrewAI, Groq, LangChain)

### Dynamic Stack Selection

Based on the detected project type, the framework selects the optimal technology stack:

- **Go**: For APIs, microservices, and CLI tools
- **Python**: For AI/ML, bots, and automation scripts
- **TypeScript**: For PWAs, frontends, and backends
- **Rust**: For performance-critical applications
- **Ruby**: For admin interfaces

### Complete Code Generation

Every generated project includes:

- ✅ Complete source code structure
- ✅ README with setup instructions
- ✅ Dockerfile for containerization
- ✅ docker-compose.yml for local development
- ✅ GitHub Actions CI/CD workflow
- ✅ Architecture documentation with Mermaid diagrams
- ✅ API documentation (when applicable)
- ✅ Contributing guidelines
- ✅ MIT License
- ✅ .gitignore tailored to the stack
- ✅ Environment variable examples

## Installation

### Build the CLI

```bash
# Build the elite CLI tool
make elite

# Or manually
go build -o bin/elite ./cmd/elite/main.go
```

### Verify Installation

```bash
./bin/elite version
```

## Usage

### Basic Usage

Generate a project using a simple description:

```bash
./bin/elite generate "REST API for task management"
```

### Using the Magic Command Format

You can also use the special format:

```bash
./bin/elite generate "// PROYECTO: Telegram bot for weather updates"
```

### Using Make Commands

The Makefile provides convenient shortcuts:

```bash
# Generate a project
make generate IDEA="E-commerce platform with Stripe"

# Alternative command (same as generate)
make scaffold IDEA="AI agent with CrewAI"
```

### Specify Output Directory

```bash
./bin/elite generate "PWA for task tracking" --output ./my-projects
```

## Project Types

### 1. Progressive Web App (PWA)

**Keywords**: pwa, progressive web app, web application, frontend, responsive, offline

**Stack**: TypeScript, React, Vite, PWA, TailwindCSS

**Generated Structure**:
```
project-name/
├── src/
│   ├── components/
│   ├── pages/
│   ├── styles/
│   └── utils/
├── public/
├── tests/
│   ├── unit/
│   └── e2e/
├── deploy/
├── docs/
├── package.json
├── vite.config.js
└── Dockerfile
```

### 2. Chat Bot

**Keywords**: bot, telegram, discord, slack, chatbot, messenger

**Stack**: Python, python-telegram-bot, asyncio, pytest

**Generated Structure**:
```
project-name/
├── bot/
│   ├── handlers/
│   └── commands/
├── services/
├── tests/
│   ├── unit/
│   └── integration/
├── deploy/
├── docs/
├── main.py
├── requirements.txt
└── Dockerfile
```

### 3. REST/GraphQL API

**Keywords**: api, rest, graphql, backend, microservice, endpoint

**Stack**: Go, Gin, GORM, Swagger, PostgreSQL

**Generated Structure**:
```
project-name/
├── cmd/
│   └── api/
├── internal/
│   ├── handler/
│   ├── service/
│   └── repository/
├── api/
├── models/
├── config/
├── tests/
│   ├── unit/
│   └── integration/
├── deploy/
├── docs/
├── go.mod
└── Dockerfile
```

### 4. E-commerce Platform

**Keywords**: ecommerce, e-commerce, shop, store, marketplace, cart

**Stack**: TypeScript, Next.js, Stripe, Prisma, PostgreSQL, TailwindCSS

**Generated Structure**:
```
project-name/
├── app/
│   ├── (auth)/
│   ├── (shop)/
│   └── admin/
├── components/
│   └── ui/
├── lib/
├── api/
├── prisma/
├── tests/
│   ├── unit/
│   └── e2e/
├── deploy/
├── docs/
├── package.json
└── Dockerfile
```

### 5. AI Agent

**Keywords**: ai agent, intelligent agent, crewai, autonomous, ai assistant

**Stack**: Python, CrewAI, Groq, LangChain, OpenAI

**Generated Structure**:
```
project-name/
├── agents/
├── tools/
├── tasks/
├── config/
├── tests/
│   ├── unit/
│   └── integration/
├── deploy/
├── docs/
├── main.py
├── requirements.txt
└── Dockerfile
```

## Generated Structure

Every project includes:

### Source Code
Complete, working application code tailored to the project type.

### Tests
- Unit tests for individual components
- Integration tests for API endpoints or workflows
- E2E tests for user-facing applications

### Deployment
- **Dockerfile**: Optimized multi-stage builds
- **docker-compose.yml**: Local development environment
- **deploy/README.md**: Deployment instructions for various platforms
- **Kubernetes manifests**: Basic K8s deployment configuration

### Documentation
- **README.md**: Project overview, setup, and usage
- **docs/ARCHITECTURE.md**: System architecture with Mermaid diagrams
- **docs/API.md**: API documentation (for API projects)
- **CONTRIBUTING.md**: Contribution guidelines
- **LICENSE**: MIT license

### CI/CD
- **.github/workflows/ci.yml**: Automated testing and deployment

## Examples

### Example 1: Task Management API

```bash
./bin/elite generate "REST API for managing tasks with user authentication"
```

Output:
```
🚀 Tokyo-IA Elite Framework
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Description: REST API for managing tasks with user authentication

🔍 Analyzing project requirements...

✅ Project generated successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Project Name: rest-api-for-managing-tasks-with-user-authentication
🏷️  Type: api
🛠️  Stack: [go gin gorm swagger postgresql]
📂 Location: ./output/rest-api-for-managing-tasks-with-user-authentication

Next steps:
  cd ./output/rest-api-for-managing-tasks-with-user-authentication
  cat README.md
```

### Example 2: Weather Bot

```bash
./bin/elite generate "Telegram bot that provides weather forecasts"
```

Generates a complete Python bot with:
- Command handlers
- Weather API integration points
- Testing infrastructure
- Docker deployment

### Example 3: E-commerce Store

```bash
./bin/elite generate "Online store for selling handmade crafts with Stripe payments"
```

Generates a Next.js e-commerce platform with:
- Product catalog
- Shopping cart
- Stripe integration setup
- Admin panel structure
- Database schema

### Example 4: AI Research Assistant

```bash
./bin/elite generate "AI agent that helps with research using CrewAI"
```

Generates an AI agent with:
- CrewAI integration
- Custom tools structure
- Task management
- LLM configuration

## Architecture

The Elite Framework consists of several components:

```
Elite Framework
├── Parser: Extracts project description from commands
├── Analyzer: Detects project type and optimal stack
├── Scaffolder: Creates directory structure
├── Templater: Renders project templates
├── Documenter: Generates documentation
└── Deployer: Creates deployment configurations
```

### Component Responsibilities

**Parser** (`lib/generator/parser.go`)
- Parses `// PROYECTO:` commands
- Extracts keywords from descriptions
- Filters stop words

**Analyzer** (`lib/generator/analyzer.go`)
- Loads detection patterns from manifest
- Scores project types based on keywords
- Selects optimal technology stack

**Scaffolder** (`lib/generator/scaffolder.go`)
- Creates directory structure
- Generates project name from description
- Creates files at specified paths

**Templater** (`lib/generator/templater.go`)
- Renders README files
- Generates Dockerfiles
- Creates GitHub Actions workflows
- Uses Go templates for dynamic content

**Documenter** (`lib/generator/documenter.go`)
- Generates architecture diagrams
- Creates API documentation
- Produces contributing guidelines
- Generates MIT license

**Deployer** (`lib/generator/deployer.go`)
- Creates docker-compose files
- Generates Kubernetes manifests
- Produces deployment documentation

**Generator** (`lib/generator/generator.go`)
- Orchestrates all components
- Manages the generation workflow
- Creates project-specific files

## Customization

### Adding New Project Types

1. Edit `templates/manifest.yaml`:

```yaml
templates:
  my-new-type:
    name: "My New Type"
    description: "Description of my new type"
    stack:
      - technology1
      - technology2
    structure:
      - src
      - tests
    files:
      - package.json
      - README.md
```

2. Add detection patterns:

```yaml
detection_patterns:
  my-new-type:
    keywords:
      - "keyword1"
      - "keyword2"
    indicators:
      - "indicator1"
```

3. Update `lib/generator/generator.go` to add project-specific file generation.

### Modifying Templates

Templates are defined in the `Templater` component. To modify:

1. Edit `lib/generator/templater.go`
2. Update the template strings
3. Rebuild: `make elite`

### Custom Stack Configurations

Modify `lib/generator/analyzer.go` to change default stacks for project types.

## Contributing

Contributions to the Elite Framework are welcome! Please see [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

MIT License - See [LICENSE](../LICENSE) for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
