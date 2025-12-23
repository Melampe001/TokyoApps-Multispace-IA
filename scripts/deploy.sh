#!/bin/bash
set -e

echo "🚀 Tokyo-IA Deployment Script"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
info() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }
section() { echo -e "\n${BLUE}==>${NC} $1"; }

# Check Railway CLI
if ! command -v railway &> /dev/null; then
    error "Railway CLI not found. Install: curl -fsSL https://railway.app/install.sh | sh"
fi

# Environment selection
ENVIRONMENT=${1:-staging}
info "Deploying to: $ENVIRONMENT"

# Validate environment
if [[ "$ENVIRONMENT" != "staging" && "$ENVIRONMENT" != "production" ]]; then
    error "Invalid environment. Use 'staging' or 'production'"
fi

# Check if we're in a git repository
if [ ! -d .git ]; then
    error "Not in a git repository. Please run from project root."
fi

section "Checking git status"
if [[ -n $(git status -s) ]]; then
    warn "You have uncommitted changes. Consider committing them first."
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

section "Linking Railway project"
railway link || error "Failed to link Railway project"

section "Switching to $ENVIRONMENT environment"
railway environment $ENVIRONMENT || error "Failed to switch environment"

section "Deploying to Railway..."
railway up --detach || error "Deployment failed"

info "Waiting for deployment to complete (30s)..."
sleep 30

# Health check
if [ "$ENVIRONMENT" = "production" ]; then
    URL="${PRODUCTION_URL:-https://tokyo-ia.up.railway.app}"
else
    URL="${STAGING_URL:-https://tokyo-ia-staging.up.railway.app}"
fi

section "Health checking: $URL/health"
info "Note: Update PRODUCTION_URL or STAGING_URL environment variables if using custom domains"
if curl -f -s "$URL/health" > /dev/null; then
    info "✅ Health check passed!"
else
    warn "❌ Health check failed! Service might still be starting..."
    info "Check Railway dashboard: https://railway.app/dashboard"
    exit 1
fi

section "Running smoke tests"
if [ "$ENVIRONMENT" = "production" ]; then
    info "Testing /api/agents endpoint..."
    if curl -f -s "$URL/api/agents" > /dev/null; then
        info "✅ Smoke tests passed!"
    else
        warn "⚠️  Smoke test failed for /api/agents"
    fi
fi

section "Deployment Summary"
info "Environment: $ENVIRONMENT"
info "URL: $URL"
info "Railway Dashboard: https://railway.app/dashboard"
info ""
info "✅ Deployment completed successfully!"

# Optional: Show recent logs
read -p "Show recent logs? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    railway logs
fi
