# API Template

This template generates a REST/GraphQL API using Go.

## Features

- Go 1.21+
- Gin web framework
- GORM for database operations
- PostgreSQL support
- Swagger documentation
- Clean architecture

## Structure

```
api-project/
├── cmd/
│   └── api/          # Application entry point
├── internal/
│   ├── handler/      # HTTP handlers
│   ├── service/      # Business logic
│   └── repository/   # Data access layer
├── api/              # API definitions
├── models/           # Data models
├── config/           # Configuration
├── tests/
│   ├── unit/         # Unit tests
│   └── integration/  # Integration tests
└── deploy/           # Deployment configs
```

## Generated Files

- `cmd/api/main.go` - Application entry point
- `go.mod` - Go module definition
- `Dockerfile` - Multi-stage container build
- `docker-compose.yml` - Local development setup
- `.github/workflows/ci.yml` - CI/CD pipeline

## Next Steps

1. Install dependencies: `go mod download`
2. Run the API: `go run cmd/api/main.go`
3. Run tests: `go test ./...`
4. Build: `go build ./cmd/api`
5. Access API: `http://localhost:8080`
