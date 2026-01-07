# 🔐 Security Best Practices

Security guidelines and best practices for deploying and using Tokyo-IA safely.

## 📋 Table of Contents

- [Security Philosophy](#security-philosophy)
- [Authentication & Authorization](#authentication--authorization)
- [API Security](#api-security)
- [Database Security](#database-security)
- [Secret Management](#secret-management)
- [Network Security](#network-security)
- [Code Security](#code-security)
- [Deployment Security](#deployment-security)
- [Monitoring & Auditing](#monitoring--auditing)
- [Incident Response](#incident-response)

---

## Security Philosophy

Tokyo-IA follows security best practices:

- **Defense in Depth** - Multiple layers of security
- **Least Privilege** - Minimum necessary permissions
- **Zero Trust** - Verify everything, trust nothing
- **Secure by Default** - Secure configurations out of the box
- **Transparency** - Open source, auditable code

---

## Authentication & Authorization

### Current State (v1.0)

**API Key Authentication** (Optional):
```bash
# Enable API key requirement
API_KEY_REQUIRED=true

# Generate strong API keys
openssl rand -hex 32

# Use in requests
curl -H "X-API-Key: your-api-key" https://api.tokyo-ia.com/agents
```

### Coming Soon (v1.5+)

- **JWT Authentication** - Token-based auth
- **OAuth2** - Third-party authentication
- **SSO** - Single sign-on
- **RBAC** - Role-based access control

### Best Practices

1. **Strong API Keys**
   ```bash
   # Good: 64 characters, random
   API_KEY=$(openssl rand -hex 32)
   
   # Bad: Short, predictable
   API_KEY="mykey123"  # ❌ Never do this
   ```

2. **Rotate Keys Regularly**
   ```bash
   # Rotate every 90 days
   # Set calendar reminder
   # Use secret manager rotation policies
   ```

3. **Separate Keys per Environment**
   ```bash
   # Development
   DEV_API_KEY="dev_..."
   
   # Staging
   STAGING_API_KEY="staging_..."
   
   # Production
   PROD_API_KEY="prod_..."
   ```

4. **Limit Key Scope**
   ```bash
   # Coming in v1.5: scoped keys
   API_KEY_SCOPES="read:agents,write:tasks"
   ```

---

## API Security

### HTTPS/TLS

**Always use HTTPS in production:**

```bash
# ✅ Good
https://tokyo-ia.up.railway.app

# ❌ Bad
http://tokyo-ia.up.railway.app
```

Railway provides free SSL certificates automatically.

### CORS Configuration

**Production:**
```bash
# Specific origins only
CORS_ORIGINS="https://app.example.com,https://admin.example.com"
```

**Development:**
```bash
# Local development only
CORS_ORIGINS="http://localhost:3000,http://localhost:5173"
```

**Never in Production:**
```bash
# ❌ Dangerous!
CORS_ORIGINS="*"
```

### Rate Limiting

**Enable rate limiting:**
```bash
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_BURST=10
```

**Monitor for abuse:**
```sql
-- Check for suspicious activity
SELECT 
    client_ip,
    COUNT(*) as request_count,
    COUNT(DISTINCT agent_id) as agents_accessed
FROM request_logs
WHERE timestamp > NOW() - INTERVAL '1 hour'
GROUP BY client_ip
HAVING COUNT(*) > 1000
ORDER BY request_count DESC;
```

### Input Validation

All inputs are validated:

```go
// Example: Agent ID validation
func validateAgentID(id string) error {
    if !regexp.MustCompile(`^[a-z]+-\d{3}$`).MatchString(id) {
        return errors.New("invalid agent ID format")
    }
    return nil
}
```

### SQL Injection Prevention

**Always use parameterized queries:**

```go
// ✅ Good: Parameterized query
db.Query("SELECT * FROM agents WHERE id = $1", agentID)

// ❌ Bad: String interpolation
db.Query(fmt.Sprintf("SELECT * FROM agents WHERE id = '%s'", agentID))
```

### XSS Prevention

**Sanitize outputs:**

```go
import "html"

// Escape HTML in responses
output := html.EscapeString(userInput)
```

---

## Database Security

### Connection Security

**Use SSL for database connections:**

```bash
# Production: SSL required
DATABASE_URL="postgresql://user:pass@host:5432/db?sslmode=require"

# Development: SSL preferred
DATABASE_URL="postgresql://user:pass@localhost:5432/db?sslmode=prefer"
```

### Access Control

**Principle of least privilege:**

```sql
-- Create read-only user for analytics
CREATE USER readonly_user WITH PASSWORD 'strong_password';
GRANT CONNECT ON DATABASE tokyoia TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;

-- Create app user with limited permissions
CREATE USER app_user WITH PASSWORD 'strong_password';
GRANT CONNECT ON DATABASE tokyoia TO app_user;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO app_user;
-- No DELETE or DROP permissions
```

### Password Security

**Strong passwords:**

```bash
# Generate strong passwords
openssl rand -base64 32

# Use password managers
# Never store passwords in code
# Use environment variables
```

### Backup Security

**Encrypt backups:**

```bash
# Encrypted backup
pg_dump tokyoia | gpg --encrypt --recipient admin@example.com > backup.sql.gpg

# Encrypted restore
gpg --decrypt backup.sql.gpg | psql tokyoia
```

**Store securely:**
- AWS S3 with encryption
- Google Cloud Storage with encryption
- Azure Blob Storage with encryption
- Never store on public repositories

---

## Secret Management

### Never Commit Secrets

**❌ Bad:**
```go
// NEVER do this
const ANTHROPIC_API_KEY = "sk-ant-api03-..."
```

**✅ Good:**
```go
apiKey := os.Getenv("ANTHROPIC_API_KEY")
if apiKey == "" {
    log.Fatal("ANTHROPIC_API_KEY not set")
}
```

### .gitignore

**Always ignore secret files:**

```gitignore
# Environment variables
.env
.env.local
.env.*.local

# API keys
*.key
*.pem
secrets/

# Credentials
credentials.json
service-account.json
```

### Environment Variables

**Development:**
```bash
# .env file (gitignored)
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
```

**Production:**

Use secret managers:

**Railway:**
- Use environment variables in dashboard
- Automatic encryption
- No need for .env files

**AWS:**
```bash
# AWS Secrets Manager
aws secretsmanager create-secret \
    --name tokyo-ia/api-keys \
    --secret-string '{"ANTHROPIC_API_KEY":"sk-ant-..."}'
```

**Kubernetes:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: tokyo-ia-secrets
type: Opaque
stringData:
  ANTHROPIC_API_KEY: sk-ant-...
```

### Secret Rotation

**Regular rotation schedule:**

| Secret Type | Rotation Frequency |
|-------------|-------------------|
| API Keys | 90 days |
| Database Passwords | 180 days |
| TLS Certificates | 365 days |
| SSH Keys | 365 days |

**Automated rotation:**

```bash
# Example: Rotate API key
NEW_KEY=$(openssl rand -hex 32)

# Update in secret manager
railway variables set API_KEY=$NEW_KEY

# Deploy with new key
railway up
```

---

## Network Security

### Firewall Rules

**Restrict database access:**

```bash
# Only allow app servers
# PostgreSQL: Port 5432
Allow: 10.0.1.0/24  # App server subnet
Deny: 0.0.0.0/0     # Everything else
```

**API server:**

```bash
# Allow HTTPS only
Allow: 0.0.0.0/0:443 # HTTPS
Deny: 0.0.0.0/0:80   # HTTP
```

### VPC/Private Networks

**Production setup:**

```
┌─────────────────────────────────────┐
│ VPC: 10.0.0.0/16                   │
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │ Public       │  │ Private     │ │
│  │ Subnet       │  │ Subnet      │ │
│  │ 10.0.1.0/24  │  │ 10.0.2.0/24 │ │
│  │              │  │             │ │
│  │ ┌──────────┐ │  │ ┌─────────┐│ │
│  │ │ API      │ │  │ │Database ││ │
│  │ │ Servers  │────▶│ │         ││ │
│  │ └──────────┘ │  │ └─────────┘│ │
│  └──────────────┘  └─────────────┘ │
└─────────────────────────────────────┘
```

### DDoS Protection

**Use CloudFlare or similar:**

```bash
# CloudFlare settings
- Rate limiting: 100 req/min
- Challenge on suspicious activity
- Bot protection enabled
- WAF rules configured
```

---

## Code Security

### Dependency Security

**Automated scanning:**

```yaml
# .github/workflows/security.yml
- name: Run CodeQL
  uses: github/codeql-action/analyze@v2

- name: Dependency Review
  uses: actions/dependency-review-action@v3
```

**Manual checks:**

```bash
# Go dependencies
go list -m -u all

# Python dependencies
pip list --outdated

# Check for known vulnerabilities
safety check  # Python
govulncheck ./...  # Go
```

### Code Review

**Security checklist:**

- [ ] Input validation on all user inputs
- [ ] Parameterized database queries
- [ ] Output encoding to prevent XSS
- [ ] Authentication checks on sensitive endpoints
- [ ] Authorization checks (RBAC)
- [ ] No secrets in code
- [ ] Error messages don't leak info
- [ ] HTTPS enforced
- [ ] CORS properly configured
- [ ] Rate limiting implemented

### Static Analysis

**Run before commit:**

```bash
# Go
golangci-lint run

# Python
bandit -r lib/
pylint lib/

# Security specific
gosec ./...
```

---

## Deployment Security

### Container Security

**Secure Dockerfile:**

```dockerfile
# ✅ Use specific versions
FROM golang:1.22-alpine AS builder

# ✅ Run as non-root
RUN adduser -D -u 1000 appuser
USER appuser

# ✅ Minimal final image
FROM alpine:latest
COPY --from=builder /app/binary /app/binary
USER appuser
CMD ["/app/binary"]
```

**Scan images:**

```bash
# Trivy scanner
trivy image tokyo-ia:latest

# Docker Scout
docker scout cves tokyo-ia:latest
```

### Kubernetes Security

**Security contexts:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: tokyo-ia
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
  containers:
  - name: api
    image: tokyo-ia:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
```

### Environment Isolation

**Separate environments:**

```
Development  → dev.tokyo-ia.internal
Staging      → staging.tokyo-ia.com
Production   → tokyo-ia.com
```

**No production secrets in dev:**

```bash
# ✅ Use test API keys in development
ANTHROPIC_API_KEY="test_key_only"

# ✅ Use separate databases
DEV_DB="tokyoia_dev"
PROD_DB="tokyoia_prod"
```

---

## Monitoring & Auditing

### Audit Logging

**Log security events:**

```go
// Log authentication attempts
log.WithFields(log.Fields{
    "event": "auth_attempt",
    "ip": clientIP,
    "success": authSuccess,
    "timestamp": time.Now(),
}).Info("Authentication attempt")
```

**What to log:**

- Authentication attempts (success/failure)
- API key usage
- Rate limit violations
- Database access
- Configuration changes
- Security-related errors

**What NOT to log:**

- ❌ Passwords (even hashed)
- ❌ API keys
- ❌ Personal information (PII)
- ❌ Credit card numbers
- ❌ Session tokens

### Security Monitoring

**Set up alerts:**

```bash
# Sentry for error tracking
SENTRY_DSN="https://...@sentry.io/..."

# Alert on:
- Multiple failed auth attempts
- Unusual API usage patterns
- Database connection failures
- High error rates
- Suspicious IP addresses
```

### Compliance

**GDPR considerations:**

- User data: Stored in database
- Right to deletion: Implement data deletion
- Data portability: Export functionality
- Consent: Track user consent

**Audit trail:**

```sql
-- Track all data access
CREATE TABLE audit_log (
    id UUID PRIMARY KEY,
    user_id VARCHAR(100),
    action VARCHAR(50),
    resource_type VARCHAR(50),
    resource_id VARCHAR(100),
    ip_address INET,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

---

## Incident Response

### Security Incident Plan

**1. Detection**
- Monitor alerts
- Review logs
- User reports

**2. Containment**
```bash
# Immediately revoke compromised keys
railway variables unset COMPROMISED_KEY

# Block suspicious IPs
# Railway → Settings → Network → Block IP
```

**3. Investigation**
```sql
-- Check for unauthorized access
SELECT * FROM audit_log
WHERE timestamp > NOW() - INTERVAL '24 hours'
AND action IN ('unauthorized_access', 'failed_auth')
ORDER BY timestamp DESC;
```

**4. Remediation**
- Rotate all keys
- Patch vulnerabilities
- Update security rules

**5. Communication**
- Notify affected users
- Post-mortem report
- Update documentation

### Contact Information

**Security Team:**
- 📧 security@tokyo-ia.example.com
- 🔒 PGP Key: [link to public key]
- 📞 Emergency: +1-XXX-XXX-XXXX

**Report Vulnerabilities:**
See [Vulnerability Reporting](vulnerability-reporting.md)

---

## Security Checklist

### Before Deployment

- [ ] All secrets in environment variables
- [ ] No secrets committed to git
- [ ] HTTPS enforced
- [ ] Database connection encrypted (SSL)
- [ ] Strong passwords generated
- [ ] API keys rotated
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Input validation on all endpoints
- [ ] Security headers configured
- [ ] Dependency scan passed
- [ ] Container scan passed
- [ ] Backup strategy in place
- [ ] Monitoring configured
- [ ] Incident response plan ready

### Regular Maintenance

- [ ] Review audit logs (weekly)
- [ ] Check for dependency updates (weekly)
- [ ] Review access permissions (monthly)
- [ ] Rotate API keys (quarterly)
- [ ] Rotate database passwords (semi-annually)
- [ ] Security audit (annually)
- [ ] Penetration testing (annually)

---

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- [Security Policy](../../SECURITY.md)

---

*Last updated: 2025-12-23*
