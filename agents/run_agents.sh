#!/bin/bash
# Tokyo-IA Agents - Sequential Execution Script
# 
# This script executes all agent tasks sequentially and generates reports.
# It validates the environment, runs each workflow, and creates timestamped reports.
#
# Usage:
#   ./agents/run_agents.sh
#
# Requirements:
#   - Python 3.11+
#   - API keys set in environment (at least one)
#   - All dependencies installed (pip install -r requirements.txt)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Header
echo "════════════════════════════════════════════════════════════════════"
echo "🗼 Tokyo-IA Agent Orchestration - Sequential Execution"
echo "════════════════════════════════════════════════════════════════════"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Navigate to project root
cd "$PROJECT_ROOT"

echo "📁 Project directory: $PROJECT_ROOT"
echo ""

# Step 1: Validate Environment
echo "Step 1: Validating Environment"
echo "────────────────────────────────────────────────────────────────────"

# Check Python version
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo -e "${GREEN}✓${NC} Python version: $(python3 --version)"
else
    echo -e "${RED}✗${NC} Python 3.11+ required (found: $(python3 --version))"
    exit 1
fi

# Check for API keys
API_KEY_COUNT=0
echo ""
echo "API Keys configured:"

if [ ! -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "  ${GREEN}✓${NC} ANTHROPIC_API_KEY (Akira)"
    API_KEY_COUNT=$((API_KEY_COUNT + 1))
else
    echo -e "  ${YELLOW}⚠${NC} ANTHROPIC_API_KEY not set (Akira unavailable)"
fi

if [ ! -z "$OPENAI_API_KEY" ]; then
    echo -e "  ${GREEN}✓${NC} OPENAI_API_KEY (Yuki & Kenji)"
    API_KEY_COUNT=$((API_KEY_COUNT + 1))
else
    echo -e "  ${YELLOW}⚠${NC} OPENAI_API_KEY not set (Yuki & Kenji unavailable)"
fi

if [ ! -z "$GROQ_API_KEY" ]; then
    echo -e "  ${GREEN}✓${NC} GROQ_API_KEY (Hiro) [FREE TIER]"
    API_KEY_COUNT=$((API_KEY_COUNT + 1))
else
    echo -e "  ${YELLOW}⚠${NC} GROQ_API_KEY not set (Hiro unavailable)"
fi

if [ ! -z "$GOOGLE_API_KEY" ]; then
    echo -e "  ${GREEN}✓${NC} GOOGLE_API_KEY (Sakura) [FREE TIER]"
    API_KEY_COUNT=$((API_KEY_COUNT + 1))
else
    echo -e "  ${YELLOW}⚠${NC} GOOGLE_API_KEY not set (Sakura unavailable)"
fi

echo ""
echo "API Keys found: $API_KEY_COUNT/4"

if [ $API_KEY_COUNT -eq 0 ]; then
    echo -e "${RED}✗${NC} No API keys configured!"
    echo ""
    echo "Please set at least one API key:"
    echo "  export ANTHROPIC_API_KEY=sk-ant-..."
    echo "  export OPENAI_API_KEY=sk-..."
    echo "  export GROQ_API_KEY=gsk_..."
    echo "  export GOOGLE_API_KEY=..."
    exit 1
fi

echo ""

# Step 2: Test API Connections
echo "Step 2: Testing API Connections"
echo "────────────────────────────────────────────────────────────────────"
echo ""

if ! python3 agents/test_all_apis.py; then
    echo ""
    echo -e "${YELLOW}⚠${NC} Some API tests failed, but continuing with available agents..."
    echo ""
fi

# Create timestamp for reports
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_DIR="agent_reports_${TIMESTAMP}"

echo ""
echo "📁 Report directory: $REPORT_DIR"
echo ""

# Step 3: Execute Workflows
echo "Step 3: Executing Agent Workflows"
echo "────────────────────────────────────────────────────────────────────"
echo ""

# Track successes and failures
WORKFLOW_SUCCESS=0
WORKFLOW_TOTAL=0

# Workflow 1: Repository Cleanup
echo "🧹 Workflow 1: Repository Cleanup Analysis"
echo "────────────────────────────────────────────────────────────────────"
WORKFLOW_TOTAL=$((WORKFLOW_TOTAL + 1))
if python3 agents/tokyo_crew.py cleanup; then
    echo -e "${GREEN}✓${NC} Repository cleanup analysis completed"
    WORKFLOW_SUCCESS=$((WORKFLOW_SUCCESS + 1))
else
    echo -e "${RED}✗${NC} Repository cleanup analysis failed"
fi
echo ""

# Workflow 2: Documentation Generation
echo "📚 Workflow 2: Documentation Generation"
echo "────────────────────────────────────────────────────────────────────"
WORKFLOW_TOTAL=$((WORKFLOW_TOTAL + 1))
if python3 agents/tokyo_crew.py generate-docs; then
    echo -e "${GREEN}✓${NC} Documentation generation completed"
    WORKFLOW_SUCCESS=$((WORKFLOW_SUCCESS + 1))
else
    echo -e "${RED}✗${NC} Documentation generation failed"
fi
echo ""

# Workflow 3: PR Analysis (example - adjust PR number as needed)
# Uncomment to analyze specific PRs:
# echo "📊 Workflow 3: PR #126 Analysis"
# echo "────────────────────────────────────────────────────────────────────"
# WORKFLOW_TOTAL=$((WORKFLOW_TOTAL + 1))
# if python3 agents/tokyo_crew.py analyze-pr 126; then
#     echo -e "${GREEN}✓${NC} PR #126 analysis completed"
#     WORKFLOW_SUCCESS=$((WORKFLOW_SUCCESS + 1))
# else
#     echo -e "${RED}✗${NC} PR #126 analysis failed"
# fi
# echo ""

# Step 4: Generate Executive Summary
echo "Step 4: Generating Executive Summary"
echo "────────────────────────────────────────────────────────────────────"
echo ""

# Find the most recent report directory
LATEST_REPORT_DIR=$(ls -td agent_reports_* 2>/dev/null | head -1)

if [ -z "$LATEST_REPORT_DIR" ]; then
    echo -e "${YELLOW}⚠${NC} No report directory found"
else
    SUMMARY_FILE="$LATEST_REPORT_DIR/EXECUTIVE_SUMMARY.md"
    
    cat > "$SUMMARY_FILE" << EOF
# Tokyo-IA Agent Execution Summary

**Generated:** $(date)
**Report Directory:** $LATEST_REPORT_DIR

## Execution Statistics

- **Workflows Executed:** $WORKFLOW_TOTAL
- **Successful:** $WORKFLOW_SUCCESS
- **Failed:** $((WORKFLOW_TOTAL - WORKFLOW_SUCCESS))
- **Success Rate:** $(( WORKFLOW_SUCCESS * 100 / WORKFLOW_TOTAL ))%

## API Configuration

- **Total API Keys:** $API_KEY_COUNT/4
- **Cost Mode:** $([ $API_KEY_COUNT -le 2 ] && echo "FREE TIER ONLY 💚" || echo "HYBRID (Free + Paid) 💰")

## Agents Deployed

EOF

    # Add agent status
    if [ ! -z "$ANTHROPIC_API_KEY" ]; then
        echo "- ✅ 侍 **Akira** (Code Review Master) - Claude 3.5 Sonnet" >> "$SUMMARY_FILE"
    fi
    if [ ! -z "$OPENAI_API_KEY" ]; then
        echo "- ✅ ❄️ **Yuki** (Test Engineering) - GPT-4o mini" >> "$SUMMARY_FILE"
        echo "- ✅ 🏗️ **Kenji** (Architecture) - GPT-4o" >> "$SUMMARY_FILE"
    fi
    if [ ! -z "$GROQ_API_KEY" ]; then
        echo "- ✅ 🛡️ **Hiro** (SRE/DevOps) - Llama 3.3 70B [FREE]" >> "$SUMMARY_FILE"
    fi
    if [ ! -z "$GOOGLE_API_KEY" ]; then
        echo "- ✅ 🌸 **Sakura** (Documentation) - Gemini 1.5 Flash [FREE]" >> "$SUMMARY_FILE"
    fi

    cat >> "$SUMMARY_FILE" << EOF

## Generated Reports

EOF

    # List all generated reports
    for file in "$LATEST_REPORT_DIR"/*.json "$LATEST_REPORT_DIR"/*.md; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            filesize=$(du -h "$file" | cut -f1)
            echo "- \`$filename\` ($filesize)" >> "$SUMMARY_FILE"
        fi
    done

    cat >> "$SUMMARY_FILE" << EOF

## Next Steps

1. Review generated reports in \`$LATEST_REPORT_DIR/\`
2. Implement recommendations from cleanup analysis
3. Update documentation based on Sakura's suggestions
4. Address any issues flagged by agents

## Commands Used

\`\`\`bash
# Repository cleanup
python agents/tokyo_crew.py cleanup

# Documentation generation
python agents/tokyo_crew.py generate-docs

# PR analysis (example)
# python agents/tokyo_crew.py analyze-pr <pr_number>
\`\`\`

---

Generated by Tokyo-IA Agent Orchestration System
EOF

    echo -e "${GREEN}✓${NC} Executive summary generated: $SUMMARY_FILE"
fi

echo ""

# Final Summary
echo "════════════════════════════════════════════════════════════════════"
echo "✨ Tokyo-IA Agent Execution Complete"
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "Summary:"
echo "  Workflows: $WORKFLOW_SUCCESS/$WORKFLOW_TOTAL successful"
echo "  Reports: $LATEST_REPORT_DIR/"
echo ""

if [ $WORKFLOW_SUCCESS -eq $WORKFLOW_TOTAL ]; then
    echo -e "${GREEN}✓${NC} All workflows completed successfully!"
    exit 0
elif [ $WORKFLOW_SUCCESS -gt 0 ]; then
    echo -e "${YELLOW}⚠${NC} Some workflows completed (see details above)"
    exit 0
else
    echo -e "${RED}✗${NC} All workflows failed"
    exit 1
fi
