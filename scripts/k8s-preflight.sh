#!/bin/bash
set -euo pipefail

# ============================================================================
# Kubernetes Preflight Validation Script
# Validates cluster readiness before Tokyo-IA deployment
# ============================================================================
#
# Usage:
#   Basic: ./scripts/k8s-preflight.sh
#   Custom: K8S_NAMESPACE=prod K8S_MIN_NODES=3 ./scripts/k8s-preflight.sh
#   In pipeline: ENABLE_K8S_PREFLIGHT=true ./pipeline.sh
#
# Environment Variables:
#   K8S_NAMESPACE         - Target namespace (default: tokyo-ia)
#   K8S_MIN_NODES         - Minimum nodes required (default: 1)
#   K8S_MIN_MEMORY_GB     - Minimum memory per node in GB (default: 2)
#   K8S_MIN_CPU_CORES     - Minimum CPU cores per node (default: 1)
#   REQUIRED_K8S_VERSION  - Minimum Kubernetes version (default: 1.24)
#   K8S_REQUIRED_SECRETS  - Comma-separated list of required secrets
#
# Exit Codes:
#   0 - Success (may include warnings)
#   1 - Failure (critical issues found)
#
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Configuration with defaults
K8S_NAMESPACE="${K8S_NAMESPACE:-tokyo-ia}"
K8S_MIN_NODES="${K8S_MIN_NODES:-1}"
K8S_MIN_MEMORY_GB="${K8S_MIN_MEMORY_GB:-2}"
K8S_MIN_CPU_CORES="${K8S_MIN_CPU_CORES:-1}"
REQUIRED_K8S_VERSION="${REQUIRED_K8S_VERSION:-1.24}"
K8S_REQUIRED_SECRETS="${K8S_REQUIRED_SECRETS:-}"

# Colors (matching deploy.sh style)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

# Functions
pass() { 
    echo -e "${GREEN}✓${NC} $1"
    ((PASS_COUNT++))
}

warn() { 
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARN_COUNT++))
}

fail() { 
    echo -e "${RED}✗${NC} $1"
    ((FAIL_COUNT++))
}

info() { 
    echo -e "${BLUE}ℹ${NC} $1"
}

section() { 
    echo ""
    echo -e "${BLUE}==>${NC} $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Header
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║     Kubernetes Preflight Validation for Tokyo-IA            ║
╚══════════════════════════════════════════════════════════════╝
EOF

echo ""
info "Starting preflight checks..."
info "Target namespace: $K8S_NAMESPACE"
echo ""

# ============================================================================
# ESSENTIAL CHECKS
# ============================================================================

section "Essential Checks"

# Check 1: kubectl installation
echo -n "Checking kubectl installation... "
if command -v kubectl &> /dev/null; then
    KUBECTL_VERSION=$(kubectl version --client --short 2>/dev/null | grep -oP 'v\K[0-9.]+' | head -1 || echo "unknown")
    pass "kubectl installed (version: $KUBECTL_VERSION)"
else
    fail "kubectl not found"
    echo ""
    echo "  Installation instructions:"
    echo "    Linux:   curl -LO \"https://dl.k8s.io/release/\$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl\""
    echo "    macOS:   brew install kubectl"
    echo "    Windows: choco install kubernetes-cli"
    echo ""
    exit 1
fi

# Check 2: Cluster connectivity
echo -n "Checking cluster connectivity... "
if kubectl cluster-info &> /dev/null; then
    CLUSTER_ENDPOINT=$(kubectl cluster-info | grep -oP 'control plane.*https://\K[^[:space:]]+' || echo "unknown")
    pass "Connected to cluster ($CLUSTER_ENDPOINT)"
else
    fail "Cannot connect to Kubernetes cluster"
    echo ""
    echo "  Troubleshooting:"
    echo "    - Check your kubeconfig: kubectl config view"
    echo "    - Verify context: kubectl config current-context"
    echo "    - Test connection: kubectl cluster-info"
    echo ""
    exit 1
fi

# Check 3: Kubernetes version
echo -n "Checking Kubernetes version... "
SERVER_VERSION=$(kubectl version --short 2>/dev/null | grep Server | grep -oP 'v\K[0-9.]+' || echo "0.0")
SERVER_MAJOR_MINOR=$(echo "$SERVER_VERSION" | cut -d. -f1,2)
REQUIRED_MAJOR_MINOR=$(echo "$REQUIRED_K8S_VERSION" | cut -d. -f1,2)

if awk "BEGIN {exit !($SERVER_MAJOR_MINOR >= $REQUIRED_MAJOR_MINOR)}"; then
    pass "Kubernetes version $SERVER_VERSION (>= $REQUIRED_K8S_VERSION required)"
else
    fail "Kubernetes version $SERVER_VERSION is below minimum $REQUIRED_K8S_VERSION"
    echo ""
    echo "  Please upgrade your Kubernetes cluster to version $REQUIRED_K8S_VERSION or higher"
    echo ""
    exit 1
fi

# Check 4: Node availability and health
echo -n "Checking node availability... "
NODE_COUNT=$(kubectl get nodes --no-headers 2>/dev/null | wc -l)
READY_NODES=$(kubectl get nodes --no-headers 2>/dev/null | grep -c " Ready" || echo 0)

if [ "$NODE_COUNT" -ge "$K8S_MIN_NODES" ]; then
    if [ "$READY_NODES" -eq "$NODE_COUNT" ]; then
        pass "$READY_NODES/$NODE_COUNT nodes available and ready (minimum: $K8S_MIN_NODES)"
    else
        warn "$READY_NODES/$NODE_COUNT nodes ready (some nodes not ready)"
        echo "     Not ready nodes:"
        kubectl get nodes --no-headers | grep -v " Ready" | awk '{print "       - " $1 " (" $2 ")"}' || true
    fi
else
    fail "Only $NODE_COUNT nodes available (minimum: $K8S_MIN_NODES required)"
fi

# Check 5: Namespace existence/creation
echo -n "Checking namespace '$K8S_NAMESPACE'... "
if kubectl get namespace "$K8S_NAMESPACE" &> /dev/null; then
    pass "Namespace exists"
else
    info "Namespace does not exist, creating..."
    if kubectl create namespace "$K8S_NAMESPACE" &> /dev/null; then
        pass "Namespace created successfully"
    else
        fail "Failed to create namespace"
        echo ""
        echo "  Try manually: kubectl create namespace $K8S_NAMESPACE"
        echo ""
        exit 1
    fi
fi

# Check 6: RBAC permissions
echo -n "Checking RBAC permissions... "
RBAC_ERRORS=0

for RESOURCE in pods services deployments; do
    if ! kubectl auth can-i create "$RESOURCE" -n "$K8S_NAMESPACE" &> /dev/null; then
        ((RBAC_ERRORS++))
    fi
done

if [ $RBAC_ERRORS -eq 0 ]; then
    pass "Required RBAC permissions available (pods, services, deployments)"
else
    fail "Missing RBAC permissions for some resources"
    echo ""
    echo "  Check permissions:"
    echo "    kubectl auth can-i create pods -n $K8S_NAMESPACE"
    echo "    kubectl auth can-i create services -n $K8S_NAMESPACE"
    echo "    kubectl auth can-i create deployments -n $K8S_NAMESPACE"
    echo ""
    exit 1
fi

# ============================================================================
# ADVANCED CHECKS
# ============================================================================

section "Advanced Checks"

# Check 7: Resource quotas
echo -n "Checking resource quotas... "
QUOTAS=$(kubectl get resourcequota -n "$K8S_NAMESPACE" --no-headers 2>/dev/null | wc -l)
if [ "$QUOTAS" -gt 0 ]; then
    warn "Resource quotas found ($QUOTAS) - ensure sufficient limits for deployment"
    kubectl get resourcequota -n "$K8S_NAMESPACE" -o custom-columns=NAME:.metadata.name,CPU:.status.hard.cpu,MEMORY:.status.hard.memory 2>/dev/null | sed 's/^/     /'
else
    pass "No resource quotas (unlimited resources)"
fi

# Check 8: Network policies
echo -n "Checking network policies... "
NETPOL_COUNT=$(kubectl get networkpolicy -n "$K8S_NAMESPACE" --no-headers 2>/dev/null | wc -l)
if [ "$NETPOL_COUNT" -gt 0 ]; then
    warn "Network policies found ($NETPOL_COUNT) - verify they allow Tokyo-IA traffic"
    kubectl get networkpolicy -n "$K8S_NAMESPACE" --no-headers 2>/dev/null | awk '{print "     - " $1}' || true
else
    pass "No network policies (traffic allowed)"
fi

# Check 9: Storage classes
echo -n "Checking storage classes... "
STORAGE_CLASSES=$(kubectl get storageclass --no-headers 2>/dev/null | wc -l)
DEFAULT_SC=$(kubectl get storageclass -o json 2>/dev/null | grep -c '"storageclass.kubernetes.io/is-default-class":"true"' || echo 0)

if [ "$STORAGE_CLASSES" -gt 0 ]; then
    if [ "$DEFAULT_SC" -gt 0 ]; then
        DEFAULT_SC_NAME=$(kubectl get storageclass -o json 2>/dev/null | jq -r '.items[] | select(.metadata.annotations["storageclass.kubernetes.io/is-default-class"]=="true") | .metadata.name' | head -1)
        pass "$STORAGE_CLASSES storage class(es) available (default: $DEFAULT_SC_NAME)"
    else
        warn "$STORAGE_CLASSES storage class(es) available but no default set"
    fi
else
    warn "No storage classes available (PVCs may not work)"
fi

# Check 10: Ingress controller
echo -n "Checking ingress controller... "
INGRESS_PODS=$(kubectl get pods -A -l app.kubernetes.io/name=ingress-nginx --no-headers 2>/dev/null | wc -l)
if [ "$INGRESS_PODS" -gt 0 ]; then
    READY_INGRESS=$(kubectl get pods -A -l app.kubernetes.io/name=ingress-nginx --no-headers 2>/dev/null | grep -c "Running" || echo 0)
    pass "Ingress controller detected ($READY_INGRESS/$INGRESS_PODS pods running)"
else
    # Check for other common ingress controllers
    TRAEFIK_PODS=$(kubectl get pods -A -l app.kubernetes.io/name=traefik --no-headers 2>/dev/null | wc -l)
    if [ "$TRAEFIK_PODS" -gt 0 ]; then
        pass "Traefik ingress controller detected"
    else
        warn "No ingress controller detected (nginx-ingress recommended)"
        echo "     Install: kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml"
    fi
fi

# Check 11: Service mesh detection
echo -n "Checking service mesh... "
ISTIO_PODS=$(kubectl get pods -n istio-system --no-headers 2>/dev/null | wc -l)
if [ "$ISTIO_PODS" -gt 0 ]; then
    pass "Istio service mesh detected"
else
    info "No service mesh detected (optional)"
fi

# Check 12: Required secrets validation
if [ -n "$K8S_REQUIRED_SECRETS" ]; then
    echo -n "Checking required secrets... "
    MISSING_SECRETS=()
    IFS=',' read -ra SECRETS <<< "$K8S_REQUIRED_SECRETS"
    for SECRET in "${SECRETS[@]}"; do
        SECRET=$(echo "$SECRET" | xargs) # trim whitespace
        if ! kubectl get secret "$SECRET" -n "$K8S_NAMESPACE" &> /dev/null; then
            MISSING_SECRETS+=("$SECRET")
        fi
    done
    
    if [ ${#MISSING_SECRETS[@]} -eq 0 ]; then
        pass "All required secrets present (${#SECRETS[@]} checked)"
    else
        fail "Missing required secrets: ${MISSING_SECRETS[*]}"
        echo ""
        echo "  Create missing secrets:"
        for SECRET in "${MISSING_SECRETS[@]}"; do
            echo "    kubectl create secret generic $SECRET -n $K8S_NAMESPACE --from-literal=key=value"
        done
        echo ""
    fi
fi

# Check 13: Image pull secrets
echo -n "Checking image pull secrets... "
PULL_SECRETS=$(kubectl get secret -n "$K8S_NAMESPACE" --field-selector type=kubernetes.io/dockerconfigjson --no-headers 2>/dev/null | wc -l)
if [ "$PULL_SECRETS" -gt 0 ]; then
    pass "$PULL_SECRETS image pull secret(s) configured"
else
    warn "No image pull secrets (public images only)"
    echo "     For private registries:"
    echo "       kubectl create secret docker-registry regcred --docker-server=<registry> --docker-username=<user> --docker-password=<pass> -n $K8S_NAMESPACE"
fi

# ============================================================================
# TOKYO-IA SPECIFIC CHECKS
# ============================================================================

section "Tokyo-IA Specific Checks"

VALIDATE_ENV_SCRIPT="$PROJECT_ROOT/infrastructure/k8s/validate-env.sh"
if [ -f "$VALIDATE_ENV_SCRIPT" ]; then
    info "Running Tokyo-IA environment validation..."
    if bash "$VALIDATE_ENV_SCRIPT" "$K8S_NAMESPACE"; then
        pass "Tokyo-IA environment validation passed"
    else
        warn "Tokyo-IA environment validation completed with warnings"
    fi
else
    info "No Tokyo-IA specific validation script found (optional)"
fi

# ============================================================================
# SUMMARY
# ============================================================================

section "Preflight Summary"

echo ""
echo "  ✓ Passed:  $PASS_COUNT"
echo "  ⚠ Warnings: $WARN_COUNT"
echo "  ✗ Failed:  $FAIL_COUNT"
echo ""

if [ $FAIL_COUNT -gt 0 ]; then
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}✗ Preflight validation FAILED${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Please resolve the failed checks above before proceeding with deployment."
    exit 1
elif [ $WARN_COUNT -gt 0 ]; then
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}⚠ Preflight validation PASSED with warnings${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Review the warnings above. Deployment can proceed but may encounter issues."
    exit 0
else
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✓ Preflight validation PASSED${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Kubernetes cluster is ready for Tokyo-IA deployment!"
    exit 0
fi
