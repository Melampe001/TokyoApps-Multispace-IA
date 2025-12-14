# Google Sheets Dashboard Setup Guide

This guide walks you through setting up the live Google Sheets dashboard for tracking repository metrics.

## Overview

The Google Sheets dashboard provides real-time visibility into:
- Daily metrics (issues, PRs, commits, quality scores)
- Weekly trends (velocity, closed items, lead time)
- Team performance (contributor stats, rankings)
- Bot activity reports
- Executive dashboard (high-level KPIs)

## Prerequisites

- Google account with access to Google Sheets
- Google Cloud Platform project (free tier is sufficient)
- Admin access to GitHub repository

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a project** → **New Project**
3. Name it "Tokyo-IA Dashboard" (or your preference)
4. Click **Create**

## Step 2: Enable Google Sheets API

1. In Google Cloud Console, go to **APIs & Services** → **Library**
2. Search for "Google Sheets API"
3. Click on it and press **Enable**
4. Wait for the API to be enabled (takes a few seconds)

## Step 3: Create Service Account

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **Service Account**
3. Fill in details:
   - **Service account name**: `tokyo-ia-sheets-bot`
   - **Service account ID**: `tokyo-ia-sheets-bot` (auto-filled)
   - **Description**: "Service account for GitHub Actions to update dashboard"
4. Click **Create and Continue**
5. Grant role: **No role needed** (we'll grant access at sheet level)
6. Click **Continue** then **Done**

## Step 4: Create Service Account Key

1. Click on the newly created service account
2. Go to the **Keys** tab
3. Click **Add Key** → **Create new key**
4. Select **JSON** format
5. Click **Create**
6. Save the downloaded JSON file securely (this contains credentials)

**⚠️ Security Warning**: This JSON file contains sensitive credentials. Never commit it to Git!

## Step 5: Create Google Sheet

### Option A: Use Template (Recommended)

1. Create a new Google Sheet
2. Name it "Tokyo-IA Dashboard"
3. Create the following tabs:
   - `Daily_Metrics`
   - `Weekly_Trends`
   - `Team_Performance`
   - `Bot_Reports`
   - `Executive_Dashboard`

### Tab Structures

#### Daily_Metrics Tab

Headers (Row 1):
```
Date | Open Issues | Open PRs | Commits 24h | PRs Merged | Test Coverage | Avg PR Age | Quality Score
```

#### Weekly_Trends Tab

Headers (Row 1):
```
Week | Issues Closed | PRs Merged | Velocity | New Bugs | Lead Time (days)
```

#### Team_Performance Tab

Headers (Row 1):
```
Contributor | Commits | PRs Opened | PRs Merged | Reviews Done | Quality Score
```

#### Bot_Reports Tab

Headers (Row 1):
```
Bot Name | Issues Triaged | Auto-Approvals | Optimizations | Time Saved (hours)
```

#### Executive_Dashboard Tab

Headers (Row 1):
```
Metric | Value
```

### Option B: Copy Template Sheet

If available, make a copy of the template sheet and skip manual tab creation.

## Step 6: Share Sheet with Service Account

1. Open your Google Sheet
2. Click **Share** button
3. Copy the email from the service account JSON (field: `client_email`)
   - It looks like: `tokyo-ia-sheets-bot@project-id.iam.gserviceaccount.com`
4. Paste it in the share dialog
5. Set permission to **Editor**
6. **Uncheck** "Notify people" (it's a bot account)
7. Click **Share**

## Step 7: Get Sheet ID

The Sheet ID is in the URL:
```
https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
                                        ^^^^^^^^^^^^^^^^
```

Copy this ID for the next step.

## Step 8: Configure GitHub Secrets

Add the following secrets to your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**

### Add GOOGLE_CREDENTIALS

1. Name: `GOOGLE_CREDENTIALS`
2. Value: Paste the **entire contents** of the JSON file from Step 4
3. Click **Add secret**

### Add GOOGLE_SHEET_ID

1. Name: `GOOGLE_SHEET_ID`
2. Value: The Sheet ID from Step 7
3. Click **Add secret**

## Step 9: Configure Update Schedule

The dashboard updates automatically on:
- Every 2 hours (scheduled)
- Push to main branch
- PR merged
- Issue closed
- Manual trigger

To adjust the schedule, edit `.github/workflows/sheets-dashboard-update.yml`:

```yaml
schedule:
  - cron: '0 */2 * * *'  # Change to your preferred interval
```

Cron examples:
- Every hour: `'0 * * * *'`
- Every 6 hours: `'0 */6 * * *'`
- Once daily at 9 AM: `'0 9 * * *'`

## Step 10: Customize Metrics

Edit `.github/workflows/config/integrations.json`:

```json
"google_sheets": {
  "enabled": true,
  "update_interval_hours": 2,
  "real_time_events": ["push", "pull_request", "issues"],
  "metrics_retention_days": 90
}
```

## Step 11: Test the Integration

### Manual Test

Trigger the workflow manually:

```bash
gh workflow run sheets-dashboard-update.yml
```

Or via GitHub UI:
1. Go to **Actions** tab
2. Select **Google Sheets Dashboard Update**
3. Click **Run workflow**
4. Click **Run workflow** button

### Verify Update

1. Check the workflow run completes successfully
2. Open your Google Sheet
3. Verify data appears in the tabs
4. Check formatting is applied (colored cells)

## Conditional Formatting

The dashboard automatically applies color coding:

### Quality Score Colors

- **Green** (≥85): Good quality
- **Yellow** (70-84): Needs improvement
- **Red** (<70): Requires attention

### Velocity Colors

- **Bright Green** (>1.5x): Excellent
- **Green** (0.8-1.5x): On track
- **Yellow** (0.5-0.8x): Below target
- **Red** (<0.5x): Critical

### Blocker Colors

- **Green** (0): No blockers
- **Yellow** (1-2): Monitor
- **Red + Bold** (3+): Urgent attention needed

## Dashboard Usage

### Daily Metrics Tab

Track day-to-day activity:
- Monitor open issues and PRs
- Track daily commit velocity
- Observe quality trends

### Weekly Trends Tab

View aggregated weekly data:
- Sprint velocity
- Issue closure rate
- Team capacity utilization

### Team Performance Tab

Analyze individual contributions:
- Commit counts per developer
- PR creation and merge rates
- Code review participation
- Quality scores by contributor

### Executive Dashboard Tab

High-level KPIs for leadership:
- Current sprint health
- Quality score trends
- Active blocker count
- Team capacity metrics

## Creating Charts

### Add a Line Chart for Quality Score Trend

1. Select data from `Daily_Metrics` tab (Date and Quality Score columns)
2. Click **Insert** → **Chart**
3. Choose **Line chart**
4. Customize title, axis labels
5. Move chart to `Executive_Dashboard` tab

### Add a Bar Chart for Team Performance

1. Select data from `Team_Performance` tab
2. Click **Insert** → **Chart**
3. Choose **Bar chart**
4. Show commits per contributor
5. Sort by commits (descending)

## Advanced Configuration

### Custom Metrics

To add custom metrics, modify `.github/workflows/scripts/sheets_updater.py`:

```python
def update_daily_metrics(sheets: SheetsUpdater, github: GitHubMetricsCollector):
    metrics = [
        datetime.utcnow().strftime('%Y-%m-%d'),
        github.get_open_issues_count(),
        # Add your custom metric here
        github.get_custom_metric(),
    ]
    sheets.append_row('Daily_Metrics', metrics)
```

### Integration with Jira

If Jira sync is enabled, velocity data is pulled from Jira:

```python
# In sheets_updater.py
jira_metrics = JiraMetricsCollector()
velocity = jira_metrics.get_sprint_velocity()
```

## Monitoring

### View Update Logs

1. Go to **Actions** tab
2. Select **Google Sheets Dashboard Update** workflow
3. View recent runs and logs
4. Check for errors or warnings

### Health Checks

Automatic health checks run every 30 minutes:
- Tests Google Sheets write access
- Verifies service account permissions
- Creates alert if updates fail

## Troubleshooting

### Common Issues

**Issue**: "Permission denied" error
- Verify service account email is shared with Editor access
- Check `GOOGLE_CREDENTIALS` secret is set correctly
- Ensure Google Sheets API is enabled

**Issue**: "Invalid credentials" error
- Regenerate service account key
- Update `GOOGLE_CREDENTIALS` secret
- Verify JSON format is valid

**Issue**: Data not updating
- Check workflow runs are successful
- Verify `GOOGLE_SHEET_ID` is correct
- Ensure sheet tabs have correct names

**Issue**: Formatting not applied
- Check sheets_formatter.py is executed
- Verify tab names match exactly
- Review conditional formatting rules

For more help, see [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

## Security Best Practices

1. **Never commit credentials**: Keep JSON file secure and out of Git
2. **Use dedicated service account**: Don't use personal Google account
3. **Limit sheet sharing**: Only share with necessary users
4. **Rotate keys regularly**: Regenerate service account keys periodically
5. **Monitor access**: Review Google Cloud audit logs

## Data Retention

Configure retention policy in `integrations.json`:

```json
"metrics_retention_days": 90  # Keep 90 days of historical data
```

To archive old data:
1. Create an "Archive" tab
2. Move old rows from main tabs
3. Keep last 90 days in active tabs

## Exporting Data

### Export to CSV

```bash
# Using Google Sheets API
python -c "
from sheets_updater import SheetsUpdater
import os
sheets = SheetsUpdater(os.environ['GOOGLE_CREDENTIALS'], os.environ['GOOGLE_SHEET_ID'])
data = sheets.service.spreadsheets().values().get(
    spreadsheetId=os.environ['GOOGLE_SHEET_ID'],
    range='Daily_Metrics!A:H'
).execute()
# Export to CSV
"
```

### Scheduled Backups

Set up a separate workflow to backup data weekly:
```yaml
schedule:
  - cron: '0 0 * * 0'  # Every Sunday midnight
```

## Next Steps

- [Set up Jira Integration](./JIRA_SETUP.md)
- [Configure Slack Bot](./SLACK_BOT_SETUP.md)
- [View Troubleshooting Guide](./TROUBLESHOOTING.md)
