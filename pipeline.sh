#!/bin/bash
# ============================================================================
# Tokyo-IA Agent Pipeline - Main Entry Point
# ============================================================================
# Purpose: Orchestrates the complete agent pipeline for Flutter-to-native
#          code generation across Android, iOS, and Web platforms
#
# Pipeline Flow:
#   1. PHASE 1: Agent Orchestration (orchestrator/run_flow.sh)
#      - Runs simulator to extract Flutter metadata
#      - Executes brand, UX, bridge, and autodev agents in sequence
#      - Generates platform-specific code
#
#   2. PHASE 2: Code Validation (emulator/run_emulator.sh)
#      - Validates generated code for compliance
#      - Performs security scanning
#      - Checks platform-specific requirements
#
#   3. PHASE 3: Results Summary
#      - Reports execution time
#      - Displays output structure
#      - Provides next steps
#
# Usage:
#   bash pipeline.sh
#
# Environment Variables:
#   TARGET_PLATFORM - Optional: "all", "android", "ios", or "web" (default: all)
#
# Requirements:
#   - Flutter app in flutter_app/ directory
#   - Bash 4.0+
#   - jq for JSON processing
#   - Standard Unix tools (grep, find, tree)
#
# Output:
#   - simulator/output/ - JSON metadata and reports
#   - output/ - Generated platform code (android/, ios/, web/)
#
# Exit Codes:
#   0 - Success (may have warnings)
#   1 - Fatal error (orchestrator or emulator not found, or critical failure)
# ============================================================================

# Enable strict error handling
# -e: Exit on error
# -u: Exit on undefined variable
# -o pipefail: Exit on pipe failure
set -euo pipefail

# Determine script directory for relative path resolution
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ============================================================================
# Display Banner
# ============================================================================
# Show branded ASCII art header for visual identification
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

# Display pipeline start information
echo "Starting Tokyo-IA Agent Pipeline..."
echo "Generated at: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
echo ""

# Record start time for performance metrics
# Using seconds since epoch for easy duration calculation
PIPELINE_START=$(date +%s)

# ============================================================================
# PHASE 1: Execute Orchestrator (Run All Agents)
# ============================================================================
# The orchestrator coordinates the execution of all agents in proper sequence:
#   1. Simulator - Extracts Flutter app metadata and design model
#   2. Brand Agent - Generates design tokens (colors, typography, spacing)
#   3. UX Agent - Analyzes navigation patterns and user flows
#   4. Bridge Agent - Creates widget-to-platform mappings
#   5. AutoDev Agent - Generates platform-specific native code
#
# Each agent reads from previous outputs and produces JSON/code for next steps
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PHASE 1: Agent Orchestration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Execute orchestrator script
# Exit with error if orchestrator not found (critical failure)
if [ -f "$SCRIPT_DIR/orchestrator/run_flow.sh" ]; then
    bash "$SCRIPT_DIR/orchestrator/run_flow.sh"
else
    echo "❌ Error: orchestrator/run_flow.sh not found"
    echo "   Please ensure the repository structure is intact"
    exit 1
fi

# ============================================================================
# PHASE 2: Execute Emulator (Validate Generated Code)
# ============================================================================
# The emulator performs comprehensive validation on generated code:
#   - Android: Kotlin syntax, XML validity, Material Components usage
#   - iOS: Swift syntax, UIKit/SwiftUI patterns, Auto Layout
#   - Web: React/TypeScript, semantic HTML, accessibility
#   - Security: Scans for hardcoded secrets, SQL injection risks
#   - Compliance: Checks for prohibited APIs, store policy violations
#
# Generates detailed report in simulator/output/emulator_report.txt
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PHASE 2: Code Validation & Security Scan"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Track validation status for final summary
VALIDATION_PASSED=true

# Execute emulator/validator
# Note: Emulator may return non-zero exit code for warnings (not fatal)
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
    echo "   Please ensure the repository structure is intact"
    exit 1
fi

# ============================================================================
# PHASE 3: Display Results
# ============================================================================
# Provides comprehensive summary of pipeline execution:
#   - Total execution time
#   - Output file structure
#   - Next steps for integration
#   - Warnings if validation issues found
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PHASE 3: Pipeline Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Calculate total pipeline execution time
PIPELINE_END=$(date +%s)
TOTAL_DURATION=$((PIPELINE_END - PIPELINE_START))
MINUTES=$((TOTAL_DURATION / 60))
SECONDS=$((TOTAL_DURATION % 60))

echo "⏱️  Total Pipeline Duration: ${MINUTES}m ${SECONDS}s"
echo ""

# Display directory tree if tree command available, otherwise use find
echo "📂 Output Structure:"
echo ""
if command -v tree &> /dev/null; then
    # Use tree command for nice visual output (limit depth to 2 levels)
    tree -L 2 output/ simulator/output/ 2>/dev/null || true
else
    # Fallback to find command for basic listing
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
echo ""
echo "📚 For more information, see AGENTS_README.md"
echo ""

# Display warning if validation found issues
if [ "$VALIDATION_PASSED" = false ]; then
    echo "⚠️  Note: Some validation warnings were found. Please review the emulator report."
    echo ""
fi

# Exit successfully (exit code 0 even with warnings)
exit 0
