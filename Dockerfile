# Build stage - Go
FROM golang:1.21-alpine AS go-builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache git make ca-certificates

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build binaries with optimizations
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -installsuffix cgo -ldflags="-w -s" -o /registry-api ./cmd/registry-api/main.go && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -installsuffix cgo -ldflags="-w -s" -o /tokyo-ia ./cmd/main.go && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -installsuffix cgo -ldflags="-w -s" -o /elite ./cmd/elite/main.go && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -installsuffix cgo -ldflags="-w -s" -o /ai-api ./cmd/ai-api/main.go

# Python dependencies stage
FROM python:3.11-slim AS python-base

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Go binaries from builder
COPY --from=go-builder /registry-api /usr/local/bin/registry-api
COPY --from=go-builder /tokyo-ia /usr/local/bin/tokyo-ia
COPY --from=go-builder /elite /usr/local/bin/elite
COPY --from=go-builder /ai-api /usr/local/bin/ai-api

# Copy Python packages from python-base
COPY --from=python-base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 tokyoia && \
    chown -R tokyoia:tokyoia /app

USER tokyoia

# Expose ports
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Default command - run registry API
CMD ["registry-api"]
