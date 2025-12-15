# Copilot Instructions for Tokyo-IA

## Project Overview

Tokyo-IA is a Go-based project that provides Tokyo-themed AI features. The project is structured as a standard Go application with modular packages.

**Note**: The repository documentation references future Android, Web, and MCP Server components that are planned but not yet implemented. Focus on the existing Go codebase.

## Repository Structure

```
tokyoia/
├── cmd/                    # Application entry points
│   └── main.go            # Main application
├── internal/              # Internal packages (not importable by external projects)
│   └── hello.go           # Core internal functionality
├── lib/                   # Shared library code
├── admin/                 # Admin functionality
├── config/                # Configuration packages
├── proto/                 # Protocol buffer definitions
├── testing/               # Test files
├── prompts/               # AI/LLM prompt templates
├── docs/                  # Documentation
└── .github/               # GitHub workflows and configuration
```

## Build and Test Commands

### Build
```bash
make build                 # Build the application (output: bin/tokyo-ia)
# OR
go build -o bin/tokyo-ia ./cmd/main.go
```

### Format
```bash
make fmt                   # Format all Go source code
# OR
go fmt ./...
```

### Test
```bash
make test                  # Run all tests
# OR
go test ./...
```

### Clean
```bash
make clean                 # Remove build artifacts
```

### Run
```bash
./bin/tokyo-ia            # Run the built application
# OR
go run ./cmd/main.go      # Run directly without building
```

## Coding Standards

### Go Style Guidelines
- Follow the [Effective Go](https://go.dev/doc/effective_go) guidelines
- Follow the [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- Use `gofmt` or `make fmt` to format all Go code before committing
- Write clear, self-documenting code with meaningful variable and function names
- Keep functions small and focused on a single responsibility
- Add comments only when the code logic is complex or non-obvious
- Use Go idioms:
  - Prefer early returns over nested if statements
  - Use descriptive error messages with context
  - Follow the standard package layout conventions
  - Export only what needs to be public (capitalize for exports)

### Package Organization
- Place main applications in `cmd/` directory
- Use `internal/` for packages that should not be imported by external projects
- Shared library code goes in `lib/` or as top-level packages
- Keep package-level documentation in doc.go files when appropriate

### Error Handling
- Always check and handle errors explicitly
- Provide context in error messages
- Use error wrapping when appropriate: `fmt.Errorf("context: %w", err)`

### Testing
- Place test files alongside the code they test (e.g., `hello_test.go` for `hello.go`)
- Use table-driven tests for multiple test cases
- Use meaningful test names that describe what is being tested
- Aim for high test coverage of critical paths

## Security Guidelines

**CRITICAL: Never commit secrets to the repository.**

- Do NOT store API keys, private keys, credentials, or other secrets in the repository
- Use environment variables for sensitive configuration
- Use GitHub Actions Secrets for CI/CD credentials
- If any secret was ever committed:
  1. Rotate the exposed credential immediately
  2. Remove the secret from the repository and history (use tools like `git filter-branch` or BFG Repo-Cleaner)
  3. Notify collaborators

### Go Security Best Practices
- Validate and sanitize all user inputs
- Use parameterized queries if working with databases
- Keep dependencies up to date (use `go get -u` cautiously)
- Use `go vet` to catch common mistakes
- Consider using security scanning tools like `gosec`

## Testing Requirements

- Write unit tests for new functionality
- Place test files alongside source files with `_test.go` suffix
- Use table-driven tests for testing multiple scenarios
- Ensure existing tests pass before submitting changes: `make test` or `go test ./...`
- Write tests that are:
  - **Fast**: Unit tests should run quickly
  - **Isolated**: Tests should not depend on external services or each other
  - **Repeatable**: Tests should produce the same results every time
  - **Self-checking**: Use assertions, don't rely on manual inspection
  
### Test Structure
```go
func TestFunctionName(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    string
        wantErr bool
    }{
        {"description", "input", "expected", false},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // test implementation
        })
    }
}
```

## Task Guidelines

### Ideal Tasks for Copilot
- Bug fixes with clear reproduction steps and expected behavior
- Adding new features with well-defined requirements
- Writing or updating tests
- Documentation improvements (inline comments, README updates, package docs)
- Code refactoring with clear objectives (performance, readability, maintainability)
- Adding new packages or modules following Go conventions
- Implementing standard interfaces or patterns
- Adding CLI flags or configuration options

### Tasks Requiring Human Review
- Security-sensitive changes (authentication, encryption, credential handling)
- Changes to CI/CD workflows (`.github/workflows/`)
- Significant architectural changes
- Changes affecting the public API of packages
- Performance-critical code sections
- Changes involving external service integrations

### Best Practices When Working with Copilot
- Provide clear, specific issue descriptions with:
  - What needs to be done
  - Why it's needed
  - Expected behavior or outcome
  - Any relevant context or constraints
- Include relevant file paths when possible
- Reference related issues or PRs if applicable
- For bugs, include reproduction steps and error messages

## Pull Request Guidelines

- Keep PRs focused on a single issue or feature
- Write clear PR descriptions explaining:
  - What changed and why
  - How to test the changes
  - Any breaking changes or migration notes
- Reference related issues using keywords (e.g., "Closes #123", "Fixes #456")
- Include test coverage for new code
- Ensure all checks pass before requesting review:
  - `make test` - All tests pass
  - `make fmt` - Code is properly formatted
  - `go vet ./...` - No common mistakes detected
- Keep commits atomic and well-described
- Address review feedback promptly
- Update documentation if the PR changes behavior or adds features

## Development Workflow

### Initial Setup
```bash
# Clone the repository
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA

# Verify Go installation (requires Go 1.24+)
go version

# Download dependencies
go mod download

# Build the project
make build

# Run tests
make test
```

### Making Changes
```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes, commit frequently
git add .
git commit -m "feat: descriptive message"

# Format code before committing
make fmt

# Run tests
make test

# Push to your fork or branch
git push origin feature/your-feature-name
```

## Common Commands Reference

| Command | Description |
|---------|-------------|
| `make build` | Build the application |
| `make test` | Run all tests |
| `make fmt` | Format all Go code |
| `make clean` | Remove build artifacts |
| `go run ./cmd/main.go` | Run without building |
| `go test -v ./...` | Run tests with verbose output |
| `go test -cover ./...` | Run tests with coverage |
| `go mod tidy` | Clean up dependencies |
| `go vet ./...` | Run Go vet for common mistakes |

## Project-Specific Notes

- This is a Go 1.24+ project - ensure your Go version is compatible
- The project uses a standard Go layout with `cmd/` for executables and `internal/` for private packages
- Protocol buffer definitions are in `proto/` directory
- AI/LLM prompt templates are stored in `prompts/` for reference
- The project is in early development - some features are planned but not yet implemented

## Resources

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Project Contributing Guide](../CONTRIBUTING.md)
- [Security Policy](../SECURITY.md)
