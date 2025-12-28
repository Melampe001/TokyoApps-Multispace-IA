#!/bin/bash
# Validate Vercel deployment configuration
# This script checks all required files and configurations for Vercel deployment

# Note: Not using 'set -e' to allow validation to continue even if checks fail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

# Functions
log_success() {
    echo -e "${GREEN}✅ $1${NC}"
    ((PASSED++))
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
    ((FAILED++))
}

log_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_info() {
    echo -e "${BLUE}🔍 $1${NC}"
}

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  Validating Vercel Deployment Configuration"
echo "═══════════════════════════════════════════════════════"
echo ""

# 1. Check vercel.json exists and is valid JSON
log_info "Checking vercel.json..."
if [ ! -f "vercel.json" ]; then
    log_error "vercel.json not found"
else
    log_success "vercel.json exists"
    
    # Validate JSON syntax
    if python3 -c "import json; json.load(open('vercel.json'))" 2>/dev/null; then
        log_success "vercel.json has valid JSON syntax"
        
        # Check required fields
        if grep -q '"builds"' vercel.json && \
           grep -q '"routes"' vercel.json && \
           grep -q '"functions"' vercel.json; then
            log_success "vercel.json has required sections (builds, routes, functions)"
        else
            log_error "vercel.json missing required sections"
        fi
    else
        log_error "vercel.json has JSON syntax errors"
    fi
fi

echo ""

# 2. Check API directory structure
log_info "Checking API directory structure..."
if [ ! -d "api" ]; then
    log_error "api/ directory not found"
else
    log_success "api/ directory exists"
fi

echo ""

# 3. Check required API files
log_info "Checking required API files..."
REQUIRED_FILES=("api/index.py" "api/health.py" "api/agents.py" "api/requirements.txt")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        log_success "$file exists"
    else
        log_error "$file missing"
    fi
done

echo ""

# 4. Check Python syntax for all API files
log_info "Checking Python syntax..."
for pyfile in api/*.py; do
    if [ -f "$pyfile" ]; then
        if python3 -m py_compile "$pyfile" 2>/dev/null; then
            log_success "$pyfile has valid Python syntax"
        else
            log_error "$pyfile has syntax errors"
        fi
    fi
done

echo ""

# 5. Check Python dependencies
log_info "Checking Python dependencies..."
if [ -f "api/requirements.txt" ]; then
    log_success "api/requirements.txt exists"
    
    # Check for required packages
    REQUIRED_DEPS=("crewai" "groq" "openai" "anthropic")
    for dep in "${REQUIRED_DEPS[@]}"; do
        if grep -q "$dep" api/requirements.txt; then
            log_success "Dependency '$dep' listed in requirements.txt"
        else
            log_warn "Dependency '$dep' not found in requirements.txt"
        fi
    done
else
    log_error "api/requirements.txt not found"
fi

echo ""

# 6. Check .vercelignore
log_info "Checking .vercelignore..."
if [ -f ".vercelignore" ]; then
    log_success ".vercelignore configured"
else
    log_warn ".vercelignore not found (optional but recommended)"
fi

echo ""

# 7. Check deployment script
log_info "Checking deployment script..."
if [ -f "scripts/deploy-vercel.sh" ]; then
    log_success "deploy-vercel.sh exists"
    
    # Make it executable if it isn't already
    if [ ! -x "scripts/deploy-vercel.sh" ]; then
        chmod +x scripts/deploy-vercel.sh
        log_success "Made deploy-vercel.sh executable"
    else
        log_success "deploy-vercel.sh is executable"
    fi
else
    log_error "deploy-vercel.sh missing"
fi

echo ""

# 8. Check documentation
log_info "Checking documentation..."
if [ -f "DEPLOY_VERCEL.md" ]; then
    log_success "DEPLOY_VERCEL.md exists"
    
    # Check if it has key sections
    if grep -q "Despliegue en Vercel" DEPLOY_VERCEL.md || \
       grep -q "Deployment" DEPLOY_VERCEL.md; then
        log_success "DEPLOY_VERCEL.md has deployment content"
    else
        log_warn "DEPLOY_VERCEL.md may be incomplete"
    fi
else
    log_error "DEPLOY_VERCEL.md missing"
fi

echo ""

# 9. Check README has Vercel section
log_info "Checking README.md for Vercel deployment section..."
if [ -f "README.md" ]; then
    if grep -qi "vercel" README.md; then
        log_success "README.md mentions Vercel deployment"
    else
        log_warn "README.md doesn't mention Vercel deployment"
    fi
else
    log_warn "README.md not found"
fi

echo ""

# Summary
echo "═══════════════════════════════════════════════════════"
echo "  Validation Summary"
echo "═══════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All Vercel configuration validations passed!${NC}"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Test locally (optional): vercel dev"
    echo "2. Commit changes: git commit -am 'Complete Vercel deployment config'"
    echo "3. Push to branch: git push origin copilot/finalize-vercel-deployment"
    echo "4. Mark PR as ready for review"
    echo "5. Deploy to preview: ./scripts/deploy-vercel.sh preview"
    echo ""
    exit 0
else
    echo -e "${RED}❌ Validation failed with $FAILED error(s)${NC}"
    echo ""
    echo "Please fix the errors above before deploying."
    echo ""
    exit 1
fi
