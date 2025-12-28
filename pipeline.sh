#!/bin/bash
set -euo pipefail

# ============================================================================
# Tokyo-IA Agent Pipeline
# Main entry point for the automated agent pipeline system
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ASCII Art Header
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ████████╗ ██████╗ ██╗  ██╗██╗   ██╗ ██████╗       ██╗ █████╗   ║
║   ╚══██╔══╝██╔═══██╗██║ ██╔╝╚██╗ ██╔╝██╔═══██╗     ██║██╔══██╗  ║
║      ██║   ██║   ██║█████╔╝  ╚████╔╝ ██║   ██║     ██║███████║  ║
║      ██║   ██║   ██║██╔═██╗   ╚██╔╝  ██║   ██║     ██║██╔══██║  ║
║      ██║   ╚██████╔╝██║  ██╗   ██║   ╚██████╔╝     ██║██║  ██║  ║
║      ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝      ╚═╝╚═╝  ╚═╝  ║
║                                                              ║
║          🚀 Automated Agent Pipeline System 🚀              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

EOF

echo "Starting Tokyo-IA Agent Pipeline..."
echo "Generated at: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
echo ""

# Record start time
PIPELINE_START=$(date +%s)

# ============================================================================
# PHASE 0: Kubernetes Preflight Validation (Optional)
# ============================================================================

if [ "${ENABLE_K8S_PREFLIGHT:-false}" = "true" ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "PHASE 0: Kubernetes Preflight Validation"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    if [ -f "$SCRIPT_DIR/scripts/k8s-preflight.sh" ]; then
        if bash "$SCRIPT_DIR/scripts/k8s-preflight.sh"; then
            echo ""
            echo "✅ Kubernetes preflight validation passed!"
        else
            echo ""
            echo "❌ Kubernetes preflight validation failed!"
            echo "Please resolve the issues above before proceeding."
            exit 1
        fi
    else
        echo "❌ Error: scripts/k8s-preflight.sh not found"
        exit 1
    fi
    
    echo ""
fi

# ============================================================================
# PHASE 1: Execute Orchestrator (Run All Agents)
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PHASE 1: Agent Orchestration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "$SCRIPT_DIR/orchestrator/run_flow.sh" ]; then
    bash "$SCRIPT_DIR/orchestrator/run_flow.sh"
else
    echo "❌ Error: orchestrator/run_flow.sh not found"
    exit 1
fi

# ============================================================================
# PHASE 2: Execute Emulator (Validate Generated Code)
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PHASE 2: Code Validation & Security Scan"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

VALIDATION_PASSED=true

if [ -f "$SCRIPT_DIR/emulator/run_emulator.sh" ]; then
    if bash "$SCRIPT_DIR/emulator/run_emulator.sh"; then
        echo ""
        echo "✅ Validation passed!"
    else
        echo ""
        echo "⚠️  Validation completed with warnings"
        VALIDATION_PASSED=false
    fi
else
    echo "❌ Error: emulator/run_emulator.sh not found"
    exit 1
fi

# ============================================================================
# PHASE 3: Display Results
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PHASE 3: Pipeline Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Calculate execution time
PIPELINE_END=$(date +%s)
TOTAL_DURATION=$((PIPELINE_END - PIPELINE_START))
MINUTES=$((TOTAL_DURATION / 60))
SECONDS=$((TOTAL_DURATION % 60))

echo "⏱️  Total Pipeline Duration: ${MINUTES}m ${SECONDS}s"
echo ""

# Display directory tree if available
echo "📂 Output Structure:"
echo ""
if command -v tree &> /dev/null; then
    tree -L 2 output/ simulator/output/ 2>/dev/null || true
else
    # Fallback to find command
    echo "Simulator Outputs:"
    find simulator/output/ -type f 2>/dev/null | sed 's|^|  |' || echo "  (none)"
    echo ""
    echo "Platform Code:"
    find output/ -type f 2>/dev/null | sed 's|^|  |' || echo "  (none)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Pipeline Completed Successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Next Steps:"
echo ""
echo "  1. Review generated code in output/ directory"
echo "  2. Check validation report: simulator/output/emulator_report.txt"
echo "  3. Review design model: simulator/output/design_model.json"
echo "  4. Integrate platform code into your projects"
if [ "${ENABLE_K8S_PREFLIGHT:-false}" = "true" ]; then
    echo "  5. Deploy to Kubernetes: kubectl apply -f your-manifests/"
fi
echo ""
echo "📚 For more information, see AGENTS_README.md"
echo ""

if [ "$VALIDATION_PASSED" = false ]; then
    echo "⚠️  Note: Some validation warnings were found. Please review the emulator report."
    echo ""
fi

exit 0
