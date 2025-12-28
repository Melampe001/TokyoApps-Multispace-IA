#!/bin/bash
# Deploy to Vercel - TokyoApps-Multispace-IA
# Usage: ./scripts/deploy-vercel.sh [preview|production]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Vercel CLI is installed
check_vercel_cli() {
    if ! command -v vercel &> /dev/null; then
        log_error "Vercel CLI is not installed"
        log_info "Install it with: npm install -g vercel"
        exit 1
    fi
    log_info "✓ Vercel CLI found: $(vercel --version)"
}

# Validate project files
validate_project() {
    log_info "Validating project files..."
    
    if [ ! -f "vercel.json" ]; then
        log_error "vercel.json not found"
        exit 1
    fi
    log_info "✓ vercel.json found"
    
    if [ ! -d "api" ]; then
        log_error "api/ directory not found"
        exit 1
    fi
    log_info "✓ api/ directory found"
    
    if [ ! -f "api/requirements.txt" ]; then
        log_error "api/requirements.txt not found"
        exit 1
    fi
    log_info "✓ api/requirements.txt found"
    
    # Check if api endpoints exist
    for endpoint in "index.py" "health.py" "agents.py"; do
        if [ ! -f "api/$endpoint" ]; then
            log_error "api/$endpoint not found"
            exit 1
        fi
    done
    log_info "✓ All API endpoints found"
}

# Clean previous builds
clean_builds() {
    log_info "Cleaning previous builds..."
    rm -rf .vercel/output
    log_info "✓ Build cache cleared"
}

# Deploy to Vercel
deploy() {
    local env=$1
    
    if [ "$env" = "production" ]; then
        log_info "Deploying to PRODUCTION..."
        log_warn "This will update the production environment"
        read -p "Continue? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Deployment cancelled"
            exit 0
        fi
        vercel --prod
    else
        log_info "Deploying to PREVIEW..."
        vercel
    fi
}

# Main execution
main() {
    local deploy_env="${1:-preview}"
    
    log_info "=== Vercel Deployment Script ==="
    log_info "Environment: $deploy_env"
    echo
    
    # Pre-deployment checks
    check_vercel_cli
    validate_project
    clean_builds
    
    echo
    log_info "Starting deployment..."
    echo
    
    # Deploy
    deploy "$deploy_env"
    
    echo
    log_info "=== Deployment Complete ==="
    log_info "Check your deployment at: https://vercel.com/dashboard"
    
    if [ "$deploy_env" = "preview" ]; then
        log_info "Preview URL will be displayed above"
    else
        log_info "Production deployment successful"
    fi
}

# Show usage if --help
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Usage: $0 [preview|production]"
    echo
    echo "Options:"
    echo "  preview     Deploy to preview environment (default)"
    echo "  production  Deploy to production environment"
    echo
    echo "Examples:"
    echo "  $0                  # Deploy to preview"
    echo "  $0 preview          # Deploy to preview"
    echo "  $0 production       # Deploy to production"
    exit 0
fi

# Run main
main "$@"
