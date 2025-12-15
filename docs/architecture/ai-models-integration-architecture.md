# Multi-Model AI Integration Architecture

## Overview

Tokyo-IA implements a sophisticated multi-model AI architecture that intelligently routes requests across multiple state-of-the-art LLM providers. The system is designed for production use with comprehensive monitoring, cost management, and failover capabilities.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Applications                       │
│                    (Web, Mobile, API Consumers)                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         AI API Gateway                            │
│                      (Load Balancer + Auth)                       │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Model Router Service (Go)                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Task-based routing logic                               │  │
│  │  • Budget tracking & cost optimization                    │  │
│  │  • Fallback chain management                              │  │
│  │  • Performance metrics collection                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────┬─────────────┬──────────────┬──────────────┬────────────┘
         │             │              │              │
         ▼             ▼              ▼              ▼
    ┌────────┐   ┌────────┐    ┌────────┐    ┌──────────┐
    │ Cache  │   │ Queue  │    │Metrics │    │  Budget  │
    │(Redis) │   │(Redis) │    │(Prom.) │    │ Tracker  │
    └────────┘   └────────┘    └────────┘    └──────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Model Providers                             │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤
│  OpenAI     │ Anthropic   │  Gemini     │   Grok      │  Llama  │
│  o3/o5      │Claude Opus  │  3.0 Ultra  │    4        │ 4 (405B)│
│             │  /Sonnet    │             │             │ (Local) │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────┘
         │             │              │              │         │
         └─────────────┴──────────────┴──────────────┴─────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Orchestrator (Go)                        │
│                (Bridge between Go and Python)                     │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CrewAI Agent Framework (Python)                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Code Review Agent    │  Test Generation Agent            │  │
│  │  (Claude Opus 4.1)    │  (OpenAI o3)                      │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │  SRE/Deployment Agent │  Documentation Agent              │  │
│  │  (Llama 4 Local)      │  (Gemini 3.0)                     │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Custom Tools                                 │
│  • Git Diff  • Security Scanner  • Coverage Analysis              │
│  • Kubectl   • Diagram Parser    • Test Runner                   │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Model Router (Go)

**Location**: `internal/ai/model_router.go`

The Model Router is the brain of the system, making intelligent decisions about which model to use for each request.

**Key Features**:
- Task-based routing (reasoning, code generation, multimodal, etc.)
- Complexity-based model selection
- Privacy-aware routing (local models for sensitive data)
- Budget-conscious decision making
- Automatic fallback chains for reliability
- Performance metrics collection

**Routing Logic**:
```go
Request → Analyze Task Type → Check Complexity → Consider Privacy
    ↓
Check Budget → Select Primary Model → Verify Availability
    ↓
Execute with Fallback Chain if needed → Cache Result → Return
```

### 2. Model Providers

#### Tier 1: Reasoning Models
- **OpenAI o3/o5**: Complex reasoning, advanced analysis
- **Claude Opus 4.1**: Code review, deep analysis
- **Claude Sonnet 4.5**: Balanced performance/cost

#### Tier 2: Code Generation
- **Meta Llama 4 405B**: High-performance local inference
- **Claude Opus**: Premium code generation

#### Tier 3: Multimodal
- **Gemini 3.0 Ultra**: Long context, multimodal
- **Grok 4**: Alternative multimodal

### 3. Caching Layer

**Location**: `internal/ai/cache.go`

**Features**:
- In-memory cache for fast lookups
- Redis backend support (planned)
- Configurable TTL (default: 1 hour)
- SHA-256 based cache keys
- Automatic expiration and cleanup
- Cache statistics tracking

**Benefits**:
- 40%+ cache hit rate target
- Reduces API costs
- Improves response times
- Reduces load on providers

### 4. Budget Tracker

**Location**: `internal/ai/model_router.go` (BudgetTracker)

**Features**:
- Daily spending limits ($500 default)
- Per-request budget checks
- Real-time spending tracking
- Automatic budget resets
- Alert thresholds (80% default)
- Cost attribution by provider

### 5. Metrics Collection

**Location**: `internal/ai/metrics.go`

**Collected Metrics**:
- Request counts per provider
- Token usage (total and per provider)
- Cost tracking (USD)
- Latency measurements (avg, p50, p95, p99)
- Error rates
- Cache hit rates
- Budget utilization

### 6. Agent Framework (Python)

**Location**: `lib/agents/`

**Agents**:

1. **Code Review Agent** (Claude Opus 4.1)
   - Deep code analysis
   - Security vulnerability scanning
   - Performance optimization suggestions
   - Best practices enforcement

2. **Test Generation Agent** (OpenAI o3)
   - Unit test generation
   - Edge case discovery
   - Property-based test design
   - Coverage optimization

3. **SRE Agent** (Llama 4 Local)
   - Deployment safety validation
   - Kubernetes resource checks
   - Rollback planning
   - Infrastructure analysis

4. **Documentation Agent** (Gemini 3.0)
   - Code-to-docs generation
   - API documentation
   - Architecture diagrams
   - Usage examples

### 7. Workflows

**Location**: `lib/agents/workflows.py`

**Available Workflows**:

1. **PR Review Workflow**
   ```
   Code Review → Test Generation → Deployment Safety Check
   ```

2. **Bug Fix Workflow**
   ```
   Bug Analysis → Reproduction Test → Fix Validation
   ```

3. **Feature Development Workflow**
   ```
   Architecture Planning → Design Doc → Test Strategy → Ops Review
   ```

4. **Documentation Generation Workflow**
   ```
   Codebase Analysis → Documentation Generation
   ```

## Data Flow

### Request Flow
```
1. Client sends request to AI API
2. Authentication & rate limiting check
3. Request routed to Model Router
4. Router checks cache for existing response
5. If cache miss, router makes routing decision
6. Budget check performed
7. Request sent to selected model provider
8. Response received and cached
9. Metrics recorded
10. Response returned to client
```

### Agent Workflow Flow
```
1. Workflow triggered (e.g., PR opened)
2. Agent Orchestrator receives request
3. Python agents initialized with appropriate tools
4. Tasks executed sequentially/hierarchically
5. Each agent calls Model Router for LLM operations
6. Results aggregated
7. Final report generated
8. Results posted back (e.g., PR comment)
```

## Configuration

### Model Configuration
**File**: `config/ai_models.yaml`

Defines:
- Available models and their properties
- Routing rules by task type
- Budget limits and allocation
- Cache settings
- Performance thresholds
- Feature flags

### Environment Variables
Required:
- `OPENAI_API_KEY`: OpenAI API access
- `ANTHROPIC_API_KEY`: Anthropic Claude access
- `GEMINI_API_KEY`: Google Gemini access
- `GROK_API_KEY`: xAI Grok access

Optional:
- `REDIS_URL`: Redis connection string
- `LANGFUSE_PUBLIC_KEY`: Langfuse observability
- `LANGFUSE_SECRET_KEY`: Langfuse auth
- `PROMETHEUS_PORT`: Metrics port (default: 9090)

## Deployment Architecture

### Local Development
```
Go Services: localhost:8080
Python Agents: localhost:8081
Redis: localhost:6379
Prometheus: localhost:9090
Grafana: localhost:3000
```

### Production (Kubernetes)
```
- AI API Service (3 replicas)
- Model Router Service (5 replicas)
- Agent Orchestrator (2 replicas)
- Redis Cluster (3 nodes)
- Llama 4 Inference (2 nodes, 8xH100 each)
- Prometheus + Grafana
- Langfuse
```

## Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Local Llama 4 latency | p50 < 100ms | 95% of requests |
| Cloud API latency | p99 < 2s | With retries |
| Cache hit rate | > 40% | Common queries |
| Availability | 99.9% | With fallbacks |
| Cost per request | < $0.01 | Average |
| Daily budget | $500 | Configurable |

## Security Considerations

1. **API Key Management**
   - Environment variables only
   - Never committed to code
   - Rotation every 90 days

2. **Privacy**
   - Sensitive code → Local Llama 4
   - Privacy flag support
   - No data retention in cache for sensitive requests

3. **Input Validation**
   - Request validation before routing
   - Token limit enforcement
   - Rate limiting per user/team

4. **Network Security**
   - TLS for all external API calls
   - mTLS within Kubernetes cluster
   - Network policies

## Monitoring & Observability

### Prometheus Metrics
- `model_request_duration_seconds`
- `model_tokens_used_total`
- `model_cost_usd_total`
- `model_error_rate`
- `cache_hit_rate`
- `budget_utilization_percent`

### Grafana Dashboards
1. **AI Models Dashboard**: Request distribution, latency, costs
2. **Agent Workflows Dashboard**: Workflow success rates, task duration
3. **Budget Dashboard**: Spending trends, provider breakdown

### Alerts
- High error rate (>5%)
- Budget exceeded (>80%)
- Latency spike (p99 >1s)
- Model unavailability

## Future Enhancements

1. **Streaming Support**: Real-time response streaming
2. **Function Calling**: Tool use integration
3. **Multi-region**: Deploy across multiple regions
4. **A/B Testing**: Model performance comparison
5. **Custom Models**: Fine-tuned model support
6. **Cost Optimization**: ML-based routing optimization
