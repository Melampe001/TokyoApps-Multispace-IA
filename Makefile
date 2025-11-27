.PHONY: build fmt test clean

# Build the main application
build:
	go build -o bin/tokyo-ia ./cmd/main.go

# Format Go source code
fmt:
	go fmt ./...

# Run tests
test:
	go test ./...

# Clean build artifacts
clean:
	rm -rf bin/
