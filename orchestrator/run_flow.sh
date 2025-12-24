#!/bin/bash
set -euo pipefail

# Error trap to catch any failures
trap 'echo "❌ Error in line $LINENO"; exit 1' ERR

# ============================================================================
# Tokyo-IA Agent Orchestrator
# Executes all agents in the correct sequence
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🎭 Tokyo-IA Agent Orchestrator"
echo "==============================="
echo ""

# Store start time
START_TIME=$(date +%s)

# ============================================================================
# STEP 1: Run Simulator
# ============================================================================

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 1: Running Design Simulator"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "$PROJECT_ROOT/simulator/simulate_design.sh" ]; then
    bash "$PROJECT_ROOT/simulator/simulate_design.sh"
    echo ""
    echo "✅ Simulator completed"
else
    echo "❌ Error: simulator/simulate_design.sh not found"
    exit 1
fi

# ============================================================================
# STEP 2: Run Brand Agent
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 2: Running Brand Agent"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "$PROJECT_ROOT/agents/brand_executor.sh" ]; then
    bash "$PROJECT_ROOT/agents/brand_executor.sh"
    echo ""
    echo "✅ Brand Agent completed"
else
    echo "❌ Error: agents/brand_executor.sh not found"
    exit 1
fi

# ============================================================================
# STEP 3: Run UX Agent
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 3: Running UX Agent"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "$PROJECT_ROOT/agents/ux_executor.sh" ]; then
    bash "$PROJECT_ROOT/agents/ux_executor.sh"
    echo ""
    echo "✅ UX Agent completed"
else
    echo "❌ Error: agents/ux_executor.sh not found"
    exit 1
fi

# ============================================================================
# STEP 4: Run Bridge Agent
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 4: Running Bridge Agent"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "$PROJECT_ROOT/agents/bridge_executor.sh" ]; then
    bash "$PROJECT_ROOT/agents/bridge_executor.sh"
    echo ""
    echo "✅ Bridge Agent completed"
else
    echo "❌ Error: agents/bridge_executor.sh not found"
    exit 1
fi

# ============================================================================
# STEP 5: Run AutoDev Agent
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 5: Running AutoDev Agent"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "$PROJECT_ROOT/agents/autodev_executor.sh" ]; then
    bash "$PROJECT_ROOT/agents/autodev_executor.sh"
    echo ""
    echo "✅ AutoDev Agent completed"
else
    echo "❌ Error: agents/autodev_executor.sh not found"
    exit 1
fi

# ============================================================================
# SUMMARY
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 All Agents Completed Successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📁 Generated Files:"
echo ""
echo "  Simulator Outputs:"
echo "    • simulator/output/design_model.json"
echo "    • simulator/output/flutter_doctor.txt"
echo "    • simulator/output/flutter_analyze.txt"
echo ""
echo "  Agent Outputs:"
echo "    • simulator/output/brand_tokens.json"
echo "    • simulator/output/ux_flow.json"
echo "    • simulator/output/platform_bridge.json"
echo ""
echo "  Platform Code:"
echo "    • output/android/MainActivity.kt"
echo "    • output/android/activity_main.xml"
echo "    • output/ios/MainViewController.swift"
echo "    • output/web/App.tsx"
echo "    • output/web/App.css"
echo ""

# Calculate execution time
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
echo "⏱️  Total execution time: ${DURATION}s"
echo ""
