# AI Agent Template

This template generates an AI agent using CrewAI and Groq.

## Features

- Python 3.9+
- CrewAI for agent orchestration
- Groq for fast LLM inference
- LangChain integration
- Custom tools support
- Task planning and execution

## Structure

```
ai-agent-project/
├── agents/           # Agent definitions
├── tools/            # Custom tools
├── tasks/            # Task definitions
├── config/           # Configuration files
├── utils/            # Utility functions
├── tests/
│   ├── unit/         # Unit tests
│   └── integration/  # Integration tests
└── deploy/           # Deployment configs
```

## Generated Files

- `main.py` - Agent entry point
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables (API keys)
- `Dockerfile` - Container definition
- `.github/workflows/ci.yml` - CI/CD pipeline

## Next Steps

1. Copy `.env.example` to `.env` and add API keys
   - GROQ_API_KEY
   - OPENAI_API_KEY (optional)
2. Install dependencies: `pip install -r requirements.txt`
3. Run the agent: `python main.py`
4. Run tests: `pytest`

## Required API Keys

- **Groq**: Get your key from https://console.groq.com
- **OpenAI**: Get your key from https://platform.openai.com (optional)
