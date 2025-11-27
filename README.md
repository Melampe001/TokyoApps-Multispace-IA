# Tokyo-IA

![CI](https://github.com/Melampe001/Tokyo-IA/workflows/CI/badge.svg)

Tokyo-IA is a mobile + web + server project that provides Tokyo-themed AI features and a MCP server.

## Table of Contents
- [Repository Layout](#repository-layout)
- [Quick Start](#quick-start)
- [Development](#development)
- [Pre-commit Hooks](#pre-commit-hooks)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

## Repository Layout
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
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md              # Bug report template
│   │   └── feature_request.md         # Feature request template
│   ├── workflows/
│   │   └── ci.yml                     # CI workflow (lint, build, test)
│   ├── dependabot.yml                 # Automated dependency updates
│   └── PULL_REQUEST_TEMPLATE.md       # PR template
│
├── scripts/
│   ├── bump-version.sh                    # Increment version
│   └── generate-release.sh                # Build + tag + push
│
├── docs/
│   ├── README.md                          # Documentation index
│   ├── CONTRIBUTING.md                    # Contributing guidelines
│   └── BRANCH_PROTECTION.md               # Branch protection rules
│
├── .gitignore
├── README.md
├── CHANGELOG.md
└── LICENSE

## Quick Start

### Android (local debug)
```bash
./gradlew assembleDebug
./gradlew installDebug
```

### Web (development)
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

## Development

### Available Commands

| Component | Command | Description |
|-----------|---------|-------------|
| Web | `npm run dev` | Start development server |
| Web | `npm run build` | Build for production |
| Web | `npm run lint` | Run linter |
| Web | `npm test` | Run tests |
| Server | `npm start` | Start MCP server |
| Server | `npm test` | Run tests |
| Android | `./gradlew assembleDebug` | Build debug APK |
| Android | `./gradlew test` | Run unit tests |

## Pre-commit Hooks

We recommend setting up pre-commit hooks to ensure code quality before commits.

### Installation

Run the following command in the repository root to install the pre-commit hook:

```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh

echo "Running pre-commit checks..."

# Run linting for web
if [ -d "web" ]; then
    echo "Linting web..."
    cd web && npm run lint 2>/dev/null || true
    cd ..
fi

# Run linting for server-mcp
if [ -d "server-mcp" ]; then
    echo "Linting server-mcp..."
    cd server-mcp && npm run lint 2>/dev/null || true
    cd ..
fi

echo "Pre-commit checks completed."
EOF

chmod +x .git/hooks/pre-commit
```

### Verify Installation

```bash
# Test the hook without actually committing
git commit --dry-run
```

## Security

> ⚠️ **IMPORTANT**: Do NOT store secrets in the repository!

Do NOT store service account JSONs, keystore files, private keys, or other secrets in the repository. If you need to provide credentials for CI:
- Create the credential (e.g., Google Play service account JSON) locally.
- Encode keystore files or JSON as base64 (or keep them as files) and store them in GitHub Actions Secrets.
- Reference secrets in workflows using: `${{ secrets.GOOGLE_PLAY_JSON }}`, `${{ secrets.ANDROID_KEYSTORE_BASE64 }}`, etc.

If any secret was ever committed:
1. Rotate the exposed credential immediately (revoke old key).
2. Remove the secret from the repository and history (see docs/SECRETS.md).
3. Notify collaborators and ask them to reclone if history was rewritten.

### Release Notes
- `whatsnew/en-US/whatsnew.txt`
- `whatsnew/es-MX/whatsnew.txt`

## Contributing

We welcome contributions! Please read our guidelines before submitting changes.

### Quick Guide

1. **Fork** the repository
2. **Create a branch** from `develop`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and commit using [Conventional Commits](https://www.conventionalcommits.org/)
4. **Push** to your fork and **create a Pull Request**

### Branch Rules

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code (protected) |
| `develop` | Integration branch for features (protected) |
| `feature/*` | New features |
| `bugfix/*` | Bug fixes |
| `hotfix/*` | Urgent production fixes |

### PR Requirements
- Target the `develop` branch (unless it's a hotfix)
- Pass all CI checks
- Include tests for new functionality
- At least one approving review

For detailed guidelines, see:
- [Contributing Guide](docs/CONTRIBUTING.md)
- [Branch Protection](docs/BRANCH_PROTECTION.md)

## License

See [LICENSE](LICENSE)