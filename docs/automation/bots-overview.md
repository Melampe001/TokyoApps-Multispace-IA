# Automation Bots Overview

This document provides a comprehensive inventory of all automated bots and workflows in TokyoApps-Multispace-IA.

## 🤖 Active Automation Bots

### 1. 🏷️ Auto-Labeler Bot

**Workflow**: `.github/workflows/auto-labeler.yml`  
**Configuration**: `.github/labeler.yml`  
**Trigger**: Pull requests (opened, synchronize, reopened)

**Purpose**: Automatically applies labels to PRs based on changed files and PR characteristics.

**Labels Applied**:
- **By File Type**: `backend`, `frontend`, `python`, `go`, `dart`, `typescript`, `javascript`, `ruby`
- **By Component**: `dependencies`, `documentation`, `ci/cd`, `security`, `database`, `testing`, `configuration`, `agents`, `synemu`
- **By Size**: `size/XS`, `size/S`, `size/M`, `size/L`, `size/XL`
- **By Content**: `breaking-change`, `needs-review` (for large PRs)

**Configuration**:
```yaml
# Example rule in labeler.yml
backend:
  - changed-files:
    - any-glob-to-any-file:
      - 'internal/**/*'
      - 'cmd/**/*'
```

---

### 2. 🤖 Auto-Review Bot

**Workflow**: `.github/workflows/pr-auto-review.yml`  
**Guidelines**: `.github/PULL_REQUEST_GUIDELINES.md`  
**Trigger**: Pull requests (opened, synchronize, reopened)

**Purpose**: Provides intelligent code review with constructive feedback on PRs.

**Checks Performed**:
- ✅ Naming conventions (Go, Python, TypeScript)
- ✅ File structure and organization
- ✅ Test file presence
- ✅ Documentation updates
- ✅ PR size and complexity
- ✅ Code organization patterns

**Output**:
- 👏 Compliments for good practices
- ⚠️ Issues that need fixing
- 💡 Suggestions for improvements
- 📊 Review summary

---

### 3. 📊 CodeCov Integration

**Configuration**: `.codecov.yml`  
**Workflow**: Integrated in `.github/workflows/ci.yml`  
**Trigger**: Push and pull requests

**Purpose**: Tracks code coverage and reports on test coverage quality.

**Features**:
- ✅ Minimum coverage threshold: 70%
- ✅ Automated PR comments with coverage changes
- ✅ Fails CI if coverage drops >5%
- ✅ Multi-language support (Go, Python, Dart)
- ✅ Flags for different components

**Setup Required**:
- Add `CODECOV_TOKEN` secret to repository settings
- See [codecov-setup.md](./codecov-setup.md) for details

**Coverage Flags**:
- `go`: Backend Go code
- `python`: Python libraries and agents
- `dart`: Flutter/Dart mobile app

---

### 4. 🔒 CodeQL Advanced Security

**Workflow**: `.github/workflows/codeql-analysis.yml`  
**Trigger**: Push to main/develop, PRs, weekly schedule (Mondays 6:00 UTC)

**Purpose**: Advanced security scanning with CodeQL for vulnerability detection.

**Languages Analyzed**:
- 🐹 Go
- 🐍 Python
- 📜 JavaScript/TypeScript

**Features**:
- ✅ Security-extended queries
- ✅ Security-and-quality analysis
- ✅ SARIF report generation
- ✅ GitHub Security tab integration
- ✅ Automated PR comments
- ✅ HIGH/CRITICAL alert notifications

**Security Checks**:
- SQL injection vulnerabilities
- Cross-site scripting (XSS)
- Command injection
- Path traversal
- Hardcoded credentials
- Insecure cryptography
- Memory safety issues (Go)
- And 200+ more patterns

---

### 5. 🚀 Preview Deployments

**Workflow**: `.github/workflows/preview-deploy.yml`  
**Trigger**: Pull requests affecting `web/` directory

**Purpose**: Automatic preview deployments to Vercel for each PR.

**Features**:
- ✅ Deploy preview on PR open/update
- ✅ Comment with preview URL
- ✅ Automatic cleanup on PR close
- ✅ Deployment status tracking

**Setup Required**:
- Add `VERCEL_TOKEN` secret
- Add `VERCEL_ORG_ID` secret
- Add `VERCEL_PROJECT_ID` secret
- See [preview-deployments.md](./preview-deployments.md) for setup

**Preview URL Format**:
```
pr-{number}-tokyoia.vercel.app
```

---

### 6. ⏰ Stale Bot

**Workflow**: `.github/workflows/stale.yml`  
**Trigger**: Daily at 00:00 UTC, manual trigger

**Purpose**: Manages inactive issues and pull requests.

**Configuration**:
- ⏱️ Marks stale after: 60 days
- 🔒 Closes after: 7 additional days
- 📌 Exemptions: `pinned`, `security`, `epic`, `help-wanted`
- 🚧 Draft PRs: Always exempt
- 👤 With assignees: Always exempt

**Messages**: Personalized in Spanish

---

### 7. 📝 Release Drafter

**Workflow**: `.github/workflows/release-drafter.yml`  
**Configuration**: `.github/release-drafter.yml`  
**Trigger**: Push to main, PR merge

**Purpose**: Automatically generates release notes from merged PRs.

**Features**:
- ✅ Categorizes changes by type
- ✅ Auto-increments version (semver)
- ✅ Groups by labels
- ✅ Contributor attribution
- ✅ Statistics (PRs, commits, contributors)

**Categories**:
- 🚀 New Features
- 🐛 Bug Fixes
- 🔒 Security
- ⚡ Performance
- 📚 Documentation
- 🧪 Testing
- 🔧 Maintenance
- 🎨 UI/UX
- ⚙️ CI/CD

**Version Resolution**:
- `major`: breaking-change label
- `minor`: enhancement, feature labels
- `patch`: bug, fix, security labels

---

### 8. 👥 Auto-Assign Reviewers

**Workflow**: `.github/workflows/auto-assign.yml`  
**Configuration**: `.github/auto_assign.yml`  
**Trigger**: Pull requests (opened, ready_for_review)

**Purpose**: Automatically assigns reviewers based on changed files.

**Features**:
- ✅ File pattern matching
- ✅ Round-robin distribution
- ✅ Exclude PR author
- ✅ Skip WIP PRs
- ✅ Minimum 2 reviewers

**File Patterns**:
- `**/*.go` → Go experts
- `**/*.py` → Python experts
- `web/**/*` → Frontend experts
- `app/**/*` → Mobile experts
- `.github/workflows/**/*` → DevOps experts

---

### 9. 📈 PR Metrics Bot

**Workflow**: `.github/workflows/pr-metrics.yml`  
**Trigger**: Pull requests (opened, synchronize, reopened)

**Purpose**: Posts comprehensive metrics about PR complexity and quality.

**Metrics Provided**:
- 📊 Lines added/deleted
- 📁 Files by type breakdown
- 🎯 Complexity score (XS, S, M, L, XL)
- ⏱️ Estimated review time
- 🧪 Test coverage indicator
- 💯 Quality score (0-100)

**Quality Score Factors**:
- ✅ PR size (smaller is better)
- ✅ Test coverage
- ✅ Number of files changed
- ✅ Documentation updates
- ✅ Following best practices

---

## 📋 Existing Bots (Previously Implemented)

### 10. 🔧 Dependency Agent
**Workflow**: `.github/workflows/dependency-agent.yml`  
**Purpose**: Monitors and manages project dependencies

### 11. 🤝 Bot Coordinator
**Workflow**: `.github/workflows/bot-coordinator.yml`  
**Purpose**: Coordinates multiple specialized bots

### 12. 🎨 Frontend UX Bot
**Workflow**: `.github/workflows/bot-frontend-ux.yml`  
**Purpose**: Reviews frontend UX changes

### 13. 🏗️ Frontend Build Bot
**Workflow**: `.github/workflows/bot-frontend-build.yml`  
**Purpose**: Validates frontend builds

### 14. ⚡ Backend Performance Bot
**Workflow**: `.github/workflows/bot-backend-performance.yml`  
**Purpose**: Analyzes backend performance

### 15. ✨ Backend Quality Bot
**Workflow**: `.github/workflows/bot-backend-quality.yml`  
**Purpose**: Ensures backend code quality

### 16. 🚨 Blocker Detector
**Workflow**: `.github/workflows/blocker-detector.yml`  
**Purpose**: Detects blocking issues in PRs

### 17. 📚 Auto-Documenter
**Workflow**: `.github/workflows/auto-documenter.yml`  
**Purpose**: Automatically updates documentation

### 18. 📖 Library Indexer
**Workflow**: `.github/workflows/library-indexer.yml`  
**Purpose**: Indexes and catalogs libraries

### 19. 📊 Library Report
**Workflow**: `.github/workflows/library-report.yml`  
**Purpose**: Generates library usage reports

### 20. 📈 Weekly Report
**Workflow**: `.github/workflows/weekly-report.yml`  
**Purpose**: Weekly summary of repository activity

### 21. 🦋 Flutter Agents
**Workflow**: `.github/workflows/flutter-agents.yml`  
**Purpose**: Specialized Flutter/Dart automation

### 22. 🔐 Dependabot
**Configuration**: `.github/dependabot.yml`  
**Purpose**: Automated dependency updates

---

## 🎯 Imperial Cleaner (Status Check)

**Note**: The Imperial Cleaner workflow mentioned in the requirements was not found in the repository. This may be:
- A planned feature not yet implemented
- Previously removed or renamed
- Implemented in a different way

If you need auto-merge functionality, consider:
- Enabling GitHub's built-in auto-merge feature
- Using the "Merge Queue" feature for main branch
- Creating a custom workflow for auto-merging approved PRs

---

## 🔧 Configuration Quick Reference

| Bot | Configuration File | Secrets Required |
|-----|-------------------|------------------|
| Auto-Labeler | `.github/labeler.yml` | None |
| Auto-Review | `.github/PULL_REQUEST_GUIDELINES.md` | None |
| CodeCov | `.codecov.yml` | `CODECOV_TOKEN` |
| CodeQL | (inline config) | None |
| Preview Deploy | (inline config) | `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` |
| Stale | (inline config) | None |
| Release Drafter | `.github/release-drafter.yml` | None |
| Auto-Assign | `.github/auto_assign.yml` | None |
| PR Metrics | (inline config) | None |

---

## 📚 Documentation

- [CodeCov Setup Guide](./codecov-setup.md)
- [Preview Deployments Guide](./preview-deployments.md)
- [Pull Request Guidelines](../.github/PULL_REQUEST_GUIDELINES.md)

---

## 🚀 Getting Started

All bots are automatically active. No manual intervention needed!

1. **Create a PR** → Bots automatically activate
2. **Review bot comments** → Address any issues
3. **Merge PR** → Release notes automatically updated

---

## 🛠️ Troubleshooting

### Bot Not Running?

1. Check workflow permissions in repo settings
2. Verify secrets are configured (for CodeCov, Vercel)
3. Check workflow run logs in Actions tab
4. Ensure PR doesn't skip bot triggers (e.g., draft PRs)

### Bot Comments Not Appearing?

- Check bot has `pull-requests: write` permission
- Verify workflow completed successfully
- Look for errors in Actions logs

### Need to Disable a Bot?

Edit the workflow file and add:
```yaml
if: false  # Temporarily disable
```

Or rename the workflow file to `.disabled-{name}.yml`

---

## 📝 Contributing

To add a new bot:

1. Create workflow in `.github/workflows/`
2. Follow existing bot patterns
3. Use minimal permissions
4. Add documentation here
5. Test with a PR

---

**Last Updated**: December 2024  
**Maintained By**: Tokyo-IA Team
