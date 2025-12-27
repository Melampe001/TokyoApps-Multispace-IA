# Railway Deployment Guide

This guide explains how to deploy Tokyo-IA to Railway for production.

## Prerequisites

- Railway account ([railway.app](https://railway.app))
- GitHub repository connected to Railway
- Database requirements (Railway PostgreSQL)

## Quick Start

1. **Connect Repository to Railway**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login to Railway
   railway login
   
   # Link your project
   railway link
   ```

2. **Configure Environment Variables**
   
   Navigate to your Railway project dashboard and add the following environment variables:

### Required Environment Variables

#### Application Configuration
```bash
PORT=8080                    # Railway automatically injects this
GO_ENV=production           # Set environment mode
LOG_LEVEL=info              # Logging level
```

#### Database Configuration
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}  # Railway PostgreSQL connection
```

#### AI Provider API Keys
```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic (Claude)
ANTHROPIC_API_KEY=sk-ant-...

# Google (Gemini)
GOOGLE_API_KEY=...

# Enable real AI clients (set to "true" for production)
USE_REAL_AI_CLIENTS=true
```

#### Integration Secrets (Optional)
```bash
# Jira Integration
JIRA_BASE_URL=https://your-org.atlassian.net
JIRA_API_TOKEN=...

# Google Sheets
GOOGLE_CREDENTIALS={"type":"service_account",...}
GOOGLE_SHEET_ID=...

# Slack Bot
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...

# AWS (Data Lake)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
S3_DATA_LAKE_BUCKET=tokyo-ia-data-lake
ATHENA_DATABASE=tokyo_ia_billing
```

## Database Setup

### Railway PostgreSQL

1. **Add PostgreSQL to your project:**
   ```bash
   railway add
   # Select "PostgreSQL"
   ```

2. **The `DATABASE_URL` is automatically injected** as `${{Postgres.DATABASE_URL}}`

3. **Run migrations** (if applicable):
   ```bash
   railway run make migrate
   ```

## Deployment Configuration

The deployment is configured via `railway.toml`:

```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
numReplicas = 1
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
healthcheckPath = "/health"
healthcheckTimeout = 300
```

### Key Configuration Details

- **Builder**: Uses Docker for consistent builds
- **Health Check**: Endpoint at `/health` must return 200
- **Timeout**: 300 seconds for health check (allows for slow cold starts)
- **Restart Policy**: Automatically restarts on failure, up to 10 retries

## Scaling Configuration

### Horizontal Scaling

To scale horizontally, update `railway.toml`:

```toml
[deploy]
numReplicas = 3  # Run 3 instances
```

Or use the Railway dashboard:
1. Navigate to your service
2. Click "Settings"
3. Adjust "Replicas" slider

### Vertical Scaling

Railway automatically scales compute resources. For custom sizing:
1. Navigate to service settings
2. Select a larger plan if needed

## Monitoring Setup

### Health Checks

The application exposes a health check endpoint:
```
GET /health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-27T10:00:00Z",
  "version": "1.0.0"
}
```

### Viewing Logs

```bash
# Via CLI
railway logs

# Or via dashboard
# Navigate to your service → "Deployments" → Select deployment → "View Logs"
```

### Metrics

Railway provides built-in metrics:
- CPU usage
- Memory usage
- Network traffic
- Request count

Access via the service dashboard → "Metrics" tab

## Secrets Management

### Best Practices

1. **Never commit secrets** to the repository
2. **Use Railway environment variables** for all sensitive data
3. **Rotate secrets regularly**
4. **Use different secrets per environment** (dev, staging, production)

### Adding Secrets

Via CLI:
```bash
railway variables set OPENAI_API_KEY=sk-...
```

Via Dashboard:
1. Navigate to project
2. Select "Variables" tab
3. Click "+ New Variable"
4. Enter key and value
5. Click "Add"

## Deployment Process

### Automatic Deployments

Railway automatically deploys when you push to your main branch:

```bash
git push origin main
```

### Manual Deployments

```bash
# Via CLI
railway up

# Or redeploy via dashboard
# Navigate to service → "Deployments" → Click "Redeploy"
```

### Rollback

To rollback to a previous deployment:
1. Navigate to service → "Deployments"
2. Find the working deployment
3. Click "..." menu → "Redeploy"

## Troubleshooting

### Common Issues

#### 1. Health Check Failing

**Symptoms**: Deployment shows unhealthy status

**Solutions**:
- Verify `/health` endpoint returns 200
- Check application logs: `railway logs`
- Ensure `PORT` environment variable is used
- Increase `healthcheckTimeout` if needed

#### 2. Database Connection Failed

**Symptoms**: Application crashes with database errors

**Solutions**:
- Verify `DATABASE_URL` is set correctly
- Check PostgreSQL service is running
- Ensure database migrations have run
- Check network policies allow connection

#### 3. Build Failures

**Symptoms**: Deployment fails during build

**Solutions**:
- Check Dockerfile syntax
- Verify all dependencies are specified in `go.mod`
- Review build logs for specific errors
- Test build locally: `docker build -t tokyo-ia .`

#### 4. Out of Memory

**Symptoms**: Application crashes or restarts frequently

**Solutions**:
- Monitor memory usage in Railway metrics
- Optimize memory-intensive operations
- Upgrade to a larger Railway plan
- Implement caching to reduce memory usage

#### 5. API Keys Not Working

**Symptoms**: AI provider requests fail

**Solutions**:
- Verify API keys are correct and active
- Check `USE_REAL_AI_CLIENTS=true` is set
- Ensure no quotes around environment variable values
- Test keys with provider's API documentation

### Debug Mode

Enable debug logging:
```bash
railway variables set LOG_LEVEL=debug
```

View detailed logs:
```bash
railway logs --tail 100
```

## Performance Optimization

### Caching

Enable response caching in the model router:
```go
config := &ai.RouterConfig{
    EnableCaching:    true,
    CacheTTL:         time.Hour,
    EnableFallback:   true,
    MaxRetries:       3,
}
```

### Connection Pooling

Configure database connection pooling:
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db?pool_max_conns=10
```

## Security Checklist

- [ ] All API keys stored as environment variables
- [ ] Database credentials secured
- [ ] HTTPS enabled (Railway provides this automatically)
- [ ] Secrets rotated regularly
- [ ] Access logs monitored
- [ ] Rate limiting configured
- [ ] CORS policies set appropriately

## Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Railway CLI Reference](https://docs.railway.app/develop/cli)
- [Tokyo-IA Main Documentation](../README.md)
- [AWS Setup Guide](./AWS_SETUP.md)
- [Architecture Overview](../ARCHITECTURE.md)

## Support

For deployment issues:
1. Check this guide first
2. Review Railway documentation
3. Check application logs
4. Open an issue in the GitHub repository
5. Contact the Tokyo-IA team

## Next Steps

After successful deployment:
1. Verify health check endpoint responds
2. Test AI provider integrations
3. Monitor application metrics
4. Set up alerting (via Railway webhooks or external services)
5. Configure external integrations (Jira, Sheets, Slack)
6. Review and optimize performance
