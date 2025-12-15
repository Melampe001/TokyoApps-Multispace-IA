# AI API Reference

## Base URL

```
http://localhost:8080
```

## Authentication

Currently, the API does not require authentication (development mode).

**Production:** Will require API key in `Authorization` header:
```
Authorization: Bearer <your-api-key>
```

## Endpoints

### 1. AI Completion

Process AI completion requests with intelligent model routing.

#### Request

```http
POST /ai/complete
Content-Type: application/json
```

**Body Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | The input prompt/question for the AI |
| `task_type` | string | No | "general" | Type of task (see Task Types below) |
| `max_tokens` | integer | No | 2048 | Maximum tokens in response |
| `temperature` | float | No | 0.7 | Randomness (0.0-1.0) |

**Task Types:**
- `reasoning` - Logic, analysis, problem-solving
- `creative` - Writing, storytelling, creative content
- `code_review` - Code analysis and review
- `code_generation` - Writing new code
- `translation` - Language translation
- `general` - Default for everything else

**Example Request:**

```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum entanglement in simple terms",
    "task_type": "reasoning",
    "max_tokens": 500,
    "temperature": 0.5
  }'
```

```json
{
  "prompt": "Explain quantum entanglement in simple terms",
  "task_type": "reasoning",
  "max_tokens": 500,
  "temperature": 0.5
}
```

#### Response

**Success (200 OK):**

```json
{
  "content": "Quantum entanglement is a phenomenon where two particles...",
  "model": "claude-3-mock",
  "provider": "anthropic",
  "tokens_used": 87,
  "latency_ms": 125,
  "cache_hit": false
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `content` | string | The AI-generated response |
| `model` | string | The specific model used |
| `provider` | string | The AI provider (openai, anthropic, gemini) |
| `tokens_used` | integer | Number of tokens consumed |
| `latency_ms` | integer | Response time in milliseconds |
| `cache_hit` | boolean | Whether response came from cache |

**Error Responses:**

**400 Bad Request:**
```json
{
  "error": "Prompt is required"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Completion failed: provider unavailable"
}
```

**Common Error Codes:**
- `400` - Invalid request (missing/invalid parameters)
- `429` - Rate limit exceeded
- `500` - Internal server error
- `503` - Service unavailable

---

### 2. Get Metrics

Retrieve system usage statistics and performance metrics.

#### Request

```http
GET /ai/metrics
```

**Example Request:**

```bash
curl http://localhost:8080/ai/metrics
```

#### Response

**Success (200 OK):**

```json
{
  "total_requests": 1543,
  "success_requests": 1521,
  "failed_requests": 22,
  "cache_hits": 412,
  "total_tokens": 256789,
  "success_rate": "98.57%",
  "cache_hit_rate": "27.08%",
  "average_latency": "142ms",
  "provider_stats": {
    "openai": {
      "Requests": 823,
      "AverageLatency": "135ms",
      "MinLatency": "45ms",
      "MaxLatency": "450ms"
    },
    "anthropic": {
      "Requests": 698,
      "AverageLatency": "150ms",
      "MinLatency": "52ms",
      "MaxLatency": "380ms"
    },
    "gemini": {
      "Requests": 22,
      "AverageLatency": "138ms",
      "MinLatency": "60ms",
      "MaxLatency": "250ms"
    }
  }
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `total_requests` | integer | Total API requests made |
| `success_requests` | integer | Successfully completed requests |
| `failed_requests` | integer | Failed requests |
| `cache_hits` | integer | Requests served from cache |
| `total_tokens` | integer | Total tokens consumed |
| `success_rate` | string | Percentage of successful requests |
| `cache_hit_rate` | string | Percentage of cached responses |
| `average_latency` | string | Mean response time |
| `provider_stats` | object | Per-provider statistics |

**Provider Stats Object:**

| Field | Type | Description |
|-------|------|-------------|
| `Requests` | integer | Requests to this provider |
| `AverageLatency` | string | Mean response time |
| `MinLatency` | string | Fastest response time |
| `MaxLatency` | string | Slowest response time |

---

### 3. Clear Cache

Clear the response cache, forcing fresh requests to providers.

#### Request

```http
POST /ai/cache/clear
```

**Example Request:**

```bash
curl -X POST http://localhost:8080/ai/cache/clear
```

#### Response

**Success (200 OK):**

```json
{
  "status": "cache cleared"
}
```

---

### 4. Health Check

Check if the API server is running and healthy.

#### Request

```http
GET /health
```

**Example Request:**

```bash
curl http://localhost:8080/health
```

#### Response

**Success (200 OK):**

```json
{
  "status": "ok"
}
```

---

## Rate Limiting

**Current:** No rate limiting (development mode)

**Production:** Rate limits will be enforced:
- 100 requests per minute per API key
- 1000 requests per hour per API key

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1640000000
```

**Rate Limit Exceeded (429):**
```json
{
  "error": "Rate limit exceeded",
  "retry_after": 45
}
```

---

## Request Examples

### cURL

**Basic Request:**
```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Hello, AI!","task_type":"general"}'
```

**With All Parameters:**
```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a function to sort an array",
    "task_type": "code_generation",
    "max_tokens": 300,
    "temperature": 0.3
  }'
```

### Python

```python
import requests
import json

url = "http://localhost:8080/ai/complete"
headers = {"Content-Type": "application/json"}
data = {
    "prompt": "Explain neural networks",
    "task_type": "reasoning",
    "max_tokens": 500,
    "temperature": 0.6
}

response = requests.post(url, headers=headers, json=data)
result = response.json()

print(f"Provider: {result['provider']}")
print(f"Content: {result['content']}")
print(f"Tokens: {result['tokens_used']}")
```

### Go

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
)

type CompletionRequest struct {
    Prompt      string  `json:"prompt"`
    TaskType    string  `json:"task_type"`
    MaxTokens   int     `json:"max_tokens,omitempty"`
    Temperature float64 `json:"temperature,omitempty"`
}

type CompletionResponse struct {
    Content    string `json:"content"`
    Model      string `json:"model"`
    Provider   string `json:"provider"`
    TokensUsed int    `json:"tokens_used"`
    LatencyMS  int    `json:"latency_ms"`
    CacheHit   bool   `json:"cache_hit"`
}

func main() {
    req := CompletionRequest{
        Prompt:      "What is Go?",
        TaskType:    "general",
        MaxTokens:   200,
        Temperature: 0.7,
    }

    jsonData, _ := json.Marshal(req)
    
    resp, err := http.Post(
        "http://localhost:8080/ai/complete",
        "application/json",
        bytes.NewBuffer(jsonData),
    )
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

    body, _ := io.ReadAll(resp.Body)
    
    var result CompletionResponse
    json.Unmarshal(body, &result)

    fmt.Printf("Provider: %s\n", result.Provider)
    fmt.Printf("Content: %s\n", result.Content)
}
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

async function complete(prompt, taskType = 'general') {
  try {
    const response = await axios.post('http://localhost:8080/ai/complete', {
      prompt: prompt,
      task_type: taskType,
      max_tokens: 500,
      temperature: 0.7
    });

    const { content, provider, tokens_used, cache_hit } = response.data;
    
    console.log(`Provider: ${provider}`);
    console.log(`Content: ${content}`);
    console.log(`Tokens: ${tokens_used}`);
    console.log(`Cached: ${cache_hit}`);
    
    return response.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

complete("Explain async/await in JavaScript", "reasoning");
```

### JavaScript (Fetch API)

```javascript
async function complete(prompt, taskType = 'general') {
  const response = await fetch('http://localhost:8080/ai/complete', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      prompt: prompt,
      task_type: taskType,
      max_tokens: 500,
      temperature: 0.7
    })
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

complete("Write a haiku about coding", "creative")
  .then(result => console.log(result))
  .catch(error => console.error(error));
```

---

## Error Handling Best Practices

### 1. Retry Logic

```python
import time

def complete_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json={"prompt": prompt})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:  # Rate limit
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

### 2. Timeout Handling

```go
client := &http.Client{
    Timeout: 30 * time.Second,
}

ctx, cancel := context.WithTimeout(context.Background(), 25*time.Second)
defer cancel()

req, _ := http.NewRequestWithContext(ctx, "POST", url, body)
resp, err := client.Do(req)
```

### 3. Validation

```javascript
function validateRequest(prompt, taskType) {
  if (!prompt || prompt.trim() === '') {
    throw new Error('Prompt cannot be empty');
  }
  
  const validTaskTypes = [
    'reasoning', 'creative', 'code_review', 
    'code_generation', 'translation', 'general'
  ];
  
  if (taskType && !validTaskTypes.includes(taskType)) {
    throw new Error(`Invalid task_type: ${taskType}`);
  }
}
```

---

## WebSocket Support (Future)

**Planned feature for streaming responses:**

```javascript
const ws = new WebSocket('ws://localhost:8080/ai/stream');

ws.send(JSON.stringify({
  prompt: "Write a long story...",
  task_type: "creative",
  stream: true
}));

ws.onmessage = (event) => {
  const chunk = JSON.parse(event.data);
  process.stdout.write(chunk.content);
};
```

---

## Changelog

### v1.0.0 (Current)
- Initial REST API
- Basic completion endpoint
- Metrics endpoint
- Cache management
- Health checks

### Planned (v2.0.0)
- WebSocket streaming
- Batch requests
- Authentication
- Rate limiting
- Request validation

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/Melampe001/Tokyo-IA/issues
- Documentation: `/docs`
- Architecture: `docs/architecture/ai-models-integration-architecture.md`
- User Guide: `docs/guides/ai-model-router-guide.md`
