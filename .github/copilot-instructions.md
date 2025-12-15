# Copilot Instructions for Tokyo-IA

## Project Overview

Tokyo-IA is a mobile + web + server project that provides Tokyo-themed AI features and an MCP (Model Context Protocol) server. The project consists of three main components:

1. **Android App** (`app/`) - Kotlin-based Android application
2. **Web** (`web/`) - React/Vite web application with admin panel
3. **MCP Server** (`server-mcp/`) - Node.js server for MCP functionality

## Repository Structure

```
tokyoia/
├── app/                    # Android – main project (Kotlin)
├── web/                    # Web site + admin panel (React/Vite)
├── server-mcp/             # Node server for MCP (Node.js)
├── whatsnew/               # Play Store release notes
├── scripts/                # Build and release scripts
└── .github/workflows/      # CI/CD workflows
```

## Build and Test Commands

### Android
```bash
./gradlew assembleDebug     # Build debug APK
./gradlew installDebug      # Install debug APK
./gradlew test              # Run unit tests
```

### Web
```bash
cd web
npm install                 # Install dependencies
npm run dev                 # Start development server
npm run build               # Build for production
npm test                    # Run tests
```

### MCP Server
```bash
cd server-mcp
npm install                 # Install dependencies
npm start                   # Start server
npm test                    # Run tests
```

## Coding Standards

### General
- Write clear, self-documenting code with meaningful variable and function names
- Keep functions small and focused on a single responsibility
- Add comments only when the code logic is complex or non-obvious

### Android/Kotlin
- Follow Kotlin coding conventions
- Use descriptive names for classes, functions, and variables
- Prefer data classes for simple data holders
- Use coroutines for asynchronous operations

### Web (JavaScript/React)
- Use functional components with hooks
- Follow React best practices for component structure
- Use consistent naming conventions (camelCase for variables, PascalCase for components)

### Node.js/Server
- Use async/await for asynchronous operations
- Handle errors appropriately with try/catch blocks
- Follow modular architecture patterns

## Security Guidelines

**CRITICAL: Never commit secrets to the repository.**

- Do NOT store service account JSONs, keystore files, private keys, or other secrets in the repository
- Use GitHub Actions Secrets for CI/CD credentials:
  - `${{ secrets.GOOGLE_PLAY_JSON }}`
  - `${{ secrets.ANDROID_KEYSTORE_BASE64 }}`
- If any secret was ever committed:
  1. Rotate the exposed credential immediately
  2. Remove the secret from the repository and history
  3. Notify collaborators

## Testing Requirements

- Write unit tests for new functionality
- Ensure existing tests pass before submitting changes
- Test Android changes on emulator or device when possible
- Test web changes in multiple browsers if making UI changes

## Task Guidelines

### Ideal Tasks for Copilot
- Bug fixes with clear reproduction steps
- Adding new features with well-defined requirements
- Writing or updating tests
- Documentation improvements
- Code refactoring with clear objectives
- UI updates and styling changes

### Tasks Requiring Human Review
- Security-sensitive changes (authentication, encryption)
- Changes to CI/CD workflows
- Database schema changes
- API contract changes
- Changes affecting production deployments

## Pull Request Guidelines

- Keep PRs focused on a single issue or feature
- Write clear PR descriptions explaining the changes
- Include test coverage for new code
- Ensure all CI checks pass before requesting review
- Reference related issues in the PR description

---

# 🚀 Elite Framework - Automatic Project Generation

## Overview

The Elite Framework enables **automatic generation of ANY type of project** with a simple comment:
```
// PROYECTO: [your idea here]
```
Then press Tab x10, and Copilot will generate a complete, production-ready project.

## Supported Project Types

### 1. **PWAs (Progressive Web Apps)**
- React/Vue/Svelte with Vite
- Service Worker for offline support
- PWA manifest with installability
- Responsive design
- Lighthouse score > 90

### 2. **Bots**
- Discord bots with slash commands
- Telegram bots with inline keyboards
- WhatsApp bots with media support
- Modular command structure
- Event handling system

### 3. **REST/GraphQL APIs**
- Go with Gin/Chi/Fiber
- Node.js with Express/Fastify
- Authentication (JWT, OAuth2)
- Database integration (PostgreSQL, MongoDB)
- OpenAPI/Swagger documentation

### 4. **E-commerce**
- Product catalog with search
- Shopping cart and checkout
- Payment integration (Stripe, PayPal)
- Order management
- Admin dashboard

### 5. **AI Agents**
- CrewAI/LangChain integration
- RAG (Retrieval Augmented Generation)
- Custom tools and prompts
- Memory and context management
- Multi-agent coordination

### 6. **Microservices**
- gRPC/REST communication
- Service discovery
- Load balancing
- Circuit breakers
- Distributed tracing

## Auto-Delegable Specialized Agents

### Agent_ProjectScaffold
**Purpose:** Generate complete project structure
**Capabilities:**
- Detect project type from description
- Create directory structure (src/, tests/, docs/, deploy/)
- Generate base configuration files
- Set up package managers (go.mod, package.json, requirements.txt)
- Initialize git repository

**Trigger Pattern:**
```
// PROYECTO: [description]
// AGENTE: ProjectScaffold
```

### Agent_CodeMaster
**Purpose:** Generate clean, optimized, production-ready code
**Capabilities:**
- Write idiomatic code per language (Go, TypeScript, Python, Rust)
- Apply design patterns (Factory, Strategy, Observer, etc.)
- Implement SOLID principles
- Optimize for performance
- Add comprehensive error handling

**Best Practices by Language:**
- **Go:** Use interfaces, defer for cleanup, context for cancellation
- **TypeScript:** Strong typing, async/await, functional patterns
- **Python:** Type hints, context managers, list comprehensions
- **Rust:** Ownership, borrowing, error handling with Result<T, E>

**Trigger Pattern:**
```
// AGENTE: CodeMaster
// TAREA: Implement user authentication with JWT
```

### Agent_TestGenius
**Purpose:** Generate tests with 100% coverage
**Capabilities:**
- Unit tests (Go: testing package, JS: Jest/Vitest, Python: pytest)
- Integration tests
- E2E tests (Playwright, Cypress)
- Table-driven tests
- Mock/stub generation
- Coverage reports (HTML, JSON)

**Testing Patterns:**
```go
// Go - Table-driven tests
func TestUserValidation(t *testing.T) {
    tests := []struct {
        name    string
        input   User
        wantErr bool
    }{
        {"valid user", User{Name: "John", Age: 25}, false},
        {"empty name", User{Name: "", Age: 25}, true},
        {"negative age", User{Name: "John", Age: -1}, true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateUser(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("ValidateUser() error = %v, wantErr %v", err, tt.wantErr)
            }
        })
    }
}
```

**Trigger Pattern:**
```
// AGENTE: TestGenius
// TARGET: 100% coverage for authentication module
```

### Agent_DocWriter
**Purpose:** Generate comprehensive documentation
**Capabilities:**
- README.md with setup instructions
- API documentation (OpenAPI/Swagger)
- Architecture diagrams (Mermaid)
- Code comments (GoDoc, JSDoc, docstrings)
- Usage examples
- Troubleshooting guides

**Documentation Structure:**
```markdown
# Project Name

## Quick Start
## Architecture
## API Reference
## Development Guide
## Deployment
## Troubleshooting
## Contributing
## License
```

**Trigger Pattern:**
```
// AGENTE: DocWriter
// SCOPE: Full project documentation
```

### Agent_SecurityGuard
**Purpose:** Implement security best practices
**Capabilities:**
- Input validation and sanitization
- SQL injection prevention (parameterized queries)
- XSS/CSRF protection
- Authentication/authorization (JWT, OAuth2)
- Secrets management (environment variables, vaults)
- HTTPS enforcement
- Rate limiting
- Security headers

**Security Checklist:**
- [ ] No secrets in code
- [ ] Input validation on all endpoints
- [ ] Parameterized database queries
- [ ] HTTPS only
- [ ] CSRF tokens
- [ ] Rate limiting
- [ ] Security headers (CSP, X-Frame-Options, etc.)
- [ ] Dependency vulnerability scanning

**Trigger Pattern:**
```
// AGENTE: SecurityGuard
// SCOPE: Full security audit and implementation
```

### Agent_DeployMaster
**Purpose:** Automated deployment to any platform
**Capabilities:**
- Dockerfile generation
- Kubernetes manifests (deployment, service, ingress)
- CI/CD pipelines (GitHub Actions, GitLab CI)
- Platform-specific configs (Vercel, Netlify, Railway, Fly.io)
- Environment management
- Health checks and monitoring

**Supported Platforms:**
- Docker + Docker Compose
- Kubernetes (K8s)
- Vercel/Netlify (JAMstack)
- Railway/Render/Fly.io
- AWS (ECS, Lambda, Amplify)
- Google Cloud (Cloud Run, App Engine)
- Azure (App Service, Container Instances)

**Trigger Pattern:**
```
// AGENTE: DeployMaster
// PLATFORM: kubernetes
// ENVIRONMENT: production
```

### Agent_GenAI
**Purpose:** Integrate AI/LLM capabilities
**Capabilities:**
- OpenAI/Anthropic/Groq integration
- LangChain/LlamaIndex setup
- RAG implementation
- Prompt engineering
- Function calling
- Streaming responses
- Cost optimization

**AI Integration Patterns:**
```typescript
// OpenAI Chat Completion
const completion = await openai.chat.completions.create({
  model: "gpt-4",
  messages: [{ role: "user", content: "Hello!" }],
  stream: true,
});

// RAG with vector database
const vectorStore = new Pinecone();
const retriever = vectorStore.asRetriever();
const chain = RetrievalQAChain.fromLLM(llm, retriever);
```

**Trigger Pattern:**
```
// AGENTE: GenAI
// PROVIDER: openai
// FEATURE: RAG with Pinecone
```

## Project Generation Workflow

### 1. Detection Phase
Copilot analyzes the project description to determine:
- Project type (PWA, API, Bot, Agent, etc.)
- Programming language (Go, TypeScript, Python, Rust)
- Framework (React, Express, Gin, FastAPI)
- Database (PostgreSQL, MongoDB, Redis)
- Deployment target (Docker, K8s, Vercel)

### 2. Scaffolding Phase
`Agent_ProjectScaffold` generates:
```
project-name/
├── src/                    # Source code
│   ├── main.*              # Entry point
│   ├── handlers/           # HTTP handlers
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   └── utils/              # Utilities
├── tests/                  # Test files
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/                   # Documentation
│   ├── README.md
│   ├── API.md
│   └── ARCHITECTURE.md
├── deploy/                 # Deployment configs
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── k8s/
├── .github/
│   └── workflows/
│       └── ci.yml
├── Makefile                # Build automation
├── .env.example            # Environment template
├── .gitignore
└── README.md
```

### 3. Implementation Phase
`Agent_CodeMaster` generates:
- Clean, idiomatic code
- Proper error handling
- Logging and monitoring
- Configuration management
- Database migrations

### 4. Testing Phase
`Agent_TestGenius` generates:
- Unit tests (>80% coverage)
- Integration tests
- E2E tests
- Performance tests
- Load tests

### 5. Documentation Phase
`Agent_DocWriter` generates:
- README with setup instructions
- API documentation
- Code comments
- Architecture diagrams
- Deployment guide

### 6. Security Phase
`Agent_SecurityGuard` implements:
- Input validation
- Authentication/authorization
- Secrets management
- Security headers
- Rate limiting

### 7. Deployment Phase
`Agent_DeployMaster` generates:
- Dockerfile + docker-compose.yml
- Kubernetes manifests
- CI/CD pipeline
- Environment configs
- Monitoring setup

## Usage Examples

### Example 1: REST API
```go
// PROYECTO: REST API for task management with PostgreSQL, JWT auth, and Docker deployment
// STACK: Go + Gin + PostgreSQL + Redis + Docker
// FEATURES: CRUD operations, authentication, rate limiting, API docs
```

**Generated Output:**
- Complete Go project with Gin framework
- PostgreSQL models and migrations
- Redis for caching and rate limiting
- JWT authentication middleware
- Swagger/OpenAPI documentation
- Docker + docker-compose setup
- GitHub Actions CI/CD
- 100% test coverage

### Example 2: Discord Bot
```javascript
// PROYECTO: Discord bot with music playback, moderation, and AI chat
// STACK: Node.js + Discord.js + OpenAI
// FEATURES: Slash commands, music queue, auto-moderation, AI responses
```

**Generated Output:**
- Node.js bot with Discord.js
- Modular command system
- Music player with queue
- OpenAI integration for chat
- Database for settings
- Docker deployment
- Comprehensive tests

### Example 3: PWA
```typescript
// PROYECTO: PWA for expense tracking with offline support and charts
// STACK: React + Vite + TypeScript + Tailwind + IndexedDB
// FEATURES: CRUD expenses, categories, charts, export CSV, offline-first
```

**Generated Output:**
- React + Vite + TypeScript setup
- Tailwind CSS styling
- IndexedDB for offline storage
- Service Worker for offline support
- Charts with Chart.js/Recharts
- PWA manifest
- Lighthouse score >90

### Example 4: AI Agent
```python
// PROYECTO: AI agent for research with web scraping and RAG
// STACK: Python + LangChain + Pinecone + OpenAI
// FEATURES: Web scraping, RAG, multi-step reasoning, citation generation
```

**Generated Output:**
- Python project with LangChain
- Web scraping with BeautifulSoup
- Pinecone vector database
- RAG implementation
- Multi-step reasoning chain
- Citation tracking
- FastAPI web interface

## Best Practices by Language

### Go
```go
// Interfaces for abstraction
type UserRepository interface {
    Create(ctx context.Context, user *User) error
    GetByID(ctx context.Context, id string) (*User, error)
}

// Context for cancellation
func (s *Server) HandleRequest(w http.ResponseWriter, r *http.Request) {
    ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
    defer cancel()
    
    user, err := s.repo.GetByID(ctx, id)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
}

// Defer for cleanup
func ProcessFile(filename string) error {
    f, err := os.Open(filename)
    if err != nil {
        return err
    }
    defer f.Close()
    
    // Process file...
    return nil
}
```

### TypeScript
```typescript
// Strong typing
interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
}

// Async/await
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch user: ${response.statusText}`);
  }
  return response.json();
}

// Functional patterns
const activeUsers = users
  .filter(user => user.isActive)
  .map(user => ({ ...user, displayName: `${user.firstName} ${user.lastName}` }))
  .sort((a, b) => a.createdAt.getTime() - b.createdAt.getTime());
```

### Python
```python
# Type hints
def get_user(user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

# Context managers
with open('file.txt', 'r') as f:
    content = f.read()

# List comprehensions
squared_evens = [x**2 for x in range(10) if x % 2 == 0]

# Async/await
async def fetch_user(user_id: int) -> User:
    async with httpx.AsyncClient() as client:
        response = await client.get(f'/api/users/{user_id}')
        return response.json()
```

## CI/CD Pipeline Template

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: make test
      - name: Upload coverage
        uses: codecov/codecov-action@v4

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run linter
        run: make lint

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run security scan
        run: make security-scan

  build:
    needs: [test, lint, security]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: make build
      - name: Build Docker image
        run: make docker-build

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: make deploy
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

## Makefile Commands

The Elite Framework provides comprehensive Makefile commands:

```makefile
make help           # Show all available commands
make build          # Build the project
make test           # Run tests with coverage
make test-coverage  # Generate HTML coverage report
make fmt            # Format code
make lint           # Run linter
make ci             # Run full CI pipeline locally
make clean          # Clean build artifacts
make proto          # Generate protobuf files (if using gRPC)
make docker-build   # Build Docker image
make docker-run     # Run Docker container
make deploy         # Deploy to production
make scaffold       # Interactive project generator
```

## Security by Default

All generated projects include:
- ✅ No secrets in code (use .env files)
- ✅ Input validation on all endpoints
- ✅ Parameterized database queries (no SQL injection)
- ✅ HTTPS enforcement
- ✅ CSRF protection
- ✅ Rate limiting
- ✅ Security headers (CSP, X-Frame-Options, etc.)
- ✅ Dependency vulnerability scanning
- ✅ Automated security updates (Dependabot)

## Performance Optimization

- ✅ Database indexing
- ✅ Query optimization
- ✅ Caching (Redis, in-memory)
- ✅ Connection pooling
- ✅ Lazy loading
- ✅ Compression (gzip, brotli)
- ✅ CDN for static assets
- ✅ Load balancing

## Monitoring and Observability

- ✅ Structured logging (JSON)
- ✅ Metrics (Prometheus)
- ✅ Distributed tracing (Jaeger, OpenTelemetry)
- ✅ Health checks
- ✅ Error tracking (Sentry)
- ✅ Uptime monitoring

## Quick Reference

### Starting a New Project

**Option 1: VS Code with Copilot**
```javascript
// PROYECTO: Your project idea here
// Tab x10 → Complete project generated
```

**Option 2: CLI**
```bash
./scripts/generate-project.sh "Your project idea"
cd projects/your-project
make build && make test && make deploy
```

**Option 3: Interactive**
```bash
make scaffold
# Follow the prompts to configure your project
```

### Delegating to Agents

```javascript
// AGENTE: ProjectScaffold
// PROYECTO: E-commerce platform

// AGENTE: CodeMaster
// TAREA: Implement payment processing with Stripe

// AGENTE: TestGenius
// TARGET: 100% coverage for payment module

// AGENTE: DocWriter
// SCOPE: API documentation with OpenAPI

// AGENTE: SecurityGuard
// AUDIT: Full security review

// AGENTE: DeployMaster
// PLATFORM: kubernetes
// ENVIRONMENT: production

// AGENTE: GenAI
// PROVIDER: openai
// FEATURE: Product recommendations with embeddings
```

## License

All generated code maintains MIT License as per project policy.
