# AI Models Integration Architecture

## Overview

Tokyo-IA implements a sophisticated multi-model AI orchestration system that intelligently routes requests to different AI providers based on task requirements. This architecture enables optimal performance, cost efficiency, and reliability by leveraging the strengths of multiple AI models.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Application                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI API Server (Go)                          │
│                      cmd/ai-api/main.go                          │
│                                                                   │
│  Endpoints:                                                       │
│  • POST /ai/complete    - AI completion requests                 │
│  • GET  /ai/metrics     - Usage metrics                          │
│  • POST /ai/cache/clear - Cache management                       │
│  • GET  /health         - Health check                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Model Router                               │
│                 internal/ai/model_router.go                      │
│                                                                   │
│  Features:                                                        │
│  • Intelligent task-based routing                                │
│  • Request caching                                                │
│  • Metrics collection                                             │
│  • Provider failover                                              │
└──────┬──────────────────┬──────────────────┬─────────────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   OpenAI    │    │  Anthropic  │    │   Gemini    │
│   Client    │    │   Client    │    │   Client    │
│             │    │             │    │             │
│  GPT-4      │    │  Claude-3   │    │  Gemini Pro │
│  GPT-3.5    │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
```

## Components

### 1. AI API Server (`cmd/ai-api/main.go`)

The main entry point for AI requests. Provides a RESTful API for:
- **Completion Requests**: Process natural language prompts
- **Metrics**: Monitor system usage and performance
- **Cache Management**: Control response caching
- **Health Monitoring**: System status checks

**Key Features:**
- Graceful shutdown
- Request timeout handling
- JSON-based API
- Concurrent request handling

### 2. Model Router (`internal/ai/model_router.go`)

The core routing engine that decides which AI provider should handle each request.

**Routing Strategy:**
```go
TaskType          → Provider
─────────────────────────────
Reasoning         → Anthropic (Claude-3)
Creative          → OpenAI (GPT-4)
Code Review       → Anthropic (Claude-3)
Code Generation   → OpenAI (GPT-4)
Translation       → Gemini (Gemini Pro)
General           → OpenAI (GPT-4) [Default]
```

**Configuration:**
```go
config := RouterConfig{
    EnableCache:     true,
    CacheTTL:        10 * time.Minute,
    DefaultProvider: ProviderOpenAI,
    TaskRouting: map[TaskType]Provider{
        TaskTypeReasoning:   ProviderAnthropic,
        TaskTypeCreative:    ProviderOpenAI,
        TaskTypeCodeReview:  ProviderAnthropic,
        TaskTypeCodeGen:     ProviderOpenAI,
        TaskTypeTranslation: ProviderGemini,
    },
}
```

### 3. Cache System (`internal/ai/cache.go`)

In-memory caching layer that reduces costs and improves response times.

**Features:**
- SHA-256 based cache keys
- TTL (Time To Live) expiration
- Automatic cleanup
- Thread-safe operations

**Cache Key Generation:**
```
Key = SHA256(prompt + task_type + max_tokens + temperature)
```

### 4. Metrics System (`internal/ai/metrics.go`)

Comprehensive metrics collection for monitoring and optimization.

**Tracked Metrics:**
- Total requests (success/failed)
- Cache hit rate
- Token usage
- Per-provider statistics
- Response latency (min/max/avg)

### 5. AI Clients

#### Mock Client (`internal/ai/mock_client.go`)
- Used for development and testing
- Simulates AI provider responses
- Configurable delay
- No API keys required

#### Real Clients (`internal/ai/clients/`)
- **OpenAI Client**: GPT-4, GPT-3.5
- **Anthropic Client**: Claude-3 Opus/Sonnet
- **Gemini Client**: Gemini Pro

> **Note**: Real clients are currently stubs. Implementation requires:
> - Provider SDK integration
> - API key configuration
> - Error handling and retries
> - Rate limiting

### 6. Python Agents (`lib/agents/`)

CrewAI-based agent system for complex workflows.

**Agent Types:**
- Research Specialist
- Code Reviewer
- Content Writer
- Data Analyst
- Translator
- Problem Solver

**Workflows:**
1. **Research Workflow**: Comprehensive topic research
2. **Code Review Workflow**: Detailed code analysis
3. **Content Creation Workflow**: Research + Writing
4. **Data Analysis Workflow**: Pattern identification and insights

**Custom Tools (9 tools):**
- Code Analyzer
- Text Summarizer
- JSON Parser
- Word Counter
- URL Validator
- Data Formatter
- Pattern Finder
- File Info
- List Splitter

## Data Flow

### 1. Standard Request Flow

```
Client Request
     │
     ├─> [API Server] Receive & validate
     │
     ├─> [Router] Check cache
     │   ├─> Cache Hit  → Return cached response
     │   └─> Cache Miss → Continue
     │
     ├─> [Router] Determine provider
     │   └─> Based on task_type
     │
     ├─> [Client] Execute request
     │   └─> Call provider API
     │
     ├─> [Router] Cache response
     │
     ├─> [Metrics] Record statistics
     │
     └─> Return response to client
```

### 2. Error Handling Flow

```
Request → Router
     │
     ├─> Provider unavailable
     │   └─> Return error (no fallback in v1)
     │
     ├─> Request timeout
     │   └─> Cancel & return error
     │
     └─> API error
         └─> Record metrics & return error
```

## Scalability Considerations

### Current Design (v1)
- **Single instance**: In-memory cache
- **Synchronous**: Sequential request processing
- **No persistence**: Cache cleared on restart

### Future Enhancements (v2+)
- **Distributed cache**: Redis/Memcached
- **Load balancing**: Multiple API instances
- **Async processing**: Queue-based architecture
- **Persistent storage**: Request/response logging
- **Provider fallback**: Automatic failover
- **Rate limiting**: Per-provider quotas
- **Cost optimization**: Budget-aware routing

## Security

### Current Implementation
- No authentication (development mode)
- Environment variable configuration
- No request logging

### Production Requirements
- API key authentication
- Request rate limiting
- Input validation and sanitization
- Audit logging
- Secrets management (HashiCorp Vault, AWS Secrets Manager)
- TLS/HTTPS encryption

## Performance

### Benchmarks (Mock Clients)
- **Cache Hit**: < 1ms
- **Cache Miss**: ~100ms (simulated)
- **Throughput**: Limited by AI provider APIs

### Optimization Strategies
1. **Caching**: Reduce redundant API calls
2. **Connection Pooling**: Reuse HTTP connections
3. **Request Batching**: Combine similar requests
4. **Streaming Responses**: For long completions
5. **Provider Selection**: Use fastest/cheapest for task

## Monitoring

### Key Metrics to Track
- **Request Rate**: Requests per second
- **Success Rate**: % successful requests
- **Cache Hit Rate**: % cached responses
- **Average Latency**: Response time
- **Token Usage**: Per provider
- **Error Rate**: By error type
- **Provider Availability**: Uptime %

### Recommended Tools
- Prometheus + Grafana (metrics)
- Elasticsearch + Kibana (logs)
- Jaeger (distributed tracing)
- Sentry (error tracking)

## Configuration

### Environment Variables
```bash
# API Keys (for real providers)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."

# Server Configuration
export PORT="8080"
export CACHE_TTL="600"  # seconds
export REQUEST_TIMEOUT="30"  # seconds

# Development Mode
export AI_MODE="mock"  # Use mock clients
```

### Configuration File (future)
```yaml
# config/ai-config.yaml
router:
  default_provider: openai
  cache:
    enabled: true
    ttl: 10m
  providers:
    openai:
      model: gpt-4
      max_tokens: 4096
    anthropic:
      model: claude-3-opus-20240229
      max_tokens: 4096
    gemini:
      model: gemini-pro
      max_tokens: 2048
```

## Testing Strategy

### Unit Tests
- Router logic
- Cache operations
- Metrics collection
- Client implementations

### Integration Tests
- End-to-end request flow
- Provider switching
- Cache behavior
- Error handling

### Load Tests
- Concurrent requests
- Cache performance
- Memory usage
- Provider limits

## Deployment

### Docker Container
```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o ai-api cmd/ai-api/main.go

FROM alpine:latest
COPY --from=builder /app/ai-api /usr/local/bin/
EXPOSE 8080
CMD ["ai-api"]
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tokyo-ia-ai-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tokyo-ia-ai
  template:
    spec:
      containers:
      - name: ai-api
        image: tokyo-ia/ai-api:latest
        ports:
        - containerPort: 8080
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-secrets
              key: openai-key
```

## References

- [CrewAI Documentation](https://docs.crewai.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Anthropic API Reference](https://docs.anthropic.com/claude/reference)
- [Google Gemini API](https://ai.google.dev/docs)

## Changelog

### v1.0.0 (Current)
- Initial implementation
- Mock clients for development
- Basic routing and caching
- Metrics collection
- REST API
- Python agents framework

### Planned Features
- Real provider client implementations
- Provider failover
- Distributed caching
- Authentication & authorization
- Request rate limiting
- Streaming responses
- Cost tracking and optimization
