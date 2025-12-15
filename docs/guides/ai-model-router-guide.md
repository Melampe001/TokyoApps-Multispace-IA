# AI Model Router Guide

## Table of Contents
- [Getting Started](#getting-started)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [API Reference](#api-reference)
- [Python Agents](#python-agents)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Getting Started

### Prerequisites

**Go Environment:**
- Go 1.21 or later
- Make (for build automation)

**Python Environment (optional, for agents):**
- Python 3.9 or later
- pip package manager

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA
```

2. **Install Go dependencies:**
```bash
go mod download
```

3. **Install Python dependencies (optional):**
```bash
pip install -r requirements.txt
```

### Building

**Build AI API server:**
```bash
make ai-build
```

This creates `bin/ai-api` executable.

## Quick Start

### 1. Start the AI API Server

```bash
make ai-run
```

Or directly:
```bash
./bin/ai-api
```

The server starts on `http://localhost:8080` by default.

### 2. Make Your First Request

```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is machine learning?",
    "task_type": "general"
  }'
```

**Response:**
```json
{
  "content": "Mock response from gpt-4-mock for prompt: 'What is machine learning?'",
  "model": "gpt-4-mock",
  "provider": "openai",
  "tokens_used": 15,
  "latency_ms": 102,
  "cache_hit": false
}
```

### 3. Run the Interactive Demo

```bash
make ai-demo
```

This runs `scripts/demo-ai-integration.sh` which demonstrates all features.

## Configuration

### API Keys

For production use with real AI providers, set environment variables:

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic (Claude)
export ANTHROPIC_API_KEY="sk-ant-..."

# Google Gemini
export GEMINI_API_KEY="..."
```

### Router Configuration

The router is configured in `cmd/ai-api/main.go`:

```go
config := ai.RouterConfig{
    EnableCache:     true,              // Enable response caching
    CacheTTL:        10 * time.Minute,  // Cache time-to-live
    DefaultProvider: ai.ProviderOpenAI,  // Fallback provider
    TaskRouting: map[ai.TaskType]ai.Provider{
        ai.TaskTypeReasoning:   ai.ProviderAnthropic,
        ai.TaskTypeCreative:    ai.ProviderOpenAI,
        ai.TaskTypeCodeReview:  ai.ProviderAnthropic,
        ai.TaskTypeCodeGen:     ai.ProviderOpenAI,
        ai.TaskTypeTranslation: ai.ProviderGemini,
    },
}
```

**Customization:**
- Change `DefaultProvider` to your preferred fallback
- Modify `TaskRouting` to use different providers for tasks
- Adjust `CacheTTL` based on your use case
- Disable caching with `EnableCache: false` for testing

### Server Configuration

**Port:**
```bash
export PORT=9000
./bin/ai-api
```

**Timeouts (in code):**
```go
server := &http.Server{
    Addr:         ":8080",
    ReadTimeout:  15 * time.Second,
    WriteTimeout: 45 * time.Second,
    IdleTimeout:  60 * time.Second,
}
```

## Usage Examples

### Task Types

The system routes requests based on task type:

#### 1. Reasoning Tasks
Best for: Logic, analysis, problem-solving

```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain the implications of quantum entanglement",
    "task_type": "reasoning",
    "max_tokens": 500,
    "temperature": 0.3
  }'
```

**Routes to:** Anthropic Claude (reasoning specialist)

#### 2. Creative Tasks
Best for: Writing, storytelling, creative content

```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a short story about a robot learning to paint",
    "task_type": "creative",
    "max_tokens": 800,
    "temperature": 0.9
  }'
```

**Routes to:** OpenAI GPT-4 (creative specialist)

#### 3. Code Review
Best for: Code analysis, security review, best practices

```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Review this function:\nfunc ProcessData(data []byte) error {\n    // process data\n    return nil\n}",
    "task_type": "code_review",
    "max_tokens": 600
  }'
```

**Routes to:** Anthropic Claude (code review specialist)

#### 4. Code Generation
Best for: Writing new code, implementing features

```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Go function to calculate Fibonacci numbers",
    "task_type": "code_generation",
    "max_tokens": 400
  }'
```

**Routes to:** OpenAI GPT-4 (code generation specialist)

#### 5. Translation
Best for: Language translation

```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Translate to Spanish: The quick brown fox jumps over the lazy dog",
    "task_type": "translation",
    "max_tokens": 200
  }'
```

**Routes to:** Google Gemini (translation specialist)

### Advanced Options

#### Force Specific Model

```bash
curl -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Your prompt here",
    "task_type": "general",
    "model": {
      "provider": "anthropic",
      "name": "claude-3-opus"
    }
  }'
```

#### Control Randomness

```bash
# More deterministic (temperature = 0.0 - 0.3)
{
  "prompt": "What is 2+2?",
  "temperature": 0.0
}

# Balanced (temperature = 0.5 - 0.7)
{
  "prompt": "Explain quantum physics",
  "temperature": 0.7
}

# More creative (temperature = 0.8 - 1.0)
{
  "prompt": "Write a poem",
  "temperature": 0.9
}
```

## API Reference

### POST /ai/complete

Process an AI completion request.

**Request:**
```json
{
  "prompt": "string (required)",
  "task_type": "string (optional, default: general)",
  "max_tokens": "number (optional, default: 2048)",
  "temperature": "number (optional, default: 0.7)"
}
```

**Response:**
```json
{
  "content": "string",
  "model": "string",
  "provider": "string",
  "tokens_used": "number",
  "latency_ms": "number",
  "cache_hit": "boolean"
}
```

### GET /ai/metrics

Get system usage metrics.

**Response:**
```json
{
  "total_requests": 150,
  "success_requests": 148,
  "failed_requests": 2,
  "cache_hits": 45,
  "total_tokens": 12500,
  "success_rate": "98.67%",
  "cache_hit_rate": "30.41%",
  "average_latency": "125ms",
  "provider_stats": {
    "openai": {
      "Requests": 80,
      "AverageLatency": "120ms",
      "MinLatency": "50ms",
      "MaxLatency": "200ms"
    },
    "anthropic": {
      "Requests": 68,
      "AverageLatency": "130ms",
      "MinLatency": "60ms",
      "MaxLatency": "220ms"
    }
  }
}
```

### POST /ai/cache/clear

Clear the response cache.

**Response:**
```json
{
  "status": "cache cleared"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## Python Agents

### Using CrewAI Workflows

The Python agents provide high-level workflows for complex tasks.

#### 1. Research Workflow

```python
from lib.agents import run_workflow

result = run_workflow(
    "research",
    topic="Artificial Intelligence Ethics"
)
print(result["result"])
```

#### 2. Code Review Workflow

```python
result = run_workflow(
    "code_review",
    code="""
def calculate_total(prices):
    total = 0
    for price in prices:
        total += price
    return total
""",
    language="python"
)
print(result["result"])
```

#### 3. Content Creation Workflow

```python
result = run_workflow(
    "content_creation",
    topic="The Future of Renewable Energy",
    content_type="blog"
)
print(result["result"])
```

#### 4. Data Analysis Workflow

```python
result = run_workflow(
    "data_analysis",
    data_description="Sales data from Q1-Q4 2024",
    analysis_goals=[
        "Identify seasonal trends",
        "Find top-performing products",
        "Recommend optimization strategies"
    ]
)
print(result["result"])
```

### Using Custom Tools

```python
from lib.agents.tools import (
    analyze_code,
    count_words,
    validate_url
)

# Analyze code
code_metrics = analyze_code("def hello(): print('hi')")

# Count words
stats = count_words("Hello world!")

# Validate URL
url_info = validate_url("https://example.com")
```

## Troubleshooting

### Server Won't Start

**Problem:** Port already in use
```
Error: listen tcp :8080: bind: address already in use
```

**Solution:**
```bash
# Find process using port 8080
lsof -i :8080

# Kill the process
kill <PID>

# Or use a different port
PORT=9000 ./bin/ai-api
```

### API Key Errors

**Problem:** Provider returns authentication error
```
Error: OPENAI_API_KEY not set
```

**Solution:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Verify API key is set:
```bash
echo $OPENAI_API_KEY
```

### Request Timeouts

**Problem:** Requests taking too long
```
Error: context deadline exceeded
```

**Solutions:**
1. Reduce `max_tokens` in request
2. Increase timeout in code (default: 30s)
3. Check provider API status
4. Use caching for repeated requests

### Cache Issues

**Problem:** Getting stale responses

**Solution:** Clear the cache
```bash
curl -X POST http://localhost:8080/ai/cache/clear
```

**Problem:** Cache hit rate too low

**Solutions:**
1. Increase `CacheTTL`
2. Normalize prompts (lowercase, trim whitespace)
3. Check if `temperature` varies (affects cache key)

## Best Practices

### 1. Task Type Selection

Choose the right task type for optimal routing:
- **Reasoning**: Analysis, logic, explanations
- **Creative**: Stories, poems, creative content
- **Code Review**: Security, best practices, bug finding
- **Code Generation**: Writing new code
- **Translation**: Language conversion
- **General**: Everything else

### 2. Prompt Engineering

**Be specific:**
```
❌ "Write code"
✓ "Write a Python function to validate email addresses using regex"
```

**Provide context:**
```
❌ "Fix this"
✓ "Review this Go function for memory leaks and race conditions"
```

**Use examples:**
```
"Translate to French. Example: Hello → Bonjour. Now translate: Good morning"
```

### 3. Token Management

**Estimate tokens:**
- ~4 characters = 1 token
- 1 word ≈ 1.3 tokens
- Code ≈ 1 token per symbol

**Optimize requests:**
```json
{
  "prompt": "Summarize in 2 sentences: [long text]",
  "max_tokens": 100
}
```

### 4. Temperature Settings

| Use Case | Temperature | Example |
|----------|-------------|---------|
| Factual answers | 0.0 - 0.3 | "What is the capital of France?" |
| Explanations | 0.5 - 0.7 | "Explain photosynthesis" |
| Creative writing | 0.8 - 1.0 | "Write a sci-fi story" |

### 5. Error Handling

Always handle errors in client code:

```go
resp, err := http.Post(url, contentType, body)
if err != nil {
    log.Printf("Request failed: %v", err)
    // Implement retry logic
    return
}
defer resp.Body.Close()

if resp.StatusCode != http.StatusOK {
    log.Printf("API error: %d", resp.StatusCode)
    // Handle specific error codes
}
```

### 6. Monitoring

**Track key metrics:**
- Request success rate
- Average latency
- Cache hit rate
- Token usage
- Cost per request

**Use the metrics endpoint:**
```bash
watch -n 5 'curl -s http://localhost:8080/ai/metrics | jq'
```

### 7. Production Deployment

**Security checklist:**
- [ ] API keys in secrets manager (not env vars)
- [ ] Rate limiting implemented
- [ ] Request authentication
- [ ] Input validation
- [ ] HTTPS/TLS enabled
- [ ] Audit logging
- [ ] Error monitoring (Sentry)

**Performance checklist:**
- [ ] Caching enabled
- [ ] Connection pooling
- [ ] Load balancing
- [ ] Health checks
- [ ] Graceful shutdown

## Next Steps

1. **Replace Mock Clients**: Implement real provider clients
2. **Add Authentication**: Secure your API
3. **Enable Monitoring**: Set up Prometheus + Grafana
4. **Scale Horizontally**: Deploy multiple instances
5. **Optimize Costs**: Track and reduce token usage

## Support

- **Documentation**: `/docs`
- **Issues**: https://github.com/Melampe001/Tokyo-IA/issues
- **Architecture**: See `docs/architecture/ai-models-integration-architecture.md`
- **API Reference**: See `docs/api/ai-api-reference.md`
