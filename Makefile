.PHONY: build fmt test test-agents clean

# Build the main application
build:
	go build -o bin/tokyo-ia ./cmd/main.go

# Format Go source code
fmt:
	go fmt ./...

# Run all tests (includes agents)
test:
	go test ./...

# Run agents tests only
test-agents:
	go test ./agents/... -v

# Clean build artifacts
clean:
	rm -rf bin/
