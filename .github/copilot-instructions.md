# Tokyo-IA Copilot Instructions

## Project Overview

Tokyo-IA is a mobile + web + server project that provides Tokyo-themed AI features and an MCP server. The project includes:

- **Android app** (`app/`) - Kotlin-based Android application
- **Web interface** (`web/`) - React/Vite web application with admin panel
- **MCP Server** (`server-mcp/`) - Node.js server for MCP functionality
- **Flutter app** (planned) - Cross-platform mobile application

## Commands

### Android
```bash
# Build debug APK
./gradlew assembleDebug

# Install debug APK to connected device
./gradlew installDebug

# Run unit tests
./gradlew test
```

### Web
```bash
cd web
npm install
npm run dev      # Development server
npm run build    # Production build
npm run lint     # Lint code
npm test         # Run tests
```

### MCP Server
```bash
cd server-mcp
npm install
npm start        # Start server
npm test         # Run tests
npm run lint     # Lint code
```

### Flutter (when implemented)
```bash
flutter run
flutter test
flutter analyze
```

## Code Style

### General
- Use clear, descriptive variable and function names
- Keep functions small and focused on a single responsibility
- Add comments only when necessary to explain complex logic
- Follow existing patterns in the codebase

### Kotlin (Android)
- Follow Kotlin coding conventions
- Use data classes for simple data holders
- Prefer immutable `val` over mutable `var`

### JavaScript/TypeScript (Web & Server)
- Use ES6+ features
- Prefer `const` over `let`, avoid `var`
- Use async/await for asynchronous code
- Follow ESLint rules configured in the project

### Dart/Flutter (when implemented)
- Follow Dart style guide
- Use `final` and `const` where possible
- Organize imports alphabetically

## Security Guidelines

**CRITICAL: Never commit secrets to the repository**

- Do NOT store service account JSONs, keystore files, private keys, or API keys in the repository
- Store sensitive credentials in GitHub Actions Secrets
- Reference secrets in workflows using: `${{ secrets.SECRET_NAME }}`
- Use `.env` files for local development only (must be in `.gitignore`)
- If any secret is accidentally committed:
  1. Rotate the exposed credential immediately
  2. Remove from repository and history
  3. Notify collaborators

## Boundaries - Files NOT to Modify

Unless explicitly requested, do not modify:

- `*.keystore` files
- `*.jks` files
- `.env*` files (environment configuration)
- `google-services.json`
- `GoogleService-Info.plist`
- Service account JSON files
- Any file containing API keys or credentials
- Vendor/third-party code in `node_modules/`, `build/`, `.gradle/`

## Workflow

### Branching
- `main` - Production-ready code
- `develop` - Development integration branch
- Feature branches: `feature/description`
- Bug fix branches: `fix/description`

### Pull Requests
- Keep PRs focused and small
- Provide clear description of changes
- Ensure all tests pass before merging
- Request review for significant changes

## Project-Specific Context

This project uses AI-related dependencies including:
- Firebase for authentication, storage, and vector database
- Hugging Face models for local AI inference
- Gemini and OpenAI APIs for cloud AI features
- Edge AI for on-device processing

Languages used:
- Spanish and English (documentation and comments)
- English (code, variable names, function names)
