# 🔄 PR Automation System - Flow Diagrams

## Complete System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PR AUTOMATION SYSTEM                             │
│                                                                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │Auto-Labeler│  │  Triage    │  │Auto-Merger │  │  Cleanup   │   │
│  │            │  │            │  │            │  │            │   │
│  │ • Size     │  │ • Priority │  │ • Fast-    │  │ • Stale    │   │
│  │ • Type     │  │ • Reviewers│  │   Track    │  │ • Duplicate│   │
│  │ • Language │  │ • Welcome  │  │ • Validate │  │ • Conflicts│   │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘   │
│       ↓               ↓               ↓               ↓             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              CENTRAL CONFIGURATION                           │  │
│  │         .github/pr-automation-config.yml                     │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                              ↑                                      │
│                              │                                      │
│                      ┌───────────────┐                             │
│                      │ Bot Commands  │                             │
│                      │               │                             │
│                      │ • /merge      │                             │
│                      │ • /ready      │                             │
│                      │ • /priority   │                             │
│                      │ • /retest     │                             │
│                      │ • /duplicate  │                             │
│                      │ • /assign     │                             │
│                      └───────────────┘                             │
└─────────────────────────────────────────────────────────────────────┘
```

## PR Lifecycle Flow

```
                          ┌─────────────┐
                          │   PR Opened │
                          └──────┬──────┘
                                 │
                    ┌────────────┴────────────┐
                    ↓                         ↓
            ┌───────────────┐         ┌──────────────┐
            │ Auto-Labeler  │         │   Triage     │
            │               │         │              │
            │ Runs: On PR   │         │ Runs: On PR  │
            │ change        │         │ open/reopen  │
            └───────┬───────┘         └──────┬───────┘
                    │                        │
                    └────────────┬───────────┘
                                 ↓
                    ┌─────────────────────────┐
                    │    PR Labeled + Triaged │
                    │                         │
                    │ Labels: size/*, type/*  │
                    │         lang/*, priority│
                    │ Assigned: Reviewers     │
                    │ Comment: Welcome msg    │
                    └────────────┬────────────┘
                                 │
                                 ↓
                        ┌─────────────────┐
                        │  Developer Work │
                        │                 │
                        │ • Push commits  │
                        │ • Address review│
                        │ • Run tests     │
                        └────────┬────────┘
                                 │
                                 ↓
                     ┌───────────────────────┐
                     │  Status Checks Pass?  │
                     └───────┬───────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                   YES               NO
                    │                 │
                    ↓                 ↓
         ┌──────────────────┐   ┌─────────────┐
         │  Auto-Merger     │   │    Wait     │
         │                  │   │             │
         │ Runs: Every 30min│   │ Until fixed │
         │       On reviews │   └─────────────┘
         │       On checks  │
         └────────┬─────────┘
                  │
         ┌────────┴─────────┐
         │                  │
    Fast-Track?          Normal?
         │                  │
         ↓                  ↓
    ┌─────────┐      ┌──────────────┐
    │ Merge   │      │ Wait 1 hour  │
    │ Now     │      │ + Comment    │
    └────┬────┘      └──────┬───────┘
         │                  │
         └────────┬─────────┘
                  ↓
           ┌──────────────┐
           │   Merged ✅  │
           └──────────────┘
```

## Auto-Labeler Detail

```
PR Changed
    │
    ├─→ Count Lines Changed
    │       │
    │       ├─→ 0-10: size/XS
    │       ├─→ 11-100: size/S
    │       ├─→ 101-500: size/M
    │       ├─→ 501-1000: size/L
    │       ├─→ 1001-5000: size/XL
    │       └─→ 5000+: size/XXL (+ warning comment)
    │
    ├─→ Check File Paths
    │       │
    │       ├─→ **/*.md: type/documentation
    │       ├─→ **/*_test.*: type/tests
    │       ├─→ .github/workflows/**: type/ci-cd
    │       ├─→ agents/**: type/agents
    │       └─→ infrastructure/**: type/infrastructure
    │
    └─→ Check File Extensions
            │
            ├─→ *.go: lang/go
            ├─→ *.py: lang/python
            ├─→ *.js, *.ts: lang/javascript
            ├─→ *.kt: lang/kotlin
            └─→ *.sh: lang/shell
```

## Auto-Merger Decision Tree

```
PR Ready?
    │
    ├─→ Is Draft? ──YES──→ Skip
    │       │
    │      NO
    │       │
    ├─→ Status Checks Passed? ──NO──→ Skip
    │       │
    │      YES
    │       │
    ├─→ Reviews Approved? ──NO──→ Skip
    │       │
    │      YES
    │       │
    ├─→ Changes Requested? ──YES──→ Skip
    │       │
    │      NO
    │       │
    ├─→ Has Conflicts? ──YES──→ Skip
    │       │
    │      NO
    │       │
    └─→ Fast-Track Eligible?
            │
            ├─→ YES: Documentation only (<500 lines, 0 reviews)
            │        Linter fixes (<100 lines, "lint" in title)
            │        Dependabot updates
            │        Copilot small docs (size/S, author=copilot)
            │           │
            │           └─→ Merge NOW with squash
            │
            └─→ NO: Normal PR
                    │
                    ├─→ Wait 1 hour since created
                    │       │
                    │      NO ──→ Post "Ready" comment
                    │       │
                    │      YES
                    │       │
                    └─→ Select merge method
                            │
                            ├─→ size/XS → squash
                            ├─→ type/documentation → squash
                            ├─→ hotfix label → squash
                            └─→ Default → merge
                                    │
                                    └─→ MERGE ✅
```

## Cleanup Workflow

```
Daily at 2 AM
    │
    ├─→ Scan All Open PRs
    │       │
    │       ├─→ Check Last Update
    │       │       │
    │       │       ├─→ >30 days (normal PR)
    │       │       │   or >45 days (draft)
    │       │       │       │
    │       │       │       └─→ Has exclusion label? (wip/blocked/on-hold)
    │       │       │               │
    │       │       │              NO
    │       │       │               │
    │       │       │               ├─→ Add 'stale' label
    │       │       │               ├─→ Post comment asking if still needed
    │       │       │               └─→ Close after 7 more days if no response
    │       │       │
    │       │       └─→ <30/45 days → Skip
    │       │
    │       ├─→ Compare with Other PRs
    │       │       │
    │       │       └─→ Title similarity >80%
    │       │           + File overlap >70%
    │       │               │
    │       │               └─→ Add 'duplicate' label
    │       │                   Post comment suggesting review
    │       │
    │       └─→ Check Mergeability
    │               │
    │               └─→ Has conflicts?
    │                       │
    │                       └─→ Add 'merge-conflict' label
    │                           Post instructions to resolve
    │
    └─→ Generate Report
            │
            └─→ Create/Update Issue
                    │
                    ├─→ Summary stats
                    ├─→ List of candidates
                    ├─→ Reasons for each
                    └─→ Direct links
```

## Triage Workflow

```
PR Opened/Reopened
    │
    ├─→ Analyze Title
    │       │
    │       ├─→ Contains "hotfix"/"security"/"critical" → priority/P0
    │       ├─→ Contains "bug"/"fix" → priority/P1
    │       ├─→ Contains "feat"/"feature" → priority/P2
    │       └─→ Contains "docs"/"documentation" → priority/P3
    │
    ├─→ Check Files Changed
    │       │
    │       └─→ go.mod, package.json, requirements.txt → priority/P1
    │
    ├─→ Assign Reviewers by Path
    │       │
    │       ├─→ **/*.go, go.mod → @Melampe001
    │       ├─→ agents/** → @Melampe001
    │       └─→ .github/workflows/** → @Melampe001
    │
    ├─→ Gather Statistics
    │       │
    │       ├─→ Calculate size (lines)
    │       ├─→ Count files changed
    │       ├─→ Check test status
    │       ├─→ Estimate review time
    │       └─→ Identify change types
    │
    └─→ Post Welcome Comment
            │
            ├─→ Greet author
            ├─→ Show PR summary table
            ├─→ List assigned reviewers
            └─→ Note bot commands available
```

## Bot Commands Flow

```
Comment Posted on PR
    │
    ├─→ Parse Comment
    │       │
    │       └─→ Starts with /? ──NO──→ Ignore
    │               │
    │              YES
    │               │
    │               └─→ Extract command + args
    │
    ├─→ Validate Command
    │       │
    │       └─→ Known command? ──NO──→ Reply with error + list
    │               │
    │              YES
    │               │
    │               └─→ Get required permission
    │
    ├─→ Check User Permission
    │       │
    │       ├─→ /merge requires 'write'
    │       └─→ Others require 'read'
    │               │
    │               └─→ Has permission? ──NO──→ Reply with error
    │                       │
    │                      YES
    │                       │
    │                       └─→ Execute Command
    │
    └─→ Execute Action
            │
            ├─→ /merge
            │       └─→ Merge PR immediately
            │
            ├─→ /ready
            │       └─→ Mark as ready for review
            │
            ├─→ /retest
            │       └─→ Re-run CI checks
            │
            ├─→ /priority <P0-P3>
            │       └─→ Change priority label
            │
            ├─→ /duplicate #<num>
            │       └─→ Add duplicate label + link
            │
            └─→ /assign @<user>
                    └─→ Request review from user
                            │
                            └─→ Reply with result
```

## Schedule Overview

```
Continuous (On Events):
├─→ pr-auto-labeler: On PR changes
├─→ pr-triage: On PR open/reopen
├─→ pr-bot-commands: On comment created
└─→ pr-auto-merger: On PR changes, reviews, check completion

Scheduled:
├─→ pr-auto-merger: Every 30 minutes (*/30 * * * *)
└─→ pr-cleanup: Daily at 2 AM (0 2 * * *)

Manual (workflow_dispatch):
├─→ pr-auto-merger: Run on demand
└─→ pr-cleanup: Run on demand
```

## Labels Hierarchy

```
Size Labels (Mutually Exclusive)
├─→ size/XS    (0-10 lines)
├─→ size/S     (11-100 lines)
├─→ size/M     (101-500 lines)
├─→ size/L     (501-1000 lines)
├─→ size/XL    (1001-5000 lines)
└─→ size/XXL   (5000+ lines)

Type Labels (Multiple Possible)
├─→ type/documentation
├─→ type/tests
├─→ type/ci-cd
├─→ type/agents
└─→ type/infrastructure

Language Labels (Multiple Possible)
├─→ lang/go
├─→ lang/python
├─→ lang/javascript
├─→ lang/kotlin
└─→ lang/shell

Priority Labels (Mutually Exclusive)
├─→ priority/P0  (Critical - hotfix, security)
├─→ priority/P1  (High - bugs, important fixes)
├─→ priority/P2  (Normal - features)
└─→ priority/P3  (Low - documentation)

Status Labels
├─→ stale               (Inactive PR)
├─→ duplicate           (Duplicate of another PR)
├─→ merge-conflict      (Has merge conflicts)
└─→ security-review-required  (Changes sensitive files)
```

## Integration Points

```
GitHub Events → Workflows
    │
    ├─→ pull_request
    │       └─→ [opened, synchronize, reopened, edited]
    │           └─→ pr-auto-labeler, pr-auto-merger
    │
    ├─→ pull_request
    │       └─→ [opened, reopened]
    │           └─→ pr-triage
    │
    ├─→ check_suite
    │       └─→ [completed]
    │           └─→ pr-auto-merger
    │
    ├─→ pull_request_review
    │       └─→ [submitted]
    │           └─→ pr-auto-merger
    │
    ├─→ issue_comment
    │       └─→ [created]
    │           └─→ pr-bot-commands
    │
    └─→ schedule
            ├─→ */30 * * * * → pr-auto-merger
            └─→ 0 2 * * * → pr-cleanup

Workflows → GitHub API
    │
    ├─→ github.rest.issues.addLabels()
    ├─→ github.rest.issues.removeLabel()
    ├─→ github.rest.issues.createComment()
    ├─→ github.rest.pulls.merge()
    ├─→ github.rest.pulls.update()
    ├─→ github.rest.pulls.listFiles()
    ├─→ github.rest.pulls.listReviews()
    ├─→ github.rest.pulls.requestReviewers()
    ├─→ github.rest.checks.listForRef()
    └─→ github.rest.repos.getCollaboratorPermissionLevel()

Configuration → Workflows
    │
    └─→ .github/pr-automation-config.yml
            │
            ├─→ auto_labels (sizes, types, languages)
            ├─→ auto_merge (fast-track rules, merge methods)
            ├─→ duplicate_detection (thresholds)
            ├─→ cleanup (stale days, exclusions)
            ├─→ triage (priority rules, reviewer routing)
            └─→ bot (command definitions, messages)
```

---

**Note:** All diagrams are ASCII art for maximum compatibility. For visual diagrams, see the Mermaid charts in [PR_AUTOMATION.md](PR_AUTOMATION.md).
