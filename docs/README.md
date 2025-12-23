# 📚 Tokyo-IA Documentation

Welcome to the Tokyo-IA documentation hub! This comprehensive guide will help you understand, deploy, and work with the Tokyo-IA AI agent orchestration platform.

## 🚀 Quick Links

- [**Getting Started**](getting-started/quick-start.md) - Start here! Get up and running in 5 minutes
- [**Architecture**](architecture/overview.md) - Understand the system design
- [**API Reference**](api/rest-api.md) - Complete API documentation
- [**Agents Guide**](agents/overview.md) - Learn about the AI agent system
- [**Deployment**](deployment/railway.md) - Deploy to production

## 📖 Documentation Sections

### 🎯 For Users

Get started with Tokyo-IA and learn how to use it effectively.

- [**Installation Guide**](getting-started/installation.md) - Complete installation instructions
- [**Quick Start**](getting-started/quick-start.md) - 5-minute getting started guide
- [**Configuration**](getting-started/configuration.md) - Environment variables and settings
- [**User Guide**](guides/user-guide.md) - Complete user documentation
- [**FAQ**](guides/faq.md) - Frequently asked questions

### 💻 For Developers

Everything you need to contribute to Tokyo-IA.

- [**Development Setup**](development/setup.md) - Set up your development environment
- [**Contributing Guide**](development/contributing.md) - How to contribute
- [**Code Style**](development/code-style.md) - Coding standards and conventions
- [**Testing Guide**](development/testing.md) - Write and run tests
- [**Debugging**](development/debugging.md) - Debugging tips and tricks

### 🚀 For DevOps

Deploy and operate Tokyo-IA in production.

- [**Railway Deployment**](deployment/railway.md) - Deploy to Railway (recommended)
- [**Docker Guide**](deployment/docker.md) - Run with Docker and Docker Compose
- [**Kubernetes**](deployment/kubernetes.md) - Deploy to Kubernetes
- [**Monitoring**](deployment/monitoring.md) - Observability and monitoring
- [**CI/CD Overview**](cicd/overview.md) - Continuous integration and deployment

### 🏗️ Architecture

Understand how Tokyo-IA is built.

- [**System Architecture**](architecture/overview.md) - High-level architecture overview
- [**System Design**](architecture/system-design.md) - Detailed component design
- [**Technology Stack**](architecture/technology-stack.md) - Technologies and why we chose them
- [**Data Flow**](architecture/data-flow.md) - Request lifecycle and data flow
- [**Components**](architecture/components.md) - Individual component details
- [**Database Schema**](database/schema.md) - PostgreSQL schema and design

### 🤖 AI Agents

Learn about the five specialized AI agents.

- [**Agent Overview**](agents/overview.md) - Meet the five agents
- [**Orchestrator Guide**](agents/orchestrator.md) - Multi-agent coordination
- [**Workflows**](agents/workflows.md) - Pre-built and custom workflows
- [**Individual Agents**](agents/individual-agents.md) - Detailed agent documentation
- [**Integration Guide**](agents/integration-guide.md) - Integrate agents in your app

### 🔌 API Reference

Complete API documentation for developers.

- [**REST API**](api/rest-api.md) - HTTP API reference
- [**OpenAPI Spec**](api/openapi.yaml) - Machine-readable API specification
- [**Authentication**](api/authentication.md) - API authentication and security
- [**Examples**](api/examples.md) - Code examples in multiple languages

### 🔐 Security

Keep your Tokyo-IA deployment secure.

- [**Security Overview**](security/overview.md) - Security architecture and practices
- [**Best Practices**](security/best-practices.md) - Security guidelines
- [**Vulnerability Reporting**](security/vulnerability-reporting.md) - Report security issues

### 📊 Database

Database schema and operations.

- [**Database Schema**](database/schema.md) - Complete schema documentation
- [**Migrations**](database/migrations.md) - Database migration guide
- [**Queries**](database/queries.md) - Common queries and optimization

### 🔧 CI/CD

Continuous integration and deployment.

- [**CI/CD Overview**](cicd/overview.md) - Pipeline architecture
- [**GitHub Actions**](cicd/github-actions.md) - Workflow documentation
- [**Workflows**](cicd/workflows.md) - Individual workflow details
- [**Secrets**](cicd/secrets.md) - Managing secrets securely
- [**Troubleshooting**](cicd/troubleshooting.md) - Fix common issues

### 📘 Additional Resources

- [**Glossary**](GLOSSARY.md) - Technical terms and definitions
- [**Changelog**](CHANGELOG.md) - Version history and changes
- [**Roadmap**](ROADMAP.md) - Future features and plans
- [**Pricing**](PRICING.md) - LLM API cost estimation

---

## 🎯 What is Tokyo-IA?

Tokyo-IA is an **enterprise-grade AI agent orchestration platform** featuring five specialized agents with unique personalities and expertise. Each agent is powered by state-of-the-art LLM models and designed for specific tasks:

### 🎭 The Five Agents

| Agent | ID | Role | Model | Use Cases |
|-------|-----|------|-------|-----------|
| 侍 **Akira** | akira-001 | Code Review Master | Claude Opus 4.1 | Security audits, performance reviews, architecture analysis |
| ❄️ **Yuki** | yuki-002 | Test Engineering | OpenAI o3 | Unit tests, integration tests, E2E testing |
| 🛡️ **Hiro** | hiro-003 | SRE & DevOps | Llama 4 405B | Kubernetes, CI/CD, monitoring, infrastructure |
| 🌸 **Sakura** | sakura-004 | Documentation | Gemini 3.0 Ultra | Technical docs, API docs, guides, diagrams |
| 🏗️ **Kenji** | kenji-005 | Architecture | OpenAI o3 | System design, patterns, scalability planning |

## 🌟 Key Features

- **Multi-Agent Workflows** - Coordinate multiple agents for complex tasks
- **Production Ready** - Built with Go and PostgreSQL for scale
- **Cross-Platform** - Web dashboard, Android app, CLI tools
- **Complete Tracking** - All agent activities logged and analyzable
- **Cost Optimization** - Track token usage and optimize LLM costs
- **Extensible** - Add custom agents and workflows

## 🚦 Getting Started

New to Tokyo-IA? Start here:

1. **[Quick Start Guide](getting-started/quick-start.md)** - Get running in 5 minutes
2. **[Installation](getting-started/installation.md)** - Detailed setup instructions
3. **[Your First Workflow](guides/user-guide.md)** - Run your first multi-agent task

## 📚 Learning Path

### Beginner
1. Read the [Quick Start](getting-started/quick-start.md)
2. Explore the [Agent Overview](agents/overview.md)
3. Try the [API Examples](api/examples.md)

### Intermediate
1. Learn about [Workflows](agents/workflows.md)
2. Understand the [Architecture](architecture/overview.md)
3. Deploy with [Docker](deployment/docker.md)

### Advanced
1. Deep dive into [System Design](architecture/system-design.md)
2. Deploy to [Kubernetes](deployment/kubernetes.md)
3. Contribute via [Development Guide](development/contributing.md)

## 🆘 Need Help?

- 📖 Check the [FAQ](guides/faq.md) for common questions
- 🐛 [Report Issues](https://github.com/Melampe001/Tokyo-IA/issues) on GitHub
- 💬 [Join Discussions](https://github.com/Melampe001/Tokyo-IA/discussions)
- 📧 Contact support (see [User Guide](guides/user-guide.md))

## 📊 Documentation Standards

All documentation follows these principles:

- ✅ **Clear and Concise** - Easy to understand, active voice
- ✅ **Visual** - Diagrams and examples throughout
- ✅ **Tested** - All code examples are tested and working
- ✅ **Accessible** - Written at 8th-grade reading level
- ✅ **Up-to-date** - Regularly reviewed and updated

## 🤝 Contributing to Documentation

Found an error or want to improve the docs?

1. Check the [Contributing Guide](development/contributing.md)
2. Edit the relevant `.md` file
3. Submit a pull request

Documentation improvements are always welcome!

---

<div align="center">

**🌸 Made with care by the Tokyo-IA team**

*"Beautiful documentation is not just informative—it's delightful to read."*  
— Sakura, Documentation Artist

</div>

---

*Last updated: 2025-12-23*
