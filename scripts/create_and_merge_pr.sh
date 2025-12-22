#!/usr/bin/env bash
# Crear PR desde copilot/final-testing-implementation -> Main, esperar CI y mergear (merge commit).
# Uso:
#   chmod +x scripts/create_and_merge_pr.sh
#   AUTO_MERGE=yes ./scripts/create_and_merge_pr.sh
#
set -euo pipefail

REPO="Melampe001/Tokyo-IA"
BASE_BRANCH="Main"
HEAD_BRANCH="copilot/final-testing-implementation"
PR_TITLE="Merge copilot/final-testing-implementation into Main"
read -r -d '' PR_BODY <<'PRBODY' || true
This PR integrates the final testing changes and CI adjustments from the branch `copilot/final-testing-implementation` into `Main`.

Note for reviewers: Please verify formatting and tests.

Checklist:
- [ ] Run `make fmt` and ensure code is formatted.
- [ ] Run `make test` and ensure all tests pass.
- [ ] Run `make lint` (or `golangci-lint run`) and ensure no blocking issues.
- [ ] Ensure CI status checks pass before merging.
PRBODY

AUTO_MERGE="${AUTO_MERGE:-no}"

command -v gh >/dev/null 2>&1 || { echo "gh CLI not found. Instálalo y autentícate (gh auth login)."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "git no encontrado."; exit 1; }
command -v make >/dev/null 2>&1 || { echo "make no encontrado."; exit 1; }

git fetch origin --prune

# Prepare head branch
# If remote branch exists, track it; otherwise create local branch
if git show-ref --verify --quiet refs/remotes/origin/${HEAD_BRANCH}; then
  git checkout -B "${HEAD_BRANCH}" "origin/${HEAD_BRANCH}"
else
  git checkout -B "${HEAD_BRANCH}"
fi

# Format and commit if necessary
make fmt
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "chore: apply gofmt"
fi

# Run tests locally
make test

# Push branch
git push origin "${HEAD_BRANCH}"

# Create PR or reuse existing
EXISTING_PR_NUMBER=$(gh pr list --repo "${REPO}" --head "${HEAD_BRANCH}" --base "${BASE_BRANCH}" --state open --json number -q '.[0].number' || true)
if [ -n "${EXISTING_PR_NUMBER}" ]; then
  PR_NUMBER="${EXISTING_PR_NUMBER}"
  echo "Using existing PR #${PR_NUMBER}"
else
  PR_URL=$(gh pr create --repo "${REPO}" --base "${BASE_BRANCH}" --head "${HEAD_BRANCH}" --title "${PR_TITLE}" --body "${PR_BODY}" --label "automated-pr" --json url | jq -r '.url')
  PR_NUMBER=$(basename "${PR_URL}")
  echo "PR created: ${PR_URL}"
fi

echo "Waiting for CI checks for PR #${PR_NUMBER}..."
if gh pr checks "${PR_NUMBER}" --repo "${REPO}" --watch --exit-status; then
  echo "All required checks passed for PR #${PR_NUMBER}."
  if [ "${AUTO_MERGE}" = "yes" ]; then
    echo "Merging PR #${PR_NUMBER} using merge commit (source branch will not be deleted)."
    gh pr merge "${PR_NUMBER}" --repo "${REPO}" --merge --delete-branch=false
    echo "Merged."
  else
    echo "CI green. Run again with AUTO_MERGE=yes to auto-merge, or merge manually now."
  fi
else
  echo "CI failed or timed out. Posting a comment and leaving PR open."
  gh pr comment "${PR_NUMBER}" --repo "${REPO}" --body "CI checks failed or timed out. Please review failing checks before merging."
fi
