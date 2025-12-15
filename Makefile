# ==============================================================================
# Elite Framework Makefile
# ==============================================================================
# Quick reference: make help
# ==============================================================================

.PHONY: help build fmt test test-coverage test-html lint ci clean proto docker-build docker-run deploy scaffold install-tools

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# Project variables
PROJECT_NAME := tokyo-ia
BINARY_NAME := bin/$(PROJECT_NAME)
DOCKER_IMAGE := $(PROJECT_NAME):latest
GO_VERSION := 1.24.10

# Default target
.DEFAULT_GOAL := help

# ------------------------------------------------------------------------------
# Help
# ------------------------------------------------------------------------------
help: ## Show this help message
	@echo "$(BLUE)==============================================================================$(NC)"
	@echo "$(GREEN)Tokyo-IA Elite Framework - Available Commands$(NC)"
	@echo "$(BLUE)==============================================================================$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BLUE)==============================================================================$(NC)"

# ------------------------------------------------------------------------------
# Build
# ------------------------------------------------------------------------------
build: ## Build the main application
	@echo "$(GREEN)Building $(PROJECT_NAME)...$(NC)"
	@go build -o $(BINARY_NAME) ./cmd/main.go
	@echo "$(GREEN)✓ Build complete: $(BINARY_NAME)$(NC)"

build-all: ## Build for all platforms (Linux, macOS, Windows)
	@echo "$(GREEN)Building for all platforms...$(NC)"
	@GOOS=linux GOARCH=amd64 go build -o bin/$(PROJECT_NAME)-linux-amd64 ./cmd/main.go
	@GOOS=darwin GOARCH=amd64 go build -o bin/$(PROJECT_NAME)-darwin-amd64 ./cmd/main.go
	@GOOS=windows GOARCH=amd64 go build -o bin/$(PROJECT_NAME)-windows-amd64.exe ./cmd/main.go
	@echo "$(GREEN)✓ Multi-platform build complete$(NC)"

run: build ## Build and run the application
	@echo "$(GREEN)Running $(PROJECT_NAME)...$(NC)"
	@./$(BINARY_NAME)

# ------------------------------------------------------------------------------
# Formatting
# ------------------------------------------------------------------------------
fmt: ## Format Go source code
	@echo "$(GREEN)Formatting Go code...$(NC)"
	@go fmt ./...
	@echo "$(GREEN)✓ Formatting complete$(NC)"

fmt-check: ## Check if code is formatted
	@echo "$(YELLOW)Checking code format...$(NC)"
	@test -z "$$(gofmt -l .)" || (echo "$(RED)✗ Code is not formatted. Run 'make fmt'$(NC)" && exit 1)
	@echo "$(GREEN)✓ Code is properly formatted$(NC)"

# ------------------------------------------------------------------------------
# Testing
# ------------------------------------------------------------------------------
test: ## Run tests
	@echo "$(GREEN)Running tests...$(NC)"
	@go test ./... -v -race
	@echo "$(GREEN)✓ Tests complete$(NC)"

test-coverage: ## Run tests with coverage
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	@go test ./... -race -coverprofile=coverage.out -covermode=atomic
	@go tool cover -func=coverage.out
	@echo "$(GREEN)✓ Coverage analysis complete$(NC)"

test-html: test-coverage ## Generate HTML coverage report
	@echo "$(GREEN)Generating HTML coverage report...$(NC)"
	@go tool cover -html=coverage.out -o coverage.html
	@echo "$(GREEN)✓ Coverage report: coverage.html$(NC)"

test-short: ## Run short tests only
	@echo "$(GREEN)Running short tests...$(NC)"
	@go test ./... -short
	@echo "$(GREEN)✓ Short tests complete$(NC)"

test-verbose: ## Run tests with verbose output
	@echo "$(GREEN)Running verbose tests...$(NC)"
	@go test ./... -v -race -coverprofile=coverage.out
	@echo "$(GREEN)✓ Verbose tests complete$(NC)"

benchmark: ## Run benchmarks
	@echo "$(GREEN)Running benchmarks...$(NC)"
	@go test ./... -bench=. -benchmem
	@echo "$(GREEN)✓ Benchmarks complete$(NC)"

# ------------------------------------------------------------------------------
# Linting
# ------------------------------------------------------------------------------
lint: ## Run linter (golangci-lint)
	@echo "$(GREEN)Running linter...$(NC)"
	@if command -v golangci-lint >/dev/null 2>&1; then \
		golangci-lint run ./...; \
		echo "$(GREEN)✓ Linting complete$(NC)"; \
	else \
		echo "$(YELLOW)golangci-lint not installed. Run 'make install-tools'$(NC)"; \
		go vet ./...; \
	fi

vet: ## Run go vet
	@echo "$(GREEN)Running go vet...$(NC)"
	@go vet ./...
	@echo "$(GREEN)✓ Vet complete$(NC)"

# ------------------------------------------------------------------------------
# CI/CD
# ------------------------------------------------------------------------------
ci: fmt-check lint test-coverage ## Run full CI pipeline locally
	@echo "$(GREEN)✓ CI pipeline complete$(NC)"

ci-quick: fmt-check vet test-short ## Run quick CI checks
	@echo "$(GREEN)✓ Quick CI checks complete$(NC)"

# ------------------------------------------------------------------------------
# Dependencies
# ------------------------------------------------------------------------------
deps: ## Download dependencies
	@echo "$(GREEN)Downloading dependencies...$(NC)"
	@go mod download
	@echo "$(GREEN)✓ Dependencies downloaded$(NC)"

deps-tidy: ## Tidy dependencies
	@echo "$(GREEN)Tidying dependencies...$(NC)"
	@go mod tidy
	@echo "$(GREEN)✓ Dependencies tidied$(NC)"

deps-verify: ## Verify dependencies
	@echo "$(GREEN)Verifying dependencies...$(NC)"
	@go mod verify
	@echo "$(GREEN)✓ Dependencies verified$(NC)"

deps-update: ## Update all dependencies
	@echo "$(GREEN)Updating dependencies...$(NC)"
	@go get -u ./...
	@go mod tidy
	@echo "$(GREEN)✓ Dependencies updated$(NC)"

# ------------------------------------------------------------------------------
# Clean
# ------------------------------------------------------------------------------
clean: ## Clean build artifacts
	@echo "$(YELLOW)Cleaning build artifacts...$(NC)"
	@rm -rf bin/
	@rm -f coverage.out coverage.html
	@echo "$(GREEN)✓ Clean complete$(NC)"

clean-all: clean ## Clean all generated files
	@echo "$(YELLOW)Cleaning all generated files...$(NC)"
	@rm -rf vendor/
	@rm -rf tmp/
	@find . -type f -name '*.test' -delete
	@echo "$(GREEN)✓ Deep clean complete$(NC)"

# ------------------------------------------------------------------------------
# Protocol Buffers (if using gRPC)
# ------------------------------------------------------------------------------
proto: ## Generate protobuf files
	@echo "$(GREEN)Generating protobuf files...$(NC)"
	@if [ -d "proto" ]; then \
		protoc --go_out=. --go_opt=paths=source_relative \
		       --go-grpc_out=. --go-grpc_opt=paths=source_relative \
		       proto/*.proto; \
		echo "$(GREEN)✓ Protobuf generation complete$(NC)"; \
	else \
		echo "$(YELLOW)No proto directory found$(NC)"; \
	fi

# ------------------------------------------------------------------------------
# Docker
# ------------------------------------------------------------------------------
docker-build: ## Build Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	@docker build -t $(DOCKER_IMAGE) .
	@echo "$(GREEN)✓ Docker image built: $(DOCKER_IMAGE)$(NC)"

docker-run: ## Run Docker container
	@echo "$(GREEN)Running Docker container...$(NC)"
	@docker run -p 8080:8080 --env-file .env $(DOCKER_IMAGE)

docker-push: docker-build ## Push Docker image to registry
	@echo "$(GREEN)Pushing Docker image...$(NC)"
	@docker push $(DOCKER_IMAGE)
	@echo "$(GREEN)✓ Docker image pushed$(NC)"

docker-clean: ## Remove Docker images and containers
	@echo "$(YELLOW)Cleaning Docker artifacts...$(NC)"
	@docker rmi $(DOCKER_IMAGE) 2>/dev/null || true
	@echo "$(GREEN)✓ Docker cleanup complete$(NC)"

# ------------------------------------------------------------------------------
# Deployment
# ------------------------------------------------------------------------------
deploy: ## Deploy to production (placeholder - customize for your setup)
	@echo "$(YELLOW)Deploying to production...$(NC)"
	@echo "$(RED)⚠ Implement your deployment strategy here$(NC)"
	@echo "$(BLUE)Examples:$(NC)"
	@echo "  - kubectl apply -f k8s/"
	@echo "  - vercel deploy --prod"
	@echo "  - railway up"

deploy-staging: ## Deploy to staging
	@echo "$(YELLOW)Deploying to staging...$(NC)"
	@echo "$(RED)⚠ Implement your staging deployment here$(NC)"

# ------------------------------------------------------------------------------
# Project Generation (Elite Framework)
# ------------------------------------------------------------------------------
scaffold: ## Interactive project generator
	@echo "$(BLUE)==============================================================================$(NC)"
	@echo "$(GREEN)Elite Framework - Project Generator$(NC)"
	@echo "$(BLUE)==============================================================================$(NC)"
	@if [ -f "scripts/generate-project.sh" ]; then \
		./scripts/generate-project.sh; \
	else \
		echo "$(RED)✗ scripts/generate-project.sh not found$(NC)"; \
		echo "$(YELLOW)Creating scripts directory and script...$(NC)"; \
		mkdir -p scripts; \
		echo "$(YELLOW)Please run 'make scaffold' again after setup is complete$(NC)"; \
	fi

# ------------------------------------------------------------------------------
# Development Tools
# ------------------------------------------------------------------------------
install-tools: ## Install development tools
	@echo "$(GREEN)Installing development tools...$(NC)"
	@echo "$(BLUE)Installing golangci-lint...$(NC)"
	@go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
	@echo "$(BLUE)Installing gofumpt...$(NC)"
	@go install mvdan.cc/gofumpt@latest
	@echo "$(BLUE)Installing gotestsum...$(NC)"
	@go install gotest.tools/gotestsum@latest
	@echo "$(GREEN)✓ Tools installed$(NC)"

tools-update: ## Update development tools
	@echo "$(GREEN)Updating development tools...$(NC)"
	@$(MAKE) install-tools
	@echo "$(GREEN)✓ Tools updated$(NC)"

# ------------------------------------------------------------------------------
# Git Hooks
# ------------------------------------------------------------------------------
hooks: ## Install git hooks
	@echo "$(GREEN)Installing git hooks...$(NC)"
	@echo "#!/bin/sh\nmake ci-quick" > .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo "$(GREEN)✓ Git hooks installed$(NC)"

# ------------------------------------------------------------------------------
# Security
# ------------------------------------------------------------------------------
security-scan: ## Run security vulnerability scan
	@echo "$(GREEN)Running security scan...$(NC)"
	@if command -v gosec >/dev/null 2>&1; then \
		gosec ./...; \
	else \
		echo "$(YELLOW)gosec not installed. Installing...$(NC)"; \
		go install github.com/securego/gosec/v2/cmd/gosec@latest; \
		gosec ./...; \
	fi
	@echo "$(GREEN)✓ Security scan complete$(NC)"

# ------------------------------------------------------------------------------
# Documentation
# ------------------------------------------------------------------------------
docs: ## Generate documentation
	@echo "$(GREEN)Generating documentation...$(NC)"
	@if command -v godoc >/dev/null 2>&1; then \
		echo "$(BLUE)Starting godoc server at http://localhost:6060$(NC)"; \
		godoc -http=:6060; \
	else \
		echo "$(YELLOW)godoc not installed$(NC)"; \
		echo "$(BLUE)Install with: go install golang.org/x/tools/cmd/godoc@latest$(NC)"; \
	fi

# ------------------------------------------------------------------------------
# Version Management
# ------------------------------------------------------------------------------
version: ## Show version information
	@echo "$(BLUE)Project: $(PROJECT_NAME)$(NC)"
	@echo "$(BLUE)Go version: $(GO_VERSION)$(NC)"
	@go version

# ==============================================================================
# End of Makefile
# ==============================================================================
