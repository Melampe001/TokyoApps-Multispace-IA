# Tokyo-IA Documentation

This directory contains comprehensive documentation for the Tokyo-IA project.

## Overview

Tokyo-IA is a mobile + web + server project that provides Tokyo-themed AI features and an MCP (Model Context Protocol) server.

## Documentation Index

### Getting Started
- [Main README](../README.md) - Project overview and quick start
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute to the project
- [Security Policy](../SECURITY.md) - Security best practices and reporting vulnerabilities

### Development Guides
- [CI/CD Documentation](CI_CD.md) - Continuous Integration and Deployment workflows
- [Branch Protection Rules](BRANCH_PROTECTION.md) - Git workflow and branch protection setup

### Project Components
- **Android App** (`app/`) - Kotlin-based Android application
- **Web Application** (`web/`) - React/Vite web application with admin panel
- **MCP Server** (`server-mcp/`) - Node.js server for MCP functionality

## Quick Links

### For Contributors
1. Read the [Contributing Guide](../CONTRIBUTING.md)
2. Set up your development environment
3. Review the [CI/CD Documentation](CI_CD.md)
4. Understand [Branch Protection Rules](BRANCH_PROTECTION.md)

### For Maintainers
1. Configure [Branch Protection](BRANCH_PROTECTION.md#implementation-guide)
2. Review [CI/CD workflows](CI_CD.md#workflows)
3. Monitor [Security alerts](../SECURITY.md#automated-security-scanning)
4. Manage [Dependabot updates](CI_CD.md#dependency-management)

## Additional Resources

- GitHub Actions workflows: `.github/workflows/`
- Dependabot configuration: `.github/dependabot.yml`
- Issue templates: `.github/ISSUE_TEMPLATE/`
- Pull request template: `.github/pull_request_template.md`
