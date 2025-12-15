# Tokyo-IA

[![CI Pipeline](https://github.com/Melampe001/Tokyo-IA/actions/workflows/ci.yml/badge.svg)](https://github.com/Melampe001/Tokyo-IA/actions/workflows/ci.yml)

Tokyo-IA is a mobile + web + server project that provides Tokyo-themed AI features and a MCP server.

## 📋 Table of Contents

- [Repository Structure](#repository-structure)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

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

---

## 🚀 Elite Framework - Generación Automática de Proyectos

Tokyo-IA incluye un **Elite Framework** que permite generar **CUALQUIER tipo de proyecto** de forma 100% automatizada.

### ✨ Uso Rápido

**Opción 1: Desde VS Code con Copilot**
```javascript
// PROYECTO: Bot de Discord con moderación AI y música
// Tab x10 → Proyecto completo generado
```

**Opción 2: Desde CLI**
```bash
./scripts/generate-project.sh "API REST con autenticación JWT y PostgreSQL"
cd projects/api-rest-con-autenticacion-jwt-y-postgresql
make build && make test
```

**Opción 3: Interactivo**
```bash
make scaffold
# Sigue las instrucciones para configurar tu proyecto
```

### 🎯 Proyectos Soportados

- ✅ **PWAs** - Progressive Web Apps con React/Vue/Svelte
- ✅ **Bots** - Discord, Telegram, WhatsApp con AI
- ✅ **APIs REST/GraphQL** - Go, Node.js, Python
- ✅ **E-commerce** - Tiendas completas con pagos
- ✅ **AI Agents** - LangChain, CrewAI, RAG
- ✅ **Microservicios** - gRPC, Service Mesh

### 🔧 Features del Framework

- 🎯 Detección automática de stack tecnológico
- 🧪 Tests automáticos con 100% coverage
- 📚 Documentación completa auto-generada
- 🔐 Seguridad by default
- 🚀 CI/CD automático (GitHub Actions)
- 🐳 Docker y Kubernetes ready
- 📦 Templates reutilizables

### 📖 Documentación Completa

Ver la [Documentación completa del Elite Framework](.github/copilot-instructions.md#-elite-framework---automatic-project-generation) para:
- Agentes especializados (ProjectScaffold, CodeMaster, TestGenius, etc.)
- Patrones y best practices por lenguaje
- Ejemplos de uso detallados
- Guías de deployment

---

## 📚 Documentation

- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[CI/CD Documentation](docs/CI_CD.md)** - Continuous Integration and Deployment
- **[Branch Protection](docs/BRANCH_PROTECTION.md)** - Git workflow and branch rules
- **[Security Policy](SECURITY.md)** - Security best practices

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