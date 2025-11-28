.PHONY: build fmt test clean ci proto

# Build the main application
build:
	go build -o bin/tokyo-ia ./cmd/main.go

# Format Go source code and Ruby
fmt:
	go fmt ./...
	if [ -f Gemfile ]; then rubocop; fi

# Run tests
test:
	go test ./...

# Clean build artifacts
clean:
	rm -rf bin/

# Continuous Integration: format + test
ci:
	make fmt
	make test

# Generate protocol buffers if proto/ exists
proto:
	if [ -d "proto/" ]; then \
		protoc --go_out=. --ruby_out=. proto/*.proto; \
	fi
