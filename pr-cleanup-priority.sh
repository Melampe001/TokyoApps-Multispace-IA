#!/bin/bash
set -euo pipefail

# ============================================================================
# Tokyo-IA PR Priority Cleanup Script
# Automated cleanup based on priority analysis
# ============================================================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
MERGED=0
CLOSED=0
READY=0
ERRORS=0

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Tokyo-IA PR Priority Cleanup & Automation Setup        ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================================
# PHASE 1: Auto-Merge Candidates (Quick Wins)
# ============================================================================

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}PHASE 1: Preparing Auto-Merge Candidates${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# PR #115 - Go Linter Fixes (P1, size/XS)
echo -ne "  🔧 PR #115 (Go Linter Fixes)... "
if gh pr ready 115 2>/dev/null; then
    echo -e "${GREEN}✓ Ready${NC}"
    ((READY++))
else
    echo -e "${YELLOW}⚠ Already ready or error${NC}"
fi

# PR #108 - Fix Billing References (P1, size/S, docs)
echo -ne "  📝 PR #108 (Fix Billing References)... "
if gh pr ready 108 2>/dev/null; then
    echo -e "${GREEN}✓ Ready${NC}"
    ((READY++))
else
    echo -e "${YELLOW}⚠ Already ready or error${NC}"
fi

# PR #76 - Enterprise Documentation
echo -ne "  📚 PR #76 (Enterprise Documentation)... "
if gh pr ready 76 2>/dev/null; then
    echo -e "${GREEN}✓ Ready${NC}"
    ((READY++))
else
    echo -e "${YELLOW}⚠ Already ready or error${NC}"
fi

# PR #101 - Flutter Test Imports
echo -ne "  🧪 PR #101 (Flutter Test Imports)... "
if gh pr ready 101 2>/dev/null; then
    echo -e "${GREEN}✓ Ready${NC}"
    ((READY++))
else
    echo -e "${YELLOW}⚠ Already ready or error${NC}"
fi

echo ""

# ============================================================================
# PHASE 2: Close Duplicate PRs
# ============================================================================

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}PHASE 2: Closing Duplicate PRs${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Close duplicates with comments
for pr_num in 73 6 8 25 26 31 32 33; do
    echo -ne "  🗑️  PR #${pr_num}... "
    if gh pr close ${pr_num} --comment "🔄 Closing as duplicate/consolidated" 2>/dev/null; then
        echo -e "${GREEN}✓ Closed${NC}"
        ((CLOSED++))
    else
        echo -e "${YELLOW}⚠ Already closed or error${NC}"
    fi
done

echo ""

# ============================================================================
# SUMMARY
# ============================================================================

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}CLEANUP SUMMARY${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "  ✓ PRs Marked Ready: $READY"
echo "  ✓ PRs Closed: $CLOSED"
echo "  Total Actions: $((READY + CLOSED))"
echo ""

# Generate report
cat > pr-cleanup-report.json << EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "initial_pr_count": 47,
  "actions": {
    "ready_for_merge": $READY,
    "closed_duplicates": $CLOSED
  },
  "estimated_final_count": $((47 - CLOSED))
}
EOF

echo -e "${GREEN}✅ Report saved: pr-cleanup-report.json${NC}"
