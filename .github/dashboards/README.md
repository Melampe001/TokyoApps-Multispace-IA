# 📊 PR Metrics Dashboard

This directory contains the automated PR metrics dashboard and related resources for the TokyoApps Multispace IA project.

## 📁 Files

- **`PR_METRICS_DASHBOARD.md`** - Main dashboard with comprehensive PR metrics and analytics
- **`pr-dashboard.html`** - HTML version of the dashboard for web viewing
- **`README.md`** - This file, explaining the dashboard system

## 🎯 Purpose

The PR Metrics Dashboard provides real-time insights into:
- PR distribution by priority, size, and type
- Automation impact and ROI metrics
- Time metrics and performance tracking
- Code quality trends and hotspot analysis
- Team performance and contributor activity
- Actionable recommendations and KPIs

## 🔄 Automation

### Daily Updates

The dashboard is automatically updated daily via the **PR Dashboard Update** workflow:

- **Schedule**: Every day at 9:00 AM UTC
- **Workflow**: `.github/workflows/pr-dashboard-update.yml`
- **Trigger**: Can also be manually triggered via GitHub Actions UI

### What Gets Updated

The automated workflow:
1. Collects current PR metrics from GitHub API
2. Calculates key statistics (total PRs, stale PRs, etc.)
3. Updates the dashboard with fresh data
4. Commits changes automatically via `github-actions[bot]`

### Manual Trigger

To manually update the dashboard:

1. Go to **Actions** tab in GitHub
2. Select **"📊 Update PR Metrics Dashboard"** workflow
3. Click **"Run workflow"** button
4. Select branch and click **"Run workflow"**

## 📈 Key Metrics Tracked

### Primary Metrics
- **Total Open PRs**: Current count of all open pull requests
- **Stale PRs**: PRs older than 30 days without activity
- **PR Age Distribution**: How long PRs have been open
- **Merge Velocity**: Average time from open to merge
- **Review Efficiency**: Time to first review and approval

### Quality Metrics
- **Code Coverage**: Test coverage percentage
- **Automation Coverage**: Percentage of automated checks
- **Security Scan Results**: Security vulnerabilities detected
- **CI/CD Pass Rate**: Success rate of automated builds

### Team Metrics
- **Contributor Activity**: Commits, reviews, and PRs per contributor
- **Review Load**: Distribution of review responsibilities
- **Response Times**: First response and review completion times

## 🔧 Configuration

The dashboard workflow can be configured by editing:

```yaml
# .github/workflows/pr-dashboard-update.yml
on:
  schedule:
    - cron: '0 9 * * *'  # Modify this to change update schedule
```

### Cron Schedule Examples

- `'0 */6 * * *'` - Every 6 hours
- `'0 0 * * *'` - Daily at midnight UTC
- `'0 9 * * 1-5'` - Weekdays at 9 AM UTC

## 🛠️ Maintenance

### Adding New Metrics

To add new metrics to the dashboard:

1. Edit `.github/workflows/pr-dashboard-update.yml`
2. Add metric calculation in the `Collect metrics` step
3. Update the `Update dashboard` step to include new metrics
4. Test with manual workflow trigger

### Customizing Dashboard Format

The dashboard uses Markdown format with:
- **ASCII charts** for visual representation
- **Emojis** for status indicators
- **Tables** for structured data
- **Progress bars** using Unicode characters

## 📊 Reading the Dashboard

### Status Indicators

- 🟢 **Green**: Excellent/On track
- 🟡 **Yellow**: Needs attention/Warning
- 🔴 **Red**: Critical/Action required
- ⚡ **Lightning**: Fast/Optimal
- 🚨 **Alert**: High priority issue

### Priority Levels

- **P0/Critical**: Must be addressed immediately
- **P1/High**: High priority, address within 24-48 hours
- **P2/Medium**: Standard priority
- **P3/Low**: Nice to have, backlog items

### Size Categories

- **XS**: < 50 lines changed (quick reviews)
- **S**: 50-150 lines (optimal size)
- **M**: 150-400 lines (review intensive)
- **L**: 400-800 lines (consider splitting)
- **XL**: > 800 lines (high risk, should be split)

## 🔗 Related Resources

- [PR Guidelines](../PULL_REQUEST_GUIDELINES.md)
- [Automation Config](../pr-automation-config.yml)
- [Workflows README](../workflows/README.md)
- [Contributing Guide](../../CONTRIBUTING.md)

## 🚀 Usage Examples

### Check Current PR Status

Simply view `PR_METRICS_DASHBOARD.md` to see:
- How many PRs are currently open
- Which PRs need urgent attention
- Team capacity and bottlenecks
- Automation effectiveness

### Identify Bottlenecks

Look for:
- 🔴 High "Avg Age" in priority sections
- ⚠️ Capacity gaps in planning section
- 🚨 Critical bottlenecks in review section

### Track Progress

Monitor trends over time:
- Compare current metrics with previous updates
- Track KPI progress toward goals
- Identify improvement areas

## 🤝 Contributing

To improve the dashboard:

1. Create a feature branch
2. Make changes to workflow or dashboard template
3. Test changes with manual workflow run
4. Submit PR with clear description of changes
5. Request review from team leads

## 📞 Support

For questions or issues:
- Open an issue with label `dashboard` or `automation`
- Contact DevOps team via team chat
- Check workflow logs in Actions tab for errors

## 🔒 Permissions

The dashboard workflow requires:
- `contents: write` - To commit dashboard updates
- `pull-requests: read` - To fetch PR data from GitHub API

These permissions are scoped to the repository and use `GITHUB_TOKEN` automatically provided by GitHub Actions.

## 📝 Notes

- Dashboard data is cached and updated on schedule
- Manual triggers don't count against GitHub Actions quotas differently than scheduled runs
- Historical data is preserved in git history
- Dashboard is view-only; metrics calculation is automated

---

**Last Updated**: 2025-12-28  
**Version**: 1.0  
**Maintained by**: DevOps Team & GitHub Actions
