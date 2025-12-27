# Google Sheets Dashboard Setup Guide

This guide explains how to set up automated metrics reporting to a Google Sheets dashboard.

## Overview

The Google Sheets integration automatically updates a dashboard with:
- Daily metrics (issues, PRs, commits)
- Weekly aggregated metrics
- Team performance data
- Velocity tracking
- Quality metrics

Updates run every 2 hours and on pushes to main branch.

## Prerequisites

- Google Cloud Project with Sheets API enabled
- Service account with Sheets access
- GitHub repository with Actions enabled
- Google Sheets document

## Setup Steps

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable the Google Sheets API:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

### 2. Create Service Account

1. Go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Name it (e.g., "tokyo-ia-sheets-updater")
4. Grant "Editor" role (or minimum necessary permissions)
5. Click "Done"

### 3. Generate Service Account Key

1. Click on the service account you created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON" format
5. Click "Create" - a JSON file will download
6. **Keep this file secure!**

### 4. Create Google Sheets Dashboard

1. Create a new Google Sheet
2. Name it "Tokyo-IA Dashboard"
3. Create the following tabs (sheets):
   - **Daily** - For daily metrics
   - **Weekly** - For weekly aggregates
   - **Team** - For team member metrics
   - **Bots** - For bot performance (optional)
   - **Executive** - For executive summary (optional)

#### Daily Tab Header Row

Add these headers in row 1:

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| Date | Issues Opened | Issues Closed | PRs Opened | PRs Merged | Commits | Net Issues |

#### Weekly Tab Header Row

Add these headers in row 1:

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| Week Start | Week End | Issues Opened | Issues Closed | PRs Opened | PRs Merged | Commits | Velocity |

#### Team Tab Header Row

Add these headers in row 1:

| A | B | C | D |
|---|---|---|---|
| User | Issues | PRs | Commits |

### 5. Share Sheet with Service Account

1. Open your Google Sheet
2. Click "Share" button
3. Add the service account email (found in the JSON key file, looks like `tokyo-ia-sheets-updater@project-id.iam.gserviceaccount.com`)
4. Give "Editor" permissions
5. Click "Send"

### 6. Get Sheet ID

The Sheet ID is in the URL:
```
https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
```

Copy the `SHEET_ID_HERE` part.

### 7. Configure GitHub Secrets

Add the following secrets to your GitHub repository:

1. Navigate to: `Settings` → `Secrets and variables` → `Actions`

2. Add these secrets:

   **GOOGLE_CREDENTIALS**
   ```json
   {
     "type": "service_account",
     "project_id": "your-project-id",
     "private_key_id": "...",
     "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
     "client_email": "tokyo-ia-sheets-updater@your-project.iam.gserviceaccount.com",
     "client_id": "...",
     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
     "token_uri": "https://oauth2.googleapis.com/token",
     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
     "client_x509_cert_url": "..."
   }
   ```
   
   **Tip:** Copy the entire contents of the JSON key file you downloaded.

   **GOOGLE_SHEET_ID**
   ```
   your-sheet-id-here
   ```

### 8. Configure Integration Settings

Edit `.github/workflows/config/integrations.json`:

```json
{
  "google_sheets": {
    "enabled": true,
    "update_interval_hours": 2,
    "metrics": ["issues", "prs", "velocity", "quality", "team"]
  }
}
```

### 9. Test the Integration

1. Go to GitHub Actions
2. Find "Update Dashboard" workflow
3. Click "Run workflow" → "Run workflow"
4. Wait for completion
5. Check your Google Sheet for new data

## Dashboard Features

### Daily Metrics

Tracks day-by-day activity:
- Issues opened/closed
- PRs opened/merged
- Commit count
- Net issue change (opened - closed)

**Use cases:**
- Daily standup reference
- Spot trends and patterns
- Identify busy/slow days

### Weekly Metrics

Aggregates weekly performance:
- Total issues and PRs
- Team velocity (issues closed per day)
- Weekly commit volume

**Use cases:**
- Sprint reviews
- Weekly team meetings
- Trend analysis

### Team Metrics

Per-developer contributions:
- Issues created
- PRs submitted
- Commits authored

**Use cases:**
- Team performance reviews
- Load balancing
- Recognition and kudos

## Creating Charts

### Burndown Chart

1. Select Daily tab data (columns A, B, C)
2. Insert → Chart
3. Chart type: Line chart
4. X-axis: Date
5. Y-axis: Issues Opened, Issues Closed

### Velocity Chart

1. Select Weekly tab data (columns A, H)
2. Insert → Chart
3. Chart type: Column chart
4. X-axis: Week Start
5. Y-axis: Velocity

### Team Contribution Chart

1. Select Team tab data (columns A, D)
2. Insert → Chart
3. Chart type: Bar chart
4. X-axis: User
5. Y-axis: Commits

## Customization

### Add Custom Metrics

Edit `.github/workflows/scripts/sheets_updater.py`:

```python
def calculate_custom_metric():
    # Your custom calculation
    return value

# In update_daily_tab():
values = [[
    metrics['date'],
    metrics['issues_opened'],
    # ... existing fields
    calculate_custom_metric()  # Add custom metric
]]
```

### Change Update Frequency

Edit `.github/workflows/sheets-update.yml`:

```yaml
on:
  schedule:
    - cron: '0 */4 * * *'  # Every 4 hours instead of 2
```

### Add Conditional Formatting

In Google Sheets:
1. Select range (e.g., G2:G1000 for Net Issues)
2. Format → Conditional formatting
3. Format rules:
   - If greater than 0 → Red (issues increasing)
   - If less than 0 → Green (issues decreasing)

## Troubleshooting

### Issue: Authentication Failed

**Symptoms:** "401 Unauthorized" or "403 Forbidden" errors

**Solutions:**
1. Verify service account email has editor access to sheet
2. Check GOOGLE_CREDENTIALS secret contains valid JSON
3. Ensure private key includes `\n` newlines correctly
4. Regenerate service account key

### Issue: Sheet Not Found

**Symptoms:** "Requested entity was not found" errors

**Solutions:**
1. Verify GOOGLE_SHEET_ID is correct
2. Check service account has access to the sheet
3. Ensure sheet hasn't been deleted

### Issue: No Data Appearing

**Symptoms:** Workflow succeeds but no data in sheet

**Solutions:**
1. Check tab names match exactly (case-sensitive)
2. Verify headers are in row 1
3. Check GitHub Actions logs for errors
4. Ensure GITHUB_TOKEN has read access

### Issue: Data Overwrites Existing

**Symptoms:** Old data gets replaced instead of new rows added

**Solutions:**
1. Script uses `append` mode by default
2. Check if you manually cleared data
3. Verify range specifications in script

## Security Best Practices

1. **Never commit credentials** to repository
2. **Use service accounts** instead of personal accounts
3. **Limit service account permissions** to minimum needed
4. **Rotate keys regularly** (every 90 days)
5. **Monitor access logs** in Google Cloud Console
6. **Use separate projects** for dev and production

## Monitoring

### Check Update Status

View logs in GitHub Actions:
1. Go to Actions tab
2. Click "Update Dashboard" workflow
3. View recent runs

### Verify Data Accuracy

Periodically verify:
1. Date ranges are correct
2. Numbers match GitHub's counts
3. No duplicate entries
4. All tabs are updating

## Advanced Features

### Data Retention

To archive old data:
1. Create "Archive" tab
2. Periodically move old data from Daily/Weekly tabs
3. Keep only recent data in main tabs

### Alerts and Notifications

Add Google Apps Script to send alerts:

```javascript
function checkMetrics() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var lastRow = sheet.getLastRow();
  var netIssues = sheet.getRange(lastRow, 7).getValue();
  
  if (netIssues > 10) {
    // Send email alert
    MailApp.sendEmail({
      to: 'team@example.com',
      subject: 'Alert: High Issue Backlog',
      body: 'Net issues increased to ' + netIssues
    });
  }
}
```

### Data Export

Export data for analysis:
1. File → Download
2. Choose format (Excel, CSV, PDF)
3. Use for presentations or reports

## Limitations

Current limitations:
- Maximum 100 results per query (pagination not implemented)
- Updates every 2 hours (not real-time)
- Basic metrics only (no advanced analytics)
- No historical data import (starts from first run)

## Future Enhancements

Planned features:
- Real-time updates via webhooks
- More advanced metrics (code quality, test coverage)
- Custom dashboards per team
- Automated report generation
- Integration with BI tools

## Support

For issues or questions:
1. Check [troubleshooting section](#troubleshooting)
2. Review GitHub Actions logs
3. Check [Google Sheets API documentation](https://developers.google.com/sheets/api)
4. Open an issue in the Tokyo-IA repository

## Related Documentation

- [Workflow File](.github/workflows/sheets-update.yml)
- [Integration Configuration](../.github/workflows/config/integrations.json)
- [Google Sheets API Docs](https://developers.google.com/sheets/api)
