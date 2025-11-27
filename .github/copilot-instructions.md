# Copilot Instructions for Tokyo-IA

## Project Overview

Tokyo-IA is a mobile + web + server project that provides Tokyo-themed AI features and an MCP (Model Context Protocol) server. The project consists of three main components:

1. **Android App** (`app/`) - Kotlin-based Android application
2. **Web** (`web/`) - React/Vite web application with admin panel
3. **MCP Server** (`server-mcp/`) - Node.js server for MCP functionality

## Repository Structure

```
tokyoia/
├── app/                    # Android – main project (Kotlin)
├── web/                    # Web site + admin panel (React/Vite)
├── server-mcp/             # Node server for MCP (Node.js)
├── whatsnew/               # Play Store release notes
├── scripts/                # Build and release scripts
└── .github/workflows/      # CI/CD workflows
```

## Build and Test Commands

### Android
```bash
./gradlew assembleDebug     # Build debug APK
./gradlew installDebug      # Install debug APK
./gradlew test              # Run unit tests
```

### Web
```bash
cd web
npm install                 # Install dependencies
npm run dev                 # Start development server
npm run build               # Build for production
npm test                    # Run tests
```

### MCP Server
```bash
cd server-mcp
npm install                 # Install dependencies
npm start                   # Start server
npm test                    # Run tests
```

## Coding Standards

### General
- Write clear, self-documenting code with meaningful variable and function names
- Keep functions small and focused on a single responsibility
- Add comments only when the code logic is complex or non-obvious

### Android/Kotlin
- Follow Kotlin coding conventions
- Use descriptive names for classes, functions, and variables
- Prefer data classes for simple data holders
- Use coroutines for asynchronous operations

### Web (JavaScript/React)
- Use functional components with hooks
- Follow React best practices for component structure
- Use consistent naming conventions (camelCase for variables, PascalCase for components)

### Node.js/Server
- Use async/await for asynchronous operations
- Handle errors appropriately with try/catch blocks
- Follow modular architecture patterns

## Security Guidelines

**CRITICAL: Never commit secrets to the repository.**

- Do NOT store service account JSONs, keystore files, private keys, or other secrets in the repository
- Use GitHub Actions Secrets for CI/CD credentials:
  - `${{ secrets.GOOGLE_PLAY_JSON }}`
  - `${{ secrets.ANDROID_KEYSTORE_BASE64 }}`
- If any secret was ever committed:
  1. Rotate the exposed credential immediately
  2. Remove the secret from the repository and history
  3. Notify collaborators

## Testing Requirements

- Write unit tests for new functionality
- Ensure existing tests pass before submitting changes
- Test Android changes on emulator or device when possible
- Test web changes in multiple browsers if making UI changes

## Task Guidelines

### Ideal Tasks for Copilot
- Bug fixes with clear reproduction steps
- Adding new features with well-defined requirements
- Writing or updating tests
- Documentation improvements
- Code refactoring with clear objectives
- UI updates and styling changes

### Tasks Requiring Human Review
- Security-sensitive changes (authentication, encryption)
- Changes to CI/CD workflows
- Database schema changes
- API contract changes
- Changes affecting production deployments

## Pull Request Guidelines

- Keep PRs focused on a single issue or feature
- Write clear PR descriptions explaining the changes
- Include test coverage for new code
- Ensure all CI checks pass before requesting review
- Reference related issues in the PR description
