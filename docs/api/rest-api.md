# 🔌 REST API Reference

Complete REST API documentation for Tokyo-IA. All endpoints are available at the base URL.

## 📋 Table of Contents

- [Base URL](#base-url)
- [Authentication](#authentication)
- [Response Format](#response-format)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Endpoints](#endpoints)
  - [Health Check](#health-check)
  - [Agents](#agents)
  - [Tasks](#tasks)
  - [Workflows](#workflows)
  - [Metrics](#metrics)

---

## Base URL

| Environment | URL |
|-------------|-----|
| **Production** | `https://tokyo-ia.up.railway.app` |
| **Staging** | `https://tokyo-ia-staging.up.railway.app` |
| **Local** | `http://localhost:8080` |

---

## Authentication

### Current: API Key (Optional)

For development, authentication is optional. For production deployments, set `API_KEY_REQUIRED=true`.

```bash
curl -H "X-API-Key: your-api-key" \
  https://tokyo-ia.up.railway.app/api/agents
```

### Coming Soon: JWT

JWT-based authentication is planned for a future release.

---

## Response Format

### Success Response

All successful responses follow this structure:

```json
{
  "success": true,
  "data": { /* response data */ },
  "metadata": {
    "timestamp": "2025-12-23T04:25:00Z",
    "request_id": "req_abc123"
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid agent ID format",
    "details": {
      "field": "agent_id",
      "constraint": "must be alphanumeric with dashes"
    }
  },
  "metadata": {
    "timestamp": "2025-12-23T04:25:00Z",
    "request_id": "req_abc123"
  }
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 202 | Accepted | Request accepted, processing async |
| 400 | Bad Request | Invalid request format or parameters |
| 401 | Unauthorized | Authentication required or failed |
| 403 | Forbidden | Access denied |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource conflict (e.g., duplicate) |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily unavailable |

### Error Codes

| Code | Description |
|------|-------------|
| `INVALID_REQUEST` | Request validation failed |
| `AGENT_NOT_FOUND` | Agent ID does not exist |
| `TASK_NOT_FOUND` | Task ID does not exist |
| `WORKFLOW_NOT_FOUND` | Workflow ID does not exist |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `DATABASE_ERROR` | Database operation failed |
| `AGENT_UNAVAILABLE` | Agent temporarily unavailable |
| `TASK_TIMEOUT` | Task execution timeout |
| `INTERNAL_ERROR` | Unexpected server error |

---

## Rate Limiting

### Limits

| Environment | Requests/Minute | Burst |
|-------------|----------------|-------|
| Development | Unlimited | - |
| Production | 60 | 10 |

### Headers

Response includes rate limit headers:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1703304000
```

### Rate Limit Exceeded Response

```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 45 seconds.",
    "retry_after": 45
  }
}
```

---

## Endpoints

### Health Check

#### GET /health

Check API server health status.

**Request:**
```bash
curl http://localhost:8080/health
```

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-12-23T04:25:00Z",
  "version": "1.0.0"
}
```

---

### Agents

#### GET /api/agents

List all registered agents.

**Request:**
```bash
curl http://localhost:8080/api/agents
```

**Response:** `200 OK`
```json
[
  {
    "id": "akira-001",
    "name": "Akira - Code Review Master",
    "role": "code_review",
    "model": "claude-opus-4.1",
    "specialties": ["security", "performance", "architecture"],
    "status": "active",
    "personality_emoji": "侍",
    "total_tasks_completed": 1247,
    "average_latency_ms": 2340,
    "success_rate": 98.5,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-12-23T04:20:00Z"
  },
  {
    "id": "yuki-002",
    "name": "Yuki - Test Engineering Specialist",
    "role": "test_engineering",
    "model": "openai-o3",
    "specialties": ["unit_testing", "integration_testing", "e2e_testing"],
    "status": "active",
    "personality_emoji": "❄️",
    "total_tasks_completed": 892,
    "average_latency_ms": 1980,
    "success_rate": 97.2,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-12-23T04:15:00Z"
  }
  // ... more agents
]
```

---

#### GET /api/agents/:id

Get detailed information about a specific agent.

**Parameters:**
- `id` (path) - Agent ID (e.g., "akira-001")

**Request:**
```bash
curl http://localhost:8080/api/agents/akira-001
```

**Response:** `200 OK`
```json
{
  "id": "akira-001",
  "name": "Akira - Code Review Master",
  "role": "code_review",
  "model": "claude-opus-4.1",
  "specialties": ["security", "performance", "architecture"],
  "backstory": "Master code reviewer with expertise in security...",
  "personality_emoji": "侍",
  "status": "active",
  "total_tasks_completed": 1247,
  "total_tokens_used": 5482394,
  "average_latency_ms": 2340,
  "success_rate": 98.5,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-12-23T04:20:00Z",
  "metadata": {
    "max_tokens": 200000,
    "temperature": 0.3,
    "supported_languages": ["python", "javascript", "go", "java"]
  }
}
```

**Errors:**
- `404 Not Found` - Agent ID does not exist

---

#### GET /api/agents/:id/stats

Get performance statistics for an agent.

**Parameters:**
- `id` (path) - Agent ID
- `timeframe` (query, optional) - Time period: "1h", "24h", "7d", "30d", "all" (default: "all")

**Request:**
```bash
curl http://localhost:8080/api/agents/akira-001/stats?timeframe=24h
```

**Response:** `200 OK`
```json
{
  "agent_id": "akira-001",
  "timeframe": "24h",
  "total_tasks": 42,
  "completed_tasks": 41,
  "failed_tasks": 1,
  "pending_tasks": 0,
  "average_latency_ms": 2156,
  "p95_latency_ms": 3420,
  "p99_latency_ms": 4890,
  "total_tokens_used": 124583,
  "total_cost_usd": 3.12,
  "success_rate": 97.6,
  "tasks_by_type": {
    "code_review": 35,
    "security_audit": 7
  }
}
```

---

#### GET /api/agents/:id/tasks

Get recent tasks for an agent.

**Parameters:**
- `id` (path) - Agent ID
- `limit` (query, optional) - Number of tasks (default: 20, max: 100)
- `offset` (query, optional) - Pagination offset (default: 0)
- `status` (query, optional) - Filter by status: "pending", "running", "completed", "failed"

**Request:**
```bash
curl http://localhost:8080/api/agents/akira-001/tasks?limit=10&status=completed
```

**Response:** `200 OK`
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "agent_id": "akira-001",
      "task_type": "code_review",
      "description": "Review authentication code",
      "status": "completed",
      "started_at": "2025-12-23T04:20:00Z",
      "completed_at": "2025-12-23T04:20:03Z",
      "duration_ms": 3120,
      "tokens_used": 2847,
      "cost_usd": 0.071
    }
    // ... more tasks
  ],
  "pagination": {
    "total": 1247,
    "limit": 10,
    "offset": 0,
    "has_more": true
  }
}
```

---

### Tasks

#### POST /api/tasks

Create a new agent task.

**Request Body:**
```json
{
  "agent_id": "akira-001",
  "task_type": "code_review",
  "description": "Review authentication function for security issues",
  "input_data": {
    "code": "def authenticate(username, password):\n    query = f\"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'\"",
    "language": "python",
    "focus_areas": ["security", "best_practices"]
  }
}
```

**Request:**
```bash
curl -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "akira-001",
    "task_type": "code_review",
    "description": "Review authentication code",
    "input_data": {
      "code": "def authenticate(u, p): ...",
      "language": "python"
    }
  }'
```

**Response:** `202 Accepted`
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "agent_id": "akira-001",
  "status": "pending",
  "created_at": "2025-12-23T04:25:00Z",
  "estimated_completion": "2025-12-23T04:25:05Z"
}
```

**Errors:**
- `400 Bad Request` - Invalid request format
- `404 Not Found` - Agent not found
- `503 Service Unavailable` - Agent unavailable

---

#### GET /api/tasks/:id

Get task status and results.

**Parameters:**
- `id` (path) - Task ID (UUID)

**Request:**
```bash
curl http://localhost:8080/api/tasks/550e8400-e29b-41d4-a716-446655440000
```

**Response:** `200 OK`

**Pending Task:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "agent_id": "akira-001",
  "task_type": "code_review",
  "description": "Review authentication code",
  "status": "pending",
  "created_at": "2025-12-23T04:25:00Z"
}
```

**Completed Task:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "agent_id": "akira-001",
  "task_type": "code_review",
  "description": "Review authentication code",
  "status": "completed",
  "input_data": { /* ... */ },
  "output_data": {
    "severity": "critical",
    "issues": [
      {
        "type": "SQL Injection",
        "line": 2,
        "severity": "critical",
        "description": "Vulnerable to SQL injection attack",
        "recommendation": "Use parameterized queries"
      },
      {
        "type": "Password Security",
        "line": 2,
        "severity": "high",
        "description": "Password stored in plaintext",
        "recommendation": "Use bcrypt for password hashing"
      }
    ],
    "recommendations": [
      "Use SQLAlchemy ORM or parameterized queries",
      "Implement password hashing with bcrypt",
      "Add input validation",
      "Add rate limiting"
    ]
  },
  "started_at": "2025-12-23T04:25:01Z",
  "completed_at": "2025-12-23T04:25:04Z",
  "duration_ms": 3120,
  "tokens_used": 2847,
  "cost_usd": 0.071,
  "created_at": "2025-12-23T04:25:00Z"
}
```

**Failed Task:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "agent_id": "akira-001",
  "status": "failed",
  "error_message": "Task timeout after 300 seconds",
  "retry_count": 3,
  "created_at": "2025-12-23T04:20:00Z",
  "started_at": "2025-12-23T04:20:01Z",
  "completed_at": "2025-12-23T04:25:01Z"
}
```

**Errors:**
- `404 Not Found` - Task ID does not exist

---

#### PUT /api/tasks/:id

Update task status (admin only).

**Parameters:**
- `id` (path) - Task ID

**Request Body:**
```json
{
  "status": "cancelled"
}
```

**Response:** `200 OK`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "cancelled",
  "updated_at": "2025-12-23T04:25:00Z"
}
```

---

### Workflows

#### POST /api/workflows

Create and execute a multi-agent workflow.

**Request Body:**
```json
{
  "name": "Full Code Review Workflow",
  "description": "Complete code review with all agents",
  "workflow_type": "code_review",
  "input_data": {
    "code": "def process_payment(amount): ...",
    "language": "python"
  }
}
```

**Response:** `202 Accepted`
```json
{
  "workflow_id": "670e9511-f3ac-52e5-b827-557766551111",
  "name": "Full Code Review Workflow",
  "status": "pending",
  "total_tasks": 4,
  "completed_tasks": 0,
  "created_at": "2025-12-23T04:25:00Z",
  "estimated_completion": "2025-12-23T04:27:00Z"
}
```

---

#### GET /api/workflows/:id

Get workflow status and results.

**Parameters:**
- `id` (path) - Workflow ID (UUID)

**Response:** `200 OK`
```json
{
  "id": "670e9511-f3ac-52e5-b827-557766551111",
  "name": "Full Code Review Workflow",
  "description": "Complete code review with all agents",
  "status": "completed",
  "workflow_type": "code_review",
  "total_tasks": 4,
  "completed_tasks": 4,
  "failed_tasks": 0,
  "started_at": "2025-12-23T04:25:00Z",
  "completed_at": "2025-12-23T04:27:15Z",
  "duration_ms": 135000,
  "total_tokens_used": 12483,
  "total_cost_usd": 0.31,
  "created_at": "2025-12-23T04:25:00Z"
}
```

---

#### GET /api/workflows/:id/tasks

Get all tasks in a workflow.

**Response:** `200 OK`
```json
{
  "workflow_id": "670e9511-f3ac-52e5-b827-557766551111",
  "tasks": [
    {
      "id": "task-1",
      "agent_id": "akira-001",
      "task_type": "code_review",
      "status": "completed",
      "order": 1
    },
    {
      "id": "task-2",
      "agent_id": "yuki-002",
      "task_type": "generate_tests",
      "status": "completed",
      "order": 2
    },
    {
      "id": "task-3",
      "agent_id": "hiro-003",
      "task_type": "setup_cicd",
      "status": "completed",
      "order": 3
    },
    {
      "id": "task-4",
      "agent_id": "sakura-004",
      "task_type": "generate_docs",
      "status": "completed",
      "order": 4
    }
  ]
}
```

---

### Metrics

#### GET /api/metrics

Get system-wide metrics.

**Parameters:**
- `agent_id` (query, optional) - Filter by agent
- `metric_type` (query, optional) - Type: "latency", "tokens", "cost", "success_rate"
- `timeframe` (query, optional) - "1h", "24h", "7d", "30d"

**Response:** `200 OK`
```json
{
  "timeframe": "24h",
  "metrics": {
    "total_tasks": 342,
    "completed_tasks": 335,
    "failed_tasks": 7,
    "average_latency_ms": 2234,
    "total_tokens_used": 847392,
    "total_cost_usd": 21.18,
    "success_rate": 97.95
  },
  "by_agent": {
    "akira-001": {
      "tasks": 142,
      "latency_ms": 2456,
      "tokens": 325847,
      "cost_usd": 8.15
    }
    // ... more agents
  }
}
```

---

## Pagination

List endpoints support pagination:

**Parameters:**
- `limit` - Items per page (default: 20, max: 100)
- `offset` - Starting position (default: 0)

**Example:**
```bash
curl "http://localhost:8080/api/agents/akira-001/tasks?limit=50&offset=100"
```

**Response includes:**
```json
{
  "data": [ /* ... */ ],
  "pagination": {
    "total": 1247,
    "limit": 50,
    "offset": 100,
    "has_more": true
  }
}
```

---

## Next Steps

- **[OpenAPI Spec](openapi.yaml)** - Machine-readable API specification
- **[Authentication](authentication.md)** - API authentication details
- **[Examples](examples.md)** - Code examples in multiple languages

---

*Last updated: 2025-12-23*
