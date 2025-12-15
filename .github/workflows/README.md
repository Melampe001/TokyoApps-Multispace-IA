# GitHub Workflows Documentation

This directory contains automated workflows for project monitoring and reporting.

## 📋 Available Workflows

### 1. Blocker Detector (`blocker-detector.yml`)

**Purpose:** Automatically detect and report stalled work items to prevent bottlenecks.

**Schedule:** Runs daily, Monday through Friday at 9:00 AM UTC

**What it detects:**
- 📝 **Draft Pull Requests** that haven't been updated in more than 3 days
- 🐛 **Open Issues** without updates for more than 5 days

**Actions taken:**
- Creates a GitHub issue with detailed blocker report (only if blockers are found)
- Optionally sends Slack notification (if configured)
- Labels the issue with `blocker-alert` and `automated`

**Issue format:**
- Lists all stalled draft PRs with links, days stalled, and author
- Lists all stalled issues with links, days stalled, and assignees
- Provides actionable recommendations

### 2. Weekly Report (`weekly-report.yml`)

**Purpose:** Generate comprehensive weekly project metrics and health report.

**Schedule:** Runs every Friday at 15:00 UTC (3:00 PM)

**Metrics collected:**
- 📊 **Development Activity**
  - Number of commits pushed
  - Pull requests opened vs merged
  - Issues closed
  - Team velocity (% of PRs completed)
  
- 🏥 **Project Health**
  - Active blocker count
  - Health status: 🟢 Excellent (0 blockers), 🟡 Good (1-2), 🔴 Needs Attention (3+)
  
- 👥 **Contributors**
  - Top contributors by commit count

**Report sections:**
1. **Achievements** - Summary of work completed during the week
2. **Blockers** - Table of current stalled items
3. **Metrics Summary** - Quantitative overview
4. **Recommendations** - Context-aware suggestions

**Issue format:**
- Professional markdown report with tables and emojis
- Direct links to all referenced PRs and issues
- Labels: `weekly-report`, `automated`

## 🚀 How to Use

### Viewing Reports

1. **Blocker Alerts:** Navigate to Issues tab and filter by label `blocker-alert`
2. **Weekly Reports:** Navigate to Issues tab and filter by label `weekly-report`

### Manual Execution

Both workflows can be triggered manually for testing or on-demand reports:

1. Go to **Actions** tab in your repository
2. Select the workflow (`Blocker Detector` or `Weekly Report`)
3. Click **Run workflow** button
4. Select the branch (usually `main`)
5. Click **Run workflow**

The workflow will execute immediately and create an issue with results.

### Interpreting Health Status

| Status | Emoji | Blocker Count | Action Needed |
|--------|-------|---------------|---------------|
| Excellent | 🟢 | 0 | Keep up the great work! |
| Good | 🟡 | 1-2 | Monitor blockers, address if persisting |
| Needs Attention | 🔴 | 3+ | Schedule sync meeting, prioritize unblocking |

## ⚙️ Configuration

### Required Permissions

Both workflows use `GITHUB_TOKEN` which is automatically provided by GitHub Actions. No additional configuration needed for basic functionality.

**Permissions used:**
- `issues: write` - Create blocker alerts and weekly reports
- `pull-requests: read` - Read PR data for metrics
- `contents: read` - Access repository data

### Optional: Slack Notifications

The Blocker Detector can send notifications to Slack when blockers are found.

**Setup:**

1. Create a Slack webhook URL:
   - Go to https://api.slack.com/messaging/webhooks
   - Create a new webhook for your channel
   - Copy the webhook URL

2. Add the webhook as a GitHub secret:
   - Go to repository **Settings** > **Secrets and variables** > **Actions**
   - Click **New repository secret**
   - Name: `SLACK_WEBHOOK_URL`
   - Value: Paste your webhook URL
   - Click **Add secret**

3. The workflow will automatically use the webhook if present

**Note:** Slack integration is completely optional. The workflows work perfectly without it.

## 🔧 Customization

### Adjusting Thresholds

To change what qualifies as "stalled":

**Blocker Detector:**
- Edit line with `threeDaysAgo` to adjust draft PR threshold
- Edit line with `fiveDaysAgo` to adjust issue threshold

**Weekly Report:**
- Edit health status ranges in Python script
- Modify recommendations based on your team's needs

### Changing Schedule

Both workflows use cron syntax for scheduling:

```yaml
on:
  schedule:
    - cron: '0 9 * * 1-5'  # Example: 9 AM UTC, weekdays
```

**Cron format:** `minute hour day month weekday`

Examples:
- `'0 9 * * 1-5'` - 9 AM UTC, Monday-Friday
- `'0 15 * * 5'` - 3 PM UTC, Fridays only
- `'0 10 * * *'` - 10 AM UTC, every day

Use [crontab.guru](https://crontab.guru/) to help build cron expressions.

## 📊 Expected Benefits

**Time Savings:**
- Estimated 3.5 hours per week saved on manual tracking
- Automatic identification of work that needs attention
- Proactive blocker detection

**Improved Visibility:**
- Weekly quantitative metrics
- Trend tracking over time
- Early warning system for bottlenecks

**Better Collaboration:**
- Clear communication of project status
- Automatic notifications keep team aligned
- Data-driven sprint retrospectives

## 🐛 Troubleshooting

### Workflow not running

1. Check that the workflow file is on the default branch (`main`)
2. Verify the cron schedule is correct for your timezone
3. Ensure repository has Actions enabled (Settings > Actions)

### No issues being created

**Blocker Detector:** This is expected if no blockers exist! The workflow only creates issues when it finds stalled work.

**Weekly Report:** Check the Actions logs for errors. Ensure the workflow has proper permissions.

### Slack notifications not working

1. Verify `SLACK_WEBHOOK_URL` secret is set correctly
2. Test the webhook URL manually using `curl`
3. Check workflow logs for error messages

## 📝 Maintenance

These workflows are designed to be low-maintenance:

- **No dependencies to update** (uses official GitHub actions)
- **Self-documenting** (issues include timestamps and metadata)
- **Fail-safe** (won't block other workflows if they fail)

**Recommended review cadence:**
- Monthly: Review if thresholds need adjustment
- Quarterly: Check if reports remain useful
- As needed: Customize based on team feedback

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub REST API](https://docs.github.com/en/rest)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [Slack Webhooks Guide](https://api.slack.com/messaging/webhooks)

---

*For questions or suggestions about these workflows, please open an issue with the label `workflow-feedback`.*
