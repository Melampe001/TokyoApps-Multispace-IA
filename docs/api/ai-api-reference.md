# Tokyo-IA AI API Reference

## Overview

The Tokyo-IA AI API provides HTTP endpoints for accessing multi-model AI capabilities with intelligent routing, cost optimization, and comprehensive metrics.

**Base URL**: `http://localhost:8080` (development)  
**Production URL**: `https://api.tokyo-ia.example.com` (when deployed)

## Authentication

Currently in development mode, no authentication is required. In production:

```http
Authorization: Bearer YOUR_API_KEY
```

## Rate Limiting

- **Development**: No limits
- **Production**: 1000 requests/minute per API key

## Endpoints

### Health Check

Check API service health and uptime.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "uptime": "2h30m15s",
  "version": "0.1.0"
}
```

**Status Codes**:
- `200`: Service is healthy
- `503`: Service unavailable

**Example**:
```bash
curl http://localhost:8080/health
```

---

### AI Completion

Request an AI model completion with intelligent routing.

**Endpoint**: `POST /ai/complete`

**Request Body**:
```json
{
  "prompt": "Your prompt text here",
  "task_type": "reasoning",
  "complexity": "moderate",
  "max_tokens": 1000,
  "temperature": 0.7,
  "privacy_required": false
}
```

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | The input prompt for the AI model |
| `task_type` | string | Yes | Type of task: `reasoning`, `code_generation`, `code_review`, `multimodal`, `documentation`, `chat` |
| `complexity` | string | No | Complexity level: `simple`, `moderate`, `complex` (default: `moderate`) |
| `max_tokens` | integer | No | Maximum tokens in response (default: 2048, max: 128000) |
| `temperature` | float | No | Sampling temperature 0.0-2.0 (default: 0.7) |
| `privacy_required` | boolean | No | Force local model for privacy (default: false) |

**Response**:
```json
{
  "content": "Generated response text...",
  "model": "claude-sonnet-4.5",
  "provider": "anthropic",
  "tokens_used": 523,
  "latency_ms": 1250,
  "cost_usd": 0.0042,
  "cached_result": false
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `content` | string | The generated response text |
| `model` | string | Name of the model that generated the response |
| `provider` | string | Provider name: `openai`, `anthropic`, `gemini`, `grok`, `llama` |
| `tokens_used` | integer | Total tokens consumed |
| `latency_ms` | integer | Response time in milliseconds |
| `cost_usd` | float | Cost of the request in USD |
| `cached_result` | boolean | Whether response was served from cache |

**Status Codes**:
- `200`: Success
- `400`: Invalid request (malformed JSON, missing required fields)
- `429`: Rate limit exceeded
- `500`: Internal server error
- `503`: No models available or budget exceeded

**Examples**:

**Simple Chat**:
```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the capital of France?",
    "task_type": "chat"
  }'
```

**Code Review**:
```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Review this code:\nfunc Add(a, b int) int {\n  return a + b\n}",
    "task_type": "code_review",
    "complexity": "simple",
    "max_tokens": 500
  }'
```

**Complex Reasoning**:
```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Solve this complex math problem: ...",
    "task_type": "reasoning",
    "complexity": "complex",
    "max_tokens": 2000,
    "temperature": 0.3
  }'
```

**Privacy-Sensitive Code Generation**:
```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Generate authentication logic for user login",
    "task_type": "code_generation",
    "privacy_required": true,
    "max_tokens": 1500
  }'
```

---

### Usage Metrics

Get current usage statistics and costs.

**Endpoint**: `GET /ai/metrics`

**Response**:
```json
{
  "total_requests": 1523,
  "total_cost_usd": 45.67,
  "providers": {
    "openai": {
      "requests": 234,
      "tokens": 125430,
      "cost_usd": 3.76,
      "avg_latency_ms": 1234.5,
      "error_rate": 0.02
    },
    "anthropic": {
      "requests": 890,
      "tokens": 445120,
      "cost_usd": 35.21,
      "avg_latency_ms": 987.3,
      "error_rate": 0.01
    },
    "llama": {
      "requests": 399,
      "tokens": 189340,
      "cost_usd": 0.0,
      "avg_latency_ms": 156.2,
      "error_rate": 0.005
    }
  },
  "budget": {
    "daily_limit_usd": 500.0,
    "current_spend_usd": 45.67,
    "percent_used": 9.13,
    "remaining_usd": 454.33
  }
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `total_requests` | integer | Total number of requests across all providers |
| `total_cost_usd` | float | Total cost in USD |
| `providers` | object | Breakdown by provider |
| `providers.*.requests` | integer | Request count for this provider |
| `providers.*.tokens` | integer | Total tokens used |
| `providers.*.cost_usd` | float | Cost for this provider |
| `providers.*.avg_latency_ms` | float | Average response time |
| `providers.*.error_rate` | float | Error rate (0.0-1.0) |
| `budget.daily_limit_usd` | float | Daily budget limit |
| `budget.current_spend_usd` | float | Current spending today |
| `budget.percent_used` | float | Percentage of budget used |
| `budget.remaining_usd` | float | Remaining budget |

**Status Codes**:
- `200`: Success

**Example**:
```bash
curl http://localhost:8080/ai/metrics
```

---

## Task Types

### reasoning
Complex reasoning, analysis, problem-solving tasks.

**Models Used**: OpenAI o3, Claude Opus, Claude Sonnet

**Best For**:
- Mathematical reasoning
- Logic puzzles
- Strategic analysis
- Complex decision making

### code_generation
Generate code snippets, functions, or complete programs.

**Models Used**: Claude Opus, OpenAI o3-mini, Llama 4 (privacy)

**Best For**:
- Writing new code
- Algorithm implementation
- Boilerplate generation
- Code refactoring

### code_review
Review and analyze existing code for quality, security, performance.

**Models Used**: Claude Opus, Claude Sonnet, OpenAI o3-mini

**Best For**:
- Security vulnerability detection
- Code quality assessment
- Performance optimization suggestions
- Best practices validation

### multimodal
Process and analyze images, diagrams, or mixed media.

**Models Used**: Gemini 3.0 Ultra, Grok 4

**Best For**:
- Image analysis
- Diagram understanding
- OCR tasks
- Visual question answering

### documentation
Generate documentation from code or create technical writing.

**Models Used**: Gemini 3.0, Claude Sonnet

**Best For**:
- API documentation
- Code comments
- Technical guides
- README generation

### chat
General conversational tasks.

**Models Used**: Claude Sonnet, Llama 4

**Best For**:
- Q&A
- General assistance
- Conversational interfaces
- Support chatbots

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error description",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional context"
  }
}
```

**Common Error Codes**:

| Code | Description | Resolution |
|------|-------------|------------|
| `INVALID_REQUEST` | Malformed request | Check request format and required fields |
| `BUDGET_EXCEEDED` | Daily budget limit reached | Wait for budget reset or increase limit |
| `NO_MODELS_AVAILABLE` | All models unavailable | Check API keys and provider status |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Implement request throttling |
| `INVALID_TASK_TYPE` | Unknown task type | Use valid task type from documentation |
| `TOKEN_LIMIT_EXCEEDED` | Requested tokens exceed model limit | Reduce max_tokens or prompt length |

**Example Error Response**:
```json
{
  "error": "Daily budget limit exceeded",
  "code": "BUDGET_EXCEEDED",
  "details": {
    "current_spend": 500.0,
    "daily_limit": 500.0,
    "reset_time": "2024-01-02T00:00:00Z"
  }
}
```

## SDKs and Client Libraries

### Go Client

```go
import "github.com/Melampe001/Tokyo-IA/internal/ai"

// See Model Router Guide for usage
```

### Python Client

```python
import requests

def complete(prompt, task_type="chat"):
    response = requests.post(
        "http://localhost:8080/ai/complete",
        json={
            "prompt": prompt,
            "task_type": task_type
        }
    )
    return response.json()

result = complete("Hello, world!", "chat")
print(result["content"])
```

### JavaScript/TypeScript Client

```typescript
async function complete(prompt: string, taskType: string = "chat") {
  const response = await fetch("http://localhost:8080/ai/complete", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      prompt,
      task_type: taskType,
    }),
  });
  return response.json();
}

const result = await complete("Hello, world!", "chat");
console.log(result.content);
```

## Best Practices

### 1. Set Appropriate Max Tokens

Always set `max_tokens` to avoid unexpectedly large responses:

```json
{
  "max_tokens": 1000
}
```

### 2. Use Specific Task Types

Use the most specific task type for better model selection:

```json
{
  "task_type": "code_review"  // Not "chat"
}
```

### 3. Implement Retry Logic

Implement exponential backoff for transient errors:

```python
import time

def complete_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(...)
            return response.json()
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise
```

### 4. Monitor Costs

Regularly check metrics to track spending:

```bash
# Monitor costs
curl http://localhost:8080/ai/metrics | jq '.budget'
```

### 5. Cache Results

For repeated queries, implement client-side caching:

```python
cache = {}

def complete_cached(prompt, task_type):
    key = f"{prompt}:{task_type}"
    if key in cache:
        return cache[key]
    
    result = complete(prompt, task_type)
    cache[key] = result
    return result
```

## Rate Limiting

Production rate limits (per API key):
- **Standard**: 1000 requests/minute, 100,000 requests/day
- **Premium**: 5000 requests/minute, 500,000 requests/day
- **Enterprise**: Custom limits

Rate limit headers in response:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1640000000
```

## Webhooks (Planned)

Future support for webhooks to receive completion results asynchronously:

```json
{
  "prompt": "Long analysis task...",
  "task_type": "reasoning",
  "webhook_url": "https://your-app.com/webhook",
  "webhook_secret": "your-secret"
}
```

## Support

- Documentation: `/docs`
- GitHub Issues: `https://github.com/Melampe001/Tokyo-IA/issues`
- Email: `support@tokyo-ia.example.com`

## Changelog

### v0.1.0 (Current)
- Initial API release
- Support for 5 model providers
- Intelligent routing
- Budget tracking
- Metrics endpoint
- Caching support
