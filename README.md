# Tokyo-IA

[![CI Pipeline](https://github.com/Melampe001/Tokyo-IA/actions/workflows/ci.yml/badge.svg)](https://github.com/Melampe001/Tokyo-IA/actions/workflows/ci.yml)

Tokyo-IA is a mobile + web + server project that provides Tokyo-themed AI features and a MCP server.

## 📋 Table of Contents

- [Repository Structure](#repository-structure)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

## 🏗️ Repository Structure
tokyoia/
│
├── app/                                   # Android – main project
│   ├── build.gradle                       # Config signed + release
│   ├── proguard-rules.pro
│   ├── src/
│   │   ├── main/
│   │   │   ├── AndroidManifest.xml
│   │   │   ├── java/com/tokyoia/app/
│   │   │   │   └── TokyoApp.kt
│   │   │   └── res/
│   │   │       ├── layout/activity_main.xml
│   │   │       ├── mipmap-*/              # App icons
│   │   │       └── values/strings.xml
│   │   └── test/
│   │       └── ExampleUnitTest.kt
│   └── gradle.properties
│
├── web/                                   # Web site + admin panel
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── components/
│       └── styles/
│
├── server-mcp/                            # Node server for MCP
│   ├── index.js
│   ├── package.json
│   ├── tokyo-rules.json
│   └── src/
│       ├── actions/
│       └── context/
│
├── whatsnew/                              # Play Store release notes
│   ├── en-US/whatsnew.txt
│   └── es-MX/whatsnew.txt
│
├── .github/
│   ├── workflows/
│   │   └── ci.yml                       # CI pipeline for all components
│   ├── ISSUE_TEMPLATE/                  # Issue templates
│   ├── dependabot.yml                   # Automated dependency updates
│   └── pull_request_template.md         # PR template
│
├── docs/
│   ├── README.md                        # Documentation index
│   ├── CI_CD.md                         # CI/CD documentation
│   └── BRANCH_PROTECTION.md             # Branch protection guide
│
├── scripts/
│   ├── bump-version.sh                    # Increment version
│   └── generate-release.sh                # Build + tag + push
│
├── .gitignore
├── README.md
├── CONTRIBUTING.md                        # Contribution guidelines
├── SECURITY.md                            # Security policy
└── LICENSE

## 🚀 Quick Start

### Android (local debug)
```bash
./gradlew assembleDebug
./gradlew installDebug
```

### Web (dev)
```bash
cd web
npm install
npm run dev
```

### Server (local)
```bash
cd server-mcp
npm install
npm start
```

## 📚 Documentation

- **[AI Integration](docs/IMPLEMENTATION_SUMMARY_AI.md)** - Multi-model AI orchestration system
- **[Elite Framework](docs/elite-framework.md)** - Automated project generation system
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[CI/CD Documentation](docs/CI_CD.md)** - Continuous Integration and Deployment
- **[Branch Protection](docs/BRANCH_PROTECTION.md)** - Git workflow and branch rules
- **[Security Policy](SECURITY.md)** - Security best practices

## 🤖 AI Integration - Multi-Model Orchestration

Tokyo-IA includes a sophisticated AI orchestration system that intelligently routes requests to different AI providers (OpenAI, Anthropic, Gemini) based on task requirements.

### Features

- **Intelligent Routing**: Automatic provider selection based on task type
- **Response Caching**: In-memory cache with TTL for cost optimization
- **Metrics Collection**: Comprehensive usage statistics and performance tracking
- **Mock Development**: Work without API keys using mock clients
- **Python Agents**: CrewAI-based agents for complex workflows
- **REST API**: Simple HTTP interface for AI completions

### Quick Start

```bash
# Build AI API
make ai-build

# Run server
make ai-run

# Test endpoint
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing",
    "task_type": "reasoning"
  }'

# Run interactive demo
make ai-demo
```

### Task Routing

| Task Type | Provider | Use Case |
|-----------|----------|----------|
| Reasoning | Anthropic Claude | Logic, analysis, problem-solving |
| Creative | OpenAI GPT-4 | Writing, storytelling, creative content |
| Code Review | Anthropic Claude | Code analysis, security, best practices |
| Code Generation | OpenAI GPT-4 | Writing new code, implementing features |
| Translation | Google Gemini | Language translation |
| General | OpenAI GPT-4 | Default for other tasks |

### Documentation

- **[Architecture Guide](docs/architecture/ai-models-integration-architecture.md)** - System design and components
- **[User Guide](docs/guides/ai-model-router-guide.md)** - Configuration and usage examples
- **[API Reference](docs/api/ai-api-reference.md)** - REST API documentation
- **[Implementation Summary](docs/IMPLEMENTATION_SUMMARY_AI.md)** - Complete feature list

### Python Agents

The system includes CrewAI-based agents for complex workflows:

```python
from lib.agents import run_workflow

# Research workflow
result = run_workflow("research", topic="AI Ethics")

# Code review workflow
result = run_workflow("code_review", code="...", language="python")

# Content creation workflow
result = run_workflow("content_creation", topic="Climate Change", content_type="blog")
```

**Available Tools:**
- Code Analyzer
- Text Summarizer
- JSON Parser
- URL Validator
- And 5 more...

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