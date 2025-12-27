#!/bin/bash
set -euo pipefail

# ============================================================================
# Tokyo-IA Kubernetes Environment Validation
# Environment-specific validation for Tokyo-IA deployment
# ============================================================================
#
# Usage:
#   ./infrastructure/k8s/validate-env.sh [namespace]
#
# This script performs Tokyo-IA specific checks:
#   - Required secrets validation
#   - ConfigMap presence
#   - PVC status checks
#   - Image pull secrets
#   - Custom Resource Definitions
#
# Exit Codes:
#   0 - Success (warnings allowed)
#   1 - Failure (critical issues)
#
# ============================================================================

# Namespace parameter (default: tokyo-ia)
NAMESPACE="${1:-tokyo-ia}"

# Colors
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Functions
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
pass() { echo -e "${GREEN}✓${NC} $1"; }
info() { echo -e "${BLUE}ℹ${NC} $1"; }

echo ""
info "Validating Tokyo-IA specific environment in namespace: $NAMESPACE"
echo ""

# ============================================================================
# REQUIRED SECRETS
# ============================================================================

echo -n "Checking Tokyo-IA required secrets... "
REQUIRED_SECRETS=("tokyo-ia-api-key" "tokyo-ia-db-credentials" "tokyo-ia-redis-url")
MISSING_SECRETS=()

for SECRET in "${REQUIRED_SECRETS[@]}"; do
    if ! kubectl get secret "$SECRET" -n "$NAMESPACE" &> /dev/null; then
        MISSING_SECRETS+=("$SECRET")
    fi
done

if [ ${#MISSING_SECRETS[@]} -eq 0 ]; then
    pass "All Tokyo-IA secrets present (${#REQUIRED_SECRETS[@]} checked)"
else
    warn "Missing Tokyo-IA secrets: ${MISSING_SECRETS[*]}"
    echo ""
    echo "  Create missing secrets before deployment:"
    for SECRET in "${MISSING_SECRETS[@]}"; do
        echo "    kubectl create secret generic $SECRET -n $NAMESPACE \\"
        echo "      --from-literal=key=<your-value>"
    done
    echo ""
fi

# ============================================================================
# CONFIGMAP
# ============================================================================

echo -n "Checking Tokyo-IA ConfigMap... "
if kubectl get configmap tokyo-ia-config -n "$NAMESPACE" &> /dev/null; then
    pass "ConfigMap 'tokyo-ia-config' exists"
else
    warn "ConfigMap 'tokyo-ia-config' not found"
    echo "     Create with: kubectl create configmap tokyo-ia-config -n $NAMESPACE \\"
    echo "                    --from-file=config.yaml=path/to/config.yaml"
fi

# ============================================================================
# PERSISTENTVOLUMECLAIMS
# ============================================================================

echo -n "Checking PersistentVolumeClaims... "
PVCS=$(kubectl get pvc -n "$NAMESPACE" --no-headers 2>/dev/null | wc -l)
if [ "$PVCS" -gt 0 ]; then
    BOUND_PVCS=$(kubectl get pvc -n "$NAMESPACE" --no-headers 2>/dev/null | grep -c "Bound" || echo 0)
    if [ "$BOUND_PVCS" -eq "$PVCS" ]; then
        pass "$PVCS PVC(s) found and all bound"
    else
        warn "$BOUND_PVCS/$PVCS PVC(s) bound (some pending)"
        kubectl get pvc -n "$NAMESPACE" --no-headers | grep -v "Bound" | awk '{print "     - " $1 " (" $2 ")"}' || true
    fi
else
    info "No PVCs found (stateless deployment)"
fi

# ============================================================================
# IMAGE PULL SECRETS
# ============================================================================

echo -n "Checking image pull secret 'regcred'... "
if kubectl get secret regcred -n "$NAMESPACE" &> /dev/null; then
    # Verify it's a docker config secret
    SECRET_TYPE=$(kubectl get secret regcred -n "$NAMESPACE" -o jsonpath='{.type}')
    if [[ "$SECRET_TYPE" == "kubernetes.io/dockerconfigjson" ]]; then
        pass "Image pull secret 'regcred' configured"
    else
        warn "Secret 'regcred' exists but is not a docker config secret (type: $SECRET_TYPE)"
    fi
else
    warn "Image pull secret 'regcred' not found"
    echo "     For private registry access:"
    echo "       kubectl create secret docker-registry regcred \\"
    echo "         --docker-server=<registry> \\"
    echo "         --docker-username=<username> \\"
    echo "         --docker-password=<password> \\"
    echo "         -n $NAMESPACE"
fi

# ============================================================================
# CUSTOM RESOURCE DEFINITIONS
# ============================================================================

echo -n "Checking Tokyo-IA Custom Resource Definitions... "
TOKYO_CRDS=$(kubectl get crd 2>/dev/null | grep -c "tokyo-ia" || echo 0)
if [ "$TOKYO_CRDS" -gt 0 ]; then
    pass "$TOKYO_CRDS Tokyo-IA CRD(s) found"
    kubectl get crd 2>/dev/null | grep "tokyo-ia" | awk '{print "     - " $1}' || true
else
    info "No Tokyo-IA CRDs found (not using operators)"
fi

echo ""
info "Tokyo-IA environment validation complete"
echo ""

# Always exit 0 (warnings are non-blocking)
exit 0
