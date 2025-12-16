# Bot Template

This template generates a chat bot compatible with Telegram, Discord, or Slack.

## Features

- Python 3.9+
- Async/await support
- Command routing
- Service layer architecture
- Environment configuration
- Comprehensive testing

## Structure

```
bot-project/
├── bot/
│   ├── handlers/     # Command handlers
│   └── commands/     # Command definitions
├── services/         # Business logic
├── utils/            # Utility functions
├── tests/
│   ├── unit/         # Unit tests
│   └── integration/  # Integration tests
└── deploy/           # Deployment configs
```

## Generated Files

- `main.py` - Bot entry point
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `Dockerfile` - Container definition
- `.github/workflows/ci.yml` - CI/CD pipeline

## Next Steps

1. Copy `.env.example` to `.env` and configure
2. Install dependencies: `pip install -r requirements.txt`
3. Run the bot: `python main.py`
4. Run tests: `pytest`
