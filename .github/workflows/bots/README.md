# 🤖 Tokyo-IA Automated Bots Documentation

This directory contains automated bot agents that monitor, classify, and manage issues and PRs for the Tokyo-IA project.

## Overview

We have 4 specialized bot agents organized by area:

### 🔧 Backend Bots

#### Bot #1: Backend Code Quality Guardian
**File:** `.github/workflows/bot-backend-quality.yml`

Monitors code quality in backend Go code (`lib/`, `internal/`, `cmd/`):
- ✅ Verifies tests are included in PRs
- ✅ Checks for documentation comments on exported functions
- ✅ Validates error handling patterns
- ✅ Detects unused imports
- ✅ Calculates quality score (0-100)
- ✅ Auto-approves PRs meeting quality threshold (90+)
- ✅ Labels: `backend`, `needs-tests`, `needs-docs`

**Special behaviors:**
- If PR modifies `proto/`: reminds to run `make proto`
- If PR modifies billing code: requires billing tests
- Runs daily at 10:00 UTC and on PR events

#### Bot #2: Backend Performance Monitor
**File:** `.github/workflows/bot-backend-performance.yml`

Analyzes performance issues in backend code:
- ⚡ Detects nested loops
- ⚡ Identifies potential N+1 query patterns
- ⚡ Warns about large memory allocations
- ⚡ Checks for uncontrolled goroutines
- ⚡ Runs benchmarks if available
- ⚡ Labels: `performance`, `needs-optimization`

**Special behaviors:**
- If >3 issues detected: requests tech lead review
- If benchmarks show >20% degradation: blocks merge

### 🎨 Frontend Bots

#### Bot #3: Frontend UI/UX Compliance Bot
**File:** `.github/workflows/bot-frontend-ux.yml`

Ensures UI/UX consistency in Dart/Flutter code:
- 🎨 Validates file naming (snake_case)
- 🎨 Checks widget organization
- 🎨 Detects hardcoded UI strings
- 🎨 Verifies theme constant usage
- 🎨 Labels: `frontend`, `ui`, `a11y`

**Special behaviors:**
- If new screen added: requests navigation docs update
- If main widgets modified: notifies designers
- Generates visual change reports

#### Bot #4: Frontend Build & Asset Optimizer
**File:** `.github/workflows/bot-frontend-build.yml`

Optimizes frontend assets and build size:
- 📦 Tracks bundle size changes
- 📦 Identifies large images (>500KB)
- 📦 Detects non-tree-shakeable dependencies
- 📦 Auto-compresses PNGs with pngquant
- 📦 Auto-converts large JPGs to WebP
- 📦 Removes EXIF metadata
- 📦 Auto-commits optimizations
- 📦 Labels: `frontend`, `asset-optimization`, `bundle-size`

### 🤖 Coordination System

#### Bot Coordinator
**File:** `.github/workflows/bot-coordinator.yml`

Aggregates reports from all bots:
- 📊 Generates weekly summary reports
- 📊 Tracks total issues triaged
- 📊 Counts PRs auto-approved/blocked
- 📊 Measures optimizations applied
- 📊 Estimates time saved
- 📊 Detects bot conflicts

## Configuration Files

### `backend-quality-rules.json`
```json
{
  "quality_thresholds": {
    "min_test_coverage": 80,
    "max_function_length": 50,
    "max_cyclomatic_complexity": 10
  },
  "auto_approve": {
    "enabled": true,
    "require_tests": true,
    "require_docs": true,
    "min_quality_score": 90
  }
}
```

### `frontend-ux-guidelines.json`
```json
{
  "naming_conventions": {
    "files": "snake_case",
    "classes": "PascalCase",
    "widgets": "PascalCase"
  },
  "asset_limits": {
    "max_image_size_kb": 500,
    "max_bundle_increase_mb": 2
  }
}
```

## Scripts

Located in `scripts/` directory:

- **`analyze_go_code.py`** - Analyzes Go code for quality metrics
- **`analyze_dart_code.py`** - Analyzes Dart/Flutter code for UI/UX compliance
- **`compress_assets.sh`** - Compresses and optimizes image assets
- **`generate_report.py`** - Generates aggregated bot reports

## Slash Commands

Interact with bots via PR comments:

```markdown
/bot recheck          # Re-run analysis
/bot approve-force    # Manual approval (maintainers only)
/bot skip-quality     # Skip quality checks (requires justification)
/bot report           # Generate detailed report
/bot optimize-assets  # Re-run asset optimization
```

## Example Bot Comments

### Backend Quality Bot Comment:
```markdown
## 🤖 Backend Quality Report

**Quality Score:** 85/100 ✅

### ✅ Approved
- [x] Tests included (3 new tests)
- [x] Error handling correct
- [x] Imports clean

### ⚠️ Suggestions
- [ ] Function `ProcessBilling` (line 45) needs documentation
- [ ] Consider adding benchmark for `CalculateTotal`

**Estimated fix time:** 10 minutes

---
_Run `/bot recheck` after fixes_
```

### Frontend Build Bot Comment:
```markdown
## 🎨 Frontend Build Report

**Bundle Size:** 12.3 MB → 11.1 MB (-9.8%) ✅

### 🚀 Auto-Optimizations Applied
- ✅ Compressed 5 PNGs (saved: 890 KB)
- ✅ Converted hero_image.jpg to WebP (saved: 320 KB)

### 📊 Analysis
- Optimized commits: `a7b3c2d`
- Total assets: 47 files
- Images pending optimization: 0

**🏆 Great job keeping the bundle light!**
```

## Metrics & Success Tracking

Each bot tracks:
- Issues classified automatically
- PRs approved without human intervention
- Optimizations applied
- Time saved (estimated)

**Weekly Dashboard Example:**
```
📊 Bot Report - Week 50/2025

Backend Quality Guardian:
  - 12 PRs analyzed
  - 8 auto-approved
  - 47 issues detected
  - ⏱️ Time saved: ~4h

Backend Performance Monitor:
  - 5 PRs analyzed
  - 2 optimizations suggested
  - 0 critical degradations
  - ⏱️ Time saved: ~2h

Frontend UX Compliance:
  - 8 PRs reviewed
  - 14 hardcoded strings found
  - 3 a11y issues detected
  - ⏱️ Time saved: ~3h

Frontend Build Optimizer:
  - 23 assets optimized
  - Bundle size: -15%
  - ⏱️ Time saved: ~1.5h

🎯 TOTAL TIME SAVED: ~10.5 hours
```

## Security Considerations

- Bots **never** auto-merge (only approve)
- Optimization commits are signed
- Access to secrets is limited per bot
- All decisions are logged

## Integration with Existing Workflows

These bots complement existing workflows:
- **CI Pipeline** - Bots run alongside standard CI
- **Code Review** - Bots provide pre-review feedback
- **Future Jira Sync** - Bots can create/update tickets

## Maintenance

To update bot behavior:
1. Edit configuration JSON files
2. Update analysis scripts if needed
3. Modify workflow YAML files for trigger changes
4. Test changes in a feature branch first

## Support

For issues or questions about the bots:
- Create an issue with label `bot-support`
- Tag `@maintainers` in PR comments
- Check workflow run logs in Actions tab

---

*Last updated: 2025-12-14*
