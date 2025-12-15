.PHONY: build fmt test clean elite generate scaffold ai-build ai-test ai-run ai-demo

# Build the main application
build:
	go build -o bin/tokyo-ia ./cmd/main.go

# Format Go source code (aplica gofmt)
# Build the elite framework CLI
elite:
	go build -o bin/elite ./cmd/elite/main.go

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

# Run tests
test:
	go test ./...

# Lint (usa golangci-lint si está instalado)
lint:
	@which golangci-lint > /dev/null || (echo "Install golangci-lint: https://golangci-lint.run/usage/install/" && exit 1)
	golangci-lint run ./...

# CI composite target
ci: fmt-check lint test build

# Clean build artifacts
clean:
	rm -rf bin/ output/

# AI-specific targets
ai-build:
	@echo "Building AI API..."
	go build -o bin/ai-api cmd/ai-api/main.go
	@echo "✓ AI API built successfully"

ai-test:
	@echo "Running Go AI tests..."
	go test ./internal/ai/... -v
	@echo ""
	@echo "Running Python AI tests..."
	python -m pytest lib/agents/test_tools.py -v

ai-run:
	@echo "Starting AI API server..."
	@echo "Endpoints:"
	@echo "  - POST http://localhost:8080/ai/complete    - AI completion"
	@echo "  - GET  http://localhost:8080/ai/metrics     - Metrics"
	@echo "  - POST http://localhost:8080/ai/cache/clear - Clear cache"
	@echo "  - GET  http://localhost:8080/health         - Health check"
	@echo ""
	./bin/ai-api

ai-demo:
	@echo "Running AI integration demo..."
	./scripts/demo-ai-integration.sh
