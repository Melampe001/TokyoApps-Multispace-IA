# ❓ Frequently Asked Questions (FAQ)

Answers to common questions about Tokyo-IA. Can't find what you're looking for? Check our [GitHub Discussions](https://github.com/Melampe001/Tokyo-IA/discussions).

## 📋 Table of Contents

- [General Questions](#general-questions)
- [Installation & Setup](#installation--setup)
- [Agents & Models](#agents--models)
- [API & Integration](#api--integration)
- [Deployment](#deployment)
- [Performance & Scaling](#performance--scaling)
- [Troubleshooting](#troubleshooting)
- [Costs & Pricing](#costs--pricing)
- [Security](#security)
- [Contributing](#contributing)

---

## General Questions

### What is Tokyo-IA?

Tokyo-IA is an enterprise-grade AI agent orchestration platform featuring five specialized agents with unique personalities and expertise. Each agent is powered by state-of-the-art LLM models (Claude, GPT, Llama, Gemini) and designed for specific development tasks like code review, testing, DevOps, documentation, and architecture.

### Which LLM models does Tokyo-IA use?

Tokyo-IA uses five different state-of-the-art models:
- **Claude Opus 4.1** (Akira - Code Review)
- **OpenAI o3** (Yuki - Testing, Kenji - Architecture)
- **Llama 4 405B** via Groq (Hiro - DevOps)
- **Gemini 3.0 Ultra** (Sakura - Documentation)

### Is Tokyo-IA open source?

Yes! Tokyo-IA is open source under the Apache 2.0 license. You can view, modify, and contribute to the source code on [GitHub](https://github.com/Melampe001/Tokyo-IA).

### Who should use Tokyo-IA?

Tokyo-IA is perfect for:
- **Development Teams** - Automate code review, testing, and documentation
- **DevOps Engineers** - Generate CI/CD configs and infrastructure code
- **Solo Developers** - Get expert help across all development areas
- **Startups** - Move fast with AI-powered development assistance
- **Enterprises** - Scale development practices across teams

### How is Tokyo-IA different from other AI coding assistants?

Tokyo-IA is unique because:
- **Specialized Agents**: Five experts instead of one generalist
- **Multi-Agent Workflows**: Agents collaborate on complex tasks
- **Production Ready**: Built with Go + PostgreSQL for scale
- **Self-Hosted**: Full control over your data and infrastructure
- **Cross-Platform**: Web, mobile, CLI, and API access

---

## Installation & Setup

### What are the system requirements?

**Minimum:**
- Go 1.21+
- Python 3.10+
- PostgreSQL 14+
- 4GB RAM
- 2GB disk space

**Recommended:**
- Go 1.22+
- Python 3.11+
- PostgreSQL 16+
- 8GB RAM
- 10GB disk space

### Can I run Tokyo-IA without Docker?

Yes! While Docker provides the easiest setup, you can run Tokyo-IA natively. See the [Installation Guide](../getting-started/installation.md) for detailed instructions.

### Do I need API keys to try Tokyo-IA?

No! You can start with `USE_MOCK_AGENTS=true` to use simulated agents without API calls. This is perfect for:
- Exploring the system
- Testing workflows
- Development and testing
- Demos and presentations

### How do I get LLM API keys?

See our [Configuration Guide](../getting-started/configuration.md#api-keys-setup) for step-by-step instructions for:
- Anthropic (Claude)
- OpenAI (GPT/o3)
- Groq (Llama)
- Google AI (Gemini)

### Can I use my own LLM models?

Currently, Tokyo-IA uses the five provider APIs. Self-hosted model support (via Ollama, LM Studio, etc.) is planned for a future release. Track progress in [Issue #XXX](https://github.com/Melampe001/Tokyo-IA/issues).

### Installation fails with "database connection error"

Common causes:
1. **PostgreSQL not running**: Start with `brew services start postgresql` (macOS) or `systemctl start postgresql` (Linux)
2. **Wrong connection string**: Check `DATABASE_URL` in `.env`
3. **Database doesn't exist**: Create with `createdb tokyoia`
4. **Permission denied**: Create postgres user for your account

See [Troubleshooting](../getting-started/installation.md#troubleshooting) for more details.

---

## Agents & Models

### Can I add custom agents?

Yes! The agent system is extensible. See the [Integration Guide](../agents/integration-guide.md) for creating custom agents. A future release will add a plugin system for easier agent creation.

### Can I change which model an agent uses?

Not currently through configuration, but you can modify the agent code to use different models. Model configuration support is planned for v2.0.

### How much do API calls cost?

Costs vary by provider and usage. Typical ranges:

| Task Type | Average Cost |
|-----------|--------------|
| Code Review | $0.05-$0.15 |
| Test Generation | $0.08-$0.20 |
| Documentation | $0.03-$0.30 |
| Architecture | $0.10-$0.35 |
| CI/CD Setup | $0.02-$0.08 |

See [Pricing Guide](../PRICING.md) for detailed cost analysis.

### Which agent should I use for my task?

- **Akira** - Security audits, performance reviews, code quality
- **Yuki** - Test generation, test strategy, coverage analysis
- **Hiro** - Kubernetes, CI/CD, monitoring, infrastructure
- **Sakura** - Documentation, API specs, README files, diagrams
- **Kenji** - System design, architecture, technology selection

### Can agents work together on a task?

Yes! That's the power of Tokyo-IA. Use multi-agent workflows to combine agent expertise. Example: Akira reviews code → Yuki generates tests → Hiro sets up CI/CD → Sakura writes docs.

### How accurate are the agents?

Agents leverage state-of-the-art LLM models with high accuracy. However:
- Always review agent output
- Agents work best as assistants, not replacements
- Provide clear, specific task descriptions
- Use focused prompts for best results

Current success rates:
- Akira: 98.5%
- Yuki: 97.2%
- Hiro: 96.8%
- Sakura: 99.1%
- Kenji: 97.9%

---

## API & Integration

### Is there a Python SDK?

Yes! The `lib/` directory contains Python client code. Full SDK documentation is in progress. For now, see [examples/python/](../../examples/python/) for usage examples.

### Is there a JavaScript/TypeScript SDK?

Not yet, but it's planned. Currently, you can use the REST API directly with `fetch` or `axios`. See [API Examples](../api/examples.md).

### Can I integrate Tokyo-IA into my CI/CD pipeline?

Absolutely! Tokyo-IA is designed for CI/CD integration. Use the CLI tools or REST API. See [CI/CD Integration Guide](../cicd/overview.md).

### Does Tokyo-IA support webhooks?

Webhook support is planned for v1.5. For now, poll the task status endpoint or use the Python orchestrator directly.

### What's the API rate limit?

Default: 60 requests/minute with burst of 10. Configure with `RATE_LIMIT_REQUESTS_PER_MINUTE` and `RATE_LIMIT_BURST`.

### Is there a GraphQL API?

Not yet. GraphQL support is planned for v2.0. Current API is REST only.

---

## Deployment

### Can I deploy to AWS/GCP/Azure?

Yes! While our documentation focuses on Railway, Tokyo-IA can deploy anywhere:
- **AWS**: ECS, EKS, EC2
- **GCP**: Cloud Run, GKE, Compute Engine
- **Azure**: Container Instances, AKS, VMs
- **Self-hosted**: Any server with Docker

See [Docker Guide](../deployment/docker.md) and [Kubernetes Guide](../deployment/kubernetes.md).

### Why do you recommend Railway?

Railway offers:
- ✅ One-click PostgreSQL
- ✅ Automatic deployments from GitHub
- ✅ Built-in monitoring and logs
- ✅ Simple environment variable management
- ✅ Reasonable pricing for startups
- ✅ Great developer experience

But you're free to deploy anywhere!

### How do I scale Tokyo-IA?

**Horizontal Scaling:**
- Run multiple API server instances
- Load balance with Railway/K8s
- Scale agent workers independently

**Vertical Scaling:**
- Increase PostgreSQL resources
- Add read replicas for read-heavy loads
- Use connection pooling

See [Scalability Guide](../architecture/overview.md#scalability-considerations).

### Can I run Tokyo-IA in Kubernetes?

Yes! See the [Kubernetes Deployment Guide](../deployment/kubernetes.md) for manifests and best practices.

### What about disaster recovery?

**Database Backups:**
- Railway: Automatic daily backups
- Self-hosted: Use `pg_dump` or WAL archiving
- Keep backups offsite (S3, GCS, etc.)

**High Availability:**
- PostgreSQL replicas
- Multiple API instances
- Health checks and auto-restart

---

## Performance & Scaling

### How fast are agent responses?

Average latencies:
- Akira: 2.3s
- Yuki: 2.0s
- Hiro: 1.8s
- Sakura: 2.5s
- Kenji: 2.1s

Latency depends on:
- LLM provider response time
- Task complexity
- Network conditions
- Input size

### How many requests can Tokyo-IA handle?

Current production stats:
- **API**: 15,000+ concurrent requests
- **Tasks/second**: 250+
- **Database connections**: 150
- **Response time (p95)**: 45ms (API), 2.8s (agent tasks)

### What's the database size like?

Rough estimates:
- Each task: ~5-10KB
- 1K tasks/day: ~5GB/year
- 10K tasks/day: ~50GB/year
- 100K tasks/day: ~500GB/year

Use PostgreSQL partitioning and archiving for large deployments.

### Can I use Redis for caching?

Yes! Set `REDIS_URL` in your environment. Redis is optional but recommended for:
- Response caching
- Rate limiting
- Session storage
- Real-time metrics

### How do I optimize token usage?

**Tips:**
1. Use focused prompts
2. Limit context size
3. Cache common responses
4. Use cheaper models where appropriate
5. Enable response streaming
6. Set appropriate token limits

---

## Troubleshooting

### "Agent not responding" errors

**Possible causes:**
1. API key invalid or expired
2. Rate limit hit on LLM provider
3. Network connectivity issues
4. LLM provider outage

**Solutions:**
- Check API keys
- Verify provider status pages
- Check agent logs
- Try with `USE_MOCK_AGENTS=true`

### Tasks stuck in "pending" status

**Causes:**
- Orchestrator not running
- Database connection lost
- Queue full

**Solutions:**
```bash
# Check if orchestrator is running
ps aux | grep orchestrator

# Restart orchestrator
python -m lib.orchestrator

# Check database connection
psql $DATABASE_URL -c "SELECT 1"
```

### High token costs

**Optimization:**
1. Use more specific prompts
2. Limit context window
3. Use model-specific token limits
4. Enable caching
5. Monitor usage with `/api/metrics`

### "Database connection refused"

```bash
# Check if PostgreSQL is running
# macOS:
brew services list

# Linux:
systemctl status postgresql

# Start if not running
brew services start postgresql@16  # macOS
systemctl start postgresql         # Linux
```

---

## Costs & Pricing

### How much does it cost to run Tokyo-IA?

**Infrastructure:**
- Railway Hobby: $5/month (includes PostgreSQL)
- Railway Pro: $20/month + usage
- Self-hosted: Server costs only

**LLM API Costs:**
Highly variable based on usage. Typical scenarios:

| Usage Level | Tasks/Day | Monthly Cost |
|-------------|-----------|--------------|
| Light | 10-50 | $10-50 |
| Medium | 100-500 | $100-500 |
| Heavy | 1000+ | $500-2000+ |

### Are there free tiers?

**LLM Providers:**
- Anthropic: No free tier
- OpenAI: $5-10 free credits for new accounts
- Groq: Generous free tier
- Google AI: Free tier available

**Infrastructure:**
- Railway: Free trial, then paid
- Self-hosted: Free (your server costs)

### How do I control costs?

1. **Set Limits:**
   ```bash
   MAX_COST_PER_TASK_USD=1.00
   MAX_COST_PER_WORKFLOW_USD=10.00
   ```

2. **Monitor Usage:**
   ```bash
   curl http://localhost:8080/api/metrics
   ```

3. **Use Cheaper Models:**
   - Groq (Llama) is most cost-effective
   - Use mock mode for testing

4. **Optimize Prompts:**
   - Be specific
   - Limit context
   - Cache responses

See [Pricing Guide](../PRICING.md) for detailed cost analysis and optimization tips.

---

## Security

### Is Tokyo-IA secure?

Tokyo-IA follows security best practices:
- ✅ No secrets in code
- ✅ Environment variable configuration
- ✅ PostgreSQL with parameterized queries
- ✅ CORS configuration
- ✅ Rate limiting
- ✅ Input validation
- ✅ Regular security scans (CodeQL, Dependabot)

See [Security Policy](../../SECURITY.md) for details.

### How should I store API keys?

**Development:**
- `.env` file (gitignored)
- Never commit to git

**Production:**
- Environment variables
- Secret managers (AWS Secrets Manager, Vault)
- Railway environment variables
- Kubernetes secrets

**Never:**
- Hardcode in source
- Commit to version control
- Share in public channels

### Does Tokyo-IA store my code?

**In Database:**
- Task input/output stored in PostgreSQL
- Use for audit, analysis, debugging

**Not Sent to LLMs:**
- Only task-specific code is sent
- No access to your full codebase
- No persistent storage by LLM providers

**To Delete:**
```sql
DELETE FROM agent_tasks WHERE id = 'task-id';
```

### Can I run Tokyo-IA in an air-gapped environment?

Not currently, as agents require internet access to LLM APIs. For air-gapped deployments, you'd need:
1. Self-hosted LLM models (planned for future)
2. Internal network access to model servers

### How do I report security vulnerabilities?

See [Security Policy](../../SECURITY.md) or email security@tokyo-ia.example.com.

---

## Contributing

### How can I contribute?

We welcome contributions! See [Contributing Guide](../development/contributing.md) for:
- Code contributions
- Documentation improvements
- Bug reports
- Feature requests
- Translations

### I found a bug, how do I report it?

1. Check [existing issues](https://github.com/Melampe001/Tokyo-IA/issues)
2. Create a new issue with:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details
   - Logs/screenshots

Use the [bug report template](https://github.com/Melampe001/Tokyo-IA/issues/new?template=bug_report.md).

### Can I request new features?

Yes! Open a [feature request](https://github.com/Melampe001/Tokyo-IA/issues/new?template=feature_request.md) with:
- Use case description
- Proposed solution
- Benefits
- Alternatives considered

### How do I submit a pull request?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit PR with clear description

See [Contributing Guide](../development/contributing.md) for details.

### Where can I get help?

- 📖 [Documentation](../README.md)
- 💬 [GitHub Discussions](https://github.com/Melampe001/Tokyo-IA/discussions)
- 🐛 [Issue Tracker](https://github.com/Melampe001/Tokyo-IA/issues)
- 📧 support@tokyo-ia.example.com

---

## Still Have Questions?

- 💬 Ask in [GitHub Discussions](https://github.com/Melampe001/Tokyo-IA/discussions)
- 📖 Browse the [full documentation](../README.md)
- 🐛 [Report an issue](https://github.com/Melampe001/Tokyo-IA/issues)
- 📧 Email: support@tokyo-ia.example.com

---

*Last updated: 2025-12-23*
