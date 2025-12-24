# 🏛️ Tokyo-IA - Imperial Premium Elite Edition

[![CI Pipeline](https://github.com/Melampe001/Tokyo-IA/actions/workflows/ci.yml/badge.svg)](https://github.com/Melampe001/Tokyo-IA/actions/workflows/ci.yml)
[![CD Pipeline](https://github.com/Melampe001/Tokyo-IA/actions/workflows/cd.yml/badge.svg)](https://github.com/Melampe001/Tokyo-IA/actions/workflows/cd.yml)
[![Security Scan](https://github.com/Melampe001/Tokyo-IA/actions/workflows/security.yml/badge.svg)](https://github.com/Melampe001/Tokyo-IA/actions/workflows/security.yml)
[![Release](https://github.com/Melampe001/Tokyo-IA/actions/workflows/release.yml/badge.svg)](https://github.com/Melampe001/Tokyo-IA/actions/workflows/release.yml)
[![Vercel Deploy](https://github.com/Melampe001/Tokyo-IA/actions/workflows/deploy-vercel.yml/badge.svg)](https://github.com/Melampe001/Tokyo-IA/actions/workflows/deploy-vercel.yml)
[![Pre-Release Tests](https://github.com/Melampe001/Tokyo-IA/actions/workflows/pre-release-tests.yml/badge.svg)](https://github.com/Melampe001/Tokyo-IA/actions/workflows/pre-release-tests.yml)
[![Go Report Card](https://goreportcard.com/badge/github.com/Melampe001/Tokyo-IA)](https://goreportcard.com/report/github.com/Melampe001/Tokyo-IA)
[![codecov](https://codecov.io/gh/Melampe001/Tokyo-IA/branch/main/graph/badge.svg)](https://codecov.io/gh/Melampe001/Tokyo-IA)
[![Go Version](https://img.shields.io/badge/Go-1.21%20|%201.22-blue)](https://go.dev/)
[![Python Version](https://img.shields.io/badge/Python-3.11%20|%203.12-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

> Generador de ramas ordenadas y flujos optimizados con IA integrada
# Tokyo-IA 🗼

**Tokyo-IA** is a complete AI agent orchestration platform featuring 5 specialized agents with unique personalities and expertise. Built with Go, Python, React, and Android support.

## ✨ Features

- 🤖 **5 Specialized AI Agents**: Each with unique personality and LLM model
- 🔄 **Multi-Agent Orchestration**: Coordinate complex workflows across agents
- 📊 **Complete Tracking**: PostgreSQL database records all activities
- 🌐 **REST API**: Full programmatic access to all features
- 📱 **Cross-Platform**: Web dashboard and Android app support
- 📈 **Performance Metrics**: Track tokens, costs, and latencies
- 🛡️ **Production Ready**: Built for scale with Go and Kubernetes support
- 📊 **Hybrid Data Architecture**: PostgreSQL + AWS Athena for hot/cold path analytics

## 🎭 The Five Agents

| Agent | ID | Role | Model | Specialties |
|-------|-----|------|-------|-------------|
| 侍 **Akira** | akira-001 | Code Review Master | Claude Opus 4.1 | Security, Performance, Architecture |
| ❄️ **Yuki** | yuki-002 | Test Engineering | OpenAI o3 | Unit/Integration/E2E Testing |
| 🛡️ **Hiro** | hiro-003 | SRE & DevOps | Llama 4 405B | Kubernetes, CI/CD, Monitoring |
| 🌸 **Sakura** | sakura-004 | Documentation | Gemini 3.0 Ultra | Technical Writing, Diagrams |
| 🏗️ **Kenji** | kenji-005 | Architecture | OpenAI o3 | System Design, Patterns |

## 🎭 SYNEMU Suite (NEW!)

**SYNEMU Suite** is a premium, fully automated platform module for **SIM**ulation, **E**mulation, **M**ulti-agent orchestration, and **U**nified automation workflows.

### The SYNEMU Agents

| Agent | ID | Role | Capabilities |
|-------|-----|------|--------------|
| 🎭 **Orchestrator** | synemu-orchestrator-001 | Multi-Agent Coordinator | Task management, workflow execution |
| 🔥 **2D Flare** | synemu-2d-flare-002 | 2D Simulation | Physics, sprites, animations |
| 🎮 **3D Unity** | synemu-3d-unity-003 | 3D Integration | Unity scenes, 3D objects, physics |
| 🎬 **Video Viz** | synemu-video-viz-004 | Video Rendering | HD video, effects, format conversion |
| 🦉 **QA Owl** | synemu-qa-owl-005 | Quality Assurance | Testing, coverage, validation |
| ⚖️ **Docu Libra** | synemu-docu-libra-006 | Documentation | API docs, manuals, diagrams |
| 🗺️ **Asset Atlas** | synemu-asset-atlas-007 | Asset Management | Storage, CDN, optimization |

**Documentation:** See [SYNEMU/README.md](SYNEMU/README.md) for complete documentation.

**Quick Start:**
```python
from SYNEMU.agents_bots import SynemuOrchestrator, Synemu2DFlareAgent

orchestrator = SynemuOrchestrator()
agent_2d = Synemu2DFlareAgent()
scene_id = agent_2d.create_scene(width=1920, height=1080)
result = agent_2d.run_simulation(scene_id, duration=5.0)
```

## 📊 Project Composition

Tokyo-IA is a polyglot platform leveraging the strengths of multiple programming languages:

```mermaid
pie title Lenguajes
    "Go" : 44.8
    "Python" : 37.5
    "TypeScript" : 4.2
    "Kotlin" : 4.1
    "HTML" : 4.1
    "PLpgSQL" : 2.6
    "Otros" : 2.7
```

- **Go (44.8%)**: High-performance backend core, APIs, and CLI tools
- **Python (37.5%)**: AI agents, orchestration, and ML components
- **TypeScript (4.2%)**: Modern web dashboard
- **Kotlin (4.1%)**: Native Android application
- **HTML (4.1%)**: Web interface templates
- **PLpgSQL (2.6%)**: Database functions and procedures
- **Others (2.7%)**: Ruby version management, configs, and templates

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Hybrid Data Architecture](#hybrid-data-architecture)
- [Repository Structure](#repository-structure)
- [Documentation](#documentation)
- [API Reference](#api-reference)
- [Development](#development)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

## ✨ Features

- 🌿 **Optimized Branch Management**: Intelligent branch creation and workflow
- 📁 **Automated File Generation**: GitHub file creation with templates
- 🤖 **AI-Powered**: ML-based repository optimization
- 🔒 **Enterprise Security**: CodeQL scanning, dependency review
- 📊 **Web Dashboard**: Real-time monitoring interface
- 🎭 **SYNEMU Suite**: Complete simulation, emulation, QA, and automation platform (NEW!)

## 🚀 Quick Start

### 1. Setup Database

```bash
# Create PostgreSQL database
createdb tokyoia

# Run schema
psql tokyoia < db/schema.sql

# Set environment variable
export DATABASE_URL="postgresql://user:password@localhost:5432/tokyoia"
```

### 2. Start Registry API (Go)

```bash
# Install dependencies
go mod download

# Build and run
make build
./bin/registry-api

# Or directly
go run ./cmd/registry-api/main.go
```

The API will be available at `http://localhost:8080`

### 3. Setup Python Environment

```bash
# Install Python dependencies
pip install -r requirements.txt

# Set API keys
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GROQ_API_KEY="gsk_..."
export GOOGLE_API_KEY="..."
```

### 4. Run Your First Workflow

```python
from lib.orchestrator import AgentOrchestrator
from lib.orchestrator.workflows import full_code_review_workflow

# Initialize orchestrator
orchestrator = AgentOrchestrator()
orchestrator.initialize_agents()

# Run a code review workflow
code = """
def authenticate_user(username, password):
    query = f"SELECT * FROM users WHERE name = '{username}'"
    # ... rest of code
"""

result = full_code_review_workflow(orchestrator, code, "python")
print(result)
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                            │
│  Web Dashboard  │  Android App  │  CLI Tools  │  API Calls  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   Registry API (Go)                         │
│         REST Server - Port 8080                             │
│  Agents │ Tasks │ Workflows │ Metrics │ Sessions            │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│               PostgreSQL Database                           │
│  agents │ agent_tasks │ workflows │ metrics │ interactions  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│            Agent Orchestrator (Python)                      │
│         Multi-Agent Workflow Coordinator                    │
└────┬─────┬──────┬──────┬──────┬─────────────────────────────┘
     │     │      │      │      │
     ▼     ▼      ▼      ▼      ▼
  Akira  Yuki   Hiro  Sakura  Kenji
   侍     ❄️     🛡️    🌸     🏗️
```

See [docs/agents/ORCHESTRATION.md](docs/agents/ORCHESTRATION.md) for detailed architecture.

## 📊 Hybrid Data Architecture

Tokyo-IA implements a hybrid data architecture combining PostgreSQL (hot path) and AWS Athena (cold path) for optimal performance and cost-effectiveness:

```
┌──────────────────────────────────────────────────────────────┐
│                    Hot Path (Real-time)                       │
│                                                               │
│  Go Services  ──────▶  PostgreSQL  ◀──────  Redis Cache      │
│  (cmd/ & lib/)         (Transactions)       (Performance)     │
└────────────────────────┬─────────────────────────────────────┘
                         │ Daily ETL
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    ETL Pipeline                               │
│                                                               │
│  Python ETL  ──────▶  Parquet Files  ──────▶  S3 Data Lake   │
│  (python/etl/)        (Compressed)            (Partitioned)   │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                  Cold Path (Analytics)                        │
│                                                               │
│  AWS Glue Catalog  ──────▶  AWS Athena  ◀──────  Go Client   │
│  (Metadata)                  (SQL Queries)        (lib/analytics/) │
└──────────────────────────────────────────────────────────────┘
```

**Key Features**:
- 🔥 **Hot Path**: PostgreSQL for real-time transactions (&lt;100ms latency)
- ❄️ **Cold Path**: Athena for historical analytics (petabyte-scale)
- 🔄 **Daily ETL**: Automated data export to S3 in Parquet format
- 📊 **Partitioning**: Date-based partitioning for query optimization
- 💰 **Cost-Effective**: Pay-per-query model with Athena
- 🔒 **Secure**: SSE-S3 encryption, IAM roles, audit logs

**Documentation**:
- [Hybrid Architecture Overview](docs/HYBRID_ARCHITECTURE.md)
- [Athena Setup Guide](docs/ATHENA_SETUP.md)
- [ETL Pipeline Documentation](docs/ETL_PIPELINE.md)
- [Query Examples](docs/QUERIES_EXAMPLES.md)

## 🏗️ Repository Structure
## 🏗️ Repository Structure

```
tokyoia/
│
├── cmd/                                # Go applications
│   ├── main.go                         # Main Tokyo-IA application
│   ├── elite/main.go                   # Elite framework CLI
│   └── registry-api/main.go            # REST API server ⭐
│
├── internal/                           # Internal Go packages
│   └── registry/                       # Agent registry system ⭐
│       ├── models.go                   # Data models
│       └── agent_registry.go           # Database operations
│
├── lib/                                # Shared libraries
│   ├── generator/                      # Code generation
│   ├── analytics/                      # AWS Athena client ⭐
│   │   ├── athena_client.go            # Athena client
│   │   ├── queries.go                  # Analytics queries
│   │   ├── types.go                    # Data types
│   │   └── athena_client_test.go       # Tests
│   ├── agents/                         # AI agents ⭐
│   │   └── specialized/                # 5 specialized agents
│   │       ├── akira_code_reviewer.py  # 侍 Code Review Master
│   │       ├── yuki_test_engineer.py   # ❄️ Test Specialist
│   │       ├── hiro_sre.py             # 🛡️ SRE/DevOps Guardian
│   │       ├── sakura_documentation.py # 🌸 Documentation Artist
│   │       └── kenji_architect.py      # 🏗️ Architecture Visionary
│   └── orchestrator/                   # Multi-agent coordinator ⭐
│       ├── agent_orchestrator.py       # Orchestration engine
│       └── workflows.py                # Pre-built workflows
│
├── SYNEMU/                             # SYNEMU Suite 🎭 NEW!
│   ├── agents_bots/                    # 8 specialized SYNEMU agents
│   │   ├── synemu_integrations.py      # API key management
│   │   ├── synemu_orchestrator.py      # 🎭 Multi-agent coordinator
│   │   ├── synemu_agent2d_flare.py     # 🔥 2D simulation
│   │   ├── synemu_agent3d_unity.py     # 🎮 3D Unity integration
│   │   ├── synemu_agent_video_viz.py   # 🎬 Video rendering
│   │   ├── synemu_qa_owl.py            # 🦉 QA automation
│   │   ├── synemu_docu_libra.py        # ⚖️ Documentation
│   │   └── synemu_asset_atlas.py       # 🗺️ Asset management
│   ├── docs/                           # SYNEMU documentation
│   └── recursos/                       # Additional resources
│
├── hojas_membretadas/                  # Official letterheads 📄 NEW!
├── manuales/                           # User manuals 📖 NEW!
├── instructivos/                       # How-to guides 📝 NEW!
├── plantillas/                         # Project templates 📋 NEW!
├── recursos_identidad/                 # Brand assets 🎨 NEW!
├── reportes_graficos/                  # Reports & dashboards 📊 NEW!
│
├── db/                                 # Database ⭐
│   ├── schema.sql                      # PostgreSQL schema
│   └── README.md                       # Database documentation
│
├── admin/                              # Web dashboard ⭐
│   └── src/components/
│       ├── AgentDashboard.tsx          # Agent monitoring
│       └── WorkflowMonitor.tsx         # Workflow tracking
│
├── app/                                # Android app ⭐
│   └── src/main/java/com/tokyoia/app/
│       ├── ui/agents/                  # Agent UI screens
│       │   ├── AgentsScreen.kt
│       │   └── AgentsViewModel.kt
│       └── data/repository/            # Data layer
│           └── AgentRepository.kt
│
├── docs/                               # Documentation
│   └── agents/                         # Agent system docs ⭐
│       └── ORCHESTRATION.md            # Complete guide
│
├── examples/                           # Example code
│   └── python/
│       └── basic_agent.py              # Basic agent usage
│
├── .github/
│   └── workflows/
│       └── ci.yml                      # CI pipeline
│
├── go.mod                              # Go dependencies
├── requirements.txt                    # Python dependencies ⭐
├── Makefile                            # Build commands
├── README.md                           # This file
├── CONTRIBUTING.md                     # Contribution guidelines
└── SECURITY.md                         # Security policy

⭐ = New in Agent Orchestration System
```

## 📚 Documentation

### Getting Started
- **[🚀 Quick Setup Guide](docs/QUICKSTART.md)** - Get started in 5 minutes
- **[🏗️ Architecture Documentation](docs/ARCHITECTURE.md)** - Complete visual architecture with Mermaid diagrams
  - Language composition and project structure
  - Development workflows and CI/CD pipeline
  - Branch strategy and component interactions
  - System architecture and security measures

### CI/CD & Deployment
- **[🚀 CI/CD Pipeline](docs/CICD.md)** - Comprehensive CI/CD documentation
  - Workflow descriptions and setup
  - Railway deployment guide
  - Troubleshooting and rollback procedures
- **[🔐 Secrets Configuration](docs/SECRETS.md)** - GitHub Actions secrets setup
  - Required and optional secrets
  - How to obtain tokens
  - Security best practices

### Mobile & Web Deployment
- **[📱 Play Store Checklist](docs/PLAY_STORE_CHECKLIST.md)** - Complete guide for Google Play Store publication
  - Asset requirements and specifications
  - Release signing configuration
  - Testing and submission process
- **[📝 Store Listing Template](docs/STORE_LISTING.md)** - Pre-written content for Play Store
- **[🔐 Secrets Setup Guide](docs/SECRETS_SETUP.md)** - All required secrets for deployments
  - Android release signing
  - Vercel deployment
  - Google Play API
- **[🌐 Vercel Setup](docs/VERCEL_SETUP.md)** - Web dashboard deployment guide
  - Step-by-step Vercel configuration
  - Domain setup and SSL
  - Automated deployment workflow
- **[🔒 Privacy Policy](docs/PRIVACY_POLICY.md)** - GDPR-compliant privacy policy

### API & Integration
- **[Agent Orchestration Guide](docs/agents/ORCHESTRATION.md)** - Complete system documentation
- **[Database Schema](db/README.md)** - Database setup and operations
- **[API Reference](docs/agents/ORCHESTRATION.md#api-reference)** - REST API endpoints
- **[Workflow Examples](lib/orchestrator/workflows.py)** - Pre-built workflows
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- **[Security Policy](SECURITY.md)** - Security guidelines

## 🔌 API Reference

### Registry API Endpoints

The Registry API runs on `http://localhost:8080` by default.

#### Agents
- `GET /api/agents` - List all agents
- `GET /api/agents/{id}` - Get agent details
- `GET /api/agents/{id}/stats` - Get agent statistics
- `GET /api/agents/{id}/tasks` - Get agent tasks

#### Tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task status

#### Workflows
- `GET /api/workflows` - List workflows
- `POST /api/workflows` - Create workflow
- `GET /api/workflows/{id}` - Get workflow details
- `GET /api/workflows/{id}/tasks` - Get workflow tasks

#### Metrics
- `GET /api/metrics?agent_id={id}&metric_type={type}` - Get metrics

See [API documentation](docs/agents/ORCHESTRATION.md#registry-api) for details.

## 💻 Development

### Build Commands

```bash
# Build main application
make build

# Build Registry API
go build -o bin/registry-api ./cmd/registry-api/main.go

# Build Elite Framework
make elite

# Format code
make fmt

# Run tests
make test

# Clean build artifacts
make clean
```

### Running Tests

```bash
# Go tests
go test ./...

# Python agent tests (when available)
pytest lib/agents/

# Full CI suite
make ci
```

### Environment Variables

```bash
# Database
export DATABASE_URL="postgresql://user:password@localhost:5432/tokyoia"

# Registry API
export PORT="8080"
export REGISTRY_API_URL="http://localhost:8080"

# LLM API Keys
export ANTHROPIC_API_KEY="sk-ant-..."    # For Akira
export OPENAI_API_KEY="sk-..."           # For Yuki & Kenji
export GROQ_API_KEY="gsk_..."            # For Hiro
export GOOGLE_API_KEY="..."              # For Sakura
```

## 🚀 CI/CD Pipeline

Tokyo-IA features a comprehensive CI/CD pipeline with automated testing, security scanning, and Railway deployment.

### Continuous Integration

Every push and pull request triggers:
- ✅ **Go Tests** (1.21 & 1.22) with race detector and coverage
- ✅ **Python Tests** (3.11 & 3.12) with pytest and coverage
- ✅ **Linting** (golangci-lint, Ruff)
- ✅ **Build Verification** for all binaries
- ✅ **Database Schema Tests** with PostgreSQL
- ✅ **Security Scanning** (CodeQL, Trivy, TruffleHog)

### Continuous Deployment

**Staging:** Automatic deployment to Railway on every push to `main`
```bash
git push origin main  # → Deploys to staging automatically
```

**Production:** Automatic deployment on version tags
```bash
git tag v1.0.0
git push origin v1.0.0  # → Deploys to production + creates GitHub release
```

**Manual Deployment:**
```bash
./scripts/deploy.sh staging     # Deploy to staging
./scripts/deploy.sh production  # Deploy to production
```

### Docker Support

```bash
# Local development with Docker Compose
docker-compose up -d

# Build Docker image
docker build -t tokyo-ia:local .

# Run container
docker run -p 8080:8080 tokyo-ia:local
```

### Release Automation

Every version tag automatically:
1. 📦 Builds binaries for Linux, macOS, Windows (amd64 & arm64)
2. 🔐 Generates SHA256 checksums
3. 📝 Creates GitHub release with changelog
4. 🐳 Builds and pushes Docker images to GHCR
5. 🚀 Deploys to Railway production

**See [docs/CICD.md](docs/CICD.md) for complete CI/CD documentation.**

## 📱 Mobile & Web Deployments

### Android App - Google Play Store

Tokyo IA includes a Flutter-based Android application ready for Google Play Store publication.

**Quick Start:**
```bash
cd flutter_app/

# Build release AAB
flutter build appbundle --release

# Output: build/app/outputs/bundle/release/app-release.aab
```

**Pre-requisites:**
- Configure release signing in `flutter_app/android/app/build.gradle` ✅
- Generate and secure your keystore (see [docs/PLAY_STORE_CHECKLIST.md](docs/PLAY_STORE_CHECKLIST.md))
- Configure GitHub Secrets for automated signing

**Resources:**
- 📋 [Play Store Checklist](docs/PLAY_STORE_CHECKLIST.md) - Complete publication guide
- 📝 [Store Listing Template](docs/STORE_LISTING.md) - Pre-written descriptions
- 🔐 [Privacy Policy](docs/PRIVACY_POLICY.md) - GDPR-compliant policy
- 🎨 [Assets Guide](assets/play-store/README.md) - Icon and screenshot specs

**Automated Testing:**
The [pre-release-tests.yml](.github/workflows/pre-release-tests.yml) workflow automatically:
- Runs Flutter tests
- Builds release AAB
- Verifies signing configuration

### Web Dashboard - Vercel

The web interface is automatically deployed to Vercel on every push to `main`.

**Local Development:**
```bash
cd web/
npm install
npm run dev
# Visit http://localhost:5173
```

**Deployment:**
- **Automatic:** Push to `main` branch triggers Vercel deployment
- **Manual:** Use Vercel CLI: `vercel --prod`
- **Preview:** Every PR gets a unique preview URL

**Setup:**
1. Create Vercel account and link repo
2. Configure GitHub Secrets:
   - `VERCEL_TOKEN`
   - `VERCEL_ORG_ID`
   - `VERCEL_PROJECT_ID`
3. See [docs/VERCEL_SETUP.md](docs/VERCEL_SETUP.md) for detailed instructions

**Live Demo:**
🌐 Web Dashboard: `https://tokyo-ia-web.vercel.app` (update after deployment)

### Secrets Configuration

All deployments require GitHub Secrets. See [docs/SECRETS_SETUP.md](docs/SECRETS_SETUP.md) for complete guide:

**Android Release:**
- `KEYSTORE_FILE` - Keystore for signing
- `KEYSTORE_PASSWORD` - Keystore password
- `KEY_ALIAS` - Key alias
- `KEY_PASSWORD` - Key password

**Vercel Deployment:**
- `VERCEL_TOKEN` - Vercel authentication token
- `VERCEL_ORG_ID` - Organization/Team ID
- `VERCEL_PROJECT_ID` - Project ID

**Google Play API (Optional):**
- `GOOGLE_PLAY_JSON` - Service account credentials for automated publishing

## 🎯 Use Cases

### 1. Code Review Pipeline
Automatically review code for security, generate tests, setup CI/CD, and create documentation.

```python
from lib.orchestrator.workflows import full_code_review_workflow

result = full_code_review_workflow(orchestrator, code, "python")
```

### 2. New Feature Development
Design architecture, plan testing, and create specifications for new features.

```python
from lib.orchestrator.workflows import new_feature_workflow

result = new_feature_workflow(orchestrator, {
    "name": "User Authentication",
    "description": "OAuth2 + JWT",
    "scale": "10k users"
})
```

### 3. Production Deployment
Design Kubernetes deployment, setup monitoring, and create deployment docs.

```python
from lib.orchestrator.workflows import production_deployment_workflow

result = production_deployment_workflow(orchestrator, {
    "name": "my-app",
    "image": "my-app:latest",
    "port": 8080
})
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 🔒 Security

Security is a top priority. See [SECURITY.md](SECURITY.md) for:
- Vulnerability reporting
- Security best practices
- Supported versions

**Never commit API keys or secrets!**

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- CrewAI for the agent framework
- Anthropic, OpenAI, Meta, and Google for LLM APIs
- The Go and Python communities

## 📞 Support

- 🐛 [Report Issues](https://github.com/Melampe001/Tokyo-IA/issues)
- 💬 [Discussions](https://github.com/Melampe001/Tokyo-IA/discussions)
- 📧 [Contact](mailto:support@example.com)

---

Made with ❤️ by the Tokyo-IA team

### Prerequisites

- **Go 1.21+**: For building the AI services
- **Python 3.11+**: For agent framework
- **Make**: For build commands
- **Git**: Version control

### Installation

```bash
# Clone the repository
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA

# Install Go dependencies
go mod download

# Install Python dependencies
pip install -r requirements.txt

# Setup pre-commit hooks (optional)
pre-commit install
```

### Usage
```bash
# Build
make build

# Run tests
make test

# Format code
make fmt

# Full CI locally
make ci
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
- **[Architecture Overview](docs/ARCHITECTURE.md)** - System design and components
- **[AI Integration Architecture](docs/architecture/ai-models-integration-architecture.md)** - AI system design
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

## 🔒 Security

This project uses:
- CodeQL analysis
- Dependabot
- Pre-commit hooks
- Automated security scans

Report vulnerabilities to [security contact]

For more details, see the [Security Policy](SECURITY.md).

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:
- Development setup
- Code standards
- Pull request process
- Branch protection rules

## 🏛️ Imperial Premium Elite Standards

This repository follows the **Athena Protocol** with automated:
- ✅ CI/CD pipelines
- ✅ Security scanning
- ✅ Code quality enforcement
- ✅ Comprehensive documentation

## 📄 License

See [LICENSE](LICENSE) file for details.