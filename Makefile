.PHONY: build fmt test clean elite generate scaffold orchestrator build-all

# Build the main application
build:
	go build -o bin/tokyo-ia ./cmd/main.go

# Build the orchestrator agent system
orchestrator:
	go build -o bin/orchestrator ./cmd/orchestrator/main.go

# Build the elite framework CLI
elite:
	go build -o bin/elite ./cmd/elite/main.go

# Build all applications
build-all:
	@mkdir -p bin
	go build -o bin/tokyo-ia ./cmd/main.go
	go build -o bin/elite ./cmd/elite/main.go
	go build -o bin/orchestrator ./cmd/orchestrator/main.go
	go build -o bin/registry-api ./cmd/registry-api/main.go
	go build -o bin/ai-api ./cmd/ai-api/main.go
	go build -o bin/security-agent ./cmd/security-agent/main.go

# Generate a new project using the elite framework
generate:
	@if [ -z "$(IDEA)" ]; then \
		echo "Usage: make generate IDEA=\"your project description\""; \
		exit 1; \
	fi
	@mkdir -p bin
	@go build -o bin/elite ./cmd/elite/main.go
	@./bin/elite generate "$(IDEA)"

# Scaffold a project (alias for generate)
scaffold: generate

# Format Go source code
fmt:
	go fmt ./...

# Check formatting (fallará en CI si hay archivos sin formatear)
fmt-check:
	@echo "Checking gofmt..."
	@if [ -n "$$(gofmt -l .)" ]; then echo "gofmt found issues:"; gofmt -l .; exit 1; else echo "gofmt OK"; fi

# Run Go tests
test-go:
	go test ./...

# Run Python tests
test-python:
	@if [ -f requirements.txt ]; then \
		pip install -q pytest pytest-cov ruff 2>/dev/null || true; \
		pytest --cov=lib --cov-report=term-missing --cov-report=xml 2>/dev/null || echo "No Python tests found"; \
	fi

# Run all tests
test: test-go test-python

# Lint (usa golangci-lint si está instalado)
lint:
	@which golangci-lint > /dev/null || (echo "Install golangci-lint: https://golangci-lint.run/usage/install/" && exit 1)
	golangci-lint run ./...

# CI composite target
ci: fmt-check lint test-go build-all

# Clean build artifacts
clean:
	rm -rf bin/ output/
