.PHONY: build fmt verify-fmt lint test ci clean

# Build the main application (all cmd packages)
build:
	go build -o bin/tokyo-ia ./cmd/...

# Format Go source code in-place (use before committing)
fmt:
	gofmt -s -w .

# Verify formatting (use in CI to fail if repo is not formatted)
verify-fmt:
	@set -e; \
	files="$$(gofmt -l .)"; \
	if [ -n "$${files}" ]; then \
	  echo "The following files are not formatted:"; \
	  echo "$${files}"; \
	  exit 1; \
	else \
	  echo "All files formatted"; \
	fi

# Run linters (expects golangci-lint to be installed)
lint:
	@command -v golangci-lint >/dev/null 2>&1 || { \
	  echo "golangci-lint not found; install from https://github.com/golangci/golangci-lint/releases"; \
	  exit 1; \
	}
	golangci-lint run ./...

# Run tests (verbose)
test:
	go test ./... -v

# CI: verify formatting, lint, test and then build
ci: verify-fmt lint test build

# Clean build artifacts
clean:
	rm -rf bin/