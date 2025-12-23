# 🚀 Quick Start Guide

Get Tokyo-IA up and running in **5 minutes**! This guide will have you executing your first multi-agent workflow in no time.

## 📋 What You'll Do

1. Clone the repository
2. Start with Docker (easiest) or manual setup
3. Verify the installation
4. Make your first API call
5. Run your first agent workflow

---

## Option 1: Docker (Fastest) 🐳

Perfect for trying out Tokyo-IA quickly.

### Step 1: Prerequisites

- Docker Desktop installed ([download here](https://www.docker.com/products/docker-desktop))
- Git installed

### Step 2: Clone and Start

```bash
# Clone repository
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA

# Start everything with Docker Compose
docker-compose up -d

# Wait ~30 seconds for services to start
```

### Step 3: Verify

```bash
# Check API health
curl http://localhost:8080/health
# Expected: {"status":"healthy","database":"connected"}

# List available agents
curl http://localhost:8080/api/agents
```

**✅ Done!** Skip to [Your First API Call](#your-first-api-call).

---

## Option 2: Manual Setup 🛠️

For development or when you want more control.

### Step 1: Prerequisites

Ensure you have installed:
- Go 1.21+
- Python 3.10+
- PostgreSQL 14+

See the [Installation Guide](installation.md) for detailed instructions.

### Step 2: Clone Repository

```bash
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA
```

### Step 3: Setup Database

```bash
# Create database
createdb tokyoia

# Apply schema
psql tokyoia < db/schema.sql

# Set environment variable
export DATABASE_URL="postgresql://localhost:5432/tokyoia"
```

### Step 4: Start API Server

```bash
# Build
make build

# Run
./bin/registry-api

# Or run directly
go run ./cmd/registry-api/main.go
```

You should see:
```
🚀 Registry API server starting...
📊 Database: Connected
🌐 Server: Listening on :8080
```

### Step 5: Setup Python Environment

Open a **new terminal**:

```bash
cd Tokyo-IA

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API keys (optional for development)
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GROQ_API_KEY="gsk_..."
export GOOGLE_API_KEY="..."
```

**✅ Done!** Continue to [Your First API Call](#your-first-api-call).

---

## Your First API Call

Let's verify everything is working by interacting with the API.

### Check System Health

```bash
curl http://localhost:8080/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-12-23T04:25:00Z"
}
```

### List Available Agents

```bash
curl http://localhost:8080/api/agents | jq
```

**Expected Response:**
```json
[
  {
    "id": "akira-001",
    "name": "Akira - Code Review Master",
    "role": "code_review",
    "model": "claude-opus-4.1",
    "specialties": ["security", "performance", "architecture"],
    "status": "active",
    "personality_emoji": "侍"
  },
  {
    "id": "yuki-002",
    "name": "Yuki - Test Engineering Specialist",
    "role": "test_engineering",
    "model": "openai-o3",
    "specialties": ["unit_testing", "integration_testing", "e2e_testing"],
    "status": "active",
    "personality_emoji": "❄️"
  }
  // ... more agents
]
```

### Get Specific Agent Details

```bash
curl http://localhost:8080/api/agents/akira-001 | jq
```

### Get Agent Statistics

```bash
curl http://localhost:8080/api/agents/akira-001/stats | jq
```

**Expected Response:**
```json
{
  "agent_id": "akira-001",
  "total_tasks": 0,
  "completed_tasks": 0,
  "failed_tasks": 0,
  "average_latency_ms": 0,
  "total_tokens_used": 0,
  "success_rate": 100.0
}
```

---

## Your First Agent Workflow

Now let's run a real multi-agent workflow to review some code!

### Step 1: Create a Python Script

Create `my_first_workflow.py`:

```python
#!/usr/bin/env python3
"""My first Tokyo-IA agent workflow"""

from lib.orchestrator import AgentOrchestrator

# Sample code to review
code_to_review = """
def authenticate_user(username, password):
    # SQL query to check credentials
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    result = db.execute(query)
    return result is not None
"""

def main():
    # Initialize the orchestrator
    print("🤖 Initializing Agent Orchestrator...")
    orchestrator = AgentOrchestrator()
    
    # Load all five agents
    orchestrator.initialize_agents()
    print(f"✅ Loaded {len(orchestrator.agents)} agents")
    
    # Get Akira (code reviewer)
    akira = orchestrator.agents.get("akira-001")
    if not akira:
        print("❌ Akira agent not available")
        return
    
    print("\n侍 Akira is reviewing your code...\n")
    
    # Create a review task
    task = {
        "type": "code_review",
        "language": "python",
        "code": code_to_review,
        "focus_areas": ["security", "best_practices"]
    }
    
    # Execute the review
    result = akira.execute(task)
    
    # Display results
    print("=" * 60)
    print("REVIEW RESULTS")
    print("=" * 60)
    print(result.get("analysis", "No analysis available"))
    print()
    
    if result.get("issues"):
        print("🚨 Issues Found:")
        for i, issue in enumerate(result["issues"], 1):
            print(f"{i}. {issue['severity'].upper()}: {issue['description']}")
    else:
        print("✅ No issues found!")
    
    print(f"\n📊 Tokens used: {result.get('tokens_used', 0)}")
    print(f"⏱️  Latency: {result.get('latency_ms', 0)}ms")

if __name__ == "__main__":
    main()
```

### Step 2: Run the Workflow

```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the script
python my_first_workflow.py
```

### Expected Output

```
🤖 Initializing Agent Orchestrator...
✅ Loaded 5 agents

侍 Akira is reviewing your code...

============================================================
REVIEW RESULTS
============================================================
This code has a critical SQL injection vulnerability. The 
username and password parameters are directly interpolated 
into the SQL query without any sanitization or parameterization.

Additionally, passwords should never be stored or compared 
in plaintext - use proper password hashing (bcrypt, argon2).

🚨 Issues Found:
1. CRITICAL: SQL Injection vulnerability in line 3
2. HIGH: Plaintext password comparison
3. MEDIUM: No input validation
4. LOW: Missing error handling

📊 Tokens used: 245
⏱️  Latency: 1850ms
```

**🎉 Congratulations!** You've just run your first Tokyo-IA agent workflow!

---

## Try More Complex Workflows

### Full Code Review Workflow

All five agents collaborate to review, test, deploy, and document your code:

```python
from lib.orchestrator import AgentOrchestrator
from lib.orchestrator.workflows import full_code_review_workflow

orchestrator = AgentOrchestrator()
orchestrator.initialize_agents()

code = """
def process_payment(user_id, amount):
    user = database.get_user(user_id)
    user.balance -= amount
    database.save(user)
    return {"success": True}
"""

result = full_code_review_workflow(
    orchestrator=orchestrator,
    code=code,
    language="python"
)

print(f"Akira's Review: {result['akira_review']}")
print(f"Yuki's Tests: {result['yuki_tests']}")
print(f"Hiro's CI/CD: {result['hiro_cicd']}")
print(f"Sakura's Docs: {result['sakura_docs']}")
```

### New Feature Workflow

Design a new feature from scratch:

```python
from lib.orchestrator.workflows import new_feature_workflow

result = new_feature_workflow(
    orchestrator=orchestrator,
    feature={
        "name": "User Authentication",
        "description": "OAuth2 + JWT authentication system",
        "scale": "10,000 concurrent users"
    }
)

print(f"Kenji's Architecture: {result['architecture']}")
print(f"Yuki's Test Plan: {result['test_plan']}")
print(f"Hiro's Infrastructure: {result['infrastructure']}")
print(f"Sakura's Specifications: {result['specifications']}")
```

---

## Using the REST API Directly

You can also create tasks via the REST API:

```bash
# Create a code review task
curl -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "akira-001",
    "task_type": "code_review",
    "description": "Review authentication code",
    "input_data": {
      "code": "def login(user, pass): return user == \"admin\"",
      "language": "python"
    }
  }'

# Response includes task_id
# {
#   "task_id": "550e8400-e29b-41d4-a716-446655440000",
#   "status": "pending",
#   "agent_id": "akira-001"
# }

# Check task status
curl http://localhost:8080/api/tasks/550e8400-e29b-41d4-a716-446655440000
```

---

## What's Next?

Now that you've got Tokyo-IA running:

### Learn More
- 📖 **[User Guide](../guides/user-guide.md)** - Complete usage documentation
- 🤖 **[Agent Overview](../agents/overview.md)** - Deep dive into each agent
- 🔄 **[Workflows Guide](../agents/workflows.md)** - Create custom workflows
- 🔌 **[API Reference](../api/rest-api.md)** - Complete API documentation

### Try Examples
- 🔍 **[Code Examples](../api/examples.md)** - More code samples
- 🎯 **[Use Cases](../guides/user-guide.md#use-cases)** - Real-world scenarios
- 🏗️ **[Architecture](../architecture/overview.md)** - Understand the system

### Deploy
- 🚂 **[Railway Deployment](../deployment/railway.md)** - Deploy to production
- 🐳 **[Docker Guide](../deployment/docker.md)** - Advanced Docker setup
- ☸️ **[Kubernetes](../deployment/kubernetes.md)** - Scale with K8s

### Develop
- 🛠️ **[Development Setup](../development/setup.md)** - Set up dev environment
- 🤝 **[Contributing](../development/contributing.md)** - Contribute to Tokyo-IA
- 🧪 **[Testing](../development/testing.md)** - Write tests

---

## Common Issues

### "Connection refused" when calling API

**Solution**: Make sure the API server is running:

```bash
# Check if process is running
ps aux | grep registry-api

# Check if port is listening
lsof -i :8080  # macOS/Linux
netstat -an | findstr :8080  # Windows
```

### "Agent not found" errors

**Solution**: Initialize agents in the database:

```bash
psql tokyoia < db/seed_agents.sql
```

### API keys not working

**Solution**: For development, you can use mock mode:

```bash
export USE_MOCK_AGENTS=true
python my_first_workflow.py
```

### Import errors in Python

**Solution**: Make sure you're in the virtual environment and in the right directory:

```bash
source venv/bin/activate
cd /path/to/Tokyo-IA
python my_first_workflow.py
```

---

## Getting Help

- 📖 [FAQ](../guides/faq.md) - Frequently asked questions
- 🐛 [Report Issues](https://github.com/Melampe001/Tokyo-IA/issues)
- 💬 [Discussions](https://github.com/Melampe001/Tokyo-IA/discussions)
- 📧 support@tokyo-ia.example.com

---

<div align="center">

**🎉 You're all set!**

*Happy coding with Tokyo-IA!*

</div>

---

*Last updated: 2025-12-23*
