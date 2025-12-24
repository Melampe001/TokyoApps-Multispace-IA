# 🚀 CI/CD Pipeline Documentation

## Overview

Tokyo-IA uses a comprehensive CI/CD pipeline with automated testing, security scanning, and deployment to Railway. This document covers setup, configuration, and usage.

## Table of Contents

- [Architecture](#architecture)
- [Workflows](#workflows)
- [Railway Setup](#railway-setup)
- [GitHub Secrets Configuration](#github-secrets-configuration)
- [Local Development](#local-development)
- [Troubleshooting](#troubleshooting)
- [Rollback Procedures](#rollback-procedures)

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     GitHub Actions                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  CI Pipeline │  │   Security   │  │   Release    │ │
│  │              │  │   Scanning   │  │  Automation  │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                 │                  │          │
│         └─────────────────┴──────────────────┘          │
│                           │                              │
└───────────────────────────┼──────────────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │   CD Pipeline    │
                  │   (Railway)      │
                  └────────┬─────────┘
                           │
          ┌────────────────┴─────────────────┐
          │                                  │
          ▼                                  ▼
    ┌──────────┐                      ┌──────────┐
    │ Staging  │                      │Production│
    │Environment│                      │Environment│
    └──────────┘                      └──────────┘
```

---

## Workflows

### 1. 🧪 CI Pipeline (`.github/workflows/ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main`

**Jobs:**

#### Go Tests
- **Matrix:** Go 1.21 and 1.22
- **Steps:**
  1. Checkout code
  2. Setup Go with caching
  3. Download dependencies
  4. Run format check (`make fmt-check`)
  5. Run `go vet`
  6. Run tests with race detector
  7. Upload coverage to Codecov

#### Python Tests
- **Matrix:** Python 3.11 and 3.12
- **Steps:**
  1. Checkout code
  2. Setup Python with pip caching
  3. Install dependencies
  4. Run Ruff linting
  5. Run pytest with coverage
  6. Upload coverage to Codecov

#### Go Linting
- Uses `golangci-lint` with `.golangci.yml` config
- Checks code quality and style

#### Build Verification
- Builds all binaries:
  - `tokyo-ia` (main application)
  - `registry-api` (API server)
  - `elite` (Elite framework CLI)
  - `ai-api` (AI API server)

#### Database Schema Tests
- Runs PostgreSQL in Docker
- Tests schema creation
- Validates migrations
- Tests connection pooling

---

### 2. 🚀 CD Pipeline (`.github/workflows/cd.yml`)

**Triggers:**
- Push to `main` → deploys to **staging**
- Push tags `v*` → deploys to **production**
- Manual dispatch

**Jobs:**

#### Deploy to Staging
1. Install Railway CLI
2. Link Railway project
3. Switch to staging environment
4. Deploy with `railway up --detach`
5. Wait 30s for deployment
6. Run health check
7. Send Slack notification (optional)

#### Deploy to Production
1. Install Railway CLI
2. Link Railway project
3. Switch to production environment
4. Deploy with `railway up --detach`
5. Wait 60s for deployment
6. Run health check
7. Run smoke tests
8. Send Slack notification (optional)

---

### 3. 🔒 Security Scanning (`.github/workflows/security.yml`)

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main`
- Weekly schedule (Mondays at midnight)

**Jobs:**

#### CodeQL Analysis
- Multi-language analysis (Go and Python)
- Detects security vulnerabilities
- Uploads results to GitHub Security

#### Dependency Review
- Reviews dependency changes in PRs
- Fails on moderate+ severity vulnerabilities

#### Trivy Scan
- Filesystem vulnerability scanning
- Checks dependencies for known CVEs
- Uploads SARIF results to GitHub Security

#### Secret Scanning
- Uses TruffleHog to detect secrets
- Scans entire repository history
- Only reports verified secrets

---

### 4. 📦 Release Automation (`.github/workflows/release.yml`)

**Triggers:**
- Push tags matching `v*` (e.g., `v1.0.0`)

**Jobs:**

#### Build Artifacts
Builds binaries for multiple platforms:
- **Linux:** amd64, arm64
- **macOS:** amd64 (Intel), arm64 (Apple Silicon)
- **Windows:** amd64

Generates SHA256 checksums for all binaries.

#### Create GitHub Release
- Auto-generates changelog
- Creates release with artifacts
- Adds installation instructions
- Includes checksums for verification

#### Docker Release
- Builds multi-arch Docker images
- Pushes to GitHub Container Registry
- Tags: `latest`, version tags, SHA

---

## Railway Setup

### Prerequisites

1. **Railway Account:** Sign up at [railway.app](https://railway.app)
2. **Railway CLI:** Install locally for manual deployments

```bash
curl -fsSL https://railway.app/install.sh | sh
```

### Initial Setup

#### 1. Create Railway Project

```bash
# Login to Railway
railway login

# Create new project
railway init

# Note the project ID (shown in output or dashboard)
```

#### 2. Create Environments

Railway Dashboard → Your Project → Settings → Environments

Create two environments:
- `staging`
- `production`

#### 3. Provision PostgreSQL Database

For each environment:

```bash
# Switch to environment
railway environment staging  # or production

# Add PostgreSQL service
railway add postgres

# Note the DATABASE_URL (automatically set as environment variable)
```

#### 4. Configure Environment Variables

Set these for each environment in Railway Dashboard:

**Required:**
```
DATABASE_URL=<automatically set by Railway>
PORT=8080
```

**Optional (for AI features):**
```
ANTHROPIC_API_KEY=<your-key>
OPENAI_API_KEY=<your-key>
GROQ_API_KEY=<your-key>
GOOGLE_API_KEY=<your-key>
LOG_LEVEL=info
```

#### 5. Configure Custom Domains (Optional)

Production:
- `tokyo-ia.up.railway.app` (default)
- Or add custom domain

Staging:
- `tokyo-ia-staging.up.railway.app` (default)

---

## GitHub Secrets Configuration

Navigate to: **Repository → Settings → Secrets and variables → Actions**

### Required Secrets

#### Railway Integration
```
RAILWAY_TOKEN
```
- Get from: Railway Dashboard → Account Settings → Tokens → Create Token
- Scope: Read & Write

```
RAILWAY_PROJECT_ID
```
- Get from: Railway Dashboard → Project → Settings → Project ID

### Optional Secrets

#### Code Coverage
```
CODECOV_TOKEN
```
- Get from: [codecov.io](https://codecov.io)
- Required for private repositories

#### Slack Notifications
```
SLACK_WEBHOOK
```
- Create incoming webhook in Slack workspace
- Used for deployment notifications

#### LLM API Keys (for integration tests)
```
ANTHROPIC_API_KEY
OPENAI_API_KEY
GROQ_API_KEY
GOOGLE_API_KEY
```
- Only needed if running integration tests with real APIs
- Tests use mocks if not provided

---

## Local Development

### Using Docker Compose

```bash
# Start all services (database, API, adminer)
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Clean up volumes
docker-compose down -v
```

**Services:**
- API: http://localhost:8080
- Adminer (DB UI): http://localhost:8081
- PostgreSQL: localhost:5432

### Manual Deployment to Railway

```bash
# Deploy to staging
./scripts/deploy.sh staging

# Deploy to production
./scripts/deploy.sh production
```

### Building Docker Image Locally

```bash
# Build image
docker build -t tokyo-ia:local .

# Run container
docker run -p 8080:8080 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  tokyo-ia:local
```

### Running Tests Locally

```bash
# Go tests
make test-go

# Python tests (requires dependencies)
make test-python

# All tests
make test

# With coverage
go test -v -race -coverprofile=coverage.out ./...
pytest --cov=lib --cov-report=html
```

---

## Troubleshooting

### CI Pipeline Failures

#### Go Test Failures
```bash
# Run locally to debug
go test -v ./path/to/package

# Check race conditions
go test -race ./...

# Verbose output
go test -v -race ./...
```

#### Python Test Failures
```bash
# Run locally
pytest -v

# Run specific test
pytest lib/agents/test_crew.py::test_name -v

# Check coverage
pytest --cov=lib --cov-report=term-missing
```

#### Linting Failures

**Go:**
```bash
# Format code
make fmt

# Check formatting
make fmt-check

# Run linter
make lint
```

**Python:**
```bash
# Check with Ruff
ruff check lib/

# Auto-fix issues
ruff check lib/ --fix
```

### Deployment Failures

#### Railway Deployment Times Out

**Solution:**
1. Check Railway Dashboard logs
2. Increase `healthcheckTimeout` in `railway.toml`
3. Verify `healthcheckPath` endpoint exists

```bash
# Check logs in Railway dashboard or CLI
railway logs
```

#### Health Check Fails

**Causes:**
- Application not listening on correct PORT
- Health endpoint not implemented
- Database connection failure

**Debug:**
```bash
# Check Railway environment variables
railway variables

# Check application logs
railway logs --tail 100

# Test locally with same environment
docker-compose up
curl http://localhost:8080/health
```

#### Database Connection Issues

**Solutions:**
1. Verify `DATABASE_URL` is set correctly
2. Check PostgreSQL service is running in Railway
3. Verify database schema is initialized

```bash
# Connect to Railway database
railway connect postgres

# Check if tables exist
\dt

# Run schema manually if needed
\i db/schema.sql
```

### Security Scan Failures

#### CodeQL Issues

**Action:**
1. Review the security alert in GitHub Security tab
2. Fix the vulnerability in code
3. Push fix and re-run scan

#### Dependency Vulnerabilities

**Action:**
1. Update vulnerable dependency

```bash
# Go dependencies
go get -u github.com/vulnerable/package@latest
go mod tidy

# Python dependencies
pip install --upgrade package-name
pip freeze > requirements.txt
```

2. Run security scan locally:

```bash
# Trivy filesystem scan
trivy fs .

# Go vulnerability check
go list -json -m all | nancy sleuth
```

---

## Rollback Procedures

### Rolling Back Production Deployment

#### Method 1: Redeploy Previous Tag

```bash
# List recent tags
git tag -l

# Create rollback deployment
git checkout v1.2.3
git tag v1.2.4-rollback
git push origin v1.2.4-rollback
```

#### Method 2: Railway Dashboard

1. Go to Railway Dashboard
2. Select your project → production environment
3. Click on deployments
4. Find previous successful deployment
5. Click "Redeploy"

#### Method 3: Manual Deployment

```bash
# Checkout previous version
git checkout v1.2.3

# Deploy manually
./scripts/deploy.sh production
```

### Rolling Back Database Migrations

**⚠️ Warning:** Database rollbacks can cause data loss!

```bash
# Connect to production database
railway connect postgres --environment production

# Run rollback migration (if you have them)
# Example: undo last migration
\i db/migrations/down/002_rollback_changes.sql
```

**Best Practice:** Always test migrations in staging first!

---

## Monitoring and Alerts

### Railway Monitoring

Railway provides built-in monitoring:
- CPU usage
- Memory usage
- Response times
- Error rates

Access: Railway Dashboard → Project → Metrics

### Setting Up Alerts

1. **Railway Slack Integration:**
   - Railway Dashboard → Settings → Integrations
   - Connect Slack workspace
   - Configure alert channels

2. **Custom Monitoring:**
   - Add health check endpoints
   - Integrate with monitoring services (Datadog, New Relic, etc.)

---

## Best Practices

### Deployment Strategy

1. **Always deploy to staging first**
   ```bash
   git push origin main  # Auto-deploys to staging
   ```

2. **Test staging thoroughly**
   - Run smoke tests
   - Verify health checks
   - Test critical user flows

3. **Tag and deploy to production**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0  # Auto-deploys to production
   ```

### Version Tagging

Follow [Semantic Versioning](https://semver.org/):
- `v1.0.0` - Major release
- `v1.1.0` - Minor release (new features)
- `v1.1.1` - Patch release (bug fixes)

### Environment Parity

Keep staging and production environments as similar as possible:
- Same infrastructure configuration
- Similar data volumes
- Same environment variables (except secrets)

---

## Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Go Testing](https://golang.org/pkg/testing/)
- [pytest Documentation](https://docs.pytest.org/)

---

## Support

For issues or questions:
1. Check [GitHub Issues](https://github.com/Melampe001/Tokyo-IA/issues)
2. Review Railway logs and GitHub Actions runs
3. Contact the team via Slack (if configured)

---

**Last Updated:** 2025-12-23
**Version:** 1.0.0
