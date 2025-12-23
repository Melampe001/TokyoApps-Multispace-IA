# 🚀 Quick Setup Guide

Get Tokyo-IA running in 5 minutes!

## Prerequisites

- Go 1.21 or 1.22
- Python 3.11 or 3.12
- PostgreSQL 14+ (or use Docker)
- Docker & Docker Compose (optional, for easy setup)

## Option 1: Docker Compose (Recommended)

**Fastest way to get started!**

```bash
# Clone the repository
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA

# Create environment file
cp .env.example .env
# Edit .env and add your API keys (optional for basic testing)

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f api

# API will be available at http://localhost:8080
# Database UI (Adminer) at http://localhost:8081
```

**Test the API:**
```bash
curl http://localhost:8080/health
curl http://localhost:8080/api/agents
```

**Stop services:**
```bash
docker-compose down
```

## Option 2: Manual Setup

### 1. Setup Database

```bash
# Install PostgreSQL (if not installed)
# macOS: brew install postgresql@14
# Ubuntu: sudo apt-get install postgresql-14
# Windows: Download from postgresql.org

# Start PostgreSQL
# macOS: brew services start postgresql@14
# Ubuntu: sudo systemctl start postgresql
# Windows: Start via Services

# Create database
createdb tokyoia

# Or use psql:
psql -U postgres
CREATE DATABASE tokyoia;
CREATE USER tokyoia WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE tokyoia TO tokyoia;
\q

# Load schema
psql -U tokyoia -d tokyoia -f db/schema.sql
```

### 2. Setup Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
export DATABASE_URL="postgresql://tokyoia:your_password@localhost:5432/tokyoia"
export PORT="8080"
# Add your LLM API keys (optional)
```

### 3. Install Dependencies

```bash
# Go dependencies
go mod download

# Python dependencies
pip install -r requirements.txt
```

### 4. Build & Run

```bash
# Build all binaries
make build-all

# Run Registry API
./bin/registry-api

# Or run directly
go run ./cmd/registry-api/main.go
```

### 5. Verify Installation

```bash
# Test health endpoint
curl http://localhost:8080/health

# List agents
curl http://localhost:8080/api/agents

# You should see 5 agents (Akira, Yuki, Hiro, Sakura, Kenji)
```

## Option 3: Railway Deploy

Deploy directly to Railway:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Click the button above
2. Sign in to Railway
3. Click "Deploy Now"
4. Add environment variables in Railway dashboard
5. Wait for deployment to complete

## Development Workflow

### Running Tests

```bash
# Go tests
make test-go

# Python tests (when available)
make test-python

# All tests
make test
```

### Code Formatting

```bash
# Format Go code
make fmt

# Check formatting (CI-style)
make fmt-check
```

### Linting

```bash
# Run golangci-lint
make lint
```

### Building

```bash
# Build main application
make build

# Build all binaries
make build-all

# Clean build artifacts
make clean
```

## Using the API

### List All Agents

```bash
curl http://localhost:8080/api/agents
```

### Get Agent Details

```bash
curl http://localhost:8080/api/agents/akira-001
```

### Get Agent Statistics

```bash
curl http://localhost:8080/api/agents/akira-001/stats
```

### Create a Task

```bash
curl -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "akira-001",
    "task_type": "code_review",
    "description": "Review authentication code",
    "input_data": {"code": "def login(user, pass): ..."}
  }'
```

### Create a Workflow

```bash
curl -X POST http://localhost:8080/api/workflows \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Full Stack Code Review",
    "description": "Complete review with all agents",
    "workflow_type": "code_review"
  }'
```

## Using Python Agents

```python
from lib.orchestrator import AgentOrchestrator
from lib.orchestrator.workflows import full_code_review_workflow

# Initialize orchestrator
orchestrator = AgentOrchestrator()
orchestrator.initialize_agents()

# Run a workflow
code = """
def authenticate(username, password):
    query = f"SELECT * FROM users WHERE name = '{username}'"
    # Potential SQL injection!
"""

result = full_code_review_workflow(orchestrator, code, "python")
print(result)
```

## Troubleshooting

### Database Connection Failed

```bash
# Check PostgreSQL is running
pg_isready

# Test connection manually
psql -U tokyoia -d tokyoia
```

### Port Already in Use

```bash
# Change port in .env
export PORT=8081

# Or kill process using port 8080
# macOS/Linux: lsof -ti:8080 | xargs kill
# Windows: netstat -ano | findstr :8080
```

### Import Errors (Python)

```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.11 or 3.12
```

### Build Errors (Go)

```bash
# Clean and rebuild
make clean
go mod tidy
make build-all
```

## Next Steps

- 📚 Read the [Complete Documentation](docs/CICD.md)
- 🏗️ Check [Architecture Overview](docs/ARCHITECTURE.md)
- 🤝 See [Contributing Guide](CONTRIBUTING.md)
- 🔒 Review [Security Policy](SECURITY.md)
- 🎭 Learn about [The Five Agents](docs/agents/ORCHESTRATION.md)

## Getting Help

- **Issues:** [GitHub Issues](https://github.com/Melampe001/Tokyo-IA/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Melampe001/Tokyo-IA/discussions)
- **Documentation:** [docs/](docs/)

---

**Happy coding with Tokyo-IA! 🗼**
