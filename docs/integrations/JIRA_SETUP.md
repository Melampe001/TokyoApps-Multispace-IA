# Jira Integration Setup Guide

This guide explains how to set up bidirectional synchronization between GitHub Issues and Jira.

## Overview

The Jira sync integration automatically:
- Creates Jira tickets from GitHub issues
- Updates Jira tickets when GitHub issues change
- Syncs status changes between platforms
- Mirrors comments bidirectionally
- Maps labels to issue types

## Prerequisites

- Jira Cloud account with API access
- Admin access to your Jira project
- GitHub repository with Actions enabled

## Setup Steps

### 1. Create Jira API Token

1. Log in to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a name (e.g., "Tokyo-IA GitHub Sync")
4. Copy the token (you won't be able to see it again)

### 2. Find Your Jira Base URL

Your Jira base URL is typically:
```
https://your-organization.atlassian.net
```

Replace `your-organization` with your actual Jira subdomain.

### 3. Configure GitHub Secrets

Add the following secrets to your GitHub repository:

1. Navigate to: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

2. Add these secrets:

   **JIRA_BASE_URL**
   ```
   https://your-organization.atlassian.net
   ```

   **JIRA_API_TOKEN**
   ```
   your-api-token-here
   ```

   **JIRA_EMAIL**
   ```
   your-jira-email@example.com
   ```

### 4. Configure Integration Settings

Edit `.github/workflows/config/integrations.json`:

```json
{
  "jira": {
    "enabled": true,
    "projects": ["TOKYO"],
    "sync_interval_minutes": 15,
    "label_mappings": {
      "bug": "Bug",
      "enhancement": "Story",
      "documentation": "Task"
    }
  }
}
```

**Configuration Options:**

- `enabled`: Turn integration on/off
- `projects`: List of Jira project keys to use
- `sync_interval_minutes`: How often to check for updates (15 recommended)
- `label_mappings`: Map GitHub labels to Jira issue types

### 5. Test the Integration

1. Create a new GitHub issue
2. Add a label that's in your mappings (e.g., "bug")
3. Check GitHub Actions for the workflow run
4. Verify a Jira ticket was created

## Label Mapping

Configure how GitHub labels map to Jira issue types:

| GitHub Label | Jira Issue Type | Description |
|--------------|----------------|-------------|
| bug | Bug | Software defects |
| enhancement | Story | New features |
| feature | Story | Feature requests |
| documentation | Task | Documentation updates |
| task | Task | General tasks |
| epic | Epic | Large initiatives |

**To add custom mappings:**

```json
"label_mappings": {
  "security": "Security",
  "performance": "Technical Debt",
  "ui-ux": "Design"
}
```

## Status Synchronization

Status changes sync automatically:

| GitHub State | Jira Status |
|--------------|-------------|
| Open | To Do |
| In Progress | In Progress |
| Closed | Done |
| Reopened | To Do |

## Comment Mirroring

Comments are synced from GitHub to Jira:
- New comments on GitHub issues → New comments on Jira tickets
- Includes the GitHub username in the comment
- Preserves formatting (Markdown → Jira format)

**Note:** Jira → GitHub comment sync is not currently supported.

## Workflow Triggers

The sync runs when:
- An issue is opened
- An issue is edited
- An issue is closed
- An issue is reopened
- A comment is added to an issue

## Advanced Configuration

### Custom Issue Types

To use custom Jira issue types:

1. Find your issue type ID in Jira:
   - Go to Jira Settings → Issues → Issue types
   - Note the issue type names

2. Update your mappings:
   ```json
   "label_mappings": {
     "incident": "Incident",
     "change-request": "Change"
   }
   ```

### Priority Mapping

Add priority mapping (requires code changes in `jira_sync.py`):

```python
priority_mappings = {
    'p0': 'Highest',
    'p1': 'High',
    'p2': 'Medium',
    'p3': 'Low'
}
```

### Custom Fields

To sync custom fields:

1. Find the custom field ID in Jira (appears as `customfield_xxxxx`)
2. Modify `jira_sync.py` to include custom fields in the payload:

```python
jira_data = {
    'fields': {
        'project': {'key': project_key},
        'summary': issue['title'],
        'description': issue['body'],
        'issuetype': {'name': issue_type},
        'customfield_10001': 'Custom Value'  # Add custom field
    }
}
```

## Troubleshooting

### Issue: Sync Not Running

**Symptoms:** No Jira tickets created when issues are opened

**Solutions:**
1. Check GitHub Actions tab for workflow runs
2. Verify secrets are set correctly
3. Check Jira API token is valid
4. Ensure `enabled: true` in config

### Issue: Authentication Failed

**Symptoms:** "401 Unauthorized" errors in logs

**Solutions:**
1. Verify JIRA_EMAIL matches the account that created the API token
2. Regenerate API token
3. Check JIRA_BASE_URL format (no trailing slash)

### Issue: Issue Type Not Found

**Symptoms:** "Issue type 'Story' not found" errors

**Solutions:**
1. Verify issue types exist in your Jira project
2. Check spelling and capitalization in mappings
3. Use exact names from Jira Settings → Issues → Issue types

### Issue: Rate Limiting

**Symptoms:** "429 Too Many Requests" errors

**Solutions:**
1. Increase `sync_interval_minutes` in config
2. Implement request throttling in script
3. Contact Atlassian support for rate limit increase

## Security Best Practices

1. **Never commit secrets** to the repository
2. **Rotate API tokens** every 90 days
3. **Use least privilege** - only grant necessary Jira permissions
4. **Monitor access logs** in Jira
5. **Use separate tokens** for different environments (dev, prod)

## Monitoring

### Check Sync Status

View sync logs in GitHub Actions:
1. Go to Actions tab
2. Click on "Jira Sync" workflow
3. View recent runs and logs

### Verify Jira Tickets

After creating a GitHub issue:
1. Check the issue body for a Jira ticket reference
2. Search Jira for tickets with GitHub links in description
3. Verify status and comments are synced

## Limitations

Current limitations:
- Jira → GitHub sync not supported (GitHub → Jira only)
- Attachments are not synced
- Custom field sync requires code changes
- Sprint information not synced
- Watchers not synced

## Future Enhancements

Planned features:
- Bidirectional comment sync
- Attachment synchronization
- Sprint/Epic linking
- Automated testing
- Webhook-based real-time sync (instead of event-based)

## Support

For issues or questions:
1. Check the [troubleshooting section](#troubleshooting)
2. Review GitHub Actions logs
3. Check [Atlassian API documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
4. Open an issue in the Tokyo-IA repository

## Related Documentation

- [GitHub Actions Workflow](.github/workflows/jira-sync.yml)
- [Jira API Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [Integration Configuration](../.github/workflows/config/integrations.json)
