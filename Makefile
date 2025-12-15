.PHONY: build fmt test clean elite generate scaffold

# Build the main application
build:
	go build -o bin/tokyo-ia ./cmd/main.go

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

# Run tests
test:
	go test ./...

# Clean build artifacts
clean:
	rm -rf bin/ output/
