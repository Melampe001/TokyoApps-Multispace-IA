# Dependency Policy

This document describes the dependency management policy for the Tokyo-IA project's Flutter components.

## Overview

To maintain security, minimize attack surface, and ensure code quality, this project enforces **strict dependency control** for Flutter applications.

## Dependency Agent

The Dependency Agent is an automated system that validates all dependencies in `pubspec.yaml` files. It ensures that only authorized dependencies are used in the project.

## Allowed Dependencies

Only the following dependencies are permitted:

| Dependency | Purpose | Status |
|------------|---------|--------|
| `flutter_riverpod` | State management | ✅ Authorized |
| `shared_preferences` | Local storage | ✅ Authorized |
| `path_provider` | File system paths | ✅ Authorized |

### SDK Dependencies

The following SDK dependencies are always allowed:
- `flutter` - The Flutter SDK itself

## Policy Rules

### 🔒 Security Rules

1. **Unauthorized dependencies → FAIL**: Any dependency not in the allowed list will cause the build to fail
2. **Manual review required**: All new dependency requests must be reviewed and approved by the security team
3. **Zero tolerance**: There are no exceptions to this policy without prior approval

### ⚙️ How It Works

The Dependency Agent automatically:
1. Scans `pubspec.yaml` when changes are made
2. Compares dependencies against the allowed list
3. Reports violations with detailed information
4. Blocks merging of PRs with unauthorized dependencies

## Validation Script

The validation is performed by the script:
```
.github/workflows/bots/scripts/check_dependencies.py
```

### Running Locally

You can validate dependencies locally before committing:

```bash
# From repository root
python3 .github/workflows/bots/scripts/check_dependencies.py
```

### Example Output

**✅ Success:**
```
======================================================================
🔒 DEPENDENCY AGENT - Security Check Report
======================================================================

📦 Package: tokyo_ia
📊 Total dependencies found: 3

✅ Allowed dependencies:
   - flutter_riverpod
   - path_provider
   - shared_preferences

✅ PASS - All dependencies are authorized

📋 Found dependencies:
   ✓ flutter_riverpod
   ✓ shared_preferences
   ✓ path_provider

======================================================================
```

**❌ Failure:**
```
======================================================================
🔒 DEPENDENCY AGENT - Security Check Report
======================================================================

📦 Package: tokyo_ia_test
📊 Total dependencies found: 5

✅ Allowed dependencies:
   - flutter_riverpod
   - path_provider
   - shared_preferences

❌ FAIL - Unauthorized dependencies detected!

🚨 Violations (2):
   1. Dependency 'http' is not in the allowed list
   2. Dependency 'firebase_core' is not in the allowed list

📋 Current dependencies:
   - flutter (SDK)
   ✓ flutter_riverpod (allowed)
   ✓ shared_preferences (allowed)
   ✓ path_provider (allowed)
   ✗ http (BLOCKED)
   ✗ firebase_core (BLOCKED)

======================================================================
```

## GitHub Workflow

The Dependency Agent runs automatically via GitHub Actions:

- **Workflow**: `.github/workflows/dependency-agent.yml`
- **Triggers**:
  - Pull requests modifying `pubspec.yaml`
  - Pushes to `main`/`master` branch
  - Manual workflow dispatch

### PR Comments

The agent will post comments on pull requests:
- ✅ Success comment when all dependencies are authorized
- ❌ Failure comment with details about violations
- 🏷️ Automatic labels: `dependencies`, `flutter`, `security`, `needs-changes`

## Requesting New Dependencies

If you need to add a new dependency:

1. **Create an issue** describing:
   - The dependency name and purpose
   - Why it's necessary
   - Alternatives considered
   - Security implications

2. **Wait for approval** from:
   - Security team review
   - Architecture team review
   - Project maintainer approval

3. **Update the policy** (if approved):
   - Add dependency to allowed list in `check_dependencies.py`
   - Update this README
   - Update the workflow documentation

## Testing

Unit tests for the Dependency Agent:
```bash
# Run tests
python3 -m unittest testing.dependency_agent.test_dependency_checker -v
```

Test coverage includes:
- Valid dependency combinations
- Invalid/unauthorized dependencies
- Edge cases (empty dependencies, SDK-only, etc.)
- YAML parsing errors
- Mixed valid/invalid scenarios

## Benefits

This strict dependency policy provides:

- 🔒 **Enhanced Security**: Reduced attack surface
- 📦 **Smaller APKs**: Fewer dependencies = smaller app size
- 🚀 **Better Performance**: Less code to load and execute
- 🛠️ **Easier Maintenance**: Simpler dependency tree
- 📊 **Quality Control**: Every dependency is intentional

## Troubleshooting

### My PR is blocked by the Dependency Agent

1. Check the agent's comment for specific violations
2. Remove unauthorized dependencies from `pubspec.yaml`
3. Use only allowed dependencies
4. If you need a new dependency, follow the request process above

### The check is failing but shouldn't be

1. Verify your `pubspec.yaml` syntax is correct
2. Ensure you're only using dependencies from the allowed list
3. Check that SDK dependencies use the correct format
4. Run the validation script locally to debug

### How to override for urgent needs

**There is no override mechanism.** This is by design. All dependencies must go through the approval process to maintain security standards.

## Contact

For questions or dependency requests:
- Open an issue with the `dependencies` label
- Contact the security team
- Refer to [SECURITY.md](../SECURITY.md)

---

*This policy is enforced automatically and applies to all branches and contributors.*
