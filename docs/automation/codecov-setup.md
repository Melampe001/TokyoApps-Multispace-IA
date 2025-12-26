# CodeCov Setup Guide

This guide explains how to configure CodeCov for TokyoApps-Multispace-IA to track code coverage across multiple languages.

## Overview

CodeCov is integrated into our CI pipeline to:
- Track code coverage for Go, Python, and Dart
- Comment on PRs with coverage changes
- Fail builds if coverage drops significantly
- Provide detailed coverage reports

## Configuration

### 1. CodeCov Token Setup

#### Get Your Token

1. Visit [codecov.io](https://codecov.io)
2. Sign in with your GitHub account
3. Add your repository (if not already added)
4. Navigate to Settings → General
5. Copy the **Repository Upload Token**

#### Add Token to GitHub

1. Go to your repository on GitHub
2. Navigate to **Settings → Secrets and variables → Actions**
3. Click **New repository secret**
4. Name: `CODECOV_TOKEN`
5. Value: Paste your token
6. Click **Add secret**

### 2. Configuration File

The `.codecov.yml` file in the repository root controls CodeCov behavior:

```yaml
coverage:
  precision: 2
  round: down
  range: "70...100"
  
  status:
    project:
      default:
        target: 70%              # Minimum coverage target
        threshold: 5%            # Allow 5% drop before failing
```

#### Key Settings Explained

| Setting | Value | Purpose |
|---------|-------|---------|
| `target` | 70% | Minimum coverage required |
| `threshold` | 5% | Maximum allowed coverage drop |
| `precision` | 2 | Decimal places in reports |
| `if_ci_failed` | error | Behavior when CI fails |

### 3. Coverage Flags

We use flags to separate coverage by component:

```yaml
flags:
  go:
    paths:
      - "cmd/"
      - "internal/"
      - "lib/*.go"
  
  python:
    paths:
      - "lib/*.py"
      - "agents/"
      - "SYNEMU/"
  
  dart:
    paths:
      - "app/"
      - "flutter_app/"
```

This allows tracking coverage separately for:
- Go backend code
- Python agents and libraries
- Dart/Flutter mobile app

## Integration in CI

### Go Coverage

In `.github/workflows/ci.yml`:

```yaml
- name: Run tests with race detector
  run: go test -v -race -coverprofile=coverage.out -covermode=atomic ./...

- name: Upload coverage
  uses: codecov/codecov-action@v5
  with:
    files: ./coverage.out
    flags: go
    token: ${{ secrets.CODECOV_TOKEN }}
    fail_ci_if_error: false
```

### Python Coverage

```yaml
- name: Run pytest with coverage
  run: pytest --cov=lib --cov-report=xml --cov-report=term-missing

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    files: ./coverage.xml
    flags: python
    token: ${{ secrets.CODECOV_TOKEN }}
```

### Dart Coverage

For Flutter/Dart projects:

```bash
flutter test --coverage
```

Then upload the `coverage/lcov.info` file.

## PR Comments

CodeCov automatically comments on PRs with:

### Coverage Diff
```
Coverage Δ: +2.45% ✅
Files: 12 changed
Lines: +156 (added), -43 (removed)
```

### File-by-File Breakdown
```
Files Changed      Coverage Δ
internal/api.go    +5.2% ✅
lib/utils.py       -1.3% ⚠️
```

### Status Checks

- ✅ **Pass**: Coverage meets target
- ⚠️ **Warning**: Coverage dropped but within threshold
- ❌ **Fail**: Coverage dropped more than threshold

## Badge in README

Add a CodeCov badge to your README:

```markdown
[![codecov](https://codecov.io/gh/Melampe001/TokyoApps-Multispace-IA/branch/main/graph/badge.svg)](https://codecov.io/gh/Melampe001/TokyoApps-Multispace-IA)
```

This displays: [![codecov](https://codecov.io/gh/example/repo/branch/main/graph/badge.svg)](https://codecov.io)

## Viewing Reports

### On CodeCov Website

1. Visit https://codecov.io/gh/Melampe001/TokyoApps-Multispace-IA
2. View:
   - Overall coverage percentage
   - Coverage trends over time
   - File-by-file coverage
   - Sunburst visualization
   - Coverage by component (flags)

### In Pull Requests

- Check the CodeCov comment on your PR
- Click "Changes" to see line-by-line coverage
- Green: Covered lines
- Red: Uncovered lines
- Yellow: Partially covered (branches)

## Coverage Thresholds

### Current Targets

| Component | Target | Threshold |
|-----------|--------|-----------|
| Overall Project | 70% | 5% drop allowed |
| New Code (Patch) | 70% | 5% drop allowed |
| Go Backend | 70% | - |
| Python Libraries | 70% | - |
| Dart Mobile | 70% | - |

### Adjusting Thresholds

To change thresholds, edit `.codecov.yml`:

```yaml
coverage:
  status:
    project:
      default:
        target: 80%              # Increase to 80%
        threshold: 3%            # Stricter threshold
```

## Best Practices

### Writing Testable Code

1. **Keep functions small** - Easier to test
2. **Avoid side effects** - Makes mocking easier
3. **Dependency injection** - Simplifies testing
4. **Clear interfaces** - Better test boundaries

### Improving Coverage

1. **Test edge cases**:
   ```go
   // Test nil inputs, empty strings, boundary values
   ```

2. **Test error paths**:
   ```python
   # Don't just test success, test failures too
   ```

3. **Integration tests**:
   ```go
   // Test components working together
   ```

4. **Table-driven tests** (Go):
   ```go
   tests := []struct {
       name string
       input int
       want int
   }{
       {"positive", 5, 10},
       {"negative", -5, 0},
   }
   ```

### Excluding Files

Some files don't need coverage:

```yaml
ignore:
  - "testing/"
  - "examples/"
  - "**/*_test.go"
  - "**/*.pb.go"      # Generated protobuf
  - "**/mock_*.go"    # Mock files
```

## Troubleshooting

### Coverage Not Uploading

**Check**:
1. `CODECOV_TOKEN` is set correctly
2. CI workflow has `codecov/codecov-action` step
3. Coverage file is generated (`coverage.out`, `coverage.xml`)
4. Workflow logs for errors

**Fix**:
```yaml
- name: Upload coverage
  uses: codecov/codecov-action@v5
  with:
    files: ./coverage.out
    fail_ci_if_error: true      # See actual errors
    verbose: true               # Detailed logging
```

### Coverage Report Not Showing

**Issue**: Tests run but no coverage report

**Go Solution**:
```bash
go test -v -coverprofile=coverage.out -covermode=atomic ./...
```

**Python Solution**:
```bash
pytest --cov=lib --cov-report=xml
```

### Incorrect Coverage Percentage

**Issue**: Coverage seems wrong

**Check**:
1. All test files are being discovered
2. Import paths are correct
3. Test files have proper naming (`*_test.go`, `test_*.py`)

### CI Fails Due to Coverage

**Issue**: PR blocked by coverage check

**Temporary Fix** (use sparingly):
```yaml
fail_ci_if_error: false
```

**Permanent Fix**:
- Add tests to improve coverage
- Or adjust threshold if current level is acceptable

## Advanced Features

### Coverage Graphs

View coverage trends over time:
- https://codecov.io/gh/Melampe001/TokyoApps-Multispace-IA/graphs

### Branch Comparison

Compare coverage between branches:
```
https://codecov.io/gh/Melampe001/TokyoApps-Multispace-IA/compare/main...feature-branch
```

### Component Comparison

View coverage by flag:
- Go: `?flags=go`
- Python: `?flags=python`
- Dart: `?flags=dart`

### API Access

CodeCov provides an API:
```bash
curl -H "Authorization: Bearer $CODECOV_TOKEN" \
  https://codecov.io/api/v2/github/Melampe001/repos/TokyoApps-Multispace-IA/
```

## GitHub App (Alternative)

Instead of using the token, you can install the CodeCov GitHub App:

1. Visit https://github.com/apps/codecov
2. Click "Install"
3. Select repositories
4. Grant permissions

Benefits:
- No token management needed
- Better GitHub integration
- More granular permissions

## Resources

- [CodeCov Documentation](https://docs.codecov.com/)
- [codecov-action GitHub](https://github.com/codecov/codecov-action)
- [Coverage Best Practices](https://docs.codecov.com/docs/common-recipe-list)

## Support

For issues:
- Check [CodeCov Support](https://codecov.io/support)
- Review [GitHub Discussions](https://github.com/codecov/codecov-action/discussions)
- File issue in this repository

---

**Note**: CodeCov is already configured in this repository. You only need to add the `CODECOV_TOKEN` secret to enable it.
