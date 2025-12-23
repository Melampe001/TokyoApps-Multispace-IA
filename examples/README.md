# Tokyo-IA Examples

This directory contains examples and demonstrations of the Tokyo-IA framework capabilities.

## Quick Start Guide

**[QUICKSTART.md](QUICKSTART.md)** - Get started with the Elite Framework in minutes

Learn how to:
- Build and use the Elite Framework CLI
- Generate your first project
- Understand supported project types
- Customize generated projects
- Troubleshoot common issues

Perfect for: First-time users who want to quickly generate a project

## Python Examples

**[python/](python/)** - Python-specific examples and utilities

Contains:
- Python agent implementations
- Orchestration examples
- Integration examples

## Orchestration Demo

**[orchestration_demo.py](orchestration_demo.py)** - Multi-agent orchestration demonstration

Shows how to:
- Coordinate multiple AI agents
- Handle complex workflows
- Track agent interactions
- Manage agent tasks

## Related Documentation

For more comprehensive documentation, see:

- [Elite Framework Examples](../docs/ELITE_FRAMEWORK_EXAMPLES.md) - Detailed examples with all project types
- [Main README](../README.md) - Complete project overview
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute
- [Implementation Summary](../IMPLEMENTATION_SUMMARY.md) - What's been built

## Available Project Types

The Elite Framework can generate these project types:

| Type | Description | Stack |
|------|-------------|-------|
| **API** | REST/GraphQL APIs | Go, Gin, GORM, PostgreSQL |
| **Bot** | Chat bots | Python, python-telegram-bot |
| **PWA** | Progressive Web Apps | TypeScript, React, Vite |
| **E-commerce** | Online stores | Next.js, Stripe, Prisma |
| **AI Agent** | Intelligent agents | Python, CrewAI, Groq |

## Quick Commands

```bash
# Build the Elite Framework
make elite

# Generate a REST API
./bin/elite generate "REST API for task management"

# Generate a bot
./bin/elite generate "Telegram bot for weather"

# Generate a PWA
./bin/elite generate "PWA for task tracking"

# Generate an AI agent
./bin/elite generate "AI agent with CrewAI"
```

## Example Workflow

Here's a typical development workflow:

```bash
# 1. Generate backend API
make generate IDEA="REST API for blog platform"

# 2. Navigate to generated project
cd output/rest-api-for-blog-platform

# 3. Install dependencies
go mod download

# 4. Run the application
go run cmd/api/main.go

# 5. Test the API
curl http://localhost:8080/health
```

## Need Help?

- Check [QUICKSTART.md](QUICKSTART.md) for basic usage
- Read [Elite Framework Examples](../docs/ELITE_FRAMEWORK_EXAMPLES.md) for detailed guides
- Review [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
- Open an issue on GitHub for bugs or questions

## License

Tokyo-IA Elite Framework: Apache 2.0  
Generated projects: MIT License (can be modified)

---

*Examples and demonstrations for Tokyo-IA Elite Framework*
