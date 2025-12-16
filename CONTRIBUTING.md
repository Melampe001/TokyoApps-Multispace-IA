# Contributing to Tokyo-IA

Thank you for your interest in contributing to Tokyo-IA! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Branch Protection Rules](#branch-protection-rules)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and professional in all interactions.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Tokyo-IA.git
   cd Tokyo-IA
   ```
3. Add the upstream repository as a remote:
   ```bash
   git remote add upstream https://github.com/Melampe001/Tokyo-IA.git
   ```

## Development Setup

### Android App

1. Install Android Studio with SDK Platform 33 or higher
2. Open the project in Android Studio
3. Sync Gradle files
4. Run the app:
   ```bash
   ./gradlew assembleDebug
   ./gradlew installDebug
   ```

### Web Application

1. Install Node.js 20 or higher
2. Navigate to the web directory:
   ```bash
   cd web
   npm install
   npm run dev
   ```

### MCP Server

1. Install Node.js 20 or higher
2. Navigate to the server-mcp directory:
   ```bash
   cd server-mcp
   npm install
   npm start
   ```

## Making Changes

### Setting Up Pre-commit Hooks

We recommend setting up pre-commit hooks to ensure code quality before committing:

1. Install pre-commit hooks for Android (Kotlin):
   ```bash
   # Create a pre-commit hook
   cat > .git/hooks/pre-commit << 'EOF'
   #!/bin/bash
   # Run ktlint if available
   if command -v ktlint &> /dev/null; then
       ktlint --format "app/src/**/*.kt" || exit 1
   fi
   EOF
   chmod +x .git/hooks/pre-commit
   ```

2. Install pre-commit hooks for Web/Server (JavaScript):
   ```bash
   # For web
   cd web
   npm install --save-dev husky lint-staged
   npx husky install
   npx husky add .husky/pre-commit "npm run lint"
   
   # For server-mcp
   cd server-mcp
   npm install --save-dev husky lint-staged
   npx husky install
   npx husky add .husky/pre-commit "npm run lint"
   ```

### Creating a Branch

Always create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or changes

### Committing Changes

1. Stage your changes:
   ```bash
   git add .
   ```

2. Commit with a descriptive message:
   ```bash
   git commit -m "feat: add user authentication to Android app"
   ```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Test changes
- `chore:` - Build process or auxiliary tool changes

## Pull Request Process

1. Update your branch with the latest changes from upstream:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request on GitHub with:
   - Clear title describing the change
   - Detailed description of what changed and why
   - Reference to related issues (e.g., "Closes #123")
   - Screenshots for UI changes
   - List of testing performed

4. Ensure all CI checks pass:
   - Android build and tests
   - Web build and tests
   - MCP Server build and tests

5. Address review feedback promptly

6. Once approved, your PR will be merged by a maintainer

## Coding Standards

### Android (Kotlin)

- Follow [Kotlin coding conventions](https://kotlinlang.org/docs/coding-conventions.html)
- Use descriptive names for classes, functions, and variables
- Prefer data classes for simple data holders
- Use coroutines for asynchronous operations
- Add KDoc comments for public APIs

### Web (JavaScript/React)

- Use functional components with hooks
- Follow React best practices
- Use consistent naming conventions:
  - camelCase for variables and functions
  - PascalCase for components
- Use ESLint and Prettier for code formatting
- Add JSDoc comments for complex functions

### MCP Server (Node.js)

- Use async/await for asynchronous operations
- Handle errors appropriately with try/catch blocks
- Follow modular architecture patterns
- Use descriptive variable and function names
- Add JSDoc comments for public APIs

### General Guidelines

- Write clear, self-documenting code
- Keep functions small and focused on a single responsibility
- Add comments only when the code logic is complex or non-obvious
- Avoid magic numbers - use named constants
- Remove commented-out code before committing

## Testing

### Writing Tests

All new features should include appropriate tests:

- **Android**: Write unit tests using JUnit and instrumentation tests using Espresso
- **Web**: Write unit tests using Jest/Vitest and React Testing Library
- **Server**: Write unit tests using Jest or Mocha

### Running Tests

```bash
# Android
./gradlew test

# Web
cd web
npm test

# MCP Server
cd server-mcp
npm test
```

### Test Coverage

Aim for at least 80% code coverage for new code. The CI pipeline will report coverage metrics.

## Branch Protection Rules

The `main` branch is protected with the following rules:

1. **Require pull request reviews before merging**
   - At least 1 approval required
   - Dismiss stale reviews when new commits are pushed

2. **Require status checks to pass before merging**
   - CI Pipeline must pass
   - All component-specific checks must pass (Android, Web, MCP Server)

3. **Require branches to be up to date before merging**
   - Your branch must be rebased on the latest main

4. **Require linear history**
   - No merge commits - use rebase or squash merge

5. **Do not allow force pushes**
   - Protects against accidental history rewrites

6. **Require signed commits** (recommended)
   - Set up GPG key signing for additional security

### Setting Up Branch Protection (For Maintainers)

To configure these rules on GitHub:

1. Go to repository Settings → Branches
2. Add rule for `main` branch
3. Enable the protections listed above
4. Click "Create" or "Save changes"

## Security

**CRITICAL: Never commit secrets to the repository.**

- Do NOT store service account JSONs, keystore files, private keys, or other secrets
- Use GitHub Actions Secrets for CI/CD credentials
- If you accidentally commit a secret:
  1. Rotate the exposed credential immediately
  2. Contact a maintainer to help remove it from git history
  3. Never commit secrets again

For more details, see the [Security Guidelines](README.md#security--secrets-important) in the README.

## Questions?

If you have questions or need help:

1. Check the [README.md](README.md) for basic information
2. Search existing issues for similar questions
3. Open a new issue with the "question" label
4. Reach out to maintainers

Thank you for contributing to Tokyo-IA! 🎌
