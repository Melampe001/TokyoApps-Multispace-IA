.PHONY: build fmt fmt-check test lint ci clean

# Build the main application
build:
	go build -o bin/tokyo-ia ./cmd/main.go

# Format Go source code (aplica gofmt)
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
	rm -rf bin/
