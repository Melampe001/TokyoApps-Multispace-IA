# 💰 Pricing & Cost Guide

Understanding and optimizing costs for running Tokyo-IA, including infrastructure and LLM API costs.

## 📋 Table of Contents

- [Cost Components](#cost-components)
- [Infrastructure Costs](#infrastructure-costs)
- [LLM API Costs](#llm-api-costs)
- [Cost Calculator](#cost-calculator)
- [Cost Optimization](#cost-optimization)
- [Example Scenarios](#example-scenarios)

---

## Cost Components

Tokyo-IA costs consist of two main categories:

### 1. Infrastructure Costs
- Hosting platform (Railway, AWS, etc.)
- Database (PostgreSQL)
- Compute resources (CPU, RAM)
- Network bandwidth
- Optional: Redis cache, monitoring tools

### 2. LLM API Costs
- Anthropic (Claude) for Akira
- OpenAI (GPT/o3) for Yuki & Kenji
- Groq (Llama) for Hiro
- Google AI (Gemini) for Sakura

---

## Infrastructure Costs

### Railway (Recommended)

**Hobby Plan: $5/month**
- $5 in included credits
- PostgreSQL database included
- 512MB RAM, 1 vCPU (adjustable)
- Great for: Development, small projects

**Pro Plan: $20/month**
- $20 in included credits
- Scales with usage
- Priority support
- Great for: Production, growing projects

**Additional Costs:**
- Extra compute: ~$0.000463/GB-hour
- Extra memory: ~$0.000231/GB-hour
- Network: First 100GB free

**Example Monthly Costs:**
```
Small deployment (1GB RAM, 1 vCPU):
- Base: $5-20
- Compute: ~$35
- Total: $40-55/month

Medium deployment (4GB RAM, 2 vCPU):
- Base: $20
- Compute: ~$140
- Total: $160/month

Large deployment (8GB RAM, 4 vCPU):
- Base: $20
- Compute: ~$280
- Total: $300/month
```

### AWS (Self-Hosted)

**EC2 Costs:**
| Instance Type | vCPU | RAM | Cost/Month | Use Case |
|---------------|------|-----|------------|----------|
| t3.small | 2 | 2GB | $15 | Development |
| t3.medium | 2 | 4GB | $30 | Small production |
| t3.large | 2 | 8GB | $60 | Medium production |
| m5.xlarge | 4 | 16GB | $140 | Large production |

**RDS PostgreSQL:**
| Instance | Storage | Cost/Month |
|----------|---------|------------|
| db.t3.micro | 20GB | $15 |
| db.t3.small | 50GB | $30 |
| db.t3.medium | 100GB | $60 |

**Total AWS Estimate:**
- Small: $30-50/month
- Medium: $90-150/month
- Large: $200-400/month

### GCP & Azure
Similar pricing structures to AWS. Use their pricing calculators:
- [GCP Pricing Calculator](https://cloud.google.com/products/calculator)
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)

---

## LLM API Costs

### Pricing by Provider

#### Anthropic (Claude)
Used by: **Akira** (Code Review Master)

| Model | Input | Output | Context |
|-------|-------|--------|---------|
| Claude Opus 4 | $15/M tokens | $75/M tokens | 200K |
| Claude Sonnet 3.5 | $3/M tokens | $15/M tokens | 200K |

**Average Task Cost:** $0.05-$0.15

#### OpenAI
Used by: **Yuki** (Testing), **Kenji** (Architecture)

| Model | Input | Output | Context |
|-------|-------|--------|---------|
| GPT-4 Turbo | $10/M tokens | $30/M tokens | 128K |
| GPT-4 | $30/M tokens | $60/M tokens | 8K |
| o3-mini | $1/M tokens | $4/M tokens | 128K |
| o3 | $15/M tokens | $60/M tokens | 128K |

**Average Task Cost:** $0.08-$0.20

#### Groq (Llama)
Used by: **Hiro** (DevOps)

| Model | Input | Output | Context |
|-------|-------|--------|---------|
| Llama 3.1 405B | $0.59/M tokens | $0.79/M tokens | 128K |
| Llama 3.1 70B | $0.59/M tokens | $0.79/M tokens | 128K |

**Average Task Cost:** $0.02-$0.08 (Most cost-effective!)

#### Google AI (Gemini)
Used by: **Sakura** (Documentation)

| Model | Input | Output | Context |
|-------|-------|--------|---------|
| Gemini 1.5 Pro | $1.25/M tokens | $5/M tokens | 2M |
| Gemini 1.5 Flash | $0.075/M tokens | $0.30/M tokens | 1M |

**Average Task Cost:** $0.03-$0.30

### Token Usage by Task Type

| Task Type | Avg Input Tokens | Avg Output Tokens | Total |
|-----------|-----------------|-------------------|-------|
| Code Review (Akira) | 1,500 | 2,000 | 3,500 |
| Test Generation (Yuki) | 2,000 | 4,000 | 6,000 |
| DevOps Config (Hiro) | 1,000 | 2,500 | 3,500 |
| Documentation (Sakura) | 3,000 | 5,000 | 8,000 |
| Architecture (Kenji) | 2,500 | 4,000 | 6,500 |

### Cost per Task Type

| Task Type | Agent | Estimated Cost |
|-----------|-------|----------------|
| Code Review | Akira | $0.05 - $0.15 |
| Security Audit | Akira | $0.10 - $0.25 |
| Test Generation | Yuki | $0.08 - $0.20 |
| Test Strategy | Yuki | $0.05 - $0.15 |
| CI/CD Setup | Hiro | $0.02 - $0.08 |
| Infrastructure | Hiro | $0.03 - $0.10 |
| API Docs | Sakura | $0.03 - $0.10 |
| Long Docs | Sakura | $0.10 - $0.30 |
| System Design | Kenji | $0.10 - $0.35 |
| Refactoring Plan | Kenji | $0.08 - $0.20 |

---

## Cost Calculator

### Monthly Cost Estimator

Use this formula to estimate your monthly LLM costs:

```
Monthly Cost = (Tasks per Day) × (Avg Cost per Task) × 30 days
```

**Examples:**

**Light Usage (10 tasks/day):**
```
10 × $0.10 × 30 = $30/month
```

**Medium Usage (100 tasks/day):**
```
100 × $0.10 × 30 = $300/month
```

**Heavy Usage (500 tasks/day):**
```
500 × $0.10 × 30 = $1,500/month
```

### Interactive Calculator

Use our interactive calculator:

```python
def calculate_monthly_cost(tasks_per_day, avg_cost_per_task=0.10):
    """
    Calculate estimated monthly LLM API costs
    
    Args:
        tasks_per_day: Number of agent tasks per day
        avg_cost_per_task: Average cost per task in USD (default: $0.10)
    
    Returns:
        Monthly cost estimate in USD
    """
    daily_cost = tasks_per_day * avg_cost_per_task
    monthly_cost = daily_cost * 30
    yearly_cost = monthly_cost * 12
    
    return {
        "daily": f"${daily_cost:.2f}",
        "monthly": f"${monthly_cost:.2f}",
        "yearly": f"${yearly_cost:.2f}"
    }

# Example usage
print(calculate_monthly_cost(tasks_per_day=100))
# Output: {'daily': '$10.00', 'monthly': '$300.00', 'yearly': '$3600.00'}
```

---

## Cost Optimization

### 1. Choose Cost-Effective Models

**Recommendation by Task:**

| Task Type | Recommended Model | Why |
|-----------|-------------------|-----|
| Simple reviews | Use Groq (Llama) | 10x cheaper |
| Complex analysis | Use Claude Opus | Worth the cost |
| Documentation | Use Gemini Flash | Huge context, low cost |
| Quick tests | Use GPT-3.5 | Fast and cheap |

### 2. Optimize Prompts

**Bad Prompt (wasteful):**
```python
# Sends entire file (5,000 tokens)
result = akira.execute({
    "code": entire_file_content,
    "instruction": "review"
})
```

**Good Prompt (efficient):**
```python
# Sends only relevant function (500 tokens)
result = akira.execute({
    "code": specific_function,
    "instruction": "Review for SQL injection",
    "context": "authentication module"
})
```

**Savings:** 90% reduction in tokens!

### 3. Enable Caching

```bash
# Enable response caching
CACHE_ENABLED=true
CACHE_TTL_SECONDS=3600  # 1 hour

# Use Redis for better caching
REDIS_URL="redis://localhost:6379/0"
```

**Potential Savings:** 30-50% for repeated queries

### 4. Set Token Limits

```bash
# Prevent runaway costs
AGENT_MAX_TOKENS_PER_REQUEST=4000
AGENT_MAX_TOTAL_TOKENS=100000  # per day

# Set cost limits
MAX_COST_PER_TASK_USD=1.00
MAX_COST_PER_WORKFLOW_USD=10.00
```

### 5. Use Mock Mode for Testing

```bash
# Use mock agents during development
USE_MOCK_AGENTS=true

# No LLM API calls = $0 cost
```

**Savings:** 100% during development and testing

### 6. Batch Operations

```python
# Bad: 100 individual requests
for file in files:
    review_file(file)  # 100 API calls

# Good: 1 batch request
review_files_batch(files)  # 1 API call
```

**Savings:** Up to 99% for bulk operations

### 7. Monitor and Alert

```bash
# Set up cost monitoring
COST_ALERT_THRESHOLD_USD=100.00
COST_ALERT_EMAIL="admin@example.com"

# Check costs regularly
curl http://localhost:8080/api/metrics?metric_type=cost
```

### 8. Smart Agent Selection

Use cheaper agents when possible:

| Scenario | Instead Of | Use | Savings |
|----------|-----------|-----|---------|
| Simple config | Kenji ($0.20) | Hiro ($0.05) | 75% |
| Basic docs | Sakura Pro ($0.15) | Sakura Flash ($0.03) | 80% |
| Quick review | Akira Opus ($0.15) | Akira Sonnet ($0.05) | 67% |

---

## Example Scenarios

### Scenario 1: Solo Developer

**Usage:**
- 5 code reviews/day
- 3 test generations/day
- 2 documentation tasks/day
- Total: 10 tasks/day

**Monthly Costs:**
```
Infrastructure (Railway Hobby): $5
LLM APIs (10 tasks × $0.10 × 30): $30
Total: $35/month
```

**Optimization:**
- Use mock mode for local testing: -$10/month
- Cache common responses: -$5/month
- **Optimized Total: $20/month**

---

### Scenario 2: Small Team (5 developers)

**Usage:**
- 25 code reviews/day
- 15 test generations/day
- 10 CI/CD setups/day
- 10 documentation tasks/day
- Total: 60 tasks/day

**Monthly Costs:**
```
Infrastructure (Railway Pro): $160
LLM APIs (60 tasks × $0.10 × 30): $180
Total: $340/month
```

**Optimization:**
- Use Groq for simple tasks: -$30/month
- Enable caching: -$50/month
- Batch operations: -$20/month
- **Optimized Total: $240/month ($48/developer)**

---

### Scenario 3: Medium Company (20 developers)

**Usage:**
- 150 code reviews/day
- 80 test generations/day
- 40 CI/CD setups/day
- 30 documentation tasks/day
- Total: 300 tasks/day

**Monthly Costs:**
```
Infrastructure (Railway Pro scaled): $300
LLM APIs (300 tasks × $0.10 × 30): $900
Total: $1,200/month
```

**Optimization:**
- Aggressive caching: -$200/month
- Smart model selection: -$150/month
- Batch processing: -$100/month
- **Optimized Total: $750/month ($37.50/developer)**

---

### Scenario 4: Enterprise (100 developers)

**Usage:**
- 500 code reviews/day
- 300 test generations/day
- 150 CI/CD setups/day
- 100 documentation tasks/day
- Total: 1,050 tasks/day

**Monthly Costs:**
```
Infrastructure (AWS/self-hosted): $500
LLM APIs (1,050 tasks × $0.10 × 30): $3,150
Total: $3,650/month
```

**Optimization:**
- Enterprise caching strategy: -$800/month
- Custom fine-tuned models: -$500/month
- Bulk contracts with providers: -$400/month
- **Optimized Total: $1,950/month ($19.50/developer)**

---

## ROI Calculation

### Developer Time Saved

**Assumptions:**
- Average developer hourly rate: $75
- Time saved per task: 30 minutes

**ROI per Task:**
```
Time Saved Value = 0.5 hours × $75 = $37.50
Task Cost = $0.10
Net Savings = $37.40 per task
ROI = 37,400%
```

**Monthly ROI (100 tasks/month):**
```
Cost: $30 (10 tasks/day × $0.10 × 30)
Value: $3,750 (100 tasks × $37.50)
Net Benefit: $3,720
ROI: 12,400%
```

### Quality Improvements

Beyond time savings:
- Fewer bugs in production → Reduced incident costs
- Better test coverage → Fewer customer issues
- Improved documentation → Faster onboarding
- Consistent code review → Better codebase health

---

## Free Tier Options

### LLM Providers with Free Tiers

1. **Groq** - Generous free tier
   - Great for testing
   - Use with Hiro

2. **Google AI (Gemini)** - Free tier available
   - 60 requests/minute
   - Use with Sakura

3. **OpenAI** - $5-10 free credits for new accounts
   - Limited time offer

### Cost-Free Development

```bash
# Use mock agents (100% free)
USE_MOCK_AGENTS=true

# Local PostgreSQL (free)
# Self-hosted on your machine (free)
# Docker deployment (free, your compute)
```

---

## Monitoring Costs

### Track Usage

```bash
# Daily cost report
curl http://localhost:8080/api/metrics?metric_type=cost&timeframe=24h

# Monthly cost by agent
curl http://localhost:8080/api/agents/akira-001/stats?timeframe=30d
```

### Set Alerts

```python
# Configure cost alerts
os.environ['MAX_COST_PER_DAY_USD'] = '50.00'
os.environ['COST_ALERT_EMAIL'] = 'billing@company.com'
os.environ['COST_ALERT_SLACK_WEBHOOK'] = 'https://...'
```

### Budget Dashboard

Create a simple cost dashboard:

```python
def get_cost_summary():
    """Get current month cost summary"""
    metrics = requests.get('http://localhost:8080/api/metrics?metric_type=cost&timeframe=30d')
    data = metrics.json()
    
    return {
        "total_cost_usd": data['total_cost_usd'],
        "daily_average": data['total_cost_usd'] / 30,
        "projected_monthly": (data['total_cost_usd'] / 30) * 30,
        "by_agent": data['by_agent']
    }
```

---

## Questions?

- 📧 billing@tokyo-ia.example.com
- 💬 [GitHub Discussions - Costs](https://github.com/Melampe001/Tokyo-IA/discussions/categories/costs)
- 📊 [Cost Optimization Guide](../guides/user-guide.md#cost-optimization)

---

*Last updated: 2025-12-23*
