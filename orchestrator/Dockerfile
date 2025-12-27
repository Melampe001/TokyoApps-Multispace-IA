# ============================================================================
# Tokyo-IA Orchestrator Container
# Node.js orchestrator for multi-agent workflow coordination
# ============================================================================

# Use official Node.js slim image for security and size optimization
FROM node:20-slim AS base

# Metadata labels
LABEL maintainer="Tokyo-IA Team"
LABEL description="Tokyo-IA Agent Orchestrator"
LABEL version="1.0.0"

# ============================================================================
# Security: Non-root user
# ============================================================================
RUN adduser --disabled-password --gecos "" --uid 1001 appuser

# ============================================================================
# Build stage: Install dependencies
# ============================================================================
FROM base AS builder

# Set working directory
WORKDIR /tmp

# Copy package files
COPY orchestrator/package*.json ./

# Install dependencies (including devDependencies for build)
RUN npm ci

# ============================================================================
# Runtime stage: Final image
# ============================================================================
FROM base AS runtime

# Switch to non-root user
USER appuser

# Set working directory
WORKDIR /app/orchestrator

# Copy package files and install production dependencies
COPY --chown=appuser:appuser orchestrator/package*.json ./
RUN npm ci --production --ignore-scripts

# Copy application code with proper ownership
COPY --chown=appuser:appuser orchestrator/ .

# Health check endpoint (adjust path based on your implementation)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))" || exit 1

# Expose orchestrator port
EXPOSE 3000

# Environment variables (can be overridden in K8s deployment)
ENV NODE_ENV=production \
    PORT=3000 \
    LOG_LEVEL=info

# Default command - runs the orchestrator
CMD ["node", "index.js"]