# Copilot Instructions for Tokyo-IA

This repository contains Tokyo-IA, a mobile + web + server project providing Tokyo-themed AI features and a MCP server. The project is currently in the planning and documentation phase.

## Project Overview

Tokyo-IA is planned to consist of three main components:
- **Flutter Mobile App** - Mobile application with AI features (Android and iOS)
- **Web Frontend** - React/Vite web application with admin panel
- **MCP Server** - Node.js server for MCP functionality

## Current Repository Structure

The repository currently contains planning documents and specifications:

```
Tokyo-IA/
├── README.md             # Project overview and planned structure
├── TAREAS.md             # Task list and implementation guide
├── Setup                 # Initial setup checklist
├── Agentes y bots        # Development checklist for agents
├── Fllutter              # Flutter dependencies specification
├── Cuerpo                # GenAI code examples
├── Imitar                # Sentiment detector code
├── Sin limite            # Unrestricted mode code
├── Real                  # Additional specifications
├── Sincero               # Sincerity module specifications
└── .github/              # GitHub configuration
    └── agents/           # Custom agent definitions
```

## Planned Build Commands

Once implemented, these commands will be used:

### Flutter App
```bash
# Create project
flutter create tokyo_ia_personal --platforms=android,ios --org=com.tokyoia

# Run in development
flutter run

# Build release
flutter build apk --release
```

### Web Application
```bash
cd web
npm install
npm run dev        # Development server
npm run build      # Production build
```

### MCP Server
```bash
cd server-mcp
npm install
npm start          # Start server
```

## Code Style Guidelines

### Dart/Flutter (Mobile App)
- Follow Dart style guide and effective Dart practices
- Use meaningful variable and function names
- Document public APIs with dartdoc comments
- Keep functions focused and single-purpose
- Use proper state management patterns

### JavaScript/TypeScript (Web & Server)
- Use ES6+ features
- Prefer `const` over `let`, avoid `var`
- Use async/await for asynchronous operations
- Follow JSDoc comment style for documentation

### General
- Keep commits atomic and well-described
- Write clear, concise commit messages
- Add tests for new functionality
- Update documentation when changing APIs

## Security Guidelines

**IMPORTANT: Never commit secrets to the repository**

- Do NOT store service account JSONs, keystore files, or private keys in the repository
- Store credentials in GitHub Actions Secrets
- Reference secrets in workflows using `${{ secrets.SECRET_NAME }}`
- If secrets are accidentally committed:
  1. Rotate the exposed credential immediately
  2. Remove from repository and history
  3. Notify collaborators

## Testing

- Write unit tests for all new functionality
- Aim for high test coverage
- Run tests locally before pushing changes
- Integration tests should cover end-to-end flows

## Contributing

1. Create a feature branch from the default branch
2. Make your changes with clear commit messages
3. Ensure all tests pass
4. Submit a pull request for review

## Release Notes

Release notes for the mobile app on Play Store are maintained in:
- `whatsnew/en-US/whatsnew.txt` (English)
- `whatsnew/es-MX/whatsnew.txt` (Spanish - Mexico)

Update these files when preparing mobile app releases.
