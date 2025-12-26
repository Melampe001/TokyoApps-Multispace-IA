# Pull Request Guidelines

This document outlines the standards and best practices for pull requests in TokyoApps-Multispace-IA. The auto-review bot uses these guidelines to provide feedback on your PRs.

## General Standards

### Code Quality
- **Formatting**: Code must follow language-specific formatting standards
  - Go: `gofmt` or `make fmt`
  - Python: `black` and `ruff`
  - TypeScript/JavaScript: `prettier`
- **Linting**: All linter warnings should be addressed
- **No commented-out code**: Remove dead code instead of commenting it out
- **Error handling**: Always handle errors appropriately, never ignore them
- **Logging**: Use structured logging with appropriate levels

### Naming Conventions

#### Go
- **Files**: `lowercase_snake_case.go`
- **Packages**: Short, lowercase, single-word names
- **Exported identifiers**: `PascalCase`
- **Unexported identifiers**: `camelCase`
- **Constants**: `PascalCase` or `SCREAMING_SNAKE_CASE` for public constants

#### Python
- **Files**: `lowercase_snake_case.py`
- **Modules**: Short, lowercase names
- **Classes**: `PascalCase`
- **Functions/Variables**: `lowercase_snake_case`
- **Constants**: `SCREAMING_SNAKE_CASE`

#### TypeScript/JavaScript
- **Files**: `kebab-case.ts` or `PascalCase.tsx` for components
- **Classes/Components**: `PascalCase`
- **Functions/Variables**: `camelCase`
- **Constants**: `SCREAMING_SNAKE_CASE`

### File Structure

#### Go Files
```go
// Package comment
package packagename

import (
    // Standard library
    "fmt"
    "os"
    
    // External packages
    "github.com/external/pkg"
    
    // Internal packages
    "github.com/Melampe001/TokyoApps-Multispace-IA/internal/module"
)

// Constants
const (
    DefaultTimeout = 30 * time.Second
)

// Types
type MyStruct struct {
    Field string
}

// Functions
func NewMyStruct() *MyStruct { ... }
```

#### Python Files
```python
"""Module docstring describing purpose."""

# Standard library imports
import os
import sys

# Third-party imports
import requests

# Local imports
from lib.utils import helper_function

# Constants
MAX_RETRIES = 3

# Classes
class MyClass:
    """Class docstring."""
    
    def __init__(self):
        """Initialize the class."""
        pass
```

### Testing Requirements

- **Unit Tests**: All new functions/methods should have unit tests
- **Test Coverage**: Aim for >70% coverage for new code
- **Test Files**: 
  - Go: `*_test.go` in the same package
  - Python: `test_*.py` in `testing/` or same directory
- **Test Names**: Descriptive names that explain what is being tested
- **Table-Driven Tests**: Use for multiple test cases (Go)

### Security Best Practices

#### Never Commit Secrets
- ❌ No API keys, tokens, passwords in code
- ✅ Use environment variables
- ✅ Reference secrets in documentation
- ✅ Use `.env.example` for templates

#### Input Validation
- Always validate and sanitize user input
- Use parameterized queries for databases
- Escape output to prevent XSS

#### Dependencies
- Keep dependencies up to date
- Review security advisories
- Use `go mod tidy`, `pip check`

### Documentation

#### Code Comments
- **When to comment**:
  - Complex algorithms
  - Non-obvious business logic
  - Public APIs
  - Workarounds or hacks
- **When NOT to comment**:
  - Obvious code that explains itself
  - Redundant descriptions of what code does

#### Docstrings/Godoc
- **Go**: Package and exported function comments
```go
// ProcessData processes the input data and returns results.
// It returns an error if the data is invalid.
func ProcessData(data []byte) ([]Result, error) {
```

- **Python**: Module, class, and function docstrings
```python
def process_data(data: bytes) -> list[Result]:
    """Process the input data and return results.
    
    Args:
        data: Raw input data as bytes
        
    Returns:
        List of processed results
        
    Raises:
        ValueError: If data is invalid
    """
```

### PR Description Requirements

Your PR description should include:

1. **What**: Brief summary of changes
2. **Why**: Reason for the changes
3. **How**: Implementation approach (if complex)
4. **Testing**: How you tested the changes
5. **Related Issues**: Link to related issues
6. **Screenshots**: For UI changes
7. **Breaking Changes**: Clearly marked if applicable

### Commit Message Format

```
type(scope): brief description

Longer description if needed, explaining why the change was made.

Fixes #123
Relates to #456
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`

### Size Guidelines

- **Small PRs are better**: Aim for <300 lines changed
- **One concern per PR**: Don't mix unrelated changes
- **Break up large features**: Use feature flags or separate PRs

### Performance Considerations

- **Avoid premature optimization**: Optimize only when needed
- **Benchmark performance-critical code**: Use Go benchmarks or Python profiling
- **Consider memory allocations**: Especially in hot paths
- **Use appropriate data structures**: Choose based on access patterns

### Code Review Checklist

Before submitting your PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New code has appropriate test coverage
- [ ] Documentation is updated
- [ ] No secrets or sensitive data committed
- [ ] Linters pass without errors
- [ ] Breaking changes are clearly documented
- [ ] Performance impact is considered
- [ ] Error handling is appropriate
- [ ] Logging is meaningful and at correct level

### Anti-Patterns to Avoid

#### Go
- ❌ Ignoring errors: `result, _ := doSomething()`
- ❌ Not closing resources
- ❌ Premature channel closing
- ❌ Mutex copies
- ❌ Unused parameters in interfaces

#### Python
- ❌ Bare `except:` clauses
- ❌ Mutable default arguments
- ❌ Using `*` imports
- ❌ Not using context managers for resources
- ❌ Catching too broad exceptions

#### General
- ❌ God objects/functions (too much responsibility)
- ❌ Magic numbers (use named constants)
- ❌ Deeply nested logic (refactor into smaller functions)
- ❌ Duplicate code (DRY principle)

## Auto-Review Bot

The auto-review bot will check for:

1. **File naming**: Matches conventions
2. **Import organization**: Properly grouped
3. **Function length**: Warns if >100 lines
4. **Cyclomatic complexity**: Flags overly complex functions
5. **Security patterns**: Detects common security issues
6. **Error handling**: Ensures errors aren't ignored
7. **Test coverage**: Validates test presence
8. **Documentation**: Checks for docstrings/comments

The bot provides:
- ✅ Approval for well-structured PRs
- 💬 Constructive comments on improvements
- ⚠️ Warnings for potential issues
- ❌ Request changes for serious problems

## Getting Help

If you're unsure about any guideline:
- Check existing code for examples
- Ask in the PR comments
- Review documentation in `docs/`
- Consult with maintainers

Thank you for following these guidelines and contributing to TokyoApps-Multispace-IA! 🎉
