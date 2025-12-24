# Elite Framework Examples

This document provides real-world examples of using the Elite Framework to generate projects.

## Example 1: Task Management API

### Command
```bash
./bin/elite generate "REST API for task management with authentication"
```

### Generated Project
```
rest-api-for-task-management-with-authentication/
├── cmd/api/main.go           # HTTP server entry point
├── internal/
│   ├── handler/              # HTTP handlers
│   ├── service/              # Business logic
│   └── repository/           # Data access
├── models/                   # Data models
├── tests/                    # Unit & integration tests
├── deploy/                   # Deployment configs
├── docs/                     # Documentation
├── go.mod                    # Go dependencies
├── Dockerfile                # Container image
├── docker-compose.yml        # Local development
└── .github/workflows/ci.yml  # CI/CD pipeline
```

### Key Features
- ✅ RESTful endpoints
- ✅ PostgreSQL database
- ✅ Swagger documentation
- ✅ Docker deployment
- ✅ CI/CD workflow

### Quick Start
```bash
cd rest-api-for-task-management-with-authentication
go mod download
go run cmd/api/main.go
```

## Example 2: Weather Bot

### Command
```bash
./bin/elite generate "Telegram bot that provides weather forecasts and alerts"
```

### Generated Project
```
telegram-bot-that-provides-weather-forecasts-and-alerts/
├── main.py                   # Bot entry point
├── bot/
│   ├── handlers/             # Command handlers
│   └── commands/             # Command definitions
├── services/                 # Weather API integration
├── tests/                    # Unit & integration tests
├── requirements.txt          # Python dependencies
├── .env.example              # Configuration template
├── Dockerfile                # Container image
└── .github/workflows/ci.yml  # CI/CD pipeline
```

### Key Features
- ✅ Telegram integration
- ✅ Async command handling
- ✅ Weather API ready
- ✅ Environment config
- ✅ Docker deployment

### Quick Start
```bash
cd telegram-bot-that-provides-weather-forecasts-and-alerts
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your BOT_TOKEN
python main.py
```

## Example 3: Note-Taking PWA

### Command
```bash
./bin/elite generate "Progressive web app for note taking with offline support"
```

### Generated Project
```
progressive-web-app-for-note-taking-with-offline-support/
├── src/
│   ├── components/           # React components
│   ├── pages/                # Page views
│   ├── App.jsx               # Main app
│   └── main.jsx              # Entry point
├── public/                   # Static assets
├── tests/                    # Unit & E2E tests
├── package.json              # Node dependencies
├── vite.config.js            # Vite config
├── index.html                # HTML entry
├── Dockerfile                # Container image
└── .github/workflows/ci.yml  # CI/CD pipeline
```

### Key Features
- ✅ React 18+
- ✅ Vite for fast builds
- ✅ Service Worker ready
- ✅ Responsive design
- ✅ Vercel-ready deployment

### Quick Start
```bash
cd progressive-web-app-for-note-taking-with-offline-support
npm install
npm run dev
# Open http://localhost:5173
```

## Example 4: Digital Products Store

### Command
```bash
./bin/elite generate "E-commerce platform for selling digital downloads with Stripe"
```

### Generated Project
```
ecommerce-platform-for-selling-digital-downloads-with-stripe/
├── app/
│   ├── (auth)/               # Auth pages
│   ├── (shop)/               # Shop pages
│   ├── admin/                # Admin panel
│   └── page.tsx              # Home page
├── components/ui/            # UI components
├── lib/                      # Utilities
├── prisma/                   # Database schema
├── package.json              # Node dependencies
├── .env.example              # Configuration
├── Dockerfile                # Container image
└── .github/workflows/ci.yml  # CI/CD pipeline
```

### Key Features
- ✅ Next.js 14 App Router
- ✅ Stripe integration ready
- ✅ Prisma ORM
- ✅ PostgreSQL database
- ✅ Admin panel structure
- ✅ TypeScript support

### Quick Start
```bash
cd ecommerce-platform-for-selling-digital-downloads-with-stripe
npm install
cp .env.example .env
# Edit .env with DATABASE_URL and STRIPE keys
npx prisma migrate dev
npm run dev
# Open http://localhost:3000
```

## Example 5: Research AI Agent

### Command
```bash
./bin/elite generate "AI agent with CrewAI that helps with academic research"
```

### Generated Project
```
ai-agent-with-crewai-that-helps-with-academic-research/
├── main.py                   # Agent entry point
├── agents/                   # Agent definitions
├── tools/                    # Custom tools
├── tasks/                    # Task definitions
├── config/                   # Configuration
├── tests/                    # Unit & integration tests
├── requirements.txt          # Python dependencies
├── .env.example              # API keys template
├── Dockerfile                # Container image
└── .github/workflows/ci.yml  # CI/CD pipeline
```

### Key Features
- ✅ CrewAI integration
- ✅ Groq for fast inference
- ✅ LangChain support
- ✅ Custom tools ready
- ✅ Task orchestration

### Quick Start
```bash
cd ai-agent-with-crewai-that-helps-with-academic-research
pip install -r requirements.txt
cp .env.example .env
# Edit .env with GROQ_API_KEY and OPENAI_API_KEY
python main.py
```

## Tips for Best Results

### Be Specific
❌ Bad: "web app"
✅ Good: "Progressive web app for task tracking with offline support"

### Include Key Features
❌ Bad: "bot"
✅ Good: "Telegram bot for weather updates with location-based alerts"

### Mention Technology When Needed
❌ Bad: "online store"
✅ Good: "E-commerce platform with Stripe payments and inventory management"

### Use the Magic Format
Both formats work equally well:
```bash
./bin/elite generate "REST API for tasks"
./bin/elite generate "// PROYECTO: REST API for tasks"
```

## Common Patterns

### Microservice Architecture
```bash
./bin/elite generate "User authentication microservice with JWT"
./bin/elite generate "Product catalog microservice with search"
./bin/elite generate "Order processing microservice with queue"
```

### Full Stack Application
```bash
# Backend
./bin/elite generate "GraphQL API for social media platform"

# Frontend
./bin/elite generate "PWA for social media with real-time updates"
```

### Automation Suite
```bash
./bin/elite generate "Telegram bot for deployment notifications"
./bin/elite generate "Slack bot for monitoring alerts"
./bin/elite generate "Discord bot for team coordination"
```

### AI/ML Projects
```bash
./bin/elite generate "AI agent for customer support with CrewAI"
./bin/elite generate "AI agent for content generation with Groq"
```

## Troubleshooting

### Project Type Not Detected Correctly?
Add more specific keywords to your description:
- For APIs: Include "REST", "API", "GraphQL", "endpoint"
- For Bots: Include "Telegram", "Discord", "Slack", "bot"
- For PWAs: Include "PWA", "progressive web app", "offline"
- For E-commerce: Include "e-commerce", "shop", "store", "payment"
- For AI: Include "AI agent", "CrewAI", "intelligent", "autonomous"

### Missing Files?
All generated projects include:
- Complete source structure
- Tests directories (unit + integration)
- Dockerfile
- docker-compose.yml (where applicable)
- GitHub Actions workflow
- README.md
- Documentation (ARCHITECTURE.md, API.md)
- CONTRIBUTING.md
- LICENSE

If files are missing, please check the output directory carefully or report an issue.

## Next Steps

After generating a project:

1. **Review the README.md** - Contains setup instructions
2. **Check the docs/** - Architecture and API documentation
3. **Install dependencies** - Follow language-specific instructions
4. **Run tests** - Ensure everything works
5. **Customize** - Adapt the generated code to your needs
6. **Deploy** - Use provided Docker and CI/CD configs

## Need Help?

- Read the [Elite Framework Documentation](elite-framework.md)
- Check the [Main README](../README.md)
- Open an issue on GitHub
