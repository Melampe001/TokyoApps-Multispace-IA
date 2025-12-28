# Tokyo-IA Agent Orchestration System

Complete AI agent orchestration system using CrewAI to coordinate 5 specialized agents for repository management, code review, testing, infrastructure, and documentation.

## 🎭 The Five Agents

| Agent | ID | Role | Model | Specialties | Cost |
|-------|-----|------|-------|-------------|------|
| 侍 **Akira** | akira-001 | Code Review Master | Claude 3.5 Sonnet | Security, Performance, Architecture | Paid |
| ❄️ **Yuki** | yuki-002 | Test Engineering | GPT-4o mini | Unit/Integration/E2E Testing | Paid |
| 🛡️ **Hiro** | hiro-003 | SRE & DevOps | Llama 3.3 70B (Groq) | Kubernetes, CI/CD, Monitoring | **FREE** |
| 🌸 **Sakura** | sakura-004 | Documentation | Gemini 1.5 Flash (Google) | Technical Writing, Diagrams | **FREE** |
| 🏗️ **Kenji** | kenji-005 | Architecture | GPT-4o | System Design, Patterns | Paid |

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- At least one API key (preferably start with FREE tier)

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API keys (start with FREE tier)
export GROQ_API_KEY=gsk_...      # FREE - Hiro (SRE/DevOps)
export GOOGLE_API_KEY=...        # FREE - Sakura (Documentation)

# Optional: Add premium agents
export ANTHROPIC_API_KEY=sk-ant-...  # Akira (Code Review)
export OPENAI_API_KEY=sk-...         # Yuki & Kenji (Testing & Architecture)
```

### Test Your Setup

```bash
# Test FREE tier APIs only (recommended first)
python agents/test_free_apis.py

# Test all APIs
python agents/test_all_apis.py
```

## 📋 Usage

### Command Line Interface

```bash
# Show available agents
python agents/tokyo_crew.py list-agents

# Analyze a Pull Request
python agents/tokyo_crew.py analyze-pr 126

# Execute repository cleanup
python agents/tokyo_crew.py cleanup

# Generate documentation
python agents/tokyo_crew.py generate-docs
```

### Automated Execution

```bash
# Run all workflows sequentially
./agents/run_agents.sh

# Run workflows in parallel (advanced)
./agents/parallel_execution.sh

# Monitor progress in real-time
python agents/agent_dashboard.py
```

## 🔧 Workflows

### 1. PR Analysis Workflow

Comprehensive analysis of Pull Requests by all relevant agents.

**Agents involved:** Akira → Yuki → Hiro → Sakura → Kenji

**What it does:**
- 侍 **Akira**: Security audit, performance review, code quality
- ❄️ **Yuki**: Test coverage analysis and recommendations
- 🛡️ **Hiro**: Infrastructure impact assessment
- 🌸 **Sakura**: Documentation completeness review
- 🏗️ **Kenji**: Architectural evaluation

**Usage:**
```bash
python agents/tokyo_crew.py analyze-pr <pr_number>
```

**Output:**
- `agent_reports_YYYYMMDD_HHMMSS/pr_<number>_analysis.json`

### 2. Repository Cleanup Workflow

Automated analysis and recommendations for repository maintenance.

**Agents involved:** Hiro → Akira → Sakura → Kenji

**What it does:**
- 🛡️ **Hiro**: Branch analysis (stale/merged branches to delete)
- 侍 **Akira**: PR categorization (ready/review/close)
- 🌸 **Sakura**: Documentation audit and consolidation
- 🏗️ **Kenji**: Q1 2026 roadmap creation

**Usage:**
```bash
python agents/tokyo_crew.py cleanup
```

**Output:**
- `agent_reports_YYYYMMDD_HHMMSS/cleanup_plan.json`

### 3. Documentation Generation Workflow

Comprehensive documentation generation for the entire repository.

**Agent involved:** Sakura

**What it does:**
- 🌸 **Sakura**: Scans repository and generates:
  - Project overview
  - Architecture documentation
  - API documentation
  - Setup guides
  - Developer guidelines

**Usage:**
```bash
python agents/tokyo_crew.py generate-docs
```

**Output:**
- `agent_reports_YYYYMMDD_HHMMSS/consolidated_docs.md`

## 📊 Output Structure

All agent executions create timestamped report directories:

```
agent_reports_YYYYMMDD_HHMMSS/
├── cleanup_plan.json           # Repository cleanup recommendations
├── pr_126_analysis.json        # Individual PR analysis
├── pr_125_analysis.json
├── consolidated_docs.md        # Generated documentation
├── report.html                 # Visual report (if generated)
└── EXECUTIVE_SUMMARY.md        # High-level summary
```

## 💰 Cost Optimization

### FREE Tier (Recommended for Development)

Use only Hiro and Sakura - **$0/month**

```bash
export GROQ_API_KEY=gsk_...     # FREE - No credit card required
export GOOGLE_API_KEY=...       # FREE - No credit card required

python agents/test_free_apis.py
```

**Capabilities:**
- ✅ Infrastructure analysis and recommendations
- ✅ Documentation generation and audits
- ✅ Branch cleanup analysis
- ✅ Repository maintenance workflows
- ✅ ~80% of full functionality

### Hybrid Mode (Recommended for Production)

Add premium agents for advanced features - **~$20-35/month**

```bash
# Keep FREE tier
export GROQ_API_KEY=gsk_...
export GOOGLE_API_KEY=...

# Add premium
export ANTHROPIC_API_KEY=sk-ant-...  # Akira - Security reviews
export OPENAI_API_KEY=sk-...         # Yuki & Kenji - Testing & Architecture
```

**Additional capabilities:**
- ✅ Advanced security audits
- ✅ Test coverage analysis
- ✅ Architectural evaluations
- ✅ 100% of functionality

### Full Premium Mode

All 5 agents - **~$35-50/month**

Best for:
- Production deployments
- Critical security reviews
- Comprehensive code quality analysis
- Full PR review workflows

## 🔑 API Key Setup

### Groq (FREE) - Hiro 🛡️

1. Visit: https://console.groq.com
2. Sign up (no credit card required)
3. Create API key
4. Export: `export GROQ_API_KEY=gsk_...`

### Google AI (FREE) - Sakura 🌸

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create API key
4. Export: `export GOOGLE_API_KEY=...`

### Anthropic (Paid) - Akira 侍

1. Visit: https://console.anthropic.com
2. Add payment method
3. Create API key
4. Export: `export ANTHROPIC_API_KEY=sk-ant-...`

**Cost:** ~$15/month for moderate usage

### OpenAI (Paid) - Yuki ❄️ & Kenji 🏗️

1. Visit: https://platform.openai.com/api-keys
2. Add payment method
3. Create API key
4. Export: `export OPENAI_API_KEY=sk-...`

**Cost:** ~$10-20/month for moderate usage

## 🧪 Testing

### Test API Connectivity

```bash
# Test FREE tier only (Hiro + Sakura)
python agents/test_free_apis.py

# Test all APIs
python agents/test_all_apis.py
```

### Test Individual Workflows

```bash
# Test cleanup workflow
python agents/tokyo_crew.py cleanup

# Test documentation generation
python agents/tokyo_crew.py generate-docs

# Test PR analysis (use existing PR number)
python agents/tokyo_crew.py analyze-pr 1
```

## 🛠️ Development

### Project Structure

```
agents/
├── tokyo_crew.py              # Main orchestration system
├── test_all_apis.py          # Test all 4 LLM providers
├── test_free_apis.py         # Test FREE tier only
├── run_agents.sh             # Sequential execution script
├── parallel_execution.sh     # Parallel execution (advanced)
├── agent_dashboard.py        # Real-time monitoring UI
└── README.md                 # This file
```

### Adding Custom Workflows

Edit `agents/tokyo_crew.py` and add new methods to the `TokyoCrew` class:

```python
def custom_workflow(self) -> Dict[str, Any]:
    """Your custom workflow description."""
    results = {}
    
    # Define tasks for each agent
    if "hiro" in self.agents:
        # Create Hiro task
        pass
    
    # Save results
    output_file = self.output_dir / "custom_workflow.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    return results
```

### Environment Variables

All configuration via environment variables:

```bash
# Required (at least one)
ANTHROPIC_API_KEY     # Akira - Claude 3.5 Sonnet
OPENAI_API_KEY        # Yuki & Kenji - GPT-4o/mini
GROQ_API_KEY          # Hiro - Llama 3.3 70B [FREE]
GOOGLE_API_KEY        # Sakura - Gemini 1.5 Flash [FREE]

# Optional
AGENT_VERBOSE=true              # Enable verbose logging
AGENT_ALLOW_DELEGATION=false    # Disable agent delegation
```

## 📈 Monitoring

### Real-time Dashboard

```bash
python agents/agent_dashboard.py
```

Shows:
- Active agents status
- Current workflow progress
- Task completion status
- Resource usage

### Execution Logs

All executions create detailed logs in the report directories:
- Task descriptions
- Agent responses
- Execution times
- Error messages (if any)

## 🚨 Troubleshooting

### No agents initialized

**Problem:** All agents show "❌ NOT INITIALIZED"

**Solution:**
1. Check API keys are set: `echo $GROQ_API_KEY`
2. Test API connectivity: `python agents/test_free_apis.py`
3. Verify API keys are valid (check provider console)

### API rate limits

**Problem:** Errors about rate limits or quota exceeded

**Solution:**
1. Reduce concurrent executions
2. Add delays between workflows
3. Upgrade API plan (if using free tier)
4. Use FREE tier agents (no rate limits)

### Import errors

**Problem:** `ModuleNotFoundError: No module named 'crewai'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Workflow failures

**Problem:** Workflow fails with timeout or connection error

**Solution:**
1. Check internet connectivity
2. Verify API keys are valid
3. Check LLM provider status pages
4. Retry with `--verbose` flag for details

## 🎯 Best Practices

1. **Start with FREE tier** - Get familiar with the system at $0 cost
2. **Test before production** - Run `test_free_apis.py` first
3. **Monitor costs** - Track API usage in provider dashboards
4. **Use automation scripts** - Leverage `run_agents.sh` for consistency
5. **Review reports regularly** - Check agent_reports_* directories
6. **Keep API keys secure** - Never commit to git, use .env files

## 📚 Additional Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [Tokyo-IA Main README](../README.md)
- [Agent API Reference](../docs/agents/API.md)
- [Workflow Examples](../examples/README.md)

## 🤝 Contributing

To add new agents or workflows:

1. Follow existing agent patterns in `tokyo_crew.py`
2. Add tests in `test_*.py` files
3. Update this README with usage examples
4. Test with FREE tier first
5. Submit PR with clear documentation

## 📄 License

Apache 2.0 - See [LICENSE](../LICENSE) for details

---

**Generated by Tokyo-IA Agent Orchestration System** 🗼
