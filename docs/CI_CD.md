# CI/CD Documentation

This document describes the Continuous Integration and Continuous Deployment (CI/CD) setup for Tokyo-IA.

## Table of Contents

- [Overview](#overview)
- [CI Pipeline](#ci-pipeline)
- [Workflows](#workflows)
- [Conditional Execution](#conditional-execution)
- [Dependency Management](#dependency-management)
- [Secrets Management](#secrets-management)
- [Troubleshooting](#troubleshooting)

## Overview

Tokyo-IA uses GitHub Actions for CI/CD automation. The pipeline is designed to:

1. Automatically test changes to Android, Web, and MCP Server components
2. Only run relevant jobs based on which files changed
3. Provide fast feedback to developers
4. Ensure code quality before merging

## CI Pipeline

The main CI pipeline (`.github/workflows/ci.yml`) runs on:

- Push to `main` or `develop` branches
- Pull requests targeting `main` or `develop` branches

### Pipeline Stages

1. **Change Detection** - Identifies which components changed
2. **Component Testing** - Runs tests for affected components
3. **Artifact Upload** - Stores build artifacts and test results

## Workflows

### Main CI Workflow (`ci.yml`)

This workflow handles all three project components with intelligent path filtering.

#### Android CI Job

**Triggers when:**
- Files in `app/` directory change
- Gradle configuration files change
- Gradle wrapper files change

**Steps:**
1. Checkout code
2. Set up JDK 17
3. Cache Gradle dependencies
4. Grant execute permission for gradlew
5. Build debug APK
6. Run unit tests
7. Upload test results

**Requirements:**
- JDK 17 (Temurin distribution)
- Gradle wrapper

**Artifacts:**
- Android test results (`app/build/reports/tests/`)

#### Web CI Job

**Triggers when:**
- Files in `web/` directory change

**Steps:**
1. Checkout code
2. Set up Node.js 20
3. Cache npm dependencies
4. Install dependencies
5. Run linter (if available)
6. Run tests (if available)
7. Build production bundle
8. Upload build artifacts

**Requirements:**
- Node.js 20
- npm

**Artifacts:**
- Web build output (`web/dist/`)

#### MCP Server CI Job

**Triggers when:**
- Files in `server-mcp/` directory change

**Steps:**
1. Checkout code
2. Set up Node.js 20
3. Cache npm dependencies
4. Install dependencies
5. Run linter (if available)
6. Run tests (if available)
7. Build (if build script exists)

**Requirements:**
- Node.js 20
- npm

## Conditional Execution

The CI pipeline uses `dorny/paths-filter` to detect changes and conditionally run jobs.

### How It Works

1. The `changes` job analyzes which files changed
2. It outputs boolean flags for each component
3. Component jobs check these flags with `if` conditions
4. Only jobs for changed components execute

### Benefits

- **Faster CI** - Only relevant tests run
- **Resource Efficiency** - Saves GitHub Actions minutes
- **Clear Feedback** - Easy to see which components are affected

### Path Filters

```yaml
android:
  - 'app/**'
  - 'gradle/**'
  - '*.gradle'
  - '*.gradle.kts'
  - 'gradlew*'

web:
  - 'web/**'

server-mcp:
  - 'server-mcp/**'
```

### Testing Path Filters

To test if your changes will trigger a specific job:

```bash
# Check which files changed in your branch
git diff --name-only origin/main

# Compare against the path filters in ci.yml
```

## Dependency Management

Dependabot automatically checks for dependency updates weekly.

### Configuration (`.github/dependabot.yml`)

#### Update Schedule

- **Day:** Monday
- **Time:** 09:00 UTC
- **Frequency:** Weekly

#### Monitored Ecosystems

1. **GitHub Actions**
   - Updates workflow action versions
   - Max 5 open PRs

2. **npm (Web)**
   - Updates web application dependencies
   - Max 10 open PRs
   - Grouped by development/production

3. **npm (MCP Server)**
   - Updates server dependencies
   - Max 10 open PRs
   - Grouped by development/production

4. **Gradle (Android)**
   - Updates Android dependencies
   - Max 10 open PRs

### Handling Dependabot PRs

1. **Review the PR** - Check the changelog and breaking changes
2. **Run Tests** - CI automatically runs for Dependabot PRs
3. **Test Locally** - For major updates, test manually
4. **Merge** - If tests pass and changes look good
5. **Monitor** - Watch for issues after merging

### Dependabot Security Updates

Dependabot also creates PRs for security vulnerabilities automatically.

**Priority:** Always review and merge security updates quickly.

## Secrets Management

### Required Secrets

For CI/CD, the following secrets may be needed (stored in GitHub repository settings):

#### Android Release (Future)

- `ANDROID_KEYSTORE_BASE64` - Base64-encoded keystore file
- `KEYSTORE_PASSWORD` - Keystore password
- `KEY_ALIAS` - Key alias
- `KEY_PASSWORD` - Key password
- `GOOGLE_PLAY_JSON` - Google Play service account JSON

#### Web Deployment (Future)

- `VERCEL_TOKEN` or similar - Deployment service token
- `WEB_API_URL` - Production API URL

#### MCP Server (Future)

- `SERVER_API_KEY` - API key for production
- `DATABASE_URL` - Database connection string

### Adding Secrets

1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add name and value
4. Click "Add secret"

### Using Secrets in Workflows

```yaml
- name: Example using secret
  run: echo "Secret value"
  env:
    MY_SECRET: ${{ secrets.MY_SECRET }}
```

**Important:** Never echo or log secret values!

## Troubleshooting

### Common Issues

#### 1. Gradle Permission Denied

**Error:** `Permission denied: ./gradlew`

**Solution:** The workflow automatically runs `chmod +x gradlew`, but if you see this locally:

```bash
chmod +x gradlew
git add gradlew
git commit -m "fix: make gradlew executable"
```

#### 2. Node.js Cache Issues

**Error:** `npm ci` fails with cache errors

**Solution:** Clear npm cache in workflow:

```yaml
- name: Clear npm cache
  run: npm cache clean --force
```

#### 3. Tests Failing Only in CI

**Possible causes:**
- Different Node.js/Java versions
- Missing environment variables
- Race conditions in tests
- File path issues (case sensitivity)

**Solution:** Run tests locally with same versions:

```bash
# Match CI Node.js version
nvm use 20

# Match CI Java version
export JAVA_HOME=/path/to/jdk-17
```

#### 4. Workflow Not Triggering

**Check:**
1. Branch name matches trigger conditions
2. Workflow file is in `.github/workflows/`
3. YAML syntax is valid (use yamllint)
4. Repository Actions are enabled (Settings → Actions)

#### 5. Path Filter Not Working

**Debug:**
1. Check the `changes` job output in Actions tab
2. Verify file paths match filter patterns
3. Remember filters are case-sensitive
4. Test with: `git diff --name-only origin/main`

### Getting Help

1. Check workflow logs in Actions tab
2. Review this documentation
3. Search existing issues
4. Open new issue with:
   - Workflow run URL
   - Error message
   - Steps to reproduce

## Best Practices

### For Contributors

1. **Run Tests Locally First**
   ```bash
   # Android
   ./gradlew test
   
   # Web
   cd web && npm test
   
   # Server
   cd server-mcp && npm test
   ```

2. **Keep Dependencies Updated**
   - Review Dependabot PRs regularly
   - Update major versions carefully

3. **Write Maintainable Workflows**
   - Use clear job and step names
   - Add comments for complex logic
   - Keep workflows DRY with reusable actions

4. **Monitor CI Performance**
   - Watch for slow jobs
   - Optimize test suites
   - Use caching effectively

### For Maintainers

1. **Review Workflow Changes Carefully**
   - Test in a fork first
   - Watch first few runs
   - Have rollback plan

2. **Manage Secrets Securely**
   - Rotate secrets regularly
   - Use environment-specific secrets
   - Audit secret access

3. **Monitor Action Minutes**
   - GitHub provides limited free minutes
   - Optimize workflows for efficiency
   - Consider self-hosted runners for heavy workloads

4. **Keep Documentation Updated**
   - Update this file when workflows change
   - Document new secrets
   - Explain complex workflow logic

## Future Enhancements

Potential improvements to the CI/CD pipeline:

- [ ] Add deployment workflows
- [ ] Implement release automation
- [ ] Add code coverage reporting
- [ ] Set up preview deployments for PRs
- [ ] Add performance testing
- [ ] Implement blue-green deployments
- [ ] Add notification integrations (Slack, Discord)
- [ ] Set up automatic changelog generation

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Android CI/CD Best Practices](https://developer.android.com/studio/build/building-cmdline)
- [Node.js CI Best Practices](https://docs.npmjs.com/cli/v9/commands/npm-ci)
