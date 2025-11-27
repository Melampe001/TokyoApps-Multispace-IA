# Contributing to Tokyo-IA

Thank you for your interest in contributing to Tokyo-IA! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Branch Strategy](#branch-strategy)
- [How to Create a Pull Request](#how-to-create-a-pull-request)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)

## Code of Conduct

Please be respectful and constructive in all interactions. We're committed to providing a welcoming and inclusive environment for everyone.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Tokyo-IA.git
   cd Tokyo-IA
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/Melampe001/Tokyo-IA.git
   ```
4. **Set up the development environment** (see [README.md](../README.md))

## Branch Strategy

We follow a Git Flow-inspired branching model:

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code, protected |
| `develop` | Integration branch for features, protected |
| `feature/*` | New features (e.g., `feature/add-login`) |
| `bugfix/*` | Bug fixes (e.g., `bugfix/fix-crash-on-startup`) |
| `hotfix/*` | Urgent production fixes |
| `release/*` | Release preparation |

### Branch Naming Conventions
- `feature/short-description`
- `bugfix/issue-number-description`
- `hotfix/critical-fix-description`
- `release/v1.2.0`

## How to Create a Pull Request

1. **Create a new branch** from `develop`:
   ```bash
   git checkout develop
   git pull upstream develop
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and commit them following our commit message guidelines

3. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request** on GitHub:
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template completely

5. **Address review feedback** if requested

### PR Requirements
- [ ] Target the `develop` branch (unless it's a hotfix)
- [ ] Pass all CI checks
- [ ] Include tests for new functionality
- [ ] Update documentation if needed
- [ ] At least one approving review

## Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(auth): add Google OAuth login
fix(web): resolve CSS layout issue on mobile
docs(readme): update installation instructions
```

## Development Workflow

### Prerequisites
- Node.js 20+
- npm or yarn
- Android Studio (for Android development)
- Flutter (for mobile development)

### Local Development

#### Web Application
```bash
cd web
npm install
npm run dev        # Start development server
npm run lint       # Run linter
npm run build      # Build for production
npm test           # Run tests
```

#### MCP Server
```bash
cd server-mcp
npm install
npm start          # Start server
npm test           # Run tests
```

#### Android App
```bash
./gradlew assembleDebug    # Build debug APK
./gradlew installDebug     # Install on device
./gradlew test             # Run unit tests
```

### Pre-commit Hooks

We recommend setting up pre-commit hooks to ensure code quality:

1. **Install the pre-commit hook**:
   ```bash
   # Create the hook
   cat > .git/hooks/pre-commit << 'EOF'
   #!/bin/sh
   
   # Run linting for web
   if [ -d "web" ]; then
       cd web && npm run lint 2>/dev/null || true
       cd ..
   fi
   
   # Run linting for server-mcp
   if [ -d "server-mcp" ]; then
       cd server-mcp && npm run lint 2>/dev/null || true
       cd ..
   fi
   EOF
   
   chmod +x .git/hooks/pre-commit
   ```

2. **Verify the hook is working**:
   ```bash
   git commit --dry-run
   ```

## Code Style

### JavaScript/TypeScript
- Use ESLint configuration provided
- Prefer functional components in React
- Use async/await for asynchronous operations

### Kotlin
- Follow [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- Use meaningful variable and function names
- Prefer data classes for simple data holders

### Documentation
- Use Markdown for all documentation
- Include code examples where helpful
- Keep documentation up-to-date with code changes

## Questions?

If you have questions, feel free to:
- Open an issue
- Start a discussion
- Reach out to the maintainers

Thank you for contributing! 🎌
