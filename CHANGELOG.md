# Changelog

All notable changes to Tokyo IA will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### ✨ Added

- Complete Python automation ecosystem
- GitHub Copilot Agents:
  - `copilot-lint-agent` - Python linting with pylint, flake8, black
  - `copilot-coverage-agent` - Test coverage analysis with pytest-cov
  - `copilot-build-agent` - Python builds and packaging
  - `copilot-release-agent` - Automated versioning and releases
  - `copilot-chatops-agent` - Commands from issue/PR comments
  - `tokyo-ia-master-agent` - Master coordinator agent
- GitHub Workflows:
  - `python-ci-cd.yml` - Complete Python CI/CD pipeline
  - `security-scan.yml` - Security vulnerability scanning
  - `release.yml` - Automated release management
  - `chatops.yml` - ChatOps commands
  - `lint.yml` - Code linting with auto-fix
  - `json-cleaner.yml` - JSON validation and formatting
  - `dependency-check.yml` - Dependency auditing
- GitHub Bot Automations:
  - `auto-assign.yml` - Auto-assign issues and PRs
  - `auto-label.yml` - Auto-label based on content
  - `auto-close-stale.yml` - Close inactive issues/PRs
  - `auto-merge.yml` - Auto-merge approved PRs
  - `auto-changelog.yml` - Generate changelog
  - `auto-documentation.yml` - Generate documentation
- Self-Hosted Runners:
  - Python runner with multiple Python versions
  - Docker runner with Docker-in-Docker support
  - Kubernetes autoscale configuration
- Configuration files:
  - `pyproject.toml` - Complete Python project configuration
  - `.flake8` - Flake8 linting configuration
  - `requirements.txt` - Production dependencies
  - `requirements-dev.txt` - Development dependencies

### 🔧 Configuration

- Black: line-length 100, target Python 3.9-3.12
- isort: profile "black", integrated with Black
- pytest: 70% minimum coverage, async support
- mypy: strict optional, Python 3.11 target

## [1.0.0] - 2025-11-25

### 🎉 Initial Release

- Tokyo IA project foundation
- Agent architecture design
- Flutter/Dart code snippets
- Sentiment analysis concepts
- Unlimited mode implementation concepts
