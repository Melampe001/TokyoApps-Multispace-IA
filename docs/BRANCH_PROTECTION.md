# Branch Protection Rules

This document describes the recommended branch protection rules for Tokyo-IA to maintain code quality and prevent accidental issues.

## Table of Contents

- [Overview](#overview)
- [Recommended Rules for Main Branch](#recommended-rules-for-main-branch)
- [Implementation Guide](#implementation-guide)
- [Rule Explanations](#rule-explanations)
- [Troubleshooting](#troubleshooting)

## Overview

Branch protection rules help maintain code quality by enforcing policies on branches. For Tokyo-IA, we primarily protect the `main` branch to ensure all changes go through proper review and testing.

## Recommended Rules for Main Branch

### 1. Require Pull Request Reviews

**Setting:** Require at least 1 approval before merging

**Why:** Ensures code review by another team member, catching bugs and maintaining code quality.

**Options:**
- ✅ Dismiss stale pull request approvals when new commits are pushed
- ✅ Require review from Code Owners (if CODEOWNERS file exists)
- ⚠️ Require approval of the most recent reviewable push

### 2. Require Status Checks

**Setting:** Require status checks to pass before merging

**Required Checks:**
- `android-ci` (when Android files change)
- `web-ci` (when Web files change)  
- `server-mcp-ci` (when Server files change)

**Options:**
- ✅ Require branches to be up to date before merging
- ✅ Require status checks to pass

**Why:** Ensures all tests pass and code builds successfully before merging.

### 3. Require Conversation Resolution

**Setting:** All conversations must be resolved before merging

**Why:** Ensures all review feedback is addressed before merging.

### 4. Require Signed Commits

**Setting:** Require commits to be signed with GPG/SSH

**Why:** Verifies commit author identity, preventing impersonation.

**Note:** This is optional but recommended for security-sensitive projects.

### 5. Require Linear History

**Setting:** Require linear history (prevent merge commits)

**Options:**
- Allow squash merging
- Allow rebase merging
- Disallow merge commits

**Why:** Maintains clean, readable git history.

### 6. Block Force Pushes

**Setting:** Do not allow force pushes

**Why:** Prevents accidental history rewrites and protects against data loss.

### 7. Block Deletions

**Setting:** Do not allow branch deletion

**Why:** Prevents accidental deletion of the main branch.

## Implementation Guide

### For Repository Administrators

1. Navigate to repository on GitHub
2. Click **Settings** → **Branches**
3. Under "Branch protection rules", click **Add rule**
4. In "Branch name pattern", enter: `main`
5. Configure the following settings:

#### Required Settings

```
✅ Require a pull request before merging
   ├── ✅ Require approvals: 1
   ├── ✅ Dismiss stale pull request approvals when new commits are pushed
   └── ✅ Require review from Code Owners (if CODEOWNERS exists)

✅ Require status checks to pass before merging
   ├── ✅ Require branches to be up to date before merging
   └── Add status checks:
       - android-ci
       - web-ci
       - server-mcp-ci

✅ Require conversation resolution before merging

✅ Require linear history

✅ Do not allow bypassing the above settings

✅ Restrict who can push to matching branches
   └── Select specific teams/users who can push directly (typically none)

✅ Block force pushes

✅ Do not allow deletions
```

#### Optional Settings

```
⚠️ Require deployments to succeed before merging
   (Enable when you have deployment workflows)

⚠️ Lock branch
   (Only enable temporarily for maintenance)

⚠️ Require signed commits
   (Recommended for security, but requires GPG setup)
```

6. Click **Create** or **Save changes**

### For Contributors

#### Setting Up GPG Signing (Optional)

If signed commits are required:

1. Generate GPG key:
   ```bash
   gpg --full-generate-key
   ```

2. List GPG keys:
   ```bash
   gpg --list-secret-keys --keyid-format=long
   ```

3. Export public key:
   ```bash
   gpg --armor --export YOUR_KEY_ID
   ```

4. Add to GitHub:
   - Go to GitHub Settings → SSH and GPG keys
   - Click "New GPG key"
   - Paste the public key

5. Configure Git:
   ```bash
   git config --global user.signingkey YOUR_KEY_ID
   git config --global commit.gpgsign true
   ```

#### Working with Protected Branches

1. **Always create a feature branch:**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Keep your branch updated:**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

3. **Push changes:**
   ```bash
   git push origin feature/my-feature
   ```

4. **Create Pull Request:**
   - Go to GitHub repository
   - Click "Pull requests" → "New pull request"
   - Select your branch
   - Fill in PR template
   - Request reviewers

5. **Address review feedback:**
   - Make requested changes
   - Push new commits
   - Resolve conversations
   - Request re-review if needed

6. **Merge when approved:**
   - Wait for approval(s)
   - Wait for CI checks to pass
   - Use "Squash and merge" or "Rebase and merge"
   - Delete branch after merging

## Rule Explanations

### Why Require Pull Request Reviews?

**Benefits:**
- Catches bugs before they reach main
- Shares knowledge across team
- Maintains consistent code style
- Provides documentation of why changes were made

**Best Practices:**
- Review code promptly
- Leave constructive feedback
- Ask questions if unclear
- Approve only when confident

### Why Require Status Checks?

**Benefits:**
- Prevents broken code from being merged
- Automates quality checks
- Provides consistent testing
- Catches issues early

**Best Practices:**
- Write comprehensive tests
- Keep CI fast
- Fix failing tests immediately
- Don't disable checks to merge

### Why Require Linear History?

**Benefits:**
- Easier to understand history
- Simpler to find when bugs were introduced
- Cleaner git log
- Easier to revert changes

**Best Practices:**
- Use squash merge for small changes
- Use rebase merge for clean feature branches
- Write meaningful commit messages

### Why Block Force Pushes?

**Benefits:**
- Prevents accidental history rewrites
- Protects against data loss
- Ensures everyone has same history

**Exceptions:**
- Never needed on protected branches
- Use interactive rebase on feature branches before merging

## Troubleshooting

### "Required status check is failing"

**Solution:**
1. Click "Details" to see the error
2. Fix the issue locally
3. Push new commit
4. Wait for checks to re-run

### "Branch is out of date"

**Solution:**
```bash
# Fetch latest changes
git fetch origin

# Rebase your branch
git checkout your-branch
git rebase origin/main

# Force push to your branch (your branch, not main!)
git push --force-with-lease origin your-branch
```

### "Need 1 approval"

**Solution:**
1. Request review from team members
2. Address any feedback
3. Wait for approval

### "Conversations must be resolved"

**Solution:**
1. Review all conversation threads
2. Address feedback or respond
3. Click "Resolve conversation" on each thread
4. Request re-review if needed

### "Commits must be signed"

**Solution:**
1. Set up GPG key (see above)
2. Sign previous commits:
   ```bash
   git rebase --exec 'git commit --amend --no-edit -S' -i origin/main
   git push --force-with-lease origin your-branch
   ```

### Can't push directly to main

**This is expected!** All changes must go through pull requests.

**Solution:**
1. Create a feature branch
2. Push changes to feature branch
3. Create pull request
4. Get approval and merge

## Bypassing Protection Rules

### When Necessary

In rare cases (emergency hotfixes, critical security patches), administrators may need to bypass rules.

### How to Bypass (Administrators Only)

1. Go to Settings → Branches
2. Edit branch protection rule
3. Check "Allow specified actors to bypass required pull requests"
4. Add specific users/teams
5. Save changes

**Important:** 
- Document why bypass was needed
- Create tracking issue
- Remove bypass access immediately after
- Create follow-up PR to properly review changes

### Logging

GitHub logs all rule bypasses. Administrators should regularly review:

1. Settings → Audit log
2. Filter by "branch protection bypass"
3. Verify all bypasses were legitimate

## Advanced: CODEOWNERS File

The CODEOWNERS file automatically requests reviews from specific people for certain files.

### Creating CODEOWNERS

Create `.github/CODEOWNERS`:

```
# Default owners for everything
* @Melampe001

# Android app owners
/app/ @android-team

# Web app owners  
/web/ @web-team

# Server owners
/server-mcp/ @backend-team

# CI/CD owners
/.github/workflows/ @devops-team

# Documentation owners
/docs/ @doc-team
*.md @doc-team
```

### CODEOWNERS Syntax

```
# File pattern followed by one or more owners

# By username
path/to/file @username

# By team
path/to/file @org/team-name  

# By email
path/to/file user@example.com

# Multiple owners
path/to/file @user1 @user2 @org/team

# Specific file
README.md @maintainers

# All files in directory
/docs/ @docs-team

# All files of type
*.js @js-team

# Override default
/app/src/test/ @qa-team
```

## Monitoring Branch Protection

### Regular Checks

Administrators should periodically verify:

1. **Protection rules are active**
   - Settings → Branches
   - Verify main branch has protection

2. **Status checks are current**
   - Review required status checks
   - Remove deprecated checks
   - Add new checks as needed

3. **Team access is appropriate**
   - Settings → Manage access
   - Review who can bypass rules
   - Update as team changes

4. **Rules are being followed**
   - Audit log for bypasses
   - Check for force pushes
   - Review closed PRs

### Metrics to Track

- Number of PRs merged
- Average time to merge
- Number of failed checks
- Number of rule bypasses
- Review participation

## References

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [About CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Signing Commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)
