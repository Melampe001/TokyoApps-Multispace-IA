# Imperial Cleaner Documentation

## Status: Not Found

After thorough investigation of the repository, the **Imperial Cleaner** workflow mentioned in the requirements could not be located.

## Investigation Summary

### Search Conducted

1. **Workflow Files**: Checked all files in `.github/workflows/`
2. **Git History**: Searched commit history for "imperial", "cleaner", "auto-merge"
3. **Configuration Files**: Reviewed all YAML and config files
4. **Documentation**: Checked existing docs for references

### Findings

- ❌ No workflow file named `imperial_cleaner.yml` or similar
- ❌ No git commits mentioning "imperial" or "cleaner"
- ❌ No configuration files related to auto-merge functionality
- ❌ No documentation referencing Imperial Cleaner

## Possible Explanations

1. **Planned Feature**: Imperial Cleaner may be a planned feature not yet implemented
2. **Renamed/Removed**: Previously existed but was removed or renamed
3. **Different Implementation**: Auto-merge functionality may be implemented differently
4. **External Tool**: May be referring to an external service or tool

## Alternative Auto-Merge Solutions

If you need auto-merge functionality for approved PRs, consider these alternatives:

### 1. GitHub Native Auto-Merge

GitHub provides built-in auto-merge:

**Enable Per Repository**:
1. Go to **Settings → General**
2. Scroll to **Pull Requests**
3. Enable **Allow auto-merge**

**Use in PR**:
```bash
gh pr merge <number> --auto --merge
```

Or click "Enable auto-merge" button in PR UI.

### 2. Mergify

Free GitHub app that auto-merges PRs based on rules.

**Configuration** (`.mergify.yml`):
```yaml
pull_request_rules:
  - name: Auto-merge on approval
    conditions:
      - "#approved-reviews-by>=2"
      - "#changes-requested-reviews-by=0"
      - "status-success=ci"
      - "status-success=security"
      - "base=main"
    actions:
      merge:
        method: squash
```

### 3. Custom GitHub Action

Create `.github/workflows/auto-merge.yml`:

```yaml
name: Auto-Merge Approved PRs

on:
  pull_request_review:
    types: [submitted]
  check_suite:
    types: [completed]

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    name: Auto-Merge
    runs-on: ubuntu-latest
    if: github.event.review.state == 'approved'
    
    steps:
      - name: Check PR status
        id: pr-status
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const pr = context.payload.pull_request;
            
            // Get PR details
            const { data: prData } = await github.rest.pulls.get({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: pr.number,
            });
            
            // Check reviews
            const { data: reviews } = await github.rest.pulls.listReviews({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: pr.number,
            });
            
            const approvals = reviews.filter(r => r.state === 'APPROVED').length;
            const changesRequested = reviews.filter(r => r.state === 'CHANGES_REQUESTED').length;
            
            // Check status checks
            const { data: statuses } = await github.rest.repos.getCombinedStatusForRef({
              owner: context.repo.owner,
              repo: context.repo.repo,
              ref: pr.head.sha,
            });
            
            const allPassed = statuses.state === 'success';
            
            // Determine if should merge
            const shouldMerge = approvals >= 2 && 
                               changesRequested === 0 && 
                               allPassed &&
                               !prData.draft;
            
            core.setOutput('should-merge', shouldMerge);
            core.setOutput('pr-number', pr.number);
      
      - name: Auto-merge PR
        if: steps.pr-status.outputs.should-merge == 'true'
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const prNumber = ${{ steps.pr-status.outputs.pr-number }};
            
            await github.rest.pulls.merge({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: prNumber,
              merge_method: 'squash',  // or 'merge', 'rebase'
            });
            
            console.log(`✅ Auto-merged PR #${prNumber}`);
```

### 4. Auto-Close Stale PRs

The existing **Stale Bot** (`.github/workflows/stale.yml`) already handles closing inactive PRs:

- Marks PRs stale after 60 days
- Closes after 7 additional days
- Runs daily at 00:00 UTC

This provides the "cleanup" aspect that may have been part of Imperial Cleaner.

## Recommended Implementation

If you want to implement an "Imperial Cleaner" equivalent:

### Scope

1. **Auto-Merge Approved PRs**:
   - 2+ approvals required
   - All status checks passing
   - No requested changes
   - Not a draft PR

2. **Close Stale PRs** (already implemented via stale.yml)

3. **Cleanup Old Branches**:
   - Delete branches after PR merge
   - Clean up preview deployments

### Proposed Workflow

Create `.github/workflows/imperial-cleaner.yml`:

```yaml
name: 🏛️ Imperial Cleaner

on:
  schedule:
    - cron: '0 6,18 * * *'  # 6:00 and 18:00 UTC
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  clean-approved:
    name: Merge Approved PRs
    runs-on: ubuntu-latest
    
    steps:
      - name: Find approved PRs
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const { data: prs } = await github.rest.pulls.list({
              owner: context.repo.owner,
              repo: context.repo.repo,
              state: 'open',
              base: 'main',
            });
            
            for (const pr of prs) {
              // Check if should merge (logic here)
              // Merge if criteria met
            }
  
  clean-stale:
    name: Close Stale PRs
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/stale@v9
        with:
          days-before-stale: 60
          days-before-close: 7
          # ... (config from stale.yml)
  
  clean-branches:
    name: Delete Merged Branches
    runs-on: ubuntu-latest
    
    steps:
      - name: Delete merged branches
        uses: actions/github-script@v7
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            // Find and delete merged branches
```

## Implementation Checklist

If you want to implement Imperial Cleaner:

- [ ] Decide on exact functionality needed
- [ ] Choose implementation approach (native, Mergify, or custom)
- [ ] Create workflow file
- [ ] Configure rules and permissions
- [ ] Test with a test PR
- [ ] Document behavior
- [ ] Monitor execution logs
- [ ] Update this documentation

## Current Status

**Action Required**: 
- Clarify if Imperial Cleaner is needed
- Define exact requirements
- Approve implementation approach

**Alternatives Available**:
- ✅ Stale bot (already active)
- ⚙️ GitHub native auto-merge (needs enabling)
- 🔧 Custom workflow (can be created)

## Questions to Answer

1. **What should Imperial Cleaner do?**
   - Auto-merge approved PRs?
   - Close stale PRs? (already done by stale.yml)
   - Delete old branches?
   - Clean up deployments?
   - All of the above?

2. **What are the merge criteria?**
   - Number of approvals required?
   - Which status checks must pass?
   - Any label requirements?
   - Exclude certain branches?

3. **What is the schedule?**
   - Twice daily (as mentioned)?
   - On-demand only?
   - After each PR review?

4. **Who can trigger it?**
   - Automatic only?
   - Manual dispatch allowed?
   - Specific team members?

## Next Steps

1. **Clarify Requirements**: Determine exact functionality needed
2. **Choose Approach**: Select implementation method
3. **Create Workflow**: Implement chosen solution
4. **Test Thoroughly**: Verify behavior with test PRs
5. **Document**: Update this file with actual implementation
6. **Monitor**: Watch logs for first few runs

## Contact

For questions about implementing Imperial Cleaner:
- File an issue in this repository
- Tag: `@Melampe001`
- Label: `enhancement`, `automation`

---

**Last Updated**: December 2024  
**Status**: Not Implemented (Investigation Complete)
