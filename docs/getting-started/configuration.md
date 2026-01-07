# ⚙️ Configuration Guide

This guide covers all configuration options for Tokyo-IA, from environment variables to advanced settings.

## 📋 Table of Contents

- [Environment Variables](#environment-variables)
- [Database Configuration](#database-configuration)
- [API Keys Setup](#api-keys-setup)
- [Server Configuration](#server-configuration)
- [Agent Configuration](#agent-configuration)
- [Logging Configuration](#logging-configuration)
- [Performance Tuning](#performance-tuning)
- [Advanced Settings](#advanced-settings)

---

## Environment Variables

Tokyo-IA uses environment variables for configuration. Create a `.env` file in the project root:

### Quick Setup

```bash
cp .env.example .env
nano .env  # or use your favorite editor
```

### Core Variables

```bash
# ============================================
# Database Configuration
# ============================================
DATABASE_URL="postgresql://user:password@host:port/database"

# ============================================
# API Server Configuration
# ============================================
PORT=8080
HOST=0.0.0.0
REGISTRY_API_URL="http://localhost:8080"

# ============================================
# LLM API Keys (for AI Agents)
# ============================================
ANTHROPIC_API_KEY="sk-ant-..."     # Akira (Claude)
OPENAI_API_KEY="sk-..."            # Yuki & Kenji (OpenAI)
GROQ_API_KEY="gsk_..."             # Hiro (Llama via Groq)
GOOGLE_API_KEY="..."               # Sakura (Gemini)

# ============================================
# Development Options
# ============================================
ENV=development                     # development | staging | production
DEBUG=false                         # Enable debug logging
USE_MOCK_AGENTS=false              # Use mock responses (no API calls)

# ============================================
# Security
# ============================================
API_KEY_REQUIRED=false             # Require API key for requests
JWT_SECRET=""                      # JWT signing secret (future)
CORS_ORIGINS="*"                   # CORS allowed origins

# ============================================
# Performance
# ============================================
MAX_CONCURRENT_TASKS=10            # Max concurrent agent tasks
TASK_TIMEOUT_SECONDS=300           # Task timeout (5 minutes)
DB_MAX_CONNECTIONS=20              # Database connection pool size
DB_MAX_IDLE_CONNECTIONS=5          # Idle connections

# ============================================
# Logging
# ============================================
LOG_LEVEL=info                     # debug | info | warn | error
LOG_FORMAT=json                    # json | text
LOG_OUTPUT=stdout                  # stdout | file | both
LOG_FILE_PATH=/var/log/tokyoia.log

# ============================================
# Monitoring
# ============================================
METRICS_ENABLED=true               # Enable Prometheus metrics
METRICS_PORT=9090                  # Metrics endpoint port
SENTRY_DSN=""                      # Sentry error tracking
```

---

## Database Configuration

### Connection String Format

```bash
DATABASE_URL="postgresql://[user]:[password]@[host]:[port]/[database]?[params]"
```

### Examples

**Local Development (no password):**
```bash
DATABASE_URL="postgresql://localhost:5432/tokyoia"
```

**Local Development (with password):**
```bash
DATABASE_URL="postgresql://postgres:mypassword@localhost:5432/tokyoia"
```

**Docker Compose:**
```bash
DATABASE_URL="postgresql://tokyoia:tokyoia@postgres:5432/tokyoia"
```

**Production (Railway):**
```bash
DATABASE_URL="postgresql://postgres:abc123@containers-us-west.railway.app:5432/railway"
```

**With SSL (production):**
```bash
DATABASE_URL="postgresql://user:pass@host:5432/db?sslmode=require"
```

### Connection Pool Settings

```bash
# Maximum open connections
DB_MAX_CONNECTIONS=20

# Maximum idle connections
DB_MAX_IDLE_CONNECTIONS=5

# Connection lifetime
DB_MAX_LIFETIME_MINUTES=30

# Connection timeout
DB_CONNECTION_TIMEOUT_SECONDS=10
```

### Performance Recommendations

| Environment | Max Connections | Idle Connections |
|-------------|-----------------|------------------|
| Development | 5 | 2 |
| Testing | 10 | 3 |
| Staging | 20 | 5 |
| Production | 50-100 | 10-20 |

---

## API Keys Setup

### Getting API Keys

#### Anthropic (Claude) - For Akira

1. Visit [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Go to API Keys
4. Create new key
5. Copy the key starting with `sk-ant-`

```bash
ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxxxx"
```

**Models**: Claude Opus 4.1, Claude Sonnet 3.5

#### OpenAI - For Yuki & Kenji

1. Visit [platform.openai.com](https://platform.openai.com/)
2. Go to API Keys
3. Create new secret key
4. Copy the key starting with `sk-`

```bash
OPENAI_API_KEY="sk-xxxxxxxxxxxx"
```

**Models**: GPT-4, GPT-4 Turbo, O3

#### Groq - For Hiro

1. Visit [console.groq.com](https://console.groq.com/)
2. Create account
3. Generate API key
4. Copy the key starting with `gsk_`

```bash
GROQ_API_KEY="gsk_xxxxxxxxxxxx"
```

**Models**: Llama 3.1 405B, Llama 3.1 70B, Mixtral 8x7B

#### Google AI - For Sakura

1. Visit [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Create API key
3. Copy the key

```bash
GOOGLE_API_KEY="AIzaxxxxxxxxxxxx"
```

**Models**: Gemini 1.5 Pro, Gemini 1.5 Flash

### Development Without API Keys

For development and testing without API calls:

```bash
USE_MOCK_AGENTS=true
```

This enables mock responses that simulate agent behavior without making actual LLM API calls.

### API Key Security

**🔒 Security Best Practices:**

1. **Never commit API keys to git**
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment-specific keys**
   - Development: Free tier keys
   - Production: Production keys with rate limits

3. **Rotate keys regularly**
   - Set calendar reminders
   - Use key rotation policies

4. **Use secret managers in production**
   - AWS Secrets Manager
   - HashiCorp Vault
   - Railway environment variables

5. **Monitor usage**
   - Set up billing alerts
   - Track token consumption
   - Watch for unusual activity

---

## Server Configuration

### Port Configuration

```bash
# API server port
PORT=8080

# Bind address
HOST=0.0.0.0  # Listen on all interfaces

# Or bind to localhost only (more secure)
HOST=127.0.0.1
```

### CORS Configuration

```bash
# Allow all origins (development only!)
CORS_ORIGINS="*"

# Allow specific origins
CORS_ORIGINS="https://app.example.com,https://admin.example.com"

# Allow localhost
CORS_ORIGINS="http://localhost:3000,http://localhost:5173"
```

### Timeout Configuration

```bash
# Server read timeout
SERVER_READ_TIMEOUT_SECONDS=30

# Server write timeout
SERVER_WRITE_TIMEOUT_SECONDS=30

# Task execution timeout
TASK_TIMEOUT_SECONDS=300  # 5 minutes

# Workflow timeout
WORKFLOW_TIMEOUT_SECONDS=1800  # 30 minutes
```

### Rate Limiting

```bash
# Enable rate limiting
RATE_LIMIT_ENABLED=true

# Requests per minute per IP
RATE_LIMIT_REQUESTS_PER_MINUTE=60

# Burst size
RATE_LIMIT_BURST=10
```

---

## Agent Configuration

### Agent Behavior

```bash
# Retry configuration
AGENT_MAX_RETRIES=3
AGENT_RETRY_DELAY_SECONDS=5

# Token limits
AGENT_MAX_TOKENS_PER_REQUEST=4000
AGENT_MAX_TOTAL_TOKENS=100000

# Temperature settings (creativity)
AGENT_DEFAULT_TEMPERATURE=0.7  # 0.0 = deterministic, 1.0 = creative
```

### Agent-Specific Settings

```bash
# Akira (Code Reviewer)
AKIRA_MODEL="claude-opus-4"
AKIRA_MAX_TOKENS=8000
AKIRA_TEMPERATURE=0.3  # More deterministic for code review

# Yuki (Test Engineer)
YUKI_MODEL="o3-mini"
YUKI_MAX_TOKENS=4000
YUKI_TEMPERATURE=0.5

# Hiro (SRE/DevOps)
HIRO_MODEL="llama-3.1-405b"
HIRO_MAX_TOKENS=4000
HIRO_TEMPERATURE=0.4

# Sakura (Documentation)
SAKURA_MODEL="gemini-1.5-pro"
SAKURA_MAX_TOKENS=8000
SAKURA_TEMPERATURE=0.7  # More creative for documentation

# Kenji (Architect)
KENJI_MODEL="o3"
KENJI_MAX_TOKENS=4000
KENJI_TEMPERATURE=0.6
```

---

## Logging Configuration

### Log Level

```bash
LOG_LEVEL=info  # debug | info | warn | error | fatal
```

| Level | Description | Use Case |
|-------|-------------|----------|
| debug | Very verbose | Development, troubleshooting |
| info | General info | Default for production |
| warn | Warning messages | Production |
| error | Error messages | Production |
| fatal | Fatal errors only | Minimal logging |

### Log Format

```bash
# JSON format (recommended for production)
LOG_FORMAT=json

# Example output:
# {"level":"info","time":"2025-12-23T04:25:00Z","msg":"Server started","port":8080}
```

```bash
# Text format (easier to read in development)
LOG_FORMAT=text

# Example output:
# 2025-12-23 04:25:00 INFO Server started port=8080
```

### Log Output

```bash
# Output to stdout (default, works with Docker)
LOG_OUTPUT=stdout

# Output to file
LOG_OUTPUT=file
LOG_FILE_PATH=/var/log/tokyoia.log

# Output to both
LOG_OUTPUT=both
```

### Log Rotation

```bash
# Maximum log file size (MB)
LOG_MAX_SIZE_MB=100

# Maximum number of old log files
LOG_MAX_BACKUPS=10

# Maximum age of log files (days)
LOG_MAX_AGE_DAYS=30

# Compress old logs
LOG_COMPRESS=true
```

---

## Performance Tuning

### Concurrency

```bash
# Maximum concurrent tasks
MAX_CONCURRENT_TASKS=10

# Worker pool size
WORKER_POOL_SIZE=5

# Queue size
TASK_QUEUE_SIZE=100
```

**Recommendations:**
- Development: 2-5 concurrent tasks
- Production (small): 10-20 concurrent tasks
- Production (large): 50-100 concurrent tasks

### Caching

```bash
# Enable caching
CACHE_ENABLED=true

# Cache TTL (seconds)
CACHE_TTL_SECONDS=3600  # 1 hour

# Cache size (MB)
CACHE_MAX_SIZE_MB=100

# Redis cache (optional)
REDIS_URL="redis://localhost:6379/0"
```

### Database Performance

```bash
# Enable query logging (development only)
DB_LOG_QUERIES=false

# Slow query threshold (ms)
DB_SLOW_QUERY_THRESHOLD_MS=1000

# Enable prepared statements
DB_USE_PREPARED_STATEMENTS=true
```

---

## Advanced Settings

### Feature Flags

```bash
# Enable beta features
ENABLE_BETA_FEATURES=false

# Enable experimental workflows
ENABLE_EXPERIMENTAL_WORKFLOWS=false

# Enable GraphQL API (future)
ENABLE_GRAPHQL=false

# Enable WebSocket support (future)
ENABLE_WEBSOCKETS=false
```

### Metrics and Monitoring

```bash
# Prometheus metrics
METRICS_ENABLED=true
METRICS_PORT=9090
METRICS_PATH=/metrics

# Sentry error tracking
SENTRY_DSN="https://xxx@sentry.io/xxx"
SENTRY_ENVIRONMENT=production
SENTRY_SAMPLE_RATE=1.0

# OpenTelemetry tracing
OTEL_ENABLED=false
OTEL_ENDPOINT="http://localhost:4318"
```

### Cost Control

```bash
# Maximum cost per task (USD)
MAX_COST_PER_TASK_USD=1.00

# Maximum cost per workflow (USD)
MAX_COST_PER_WORKFLOW_USD=10.00

# Alert threshold (USD)
COST_ALERT_THRESHOLD_USD=100.00

# Alert email
COST_ALERT_EMAIL="admin@example.com"
```

---

## Configuration Files

### config.yaml (Alternative to .env)

Create `config/production.yaml`:

```yaml
server:
  port: 8080
  host: 0.0.0.0
  read_timeout: 30s
  write_timeout: 30s

database:
  url: "postgresql://..."
  max_connections: 50
  max_idle: 10

agents:
  max_concurrent: 20
  timeout: 300s
  retry:
    max_attempts: 3
    delay: 5s

logging:
  level: info
  format: json
  output: stdout

security:
  api_key_required: true
  jwt_secret: "${JWT_SECRET}"
  cors_origins:
    - "https://app.example.com"
```

Use with:
```bash
export CONFIG_FILE=config/production.yaml
./bin/registry-api
```

---

## Environment-Specific Configs

### Development (.env.development)

```bash
ENV=development
DEBUG=true
LOG_LEVEL=debug
USE_MOCK_AGENTS=true
DATABASE_URL="postgresql://localhost:5432/tokyoia_dev"
PORT=8080
```

### Staging (.env.staging)

```bash
ENV=staging
DEBUG=false
LOG_LEVEL=info
DATABASE_URL="${STAGING_DATABASE_URL}"
PORT=8080
SENTRY_DSN="${STAGING_SENTRY_DSN}"
```

### Production (.env.production)

```bash
ENV=production
DEBUG=false
LOG_LEVEL=warn
DATABASE_URL="${DATABASE_URL}"
PORT=${PORT}
API_KEY_REQUIRED=true
METRICS_ENABLED=true
SENTRY_DSN="${SENTRY_DSN}"
```

Load with:
```bash
export $(cat .env.production | xargs)
```

---

## Configuration Validation

Validate your configuration:

```bash
./bin/registry-api --validate-config
```

This checks:
- Required variables are set
- Database connection works
- API keys are valid format
- Port is available
- File paths exist

---

## Next Steps

- 📖 [Quick Start Guide](quick-start.md) - Start using Tokyo-IA
- 🚀 [Deployment Guide](../deployment/railway.md) - Deploy to production
- 🔐 [Security Best Practices](../security/best-practices.md) - Secure your deployment
- 📊 [Monitoring](../deployment/monitoring.md) - Monitor your system

---

*Last updated: 2025-12-23*
