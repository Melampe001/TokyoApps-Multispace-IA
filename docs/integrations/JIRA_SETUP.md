# Jira Integration Setup Guide

This guide walks you through setting up the bidirectional Jira synchronization for the Tokyo-IA repository.

## Prerequisites

- Jira Cloud or Server instance
- Admin access to Jira project
- Admin access to GitHub repository
- Basic understanding of webhooks

## Step 1: Create Jira API Token

### For Jira Cloud:

1. Log in to your Atlassian account at https://id.atlassian.com
2. Go to **Account Settings** → **Security** → **API tokens**
3. Click **Create API token**
4. Give it a descriptive name (e.g., "GitHub Integration - Tokyo-IA")
5. Copy the generated token immediately (you won't be able to see it again)

### For Jira Server/Data Center:

1. Log in to Jira as an admin
2. Go to **Settings** → **Products** → **Application links**
3. Create an application link for GitHub integration
4. Generate an API token or use basic authentication

## Step 2: Configure GitHub Secrets

Add the following secrets to your GitHub repository:

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `JIRA_BASE_URL` | Your Jira instance URL | `https://yourcompany.atlassian.net` |
| `JIRA_USER_EMAIL` | Email of Jira API user | `bot@yourcompany.com` |
| `JIRA_API_TOKEN` | API token from Step 1 | `abc123xyz789...` |
| `JIRA_WEBHOOK_SECRET` | Random string for webhook validation | `generate-random-string` |

### Generating Webhook Secret:

```bash
# On Linux/Mac
openssl rand -hex 32

# Or use Python
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## Step 3: Configure Jira Project

### Create/Verify Issue Types

Ensure your Jira project has the following issue types:
- **Bug** - For GitHub issues labeled as "bug"
- **Story** - For GitHub issues labeled as "enhancement" or "feature"
- **Task** - For GitHub issues labeled as "documentation" or "task"

### Set Up Priorities

Ensure the following priorities exist:
- **Highest** - For critical/blocker issues
- **High** - For high-priority issues
- **Medium** - For medium-priority issues
- **Low** - For low-priority issues

### Create Custom Fields (Optional)

If you want to sync additional data, create custom fields:

1. Go to **Project settings** → **Issue types**
2. Select an issue type
3. Add custom fields as needed
4. Note the field IDs (visible in the field configuration URL)

Update `.github/workflows/config/jira-mappings.json` with your custom field IDs.

## Step 4: Configure Jira Webhook

### For Bidirectional Sync (Jira → GitHub):

1. In Jira, go to **Settings** → **System** → **WebHooks**
2. Click **Create a WebHook**
3. Fill in the details:
   - **Name**: GitHub Integration - Tokyo-IA
   - **Status**: Enabled
   - **URL**: See note below about webhook URL
   - **Events**: Select:
     - Issue Created
     - Issue Updated
     - Issue Deleted
     - Comment Created
     - Comment Updated

4. Click **Create**

### Webhook URL Setup

GitHub Actions doesn't provide a direct webhook endpoint. You have two options:

#### Option A: Use a Webhook Relay Service

Services like [Smee.io](https://smee.io/), [Zapier](https://zapier.com/), or [Make.com](https://www.make.com/) can bridge Jira webhooks to GitHub:

1. Create a webhook relay channel
2. Point Jira webhook to relay URL
3. Configure relay to trigger GitHub `repository_dispatch` event
4. Use event type: `jira-webhook`

#### Option B: Self-Hosted Webhook Receiver

Deploy a simple webhook receiver that:
1. Receives Jira webhooks
2. Validates the webhook signature
3. Triggers GitHub repository_dispatch via GitHub API

Example using GitHub CLI:
```bash
gh api repos/OWNER/REPO/dispatches \
  -X POST \
  -f event_type=jira-webhook \
  -f "client_payload[webhookEvent]=$EVENT" \
  -f "client_payload[issue]=$ISSUE_DATA"
```

## Step 5: Customize Mappings

Edit `.github/workflows/config/jira-mappings.json` to customize:

### Label to Issue Type Mapping

```json
"label_to_type": {
  "bug": "Bug",
  "enhancement": "Story",
  "feature": "Story",
  "documentation": "Task",
  "task": "Task"
}
```

### Label to Priority Mapping

```json
"label_to_priority": {
  "priority: high": "High",
  "priority: medium": "Medium",
  "priority: low": "Low",
  "critical": "Highest",
  "blocker": "Highest"
}
```

### Status Mapping

```json
"status_mapping": {
  "github_to_jira": {
    "open": "To Do",
    "in_progress": "In Progress",
    "review": "In Review",
    "closed": "Done"
  },
  "jira_to_github": {
    "To Do": "open",
    "In Progress": "in_progress",
    "In Review": "review",
    "Done": "closed"
  }
}
```

## Step 6: Test the Integration

### Test GitHub → Jira Sync

1. Create a test issue in GitHub:
   ```bash
   gh issue create --title "Test Jira Sync" --body "Testing integration" --label bug
   ```

2. Check GitHub Actions workflow run
3. Verify Jira ticket was created
4. Check ticket has correct type and priority

### Test Jira → GitHub Sync

1. Update the Jira ticket status
2. Verify GitHub issue status updates
3. Add a comment in Jira
4. Verify comment appears in GitHub

### Trigger Manual Sync

Use the workflow dispatch feature:

```bash
gh workflow run jira-sync.yml -f issue_number=123
```

## Step 7: Configure Sync Schedule

The integration syncs automatically:
- **On GitHub events**: issues, PRs, comments
- **Scheduled**: Every 15 minutes to catch missed syncs
- **Manual**: Via workflow dispatch

To adjust the sync interval, edit `.github/workflows/jira-sync.yml`:

```yaml
schedule:
  - cron: '*/15 * * * *'  # Change to your preferred interval
```

## Conflict Resolution

The integration uses "last write wins" strategy by default:

1. Compares timestamps of GitHub and Jira updates
2. Syncs from newer to older
3. Logs conflicts for audit
4. Notifies users in both platforms

To change strategy, edit `.github/workflows/config/jira-mappings.json`:

```json
"conflict_resolution": {
  "strategy": "last_write_wins",  # or "github_wins" or "jira_wins"
  "notify_on_conflict": true
}
```

## Monitoring

### View Sync Logs

1. Go to **Actions** tab in GitHub
2. Select **Jira Sync** workflow
3. View recent runs and logs
4. Download sync log artifacts for detailed analysis

### Health Checks

The integration includes automatic health checks every 30 minutes:
- Tests Jira API connectivity
- Verifies credentials are valid
- Creates GitHub issue if sync fails repeatedly

## Troubleshooting

### Common Issues

**Issue**: Jira tickets not being created
- Verify `JIRA_BASE_URL` doesn't have trailing slash
- Check API token is valid and not expired
- Ensure project key exists in Jira
- Verify issue type mappings match your Jira configuration

**Issue**: Status sync not working
- Check status names match exactly (case-sensitive)
- Verify workflow transitions exist in Jira
- Review status mapping in configuration

**Issue**: Comments not syncing
- Ensure `sync_comments` is `true` in config
- Check comment sync is enabled in workflow
- Verify API permissions allow comment creation

For more troubleshooting tips, see [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

## Security Best Practices

1. **Use dedicated service account**: Create a dedicated Jira user for API access
2. **Limit permissions**: Grant only necessary permissions
3. **Rotate tokens regularly**: Update API tokens every 90 days
4. **Monitor access logs**: Review Jira audit logs regularly
5. **Validate webhooks**: Always validate webhook signatures

## Support

For issues or questions:
- Create an issue in this repository
- Check [Troubleshooting guide](./TROUBLESHOOTING.md)
- Review workflow logs in GitHub Actions

## Next Steps

- [Set up Google Sheets Dashboard](./GOOGLE_SHEETS_SETUP.md)
- [Configure Slack Bot](./SLACK_BOT_SETUP.md)
- [View all integrations](../README.md)
