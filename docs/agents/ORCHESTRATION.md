# Tokyo-IA Agent Orchestration System

Complete documentation for the Tokyo-IA multi-agent orchestration system.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [The Five Agents](#the-five-agents)
4. [Database Schema](#database-schema)
5. [Registry API](#registry-api)
6. [Orchestrator](#orchestrator)
7. [Workflows](#workflows)
8. [Quick Start](#quick-start)
9. [API Reference](#api-reference)
10. [Examples](#examples)

## Overview

Tokyo-IA is a full-stack agent orchestration system featuring 5 specialized AI agents, each with unique personalities and expertise. The system provides:

- **Multi-agent coordination**: Agents work together on complex workflows
- **Complete tracking**: PostgreSQL database records all activities
- **REST API**: Full programmatic access to all features
- **Real-time monitoring**: Track agent performance and workflows
- **Scalable architecture**: Built for production use

### Key Features

✨ **Specialized Agents**: Each agent has distinct personality and expertise
📊 **Complete Logging**: Every action recorded in PostgreSQL
🔄 **Workflow Orchestration**: Coordinate multiple agents seamlessly
📈 **Performance Metrics**: Track tokens, costs, latencies
🌐 **REST API**: Access everything programmatically
📱 **Cross-platform**: Web dashboard and Android app support

## Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Web[Web Dashboard]
        Android[Android App]
        CLI[CLI Tools]
    end
    
    subgraph "API Layer"
        API[Registry API<br/>Go REST Server<br/>Port 8080]
    end
    
    subgraph "Orchestration Layer"
        Orch[Agent Orchestrator<br/>Python Coordinator]
    end
    
    subgraph "Agent Layer"
        Akira[侍 Akira<br/>Code Review]
        Yuki[❄️ Yuki<br/>Testing]
        Hiro[🛡️ Hiro<br/>SRE/DevOps]
        Sakura[🌸 Sakura<br/>Documentation]
        Kenji[🏗️ Kenji<br/>Architecture]
    end
    
    subgraph "Data Layer"
        DB[(PostgreSQL<br/>Registry Database)]
    end
    
    subgraph "LLM Providers"
        Claude[Claude Opus 4.1]
        OpenAI[OpenAI o3]
        Llama[Llama 4 405B]
        Gemini[Gemini 3.0 Ultra]
    end
    
    Web --> API
    Android --> API
    CLI --> API
    CLI --> Orch
    
    API --> DB
    Orch --> API
    
    Orch --> Akira
    Orch --> Yuki
    Orch --> Hiro
    Orch --> Sakura
    Orch --> Kenji
    
    Akira --> Claude
    Yuki --> OpenAI
    Hiro --> Llama
    Sakura --> Gemini
    Kenji --> OpenAI
```

### Component Overview

#### 1. **Database Layer** (`db/`)
- PostgreSQL database with comprehensive schema
- Tracks agents, tasks, workflows, metrics, interactions
- Optimized indexes for performance
- Automatic timestamps and triggers

#### 2. **Registry System** (`internal/registry/`)
- Go-based data models and operations
- CRUD operations for all entities
- Connection pooling and error handling
- Type-safe database interactions

#### 3. **REST API** (`cmd/registry-api/`)
- Go HTTP server on port 8080
- RESTful endpoints for all operations
- CORS enabled for web access
- Request logging and error handling

#### 4. **Specialized Agents** (`lib/agents/specialized/`)
- 5 unique AI agents with personalities
- Each uses different LLM provider
- Specialized methods for their domain
- Consistent interface across agents

#### 5. **Orchestrator** (`lib/orchestrator/`)
- Python-based workflow coordinator
- Manages multi-agent workflows
- Automatic task logging to registry
- Error handling and retries

## The Five Agents

### 侍 Akira - Code Review Master
**ID**: `akira-001` | **Model**: Claude Opus 4.1

A disciplined samurai of code quality with expertise in:
- Security vulnerability detection
- Performance analysis and optimization
- Architecture review
- Code quality assessment

**Key Methods**:
```python
review_code(code, language, context)
security_audit(code, language)
performance_analysis(code, language)
```

**Use Cases**:
- Pre-commit code review
- Security audits
- Performance optimization
- Architecture validation

---

### ❄️ Yuki - Test Engineering Specialist
**ID**: `yuki-002` | **Model**: OpenAI o3

Like pristine snow ensuring purity through comprehensive testing:
- Unit test generation
- Integration test design
- E2E test creation
- Test coverage analysis

**Key Methods**:
```python
generate_unit_tests(code, language, framework)
generate_integration_tests(components, language)
generate_e2e_tests(user_stories, tool)
analyze_test_coverage(code, tests, language)
```

**Use Cases**:
- Automated test generation
- TDD support
- Coverage improvement
- Test strategy planning

---

### 🛡️ Hiro - SRE & DevOps Guardian
**ID**: `hiro-003` | **Model**: Llama 4 405B

A vigilant guardian protecting production systems:
- Kubernetes orchestration
- CI/CD pipeline design
- Monitoring and alerting
- Infrastructure reliability

**Key Methods**:
```python
design_kubernetes_deployment(app_spec)
create_cicd_pipeline(repo_info, platform)
setup_monitoring(services, stack)
design_disaster_recovery(infrastructure)
```

**Use Cases**:
- Production deployments
- Infrastructure setup
- Monitoring configuration
- Disaster recovery planning

---

### 🌸 Sakura - Documentation Artist
**ID**: `sakura-004` | **Model**: Gemini 3.0 Ultra

Transforming complexity into beautiful, clear documentation:
- API documentation
- User guides
- Architecture diagrams
- Technical specifications

**Key Methods**:
```python
generate_api_documentation(api_spec)
create_user_guide(product_info)
document_architecture(system_description, components)
create_readme(project_info)
```

**Use Cases**:
- API docs generation
- User manual creation
- Architecture documentation
- README files

---

### 🏗️ Kenji - Architecture Visionary
**ID**: `kenji-005` | **Model**: OpenAI o3

Master architect seeing the grand design in every system:
- System architecture design
- Design pattern recommendations
- Architecture review
- Refactoring planning
- Microservices design

**Key Methods**:
```python
design_system_architecture(requirements)
recommend_design_patterns(problem_description, language)
review_architecture(architecture_doc)
plan_refactoring(codebase_info)
design_microservices(monolith_description)
```

**Use Cases**:
- New system design
- Architecture reviews
- Microservices migration
- Refactoring planning

## Database Schema

### Core Tables

#### `agents`
Stores information about the 5 specialized agents.

```sql
CREATE TABLE agents (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(200) NOT NULL,
    model VARCHAR(100) NOT NULL,
    specialties TEXT[] NOT NULL,
    backstory TEXT,
    personality_emoji VARCHAR(10),
    status VARCHAR(20) DEFAULT 'active',
    total_tasks_completed INTEGER DEFAULT 0,
    total_tokens_used BIGINT DEFAULT 0,
    average_latency_ms FLOAT DEFAULT 0,
    success_rate FLOAT DEFAULT 100.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);
```

#### `workflows`
Multi-agent workflow orchestration tracking.

```sql
CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    workflow_type VARCHAR(100),
    initiator VARCHAR(100),
    total_tasks INTEGER DEFAULT 0,
    completed_tasks INTEGER DEFAULT 0,
    failed_tasks INTEGER DEFAULT 0,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,
    total_tokens_used INTEGER DEFAULT 0,
    total_cost_usd DECIMAL(10, 6) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);
```

#### `agent_tasks`
Individual task execution records.

```sql
CREATE TABLE agent_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id VARCHAR(50) NOT NULL REFERENCES agents(id),
    workflow_id UUID REFERENCES workflows(id),
    task_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,
    tokens_used INTEGER DEFAULT 0,
    cost_usd DECIMAL(10, 6) DEFAULT 0,
    retry_count INTEGER DEFAULT 0,
    parent_task_id UUID REFERENCES agent_tasks(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);
```

See `db/schema.sql` for complete schema with indexes and views.

## Registry API

The Registry API is a Go-based REST server providing full access to the orchestration system.

### Base URL
```
http://localhost:8080
```

### Authentication
Currently no authentication (planned for future).

### Endpoints

#### Agents

**List All Agents**
```http
GET /api/agents
```

**Get Agent Details**
```http
GET /api/agents/{id}
```

**Get Agent Statistics**
```http
GET /api/agents/{id}/stats
```

**Get Agent Tasks**
```http
GET /api/agents/{id}/tasks?limit=50
```

#### Tasks

**Create Task**
```http
POST /api/tasks
Content-Type: application/json

{
  "agent_id": "akira-001",
  "workflow_id": "uuid-optional",
  "task_type": "code_review",
  "description": "Review authentication code",
  "input_data": {
    "language": "python",
    "code": "..."
  }
}
```

**Update Task Status**
```http
PUT /api/tasks/{id}
Content-Type: application/json

{
  "status": "completed",
  "output_data": {...},
  "tokens_used": 1500,
  "cost_usd": 0.045
}
```

#### Workflows

**List Workflows**
```http
GET /api/workflows?limit=50
```

**Create Workflow**
```http
POST /api/workflows
Content-Type: application/json

{
  "name": "Code Review Pipeline",
  "description": "Full review with tests and docs",
  "workflow_type": "code_review",
  "initiator": "user@example.com"
}
```

**Get Workflow Details**
```http
GET /api/workflows/{id}
```

**Get Workflow Tasks**
```http
GET /api/workflows/{id}/tasks
```

#### Metrics

**Get Agent Metrics**
```http
GET /api/metrics?agent_id=akira-001&metric_type=latency&limit=100
```

#### Health Check

**Server Health**
```http
GET /health
```

### Starting the API Server

```bash
# Set database URL
export DATABASE_URL="postgresql://user:password@localhost:5432/tokyoia"

# Build and run
go build -o bin/registry-api ./cmd/registry-api/main.go
./bin/registry-api

# Or use PORT environment variable
PORT=9000 ./bin/registry-api
```

## Orchestrator

The orchestrator coordinates multiple agents in workflows.

### Basic Usage

```python
from lib.orchestrator import AgentOrchestrator

# Initialize orchestrator
orchestrator = AgentOrchestrator(
    registry_api_url="http://localhost:8080"
)

# Initialize agents with API keys
orchestrator.initialize_agents(
    anthropic_api_key="sk-ant-...",
    openai_api_key="sk-...",
    groq_api_key="gsk_...",
    google_api_key="..."
)

# Create a workflow
workflow_id = orchestrator.create_workflow(
    name="Code Review Pipeline",
    description="Full review of authentication module",
    workflow_type="code_review"
)

# Execute tasks
result = orchestrator.execute_task(
    agent_id="akira-001",
    task_func=orchestrator.agents["akira-001"].review_code,
    task_type="code_review",
    description="Review auth code",
    workflow_id=workflow_id,
    code=my_code,
    language="python"
)
```

### Workflow Execution

```python
# Define workflow tasks
tasks = [
    {
        "agent_id": "akira-001",
        "task_type": "security_audit",
        "description": "Security audit",
        "method": "security_audit",
        "args": [code, "python"]
    },
    {
        "agent_id": "yuki-002",
        "task_type": "unit_tests",
        "description": "Generate tests",
        "method": "generate_unit_tests",
        "args": [code, "python", "pytest"]
    }
]

# Run workflow
result = orchestrator.run_workflow(workflow_id, tasks)
```

## Workflows

Pre-built workflows for common scenarios.

### Full Code Review Workflow

```python
from lib.orchestrator.workflows import full_code_review_workflow

result = full_code_review_workflow(
    orchestrator=orchestrator,
    code=your_code,
    language="python"
)
```

**Steps**:
1. Akira: Security audit
2. Akira: Code review
3. Yuki: Generate unit tests
4. Hiro: Create CI/CD pipeline
5. Sakura: Generate documentation

### New Feature Development

```python
from lib.orchestrator.workflows import new_feature_workflow

result = new_feature_workflow(
    orchestrator=orchestrator,
    feature_requirements={
        "name": "User Authentication",
        "description": "OAuth2 + JWT authentication",
        "language": "python",
        "scale": "10k users"
    }
)
```

**Steps**:
1. Kenji: Design architecture
2. Yuki: Plan testing strategy
3. Sakura: Create technical spec

### Production Deployment

```python
from lib.orchestrator.workflows import production_deployment_workflow

result = production_deployment_workflow(
    orchestrator=orchestrator,
    app_spec={
        "name": "tokyo-ia-api",
        "image": "tokyo-ia/api:latest",
        "port": 8080,
        "replicas": 3
    }
)
```

**Steps**:
1. Hiro: Design Kubernetes deployment
2. Hiro: Setup monitoring
3. Sakura: Create deployment docs

## Quick Start

### 1. Setup Database

```bash
# Create database
createdb tokyoia

# Run schema
psql tokyoia < db/schema.sql

# Set environment variable
export DATABASE_URL="postgresql://user:password@localhost:5432/tokyoia"
```

### 2. Start Registry API

```bash
# Build
go build -o bin/registry-api ./cmd/registry-api/main.go

# Run
./bin/registry-api
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set API Keys

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GROQ_API_KEY="gsk_..."
export GOOGLE_API_KEY="..."
```

### 5. Run Orchestrator

```python
from lib.orchestrator import AgentOrchestrator
from lib.orchestrator.workflows import full_code_review_workflow

# Initialize
orchestrator = AgentOrchestrator()
orchestrator.initialize_agents()

# Run workflow
code = """
def authenticate_user(username, password):
    # Your code here
    pass
"""

result = full_code_review_workflow(orchestrator, code, "python")
print(result)
```

## API Reference

See individual agent files for complete method documentation:
- `lib/agents/specialized/akira_code_reviewer.py`
- `lib/agents/specialized/yuki_test_engineer.py`
- `lib/agents/specialized/hiro_sre.py`
- `lib/agents/specialized/sakura_documentation.py`
- `lib/agents/specialized/kenji_architect.py`

## Examples

### Example 1: Code Review

```python
from lib.agents.specialized import AkiraCodeReviewer

akira = AkiraCodeReviewer()
result = akira.review_code(
    code=my_code,
    language="python",
    context="Production authentication module"
)
print(result['result'])
```

### Example 2: Generate Tests

```python
from lib.agents.specialized import YukiTestEngineer

yuki = YukiTestEngineer()
result = yuki.generate_unit_tests(
    code=my_code,
    language="python",
    framework="pytest"
)
print(result['result'])
```

### Example 3: Design Architecture

```python
from lib.agents.specialized import KenjiArchitect

kenji = KenjiArchitect()
result = kenji.design_system_architecture({
    "name": "E-commerce Platform",
    "users": "1M+ concurrent",
    "features": ["catalog", "cart", "payments"],
    "constraints": ["high availability", "low latency"]
})
print(result['result'])
```

## Best Practices

1. **Always initialize agents** before running workflows
2. **Set appropriate timeouts** for long-running tasks
3. **Monitor token usage** to control costs
4. **Use workflows** for complex multi-agent tasks
5. **Check agent status** before executing tasks
6. **Handle errors gracefully** with retries
7. **Log all operations** for debugging
8. **Review security audits** carefully
9. **Test generated code** before deploying
10. **Keep API keys secure** and rotate regularly

## Troubleshooting

### Agent won't initialize
- Check API key is set correctly
- Verify API key has proper permissions
- Check network connectivity

### Task fails immediately
- Verify agent is initialized
- Check input parameters are valid
- Review agent-specific requirements

### Registry API connection fails
- Verify API server is running
- Check DATABASE_URL is set
- Ensure database is accessible

### Workflow doesn't complete
- Check all agents are initialized
- Review task definitions
- Check for errors in individual tasks

## Contributing

Contributions welcome! See `CONTRIBUTING.md` for guidelines.

## License

See `LICENSE` file for details.

## Support

For issues and questions:
- GitHub Issues: https://github.com/Melampe001/Tokyo-IA/issues
- Documentation: This file
- Examples: `lib/orchestrator/workflows.py`
