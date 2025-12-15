# Tokyo-IA

[![CI Pipeline](https://github.com/Melampe001/Tokyo-IA/actions/workflows/ci.yml/badge.svg)](https://github.com/Melampe001/Tokyo-IA/actions/workflows/ci.yml)

Tokyo-IA is a comprehensive AI-powered platform providing cost optimization, advanced security scanning, and Tokyo-themed features.

## ✨ Key Features

### 🤖 AI Intelligence (Production Ready)
- **Cost Predictor** - ML-based cost prediction with 85% confidence intervals
- Supports GPT-4, Claude, Gemini, LLaMA, and more
- Automatic optimization recommendations
- Historical data analysis (100K+ training samples)

### 🔒 Advanced Security (Production Ready)
- **Security Scanner** - OWASP Top 10 detection
- CVE database with known vulnerabilities (Log4Shell, Spring4Shell, etc.)
- Multi-standard compliance checking (SOC2, GDPR, HIPAA, PCI-DSS, ISO27001)
- Auto-fix suggestions for vulnerabilities

### 🎮 Coming Soon
- Tokyo Neon Theme (Cyberpunk UI)
- Gamification system with achievements
- Voice commands ("Hey Tokyo")
- Real-time collaboration hub
- IDE extensions (VS Code, IntelliJ)

## 📋 Table of Contents

- [Key Features](#-key-features)
- [Quick Start](#-quick-start)
- [Features Documentation](#-features-documentation)
- [API Documentation](#-api-documentation)
- [Repository Structure](#-repository-structure)
- [Elite Framework](#-elite-framework---generate-projects-instantly)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [Security](#-security)
- [License](#-license)

## 🚀 Quick Start

### Prerequisites
```bash
# Go 1.21+
go version

# Python 3.8+
python3 --version
```

### Installation
```bash
# Clone repository
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA

# Install Go dependencies
go mod download

# Install Python dependencies
pip install -r requirements.txt

# Build
make build

# Run tests
make test
```

### Usage

**Cost Prediction:**
```go
import "github.com/Melampe001/Tokyo-IA/internal/ai"

predictor := ai.NewCostPredictor()
metrics := ai.RequestMetrics{
    Tokens:      5000,
    ModelName:   "gpt-4",
    RequestType: "completion",
    Complexity:  0.7,
}

prediction, _ := predictor.PredictCost(metrics)
fmt.Printf("Estimated Cost: $%.4f\n", prediction.EstimatedCost)
// Output: Estimated Cost: $7.5150
```

**Security Scanning:**
```go
import "github.com/Melampe001/Tokyo-IA/internal/security"

scanner := security.NewAdvancedScanner()
result, _ := scanner.ScanCode(code, "myfile.go")
fmt.Printf("Status: %s (Score: %d/100)\n", result.Status, result.ComplianceScore)
// Output: Status: PASS (Score: 100/100)
```

## 📚 Features Documentation

See **[docs/FEATURES.md](docs/FEATURES.md)** for complete feature documentation including:
- Cost Predictor usage and configuration
- Security Scanner capabilities
- Compliance standards supported
- Configuration options

## 🔌 API Documentation

See **[docs/API.md](docs/API.md)** for REST API documentation including:
- Cost prediction endpoints
- Security scanning endpoints
- Request/response examples
- Authentication and rate limiting

## 📊 Implementation Status

See **[docs/IMPLEMENTATION_STATUS.md](docs/IMPLEMENTATION_STATUS.md)** for detailed implementation status:
- ✅ Completed features (P0)
- 🚧 Planned features (P1-P3)
- Test coverage and code quality metrics
- Database schema and configuration

## 🏗️ Repository Structure
tokyoia/
│
├── app/                                   # Android – main project
│   ├── build.gradle                       # Config signed + release
│   ├── proguard-rules.pro
│   ├── src/
│   │   ├── main/
│   │   │   ├── AndroidManifest.xml
│   │   │   ├── java/com/tokyoia/app/
│   │   │   │   └── TokyoApp.kt
│   │   │   └── res/
│   │   │       ├── layout/activity_main.xml
│   │   │       ├── mipmap-*/              # App icons
│   │   │       └── values/strings.xml
│   │   └── test/
│   │       └── ExampleUnitTest.kt
│   └── gradle.properties
│
├── web/                                   # Web site + admin panel
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── components/
│       └── styles/
│
├── server-mcp/                            # Node server for MCP
│   ├── index.js
│   ├── package.json
│   ├── tokyo-rules.json
│   └── src/
│       ├── actions/
│       └── context/
│
├── whatsnew/                              # Play Store release notes
│   ├── en-US/whatsnew.txt
│   └── es-MX/whatsnew.txt
│
├── .github/
│   ├── workflows/
│   │   └── ci.yml                       # CI pipeline for all components
│   ├── ISSUE_TEMPLATE/                  # Issue templates
│   ├── dependabot.yml                   # Automated dependency updates
│   └── pull_request_template.md         # PR template
│
├── docs/
│   ├── README.md                        # Documentation index
│   ├── CI_CD.md                         # CI/CD documentation
│   └── BRANCH_PROTECTION.md             # Branch protection guide
│
├── scripts/
│   ├── bump-version.sh                    # Increment version
│   └── generate-release.sh                # Build + tag + push
│
├── .gitignore
├── README.md
├── CONTRIBUTING.md                        # Contribution guidelines
├── SECURITY.md                            # Security policy
└── LICENSE

## 🚀 Quick Start

### Android (local debug)
```bash
./gradlew assembleDebug
./gradlew installDebug
```

### Web (dev)
```bash
cd web
npm install
npm run dev
```

### Server (local)
```bash
cd server-mcp
npm install
npm start
```

## 📚 Documentation

- **[Elite Framework](docs/elite-framework.md)** - Automated project generation system
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[CI/CD Documentation](docs/CI_CD.md)** - Continuous Integration and Deployment
- **[Branch Protection](docs/BRANCH_PROTECTION.md)** - Git workflow and branch rules
- **[Security Policy](SECURITY.md)** - Security best practices

## 🎯 Elite Framework - Generate Projects Instantly

Tokyo-IA includes the **Elite Framework**, an automated project generator that creates complete, production-ready projects from simple descriptions.

### Quick Start

```bash
# Build the elite CLI
make elite

# Generate a project
./bin/elite generate "REST API for task management"

# Or use make command
make generate IDEA="Telegram bot for weather updates"
```

### Supported Project Types

- **PWAs** - Progressive Web Apps with React/Vite
- **Bots** - Telegram, Discord, Slack bots
- **APIs** - REST/GraphQL APIs with Go
- **E-commerce** - Online stores with Stripe
- **AI Agents** - CrewAI/Groq powered agents

Each generated project includes:
- ✅ Complete source code
- ✅ Tests (unit + integration)
- ✅ Docker deployment
- ✅ CI/CD workflows
- ✅ Full documentation

See the [Elite Framework Documentation](docs/elite-framework.md) for details.

## 🔒 Security / Secrets (IMPORTANT)

**Do NOT store service account JSONs, keystore files, private keys, or other secrets in the repository.**

If you need to provide credentials for CI:
- Create the credential (e.g., Google Play service account JSON) locally
- Encode keystore files or JSON as base64 and store them in GitHub Actions Secrets
- Reference secrets in workflows using: `${{ secrets.GOOGLE_PLAY_JSON }}`, `${{ secrets.ANDROID_KEYSTORE_BASE64 }}`, etc.

If any secret was ever committed:
1. Rotate the exposed credential immediately (revoke old key)
2. Remove the secret from the repository and history
3. Notify collaborators and ask them to reclone if history was rewritten

For more details, see the [Security Policy](SECURITY.md).

## 📝 Release Notes

Release notes for Play Store:
- `whatsnew/en-US/whatsnew.txt`
- `whatsnew/es-MX/whatsnew.txt`

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:
- Development setup
- Code standards
- Pull request process
- Branch protection rules

## 📄 License

See [LICENSE](LICENSE) file for details.