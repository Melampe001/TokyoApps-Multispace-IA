# ============================================================================
# Tokyo-IA Agent Container
# Multi-agent system container for Brand, UX, Bridge, and AutoDev agents
# ============================================================================

# Use official Python slim image for security and size optimization
FROM python:3.11-slim AS base

# Metadata labels
LABEL maintainer="Tokyo-IA Team"
LABEL description="Tokyo-IA Multi-Agent System"
LABEL version="1.0.0"

# ============================================================================
# Security: Non-root user
# ============================================================================
RUN adduser --disabled-password --gecos "" --uid 1000 appuser

# ============================================================================
# Build stage: Install dependencies
# ============================================================================
FROM base AS builder

# Install build dependencies (removed after build for smaller image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory for build
WORKDIR /tmp

# Copy requirements file
COPY agents/requirements.txt .

# Install Python dependencies to a specific directory
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================================================
# Runtime stage: Final image
# ============================================================================
FROM base AS runtime

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local

# Set PATH to include user-installed packages
ENV PATH=/home/appuser/.local/bin:$PATH

# Switch to non-root user
USER appuser

# Set working directory
WORKDIR /app/agents

# Copy application code with proper ownership
COPY --chown=appuser:appuser agents/ .

# Health check endpoint (adjust based on your agent's health endpoint)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Expose internal port (ClusterIP handles routing in K8s)
EXPOSE 8000

# Environment variables (can be overridden in K8s deployment)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    AGENT_ENV=production

# Default command - runs the main agent orchestrator
CMD ["python", "main.py"]