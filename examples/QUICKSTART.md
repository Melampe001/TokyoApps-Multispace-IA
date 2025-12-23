# Elite Framework - Quick Start Guide

This guide demonstrates how to use the Tokyo-IA Elite Framework to generate new projects automatically.

## What is the Elite Framework?

The Elite Framework is an intelligent project generator that creates complete, production-ready applications from simple text descriptions. It analyzes your requirements and automatically selects the optimal technology stack and project structure.

## Installation

The Elite Framework is built into this repository. Simply build it:

```bash
# Build the elite CLI
make elite

# Or manually
go build -o bin/elite ./cmd/elite/main.go
```

## Basic Usage

### 1. Generate Your First Project

```bash
./bin/elite generate "REST API for task management"
```

This command will:
- Analyze the description
- Detect that you want an API
- Select Go + Gin + GORM + PostgreSQL stack
- Generate complete project structure
- Create boilerplate code, tests, and documentation

### 2. View the Generated Project

```bash
cd output/rest-api-for-task-management
cat README.md
```

### 3. Run the Generated Project

```bash
# Install dependencies
go mod download

# Run the API
go run cmd/api/main.go
```

The API will start on `http://localhost:8080`

### 4. Test the Generated Project

```bash
# Run tests
go test ./...

# Test the health endpoint
curl http://localhost:8080/health
```

## More Examples

### Generate a Telegram Bot

```bash
./bin/elite generate "Telegram bot for weather updates"
```

Generated stack: Python + python-telegram-bot + asyncio

### Generate a Progressive Web App

```bash
./bin/elite generate "PWA for task tracking"
```

Generated stack: TypeScript + React + Vite + TailwindCSS

### Generate an E-commerce Platform

```bash
./bin/elite generate "E-commerce platform with Stripe integration"
```

Generated stack: TypeScript + Next.js + Stripe + Prisma + PostgreSQL

### Generate an AI Agent

```bash
./bin/elite generate "AI agent with CrewAI for content generation"
```

Generated stack: Python + CrewAI + Groq + Langchain

## Using the Makefile

You can also use the Makefile for convenience:

```bash
make generate IDEA="REST API for user authentication"
```

## Supported Project Types

The framework automatically detects these project types:

1. **API** - REST/GraphQL APIs and microservices
2. **Bot** - Chat bots for Telegram, Discord, Slack
3. **PWA** - Progressive Web Applications
4. **E-commerce** - Online stores and marketplaces
5. **AI Agent** - Intelligent agents with LLM integration

## What You Get

Every generated project includes:

✅ Complete source code with best practices  
✅ Test infrastructure (unit + integration)  
✅ Documentation (README, API docs, architecture)  
✅ Deployment configuration (Docker, docker-compose)  
✅ CI/CD workflows (GitHub Actions)  
✅ Development environment setup  

## Advanced Options

### Custom Output Directory

```bash
./bin/elite generate "REST API for blogs" --output ./projects
```

### Check Version

```bash
./bin/elite version
# Output: Tokyo-IA Elite Framework v1.0.0
```

### Get Help

```bash
./bin/elite help
```

## Real-World Workflow

Here's a typical workflow:

```bash
# 1. Generate the backend
./bin/elite generate "REST API for blog platform"

# 2. Generate the frontend
./bin/elite generate "PWA for blog dashboard"

# 3. Navigate to backend and set up
cd output/rest-api-for-blog-platform
go mod download
go run cmd/api/main.go

# 4. In another terminal, set up frontend
cd output/pwa-for-blog-dashboard
npm install
npm run dev
```

## Customization

After generation, you can:
- Modify the generated code
- Add new features
- Extend the test coverage
- Update dependencies
- Configure for your specific needs

## Tips

1. **Be Specific**: The more detailed your description, the better the result
   - Good: "REST API for task management with PostgreSQL"
   - Better: "REST API for task management with user authentication and PostgreSQL"

2. **Use Keywords**: Include technology names if you have preferences
   - "Telegram bot with Python"
   - "API with GraphQL and PostgreSQL"

3. **Project Type**: Mention the type explicitly if needed
   - "E-commerce platform"
   - "Progressive Web App"
   - "AI agent"

4. **Review Generated Code**: Always review and customize the generated code for your needs

## Troubleshooting

### Problem: "Template not found"
**Solution**: Make sure you're in the project root directory where `templates/` exists

### Problem: "Command not found: elite"
**Solution**: Run `make elite` first to build the binary

### Problem: "Permission denied"
**Solution**: 
```bash
chmod +x bin/elite
```

### Problem: Generated project won't build
**Solution**: Make sure you have the required tools:
- Go 1.21+ for Go projects
- Node.js 18+ for TypeScript projects
- Python 3.10+ for Python projects

## Next Steps

1. Try generating different types of projects
2. Explore the generated code structure
3. Customize the projects for your needs
4. Read the comprehensive guide: [ELITE_FRAMEWORK_EXAMPLES.md](../docs/ELITE_FRAMEWORK_EXAMPLES.md)

## Example Output

When you run the generator, you'll see:

```
🚀 Tokyo-IA Elite Framework
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Description: REST API for task management

🔍 Analyzing project requirements...

✅ Project generated successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Project Name: rest-api-for-task-management
🏷️  Type: api
🛠️  Stack: [go gin gorm swagger postgresql]
📂 Location: output/rest-api-for-task-management

Next steps:
  cd output/rest-api-for-task-management
  cat README.md
```

## Learn More

- [Full Examples Documentation](../docs/ELITE_FRAMEWORK_EXAMPLES.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Project README](../README.md)

## License

The Tokyo-IA Elite Framework is licensed under Apache 2.0. Generated projects include an MIT License by default, which you can modify as needed.

---

**Happy Coding! 🚀**
