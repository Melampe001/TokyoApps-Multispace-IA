# 🚂 Railway Deployment Guide

Deploy Tokyo-IA to [Railway](https://railway.app) in minutes. Railway provides a seamless deployment experience with built-in PostgreSQL, automatic deployments, and excellent developer experience.

## 📋 Table of Contents

- [Why Railway?](#why-railway)
- [Prerequisites](#prerequisites)
- [Quick Deploy](#quick-deploy)
- [Manual Setup](#manual-setup)
- [Configuration](#configuration)
- [Monitoring](#monitoring)
- [Scaling](#scaling)
- [Troubleshooting](#troubleshooting)

---

## Why Railway?

Railway is the recommended platform for Tokyo-IA because:

- ✅ **One-Click PostgreSQL** - Provision database in seconds
- ✅ **GitHub Integration** - Auto-deploy on push
- ✅ **Environment Variables** - Easy configuration management
- ✅ **Built-in Monitoring** - Logs, metrics, and alerts
- ✅ **Auto-Scaling** - Scales with your needs
- ✅ **Affordable** - $5/month starter plan
- ✅ **Developer-Friendly** - Great DX and documentation

---

## Prerequisites

Before deploying to Railway, ensure you have:

1. **Railway Account** - Sign up at [railway.app](https://railway.app)
2. **GitHub Account** - For repository connection
3. **LLM API Keys** (optional for testing):
   - Anthropic API key for Akira
   - OpenAI API key for Yuki & Kenji
   - Groq API key for Hiro
   - Google API key for Sakura

---

## Quick Deploy

### Option 1: Deploy Button (Fastest)

Click the button below to deploy Tokyo-IA to Railway:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/tokyo-ia?referralCode=tokyo-ia)

This will:
1. Create a new Railway project
2. Provision PostgreSQL database
3. Set up the Registry API service
4. Configure environment variables
5. Deploy the application

**After deployment:**
1. Add your LLM API keys in environment variables
2. Visit your app URL
3. Test with: `curl https://your-app.railway.app/health`

---

### Option 2: Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Clone repository
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA

# Initialize Railway project
railway init

# Provision PostgreSQL
railway add --database postgresql

# Deploy
railway up

# Open in browser
railway open
```

---

## Manual Setup

### Step 1: Create Railway Project

1. Go to [railway.app/new](https://railway.app/new)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose **Melampe001/Tokyo-IA**
5. Click **"Deploy Now"**

Railway will:
- Clone your repository
- Detect Dockerfile/build configuration
- Start the initial deployment

### Step 2: Add PostgreSQL Database

1. In your project, click **"+ New"**
2. Select **"Database"**
3. Choose **"PostgreSQL"**
4. Wait for provisioning (~30 seconds)

Railway automatically creates `DATABASE_URL` environment variable.

### Step 3: Configure Environment Variables

Click on your service → **Variables** tab:

```bash
# Required
DATABASE_URL=${{Postgres.DATABASE_URL}}  # Auto-configured
PORT=8080

# Optional but recommended
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
GOOGLE_API_KEY=...

# Optional settings
ENV=production
LOG_LEVEL=info
MAX_CONCURRENT_TASKS=20
```

### Step 4: Deploy

Railway automatically deploys on configuration changes. Otherwise:

```bash
# Trigger manual deployment
railway up

# Or from GitHub
git push origin main  # If GitHub integration is enabled
```

### Step 5: Verify Deployment

```bash
# Get your Railway URL
railway domain

# Test health endpoint
curl https://your-app.railway.app/health

# Expected response:
# {"status":"healthy","database":"connected"}

# List agents
curl https://your-app.railway.app/api/agents
```

---

## Configuration

### Environment Variables

Set environment variables in Railway dashboard:

**Required:**
- `DATABASE_URL` - Auto-configured by Railway
- `PORT` - Railway auto-detects, default: 8080

**LLM API Keys:**
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
GOOGLE_API_KEY=AIza...
```

**Optional:**
```bash
# Environment
ENV=production
DEBUG=false

# Logging
LOG_LEVEL=info
LOG_FORMAT=json

# Performance
MAX_CONCURRENT_TASKS=20
DB_MAX_CONNECTIONS=50

# Security
API_KEY_REQUIRED=false
CORS_ORIGINS=https://your-frontend.com

# Monitoring
METRICS_ENABLED=true
SENTRY_DSN=https://...@sentry.io/...
```

### Custom Domain

1. Go to your service **Settings**
2. Click **"Generate Domain"** for a railway.app subdomain
3. Or add custom domain:
   - Click **"Add Domain"**
   - Enter your domain (e.g., api.tokyo-ia.com)
   - Add DNS records as shown
   - Wait for SSL certificate provisioning

### Build Configuration

Railway auto-detects build configuration from:
- `Dockerfile` (recommended)
- `railway.toml`
- `Procfile`

**Custom railway.toml:**

```toml
[build]
builder = "dockerfile"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = "./bin/registry-api"
healthcheckPath = "/health"
healthcheckTimeout = 30
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 3
```

---

## Monitoring

### Railway Dashboard

Access built-in monitoring:

1. **Logs** - Real-time application logs
   - Click service → **Deployments** → **View Logs**
   - Filter by level, search, download

2. **Metrics** - Resource usage
   - CPU, memory, network
   - Historical charts
   - Alert thresholds

3. **Events** - Deployment history
   - Build logs
   - Deploy status
   - Error messages

### Health Checks

Railway performs automatic health checks:

```bash
# Default health check endpoint
GET /health

# Configure custom health check
# Add to railway.toml:
[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 30
```

### Application Metrics

Enable Prometheus metrics:

```bash
# In your environment variables
METRICS_ENABLED=true
METRICS_PORT=9090
```

Access at: `https://your-app.railway.app:9090/metrics`

### Error Tracking

Integrate Sentry for error tracking:

```bash
# Add Sentry DSN
SENTRY_DSN=https://xxx@sentry.io/xxx
SENTRY_ENVIRONMENT=production
SENTRY_SAMPLE_RATE=1.0
```

---

## Scaling

### Vertical Scaling

Increase resources for your service:

1. Go to service **Settings**
2. Scroll to **Resources**
3. Adjust:
   - **Memory**: 512MB - 32GB
   - **vCPU**: 0.5 - 32 cores

**Recommendations:**

| Workload | Memory | vCPU |
|----------|--------|------|
| Light (< 100 req/min) | 1GB | 1 |
| Medium (< 1K req/min) | 2GB | 2 |
| Heavy (< 10K req/min) | 4-8GB | 4 |
| Very Heavy (> 10K req/min) | 16GB+ | 8+ |

### Horizontal Scaling

Railway supports horizontal scaling:

1. Go to service **Settings**
2. Enable **Horizontal Scaling**
3. Set:
   - **Min replicas**: 2
   - **Max replicas**: 10
   - **Target CPU**: 70%

### Database Scaling

For PostgreSQL scaling:

1. **Vertical Scaling** - Upgrade database plan
2. **Connection Pooling** - Use PgBouncer
3. **Read Replicas** - Add replica databases
4. **External Database** - Use managed PostgreSQL (AWS RDS, etc.)

---

## Troubleshooting

### Deployment Fails

**Check build logs:**
1. Click failed deployment
2. View build logs
3. Look for errors

**Common issues:**
- Missing dependencies
- Build timeout
- Incorrect Dockerfile

**Solutions:**
```bash
# Test build locally
docker build -t tokyo-ia .
docker run -p 8080:8080 tokyo-ia

# Check Railway build logs
railway logs --deployment
```

### Application Crashes

**Check runtime logs:**
```bash
# View logs
railway logs

# Filter by error level
railway logs --filter error
```

**Common issues:**
- Database connection failed
- Out of memory
- Unhandled exceptions
- Missing environment variables

**Solutions:**
1. Verify `DATABASE_URL` is set
2. Increase memory allocation
3. Check error logs for stack traces
4. Verify all required env vars are set

### Database Connection Issues

**Verify connection:**
```bash
# From Railway CLI
railway run psql $DATABASE_URL

# Test connection from app
curl https://your-app.railway.app/health
```

**Common issues:**
- Database not provisioned
- Connection string incorrect
- Connection pool exhausted

**Solutions:**
```bash
# Check database status
railway status

# Increase connection pool
DB_MAX_CONNECTIONS=100
```

### High Response Times

**Diagnose:**
1. Check Railway metrics
2. Review slow query logs
3. Analyze LLM API latencies

**Solutions:**
1. **Increase resources** - More vCPU/memory
2. **Enable caching** - Add Redis
3. **Optimize queries** - Add database indexes
4. **Scale horizontally** - Add replicas

### Out of Memory (OOM)

**Symptoms:**
- Application crashes
- 137 exit code
- "Out of memory" in logs

**Solutions:**
1. **Increase memory limit** in Railway settings
2. **Optimize code** - Fix memory leaks
3. **Reduce concurrency** - Lower `MAX_CONCURRENT_TASKS`
4. **Add swap space** (not recommended long-term)

### SSL/TLS Errors

**Common issues:**
- Certificate not provisioned
- Custom domain not verified
- DNS records incorrect

**Solutions:**
1. Wait 5-10 minutes for certificate provisioning
2. Verify DNS records point to Railway
3. Check domain verification status
4. Use Railway-provided subdomain temporarily

---

## Cost Management

### Railway Pricing

**Hobby Plan: $5/month**
- $5 credits included
- Pay for additional usage
- Suitable for: Development, small projects

**Pro Plan: $20/month**
- $20 credits included
- Priority support
- Advanced features
- Suitable for: Production, scaling needs

### Cost Optimization

**Tips:**
1. **Right-size resources** - Don't over-provision
2. **Use sleep/wakeup** - For dev environments
3. **Monitor usage** - Track credits in dashboard
4. **Optimize database** - Regular VACUUM, indexing
5. **Cache responses** - Reduce redundant work

**Monitor Costs:**
```bash
# View current usage
railway status

# Check billing
# Go to: dashboard → Account → Billing
```

---

## Next Steps

- **[Docker Guide](docker.md)** - Advanced Docker configuration
- **[Kubernetes](kubernetes.md)** - Deploy to Kubernetes
- **[Monitoring](monitoring.md)** - Advanced monitoring setup
- **[CI/CD](../cicd/overview.md)** - Automate deployments

---

## Getting Help

- 📖 [Railway Docs](https://docs.railway.app)
- 💬 [Railway Discord](https://discord.gg/railway)
- 🐛 [Report Issues](https://github.com/Melampe001/Tokyo-IA/issues)
- 📧 support@tokyo-ia.example.com

---

*Last updated: 2025-12-23*
