# Contributing to Tokyo-IA

Thank you for your interest in contributing to Tokyo-IA! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Branch Protection Rules](#branch-protection-rules)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and professional in all interactions.

## Getting Started

1. Fork and clone
2. Install dependencies: `go mod download && pip install -r requirements.txt`
3. Install pre-commit: `pre-commit install`
4. Create feature branch: `git checkout -b feature/amazing-feature`

## Development Setup

### Go Development

1. Install Go 1.21 or higher
2. Install dependencies:
   ```bash
   go mod download
   ```
3. Build the application:
   ```bash
   make build
   ```

### Python Development

1. Install Python 3.11 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest flake8 black
   ```

### Pre-commit Hooks Setup

Install pre-commit hooks to ensure code quality:

```bash
pip install pre-commit
pre-commit install
```

## Making Changes

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
   git commit -m "feat: add user authentication"
   ```

Commit message format: `type(scope): description`

Types: feat, fix, docs, style, refactor, test, chore

Example: `feat(branch): add ML-based branch naming`

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
   - List of testing performed

4. Ensure all CI checks pass:
   - Go tests and linting
   - Python tests and formatting
   - Security scans

5. Address review feedback promptly

6. Once approved, your PR will be merged by a maintainer

## Code Standards

### Go
- Run `make fmt` before committing
- Follow [Effective Go](https://go.dev/doc/effective_go)
- Maintain test coverage >80%
- Use meaningful variable and function names
- Keep functions small and focused

### Python
- Use Black formatter: `black .`
- Follow PEP 8
- Type hints required
- Maximum line length: 100 characters
- Use descriptive variable and function names

### General Guidelines
- Write clear, self-documenting code
- Keep functions small and focused on a single responsibility
- Add comments only when the code logic is complex or non-obvious
- Avoid magic numbers - use named constants
- Remove commented-out code before committing

## Testing

### Writing Tests

All new features should include appropriate tests:

- **Go**: Write unit tests using the standard testing package
- **Python**: Write unit tests using pytest

### Running Tests

```bash
# Go tests
make test
# or
go test ./...

# Python tests
pytest

# With coverage
go test -coverprofile=coverage.txt ./...
pytest --cov
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
   - Security scans must pass
   - All tests must pass

3. **Require branches to be up to date before merging**
   - Your branch must be rebased on the latest main

4. **Require linear history**
   - No merge commits - use rebase or squash merge

5. **Do not allow force pushes**
   - Protects against accidental history rewrites

6. **Require signed commits** (recommended)
   - Set up GPG key signing for additional security

## Security

**CRITICAL: Never commit secrets to the repository.**

- Do NOT store service account JSONs, keystore files, private keys, or other secrets
- Use GitHub Actions Secrets for CI/CD credentials
- Use environment variables for configuration
- If you accidentally commit a secret:
  1. Rotate the exposed credential immediately
  2. Contact a maintainer to help remove it from git history
  3. Never commit secrets again

For more details, see the [Security Policy](SECURITY.md).

## Questions?

If you have questions or need help:

1. Check the [README.md](README.md) for basic information
2. Review the [Architecture documentation](docs/ARCHITECTURE.md)
3. Search existing issues for similar questions
4. Open a new issue with the "question" label

Thank you for contributing to Tokyo-IA! 🏛️
