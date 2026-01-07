# 🧪 Testing Guide

Comprehensive testing guide for Tokyo-IA covering unit tests, integration tests, and end-to-end testing.

## 📋 Table of Contents

- [Testing Philosophy](#testing-philosophy)
- [Running Tests](#running-tests)
- [Writing Tests](#writing-tests)
- [Test Coverage](#test-coverage)
- [Testing Best Practices](#testing-best-practices)
- [CI/CD Testing](#cicd-testing)

---

## Testing Philosophy

Tokyo-IA follows a comprehensive testing strategy:

- **Fast Feedback** - Unit tests run in milliseconds
- **High Coverage** - Target >80% code coverage
- **Reliable** - Tests are deterministic and repeatable
- **Maintainable** - Tests are easy to understand and update
- **Practical** - Focus on testing behavior, not implementation

---

## Running Tests

### Go Tests

**Run all tests:**
```bash
go test ./...
```

**Run with coverage:**
```bash
go test -cover ./...

# Detailed coverage report
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

**Run specific package:**
```bash
go test ./internal/registry
```

**Verbose output:**
```bash
go test -v ./...
```

**Race detector:**
```bash
go test -race ./...
```

**Benchmark tests:**
```bash
go test -bench=. ./...
```

### Python Tests

**Run all tests:**
```bash
pytest
```

**Run with coverage:**
```bash
pytest --cov=lib --cov-report=html
```

**Run specific file:**
```bash
pytest lib/agents/test_orchestrator.py
```

**Verbose output:**
```bash
pytest -v
```

**Run specific test:**
```bash
pytest lib/agents/test_orchestrator.py::test_agent_initialization
```

**Parallel execution:**
```bash
pytest -n auto  # Uses all CPU cores
```

---

## Writing Tests

### Go Unit Tests

**Table-Driven Tests (Recommended):**

```go
func TestValidateAgentID(t *testing.T) {
    tests := []struct {
        name    string
        agentID string
        want    bool
        wantErr bool
    }{
        {
            name:    "valid agent ID",
            agentID: "akira-001",
            want:    true,
            wantErr: false,
        },
        {
            name:    "invalid format",
            agentID: "invalid",
            want:    false,
            wantErr: true,
        },
        {
            name:    "empty string",
            agentID: "",
            want:    false,
            wantErr: true,
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ValidateAgentID(tt.agentID)
            if (err != nil) != tt.wantErr {
                t.Errorf("ValidateAgentID() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("ValidateAgentID() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

**Testing HTTP Handlers:**

```go
func TestAgentsHandler(t *testing.T) {
    // Create test server
    req, err := http.NewRequest("GET", "/api/agents", nil)
    if err != nil {
        t.Fatal(err)
    }
    
    // Create response recorder
    rr := httptest.NewRecorder()
    handler := http.HandlerFunc(AgentsHandler)
    
    // Serve request
    handler.ServeHTTP(rr, req)
    
    // Check status code
    if status := rr.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v",
            status, http.StatusOK)
    }
    
    // Check response body
    expected := `{"agents":[]}`
    if rr.Body.String() != expected {
        t.Errorf("handler returned unexpected body: got %v want %v",
            rr.Body.String(), expected)
    }
}
```

**Testing Database Operations:**

```go
func TestCreateAgent(t *testing.T) {
    // Setup test database
    db, cleanup := setupTestDB(t)
    defer cleanup()
    
    // Create test agent
    agent := &Agent{
        ID:          "test-001",
        Name:        "Test Agent",
        Role:        "testing",
        Model:       "test-model",
        Specialties: []string{"testing"},
    }
    
    // Test creation
    err := db.CreateAgent(agent)
    if err != nil {
        t.Fatalf("CreateAgent() failed: %v", err)
    }
    
    // Verify creation
    retrieved, err := db.GetAgent(agent.ID)
    if err != nil {
        t.Fatalf("GetAgent() failed: %v", err)
    }
    
    if retrieved.Name != agent.Name {
        t.Errorf("Agent name mismatch: got %v want %v",
            retrieved.Name, agent.Name)
    }
}

func setupTestDB(t *testing.T) (*DB, func()) {
    // Create temporary test database
    db, err := ConnectDB("postgresql://localhost/test_tokyoia")
    if err != nil {
        t.Fatalf("Failed to connect to test DB: %v", err)
    }
    
    // Run migrations
    if err := db.Migrate(); err != nil {
        t.Fatalf("Failed to migrate: %v", err)
    }
    
    // Return cleanup function
    cleanup := func() {
        db.DropAll()
        db.Close()
    }
    
    return db, cleanup
}
```

### Python Unit Tests

**Using pytest:**

```python
import pytest
from lib.orchestrator import AgentOrchestrator

def test_orchestrator_initialization():
    """Test orchestrator initializes correctly"""
    orchestrator = AgentOrchestrator()
    assert orchestrator is not None
    assert len(orchestrator.agents) == 0

def test_initialize_agents():
    """Test agents are loaded correctly"""
    orchestrator = AgentOrchestrator()
    orchestrator.initialize_agents()
    
    assert len(orchestrator.agents) == 5
    assert "akira-001" in orchestrator.agents
    assert "yuki-002" in orchestrator.agents

@pytest.mark.parametrize("agent_id,expected_role", [
    ("akira-001", "code_review"),
    ("yuki-002", "test_engineering"),
    ("hiro-003", "sre_devops"),
])
def test_agent_roles(agent_id, expected_role):
    """Test agents have correct roles"""
    orchestrator = AgentOrchestrator()
    orchestrator.initialize_agents()
    
    agent = orchestrator.agents[agent_id]
    assert agent.role == expected_role
```

**Using fixtures:**

```python
import pytest
from lib.orchestrator import AgentOrchestrator

@pytest.fixture
def orchestrator():
    """Create orchestrator for tests"""
    orch = AgentOrchestrator()
    orch.initialize_agents()
    return orch

@pytest.fixture
def mock_agent():
    """Create mock agent for testing"""
    class MockAgent:
        def __init__(self):
            self.agent_id = "mock-001"
            self.name = "Mock Agent"
            
        def execute(self, task):
            return {"status": "completed", "result": "mock result"}
    
    return MockAgent()

def test_execute_task(orchestrator):
    """Test task execution"""
    task = {
        "type": "code_review",
        "code": "def test(): pass"
    }
    
    result = orchestrator.execute_task("akira-001", task)
    assert result["status"] == "completed"

def test_mock_agent(mock_agent):
    """Test with mock agent"""
    result = mock_agent.execute({"test": "data"})
    assert result["status"] == "completed"
```

**Mocking external APIs:**

```python
import pytest
from unittest.mock import Mock, patch
from lib.agents.specialized import AkiraCodeReviewer

@pytest.fixture
def mock_anthropic():
    """Mock Anthropic API"""
    with patch('anthropic.Anthropic') as mock:
        # Configure mock response
        mock.return_value.messages.create.return_value = Mock(
            content=[Mock(text='{"issues": [], "severity": "low"}')],
            usage=Mock(input_tokens=100, output_tokens=200)
        )
        yield mock

def test_code_review_with_mock(mock_anthropic):
    """Test code review with mocked API"""
    akira = AkiraCodeReviewer()
    result = akira.execute({
        "code": "def safe_function(): return True",
        "language": "python"
    })
    
    assert result["status"] == "completed"
    assert "issues" in result
    mock_anthropic.return_value.messages.create.assert_called_once()
```

---

## Test Coverage

### Coverage Goals

| Component | Target | Current |
|-----------|--------|---------|
| Go Backend | >80% | 75% |
| Python Agents | >80% | 82% |
| Integration | >60% | 55% |
| E2E | Critical paths | In progress |

### Measure Coverage

**Go:**
```bash
# Generate coverage report
go test -coverprofile=coverage.out ./...

# View in browser
go tool cover -html=coverage.out

# Coverage by package
go test -cover ./internal/...
```

**Python:**
```bash
# Generate coverage report
pytest --cov=lib --cov-report=html --cov-report=term

# View in browser
open htmlcov/index.html

# Coverage threshold
pytest --cov=lib --cov-fail-under=80
```

### Coverage in CI

```yaml
# .github/workflows/ci.yml
- name: Test with coverage
  run: |
    go test -coverprofile=coverage.out ./...
    pytest --cov=lib --cov-report=xml
    
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.out,./coverage.xml
```

---

## Testing Best Practices

### 1. Test Naming

**Go:**
```go
// Good: Descriptive name
func TestAgentRegistry_GetAgent_ReturnsErrorWhenNotFound(t *testing.T)

// Bad: Unclear name
func TestGet(t *testing.T)
```

**Python:**
```python
# Good: Descriptive name
def test_orchestrator_raises_error_when_agent_not_found():
    pass

# Bad: Unclear name  
def test_error():
    pass
```

### 2. Test Organization

**Go:**
```
internal/
├── registry/
│   ├── registry.go
│   ├── registry_test.go      # Unit tests
│   └── registry_integration_test.go  # Integration tests
```

**Python:**
```
lib/
├── agents/
│   ├── specialized/
│   │   ├── akira_code_reviewer.py
│   │   └── test_akira_code_reviewer.py
│   └── test_base_agent.py
```

### 3. Test Independence

**Good:**
```python
def test_create_agent():
    """Each test creates its own data"""
    agent = create_test_agent()
    assert agent.name == "Test Agent"

def test_update_agent():
    """Independent of previous test"""
    agent = create_test_agent()
    agent.name = "Updated"
    assert agent.name == "Updated"
```

**Bad:**
```python
# Don't do this - tests depend on each other
def test_create_agent():
    global agent
    agent = Agent("Test")

def test_update_agent():
    # Depends on test_create_agent
    agent.name = "Updated"
```

### 4. Use Subtests

**Go:**
```go
func TestMultipleScenarios(t *testing.T) {
    tests := []struct{
        name string
        // ... test data
    }{
        // ... test cases
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Test implementation
        })
    }
}
```

### 5. Test Edge Cases

```python
def test_agent_with_empty_code():
    """Test with empty input"""
    result = agent.execute({"code": ""})
    assert result["error"] == "code cannot be empty"

def test_agent_with_very_long_code():
    """Test with large input"""
    long_code = "x" * 1000000
    result = agent.execute({"code": long_code})
    assert result["error"] == "code too long"

def test_agent_with_special_characters():
    """Test with special characters"""
    code = "def test():\n\treturn '\"\\n\\t'"
    result = agent.execute({"code": code})
    assert result["status"] == "completed"
```

---

## CI/CD Testing

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test-go:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Go
        uses: actions/setup-go@v4
        with:
          go-version: '1.22'
      
      - name: Run tests
        run: |
          go test -v -race -coverprofile=coverage.out ./...
          go tool cover -func=coverage.out
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.out

  test-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          pytest --cov=lib --cov-report=xml --cov-report=term
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
```

---

## Next Steps

- [Development Setup](setup.md) - Set up development environment
- [Contributing Guide](contributing.md) - Contribution guidelines
- [Code Style](code-style.md) - Coding standards
- [Debugging](debugging.md) - Debugging tips

---

*Last updated: 2025-12-23*
