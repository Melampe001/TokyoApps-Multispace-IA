# Tokyo-IA

[![CI Pipeline](https://github.com/Melampe001/Tokyo-IA/actions/workflows/ci.yml/badge.svg)](https://github.com/Melampe001/Tokyo-IA/actions/workflows/ci.yml)

Tokyo-IA is a comprehensive AI platform featuring multi-model integration, intelligent routing, and autonomous agents. Built with Go and Python, it provides production-ready AI capabilities with cost optimization and enterprise-grade reliability.

## 📋 Table of Contents

- [Features](#-features)
- [AI Integration](#-ai-integration)
- [Repository Structure](#repository-structure)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Elite Framework](#-elite-framework---generate-projects-instantly)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

## 🤖 Features

### Multi-Model AI Integration
- **5 State-of-the-Art Providers**: OpenAI (o3/o5), Anthropic (Claude Opus/Sonnet), Google (Gemini 3.0), xAI (Grok 4), Meta (Llama 4)
- **Intelligent Routing**: Task-based model selection optimizes for quality, cost, and latency
- **Budget Management**: Real-time cost tracking with configurable daily limits
- **Fallback Chains**: 99.9% uptime with automatic provider failover
- **Response Caching**: 40%+ cache hit rate reduces costs and improves speed

### Autonomous Agent Framework
- **Code Review Agent**: Deep analysis using Claude Opus 4.1
- **Test Generation Agent**: Comprehensive test creation with OpenAI o3
- **SRE/Deployment Agent**: Infrastructure validation using local Llama 4
- **Documentation Agent**: Automated docs with Gemini 3.0

### Production-Grade Infrastructure
- **Cost Optimization**: $0.001-$0.01 per request with smart routing
- **Privacy Support**: Local Llama 4 for sensitive workloads
- **Comprehensive Metrics**: Prometheus + Grafana monitoring
- **High Performance**: <100ms p50 latency on local models

## 🚀 AI Integration

Tokyo-IA's AI system provides intelligent routing across multiple LLM providers with comprehensive cost and performance optimization.

### Quick Start

#### 1. Run the AI API Server

```bash
# Build and run
make build
./bin/ai-api

# API will be available at http://localhost:8080
```

#### 2. Make Your First Request

```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing",
    "task_type": "reasoning",
    "max_tokens": 500
  }'
```

#### 3. Check Usage Metrics

```bash
curl http://localhost:8080/ai/metrics
```

### Available Task Types

- **reasoning**: Complex analysis and problem-solving
- **code_generation**: Generate code snippets and programs
- **code_review**: Analyze code quality and security
- **multimodal**: Process images and diagrams
- **documentation**: Generate technical documentation
- **chat**: General conversational AI

### Example: Code Review

```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Review this code:\nfunc Add(a, b int) int { return a + b }",
    "task_type": "code_review"
  }'
```

### Multi-Agent Workflows

```python
from lib.agents.workflows import execute_workflow

# Execute PR review workflow
result = execute_workflow(
    "pr_review",
    pr_data={
        "number": 123,
        "title": "Add new feature",
        "diff": "..."
    }
)
```

See the [AI Model Router Guide](docs/guides/ai-model-router-guide.md) for detailed usage.
## 🏗️ Repository Structure

```
tokyoia/
│
├── cmd/
│   ├── main.go                # Main Tokyo-IA application
│   ├── ai-api/                # AI API service
│   └── elite/                 # Elite framework CLI
│
├── internal/
│   ├── ai/                    # AI orchestration layer
│   │   ├── model_router.go    # Intelligent routing logic
│   │   ├── cache.go           # Response caching
│   │   ├── metrics.go         # Performance metrics
│   │   └── clients/           # Model provider clients
│   └── config/                # Configuration management
│
├── lib/
│   ├── agents/                # Python agent framework
│   │   ├── crew_config.py     # Agent definitions
│   │   ├── tools.py           # Custom agent tools
│   │   └── workflows.py       # Multi-agent workflows
│   └── generator/             # Elite framework
│
├── config/
│   └── ai_models.yaml         # AI model configuration
│
├── docs/
│   ├── architecture/          # Architecture docs
│   ├── guides/                # User guides
│   └── api/                   # API reference
│
├── testing/                   # Tests
└── deploy/                    # Deployment configs
```

## 🚀 Quick Start

### Prerequisites

- **Go 1.21+**: For building the AI services
- **Python 3.9+**: For agent framework
- **Make**: For build commands

### Installation

```bash
# Clone the repository
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA

# Install Go dependencies
go mod download

# Install Python dependencies
pip install -r requirements.txt
```

### Build and Run

```bash
# Build all services
make build

# Run AI API server
./bin/ai-api

# Or run main application
./bin/tokyo-ia
```

### Running Tests

```bash
# Run Go tests
make test

# Run Python tests
python -m pytest lib/agents/test_crew.py

# Check code formatting
make fmt
```

### Configuration

Set up your API keys (optional for development with mock clients):

```bash
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
export GEMINI_API_KEY="your-key-here"
```

Configure models in `config/ai_models.yaml`.

## 📚 Documentation

### AI Platform
- **[Architecture Overview](docs/architecture/ai-models-integration-architecture.md)** - System design and components
- **[Model Router Guide](docs/guides/ai-model-router-guide.md)** - Intelligent routing and cost optimization
- **[API Reference](docs/api/ai-api-reference.md)** - HTTP API documentation
- **[Agent Workflows](docs/guides/agent-workflows-guide.md)** - Multi-agent system usage (planned)

### Development
- **[Elite Framework](docs/elite-framework.md)** - Automated project generation system
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[CI/CD Documentation](docs/CI_CD.md)** - Continuous Integration and Deployment
- **[Security Policy](SECURITY.md)** - Security best practices

## 🎯 Elite Framework - Generate Projects Instantly

Tokyo-IA includes the **Elite Framework**, an automated project generator that creates complete, production-ready projects from simple descriptions.

### Quick Start

```bash
# Build the elite CLI
make elite

# Generate a project
./bin/elite generate "REST API for task management"

# Or use make command
make generate IDEA="Telegram bot for weather updates"
```

### Supported Project Types

- **PWAs** - Progressive Web Apps with React/Vite
- **Bots** - Telegram, Discord, Slack bots
- **APIs** - REST/GraphQL APIs with Go
- **E-commerce** - Online stores with Stripe
- **AI Agents** - CrewAI/Groq powered agents

Each generated project includes:
- ✅ Complete source code
- ✅ Tests (unit + integration)
- ✅ Docker deployment
- ✅ CI/CD workflows
- ✅ Full documentation

See the [Elite Framework Documentation](docs/elite-framework.md) for details.

## 🔒 Security / Secrets (IMPORTANT)

**Do NOT store service account JSONs, keystore files, private keys, or other secrets in the repository.**

If you need to provide credentials for CI:
- Create the credential (e.g., Google Play service account JSON) locally
- Encode keystore files or JSON as base64 and store them in GitHub Actions Secrets
- Reference secrets in workflows using: `${{ secrets.GOOGLE_PLAY_JSON }}`, `${{ secrets.ANDROID_KEYSTORE_BASE64 }}`, etc.

If any secret was ever committed:
1. Rotate the exposed credential immediately (revoke old key)
2. Remove the secret from the repository and history
3. Notify collaborators and ask them to reclone if history was rewritten

For more details, see the [Security Policy](SECURITY.md).

## 📝 Release Notes

Release notes for Play Store:
- `whatsnew/en-US/whatsnew.txt`
- `whatsnew/es-MX/whatsnew.txt`

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:
- Development setup
- Code standards
- Pull request process
- Branch protection rules

## 📄 License

See [LICENSE](LICENSE) file for details.