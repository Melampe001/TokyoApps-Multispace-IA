# Branch Protection Rules

This document describes the recommended branch protection configuration for the Tokyo-IA repository.

## Protected Branches

The following branches should be protected:
- `main` - Production branch
- `develop` - Development integration branch

## Recommended Settings for `main`

### Branch Protection Rules
1. **Require a pull request before merging**
   - ✅ Require approvals: 1 (minimum)
   - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ Require review from Code Owners (if CODEOWNERS file exists)

2. **Require status checks to pass before merging**
   - ✅ Require branches to be up to date before merging
   - Required status checks:
     - `lint-and-build` (from CI workflow)

3. **Require conversation resolution before merging**
   - ✅ Enabled

4. **Do not allow bypassing the above settings**
   - ✅ Enabled (optional, for stricter control)

5. **Restrict who can push to matching branches**
   - Only allow merges through pull requests

6. **Do not allow deletions**
   - ✅ Enabled

## Recommended Settings for `develop`

### Branch Protection Rules
1. **Require a pull request before merging**
   - ✅ Require approvals: 1 (minimum)
   - ✅ Dismiss stale pull request approvals when new commits are pushed

2. **Require status checks to pass before merging**
   - ✅ Require branches to be up to date before merging
   - Required status checks:
     - `lint-and-build` (from CI workflow)

3. **Do not allow deletions**
   - ✅ Enabled

## How to Configure Branch Protection

1. Go to **Settings** → **Branches** in the GitHub repository
2. Click **Add rule** or edit an existing rule
3. Enter the branch name pattern (e.g., `main` or `develop`)
4. Configure the settings as described above
5. Click **Create** or **Save changes**

## Branch Protection Configuration (via GitHub API)

For automation, you can use the GitHub API or CLI:

```bash
# Using GitHub CLI (gh)
gh api repos/Melampe001/Tokyo-IA/branches/main/protection \
  --method PUT \
  -f required_status_checks='{"strict":true,"contexts":["lint-and-build"]}' \
  -f enforce_admins=false \
  -f required_pull_request_reviews='{"dismiss_stale_reviews":true,"require_code_owner_reviews":false,"required_approving_review_count":1}' \
  -f restrictions=null
```

## Additional Recommendations

### CODEOWNERS File
Consider adding a `.github/CODEOWNERS` file to automatically assign reviewers:

```
# Example CODEOWNERS
*       @Melampe001
/web/   @Melampe001
/app/   @Melampe001
```

### Rulesets (Alternative to Branch Protection)

GitHub Rulesets provide more flexibility than traditional branch protection. Consider using rulesets for:
- Repository-wide rules
- More granular control over bypass permissions
- Tag protection

## Related Documentation

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Contributing Guide](CONTRIBUTING.md)
- [CI Workflow](../.github/workflows/ci.yml)
