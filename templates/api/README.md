# REST API Template

Production-ready REST API template with Go, Gin framework, PostgreSQL, and JWT authentication.

## Features

- ✅ RESTful API with Gin framework
- ✅ PostgreSQL database with GORM
- ✅ JWT authentication
- ✅ Request validation
- ✅ Error handling middleware
- ✅ Rate limiting
- ✅ CORS support
- ✅ Swagger/OpenAPI documentation
- ✅ Docker support
- ✅ Comprehensive tests

## Quick Start

```bash
# Install dependencies
make deps

# Run database migrations
make migrate

# Start server
make run
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token

### Users
- `GET /api/v1/users` - List users (requires auth)
- `GET /api/v1/users/:id` - Get user (requires auth)
- `PUT /api/v1/users/:id` - Update user (requires auth)
- `DELETE /api/v1/users/:id` - Delete user (requires auth)

### Health
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Server
PORT=8080
HOST=localhost

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/apidb

# JWT
JWT_SECRET=your-secret-key
JWT_EXPIRES_IN=24h

# Redis (for rate limiting)
REDIS_URL=redis://localhost:6379
```

## Development

```bash
# Run tests
make test

# Run with coverage
make test-coverage

# Lint code
make lint

# Format code
make fmt
```

## Deployment

### Docker

```bash
# Build image
make docker-build

# Run container
make docker-run
```

### Kubernetes

```bash
# Apply manifests
kubectl apply -f deploy/k8s/
```

## API Documentation

API documentation is available at:
- Swagger UI: `http://localhost:8080/swagger/index.html`
- OpenAPI spec: `http://localhost:8080/swagger/doc.json`

## Architecture

```
api-template/
├── cmd/
│   └── main.go              # Entry point
├── internal/
│   ├── handlers/            # HTTP handlers
│   │   ├── auth.go
│   │   ├── user.go
│   │   └── health.go
│   ├── models/              # Data models
│   │   ├── user.go
│   │   └── token.go
│   ├── services/            # Business logic
│   │   ├── auth.go
│   │   └── user.go
│   ├── repository/          # Database layer
│   │   └── user.go
│   └── middleware/          # Middleware
│       ├── auth.go
│       ├── cors.go
│       └── ratelimit.go
├── tests/                   # Tests
│   ├── integration/
│   └── unit/
├── docs/                    # Documentation
└── deploy/                  # Deployment configs
    ├── Dockerfile
    └── k8s/
```

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Rate limiting per IP
- CORS configuration
- Input validation
- SQL injection prevention (parameterized queries)
- XSS protection

## Performance

- Connection pooling
- Database indexing
- Redis caching
- Gzip compression
- Request timeout handling

## Monitoring

- Structured logging (JSON)
- Prometheus metrics
- Health check endpoint
- Error tracking

## License

MIT License

---

Generated with Tokyo-IA Elite Framework
