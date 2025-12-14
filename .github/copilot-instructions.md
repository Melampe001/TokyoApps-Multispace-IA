# Copilot Instructions for Tokyo-IA

## Project Overview

Tokyo-IA is a Tokyo-themed AI project that provides AI features and integrations. The project is currently in documentation and planning phase, with specifications for:

1. **Flutter Mobile App** - Cross-platform mobile application (planned)
2. **AI Agents** - Autonomous agents for code generation, media creation, and more
3. **MCP Integration** - Model Context Protocol server functionality

## Current Repository Structure

```
tokyoia/
├── .github/
│   ├── copilot-instructions.md  # Copilot configuration (this file)
│   └── agents/                   # Custom agent definitions
├── prompts/                      # AI prompts and templates
│   ├── JS-Supremo.md             # JavaScript expert prompt
│   └── GitHub-Pro.md             # GitHub workflow guide
├── README.md                     # Project overview
├── TAREAS.md                     # Task list and roadmap
├── Setup                         # Initial setup checklist
├── Agentes y bots                # Agent development checklist
├── Fllutter                      # Flutter dependencies spec (note: filename typo exists)
├── Cuerpo                        # GenAI code examples
├── Imitar                        # Sentiment analysis code
├── Sin limite                    # Unrestricted mode code
├── Sincero                       # Sincere response code
└── Real                          # Reality mode code
```

## Planned Structure (When Implemented)

```
tokyoia/
├── app/                    # Flutter mobile app
├── web/                    # Web site + admin panel
├── server-mcp/             # Node server for MCP
├── agents/                 # Autonomous AI agents
├── whatsnew/               # Play Store release notes
├── scripts/                # Build and release scripts
└── .github/workflows/      # CI/CD workflows
```

## Build and Test Commands

### Flutter (When Implemented)
```bash
flutter create tokyo_ia_personal --platforms=android,ios --org=com.tokyoia
flutter pub get             # Install dependencies
flutter run                 # Run the app
flutter test                # Run unit tests
flutter build apk           # Build APK
```

### Web (When Implemented)
```bash
cd web
npm install                 # Install dependencies
npm run dev                 # Start development server
npm run build               # Build for production
npm test                    # Run tests
```

### MCP Server (When Implemented)
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
- Follow the C.R.A.F.T. prompt structure for AI interactions (see prompts/JS-Supremo.md)

### Flutter/Dart
- Follow Dart coding conventions and effective Dart guidelines
- Use descriptive names for classes, functions, and variables
- Prefer immutable data structures where possible
- Use async/await for asynchronous operations
- Organize code with proper separation of concerns (UI, business logic, data)

### Android/Kotlin
- Follow Kotlin coding conventions
- Use descriptive names for classes, functions, and variables
- Prefer data classes for simple data holders
- Use coroutines for asynchronous operations

### Web (JavaScript/React)
- Use functional components with hooks
- Follow React best practices for component structure
- Use consistent naming conventions (camelCase for variables, PascalCase for components)
- Follow JS-Supremo guidelines for production-ready code (see prompts/JS-Supremo.md)

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
- Test Flutter changes on emulator or device when possible
- Test Android changes on emulator or device when possible
- Test web changes in multiple browsers if making UI changes
- Follow the testing standards outlined in the project prompts

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
