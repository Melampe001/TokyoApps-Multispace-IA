# Slack Bot Setup Guide

This guide explains how to set up the Tokyo-IA Slack bot for repository interactions.

## Overview

The Tokyo-IA Slack bot provides:
- Project status summaries
- Issue and PR details lookup
- Search functionality
- Quick access to repository information
- Automated notifications

## Prerequisites

- Slack workspace with admin access
- GitHub repository with Actions enabled
- Slack App creation permissions

## Setup Steps

### 1. Create Slack App

1. Go to [Slack API Apps](https://api.slack.com/apps)
2. Click "Create New App"
3. Choose "From scratch"
4. Name: "Tokyo-IA Bot"
5. Select your workspace
6. Click "Create App"

### 2. Configure Bot Token Scopes

1. In your app settings, go to "OAuth & Permissions"
2. Scroll to "Bot Token Scopes"
3. Add the following scopes:
   - `chat:write` - Send messages
   - `chat:write.public` - Send messages to public channels
   - `channels:read` - View basic channel information
   - `groups:read` - View basic info about private channels
   - `im:read` - View basic info about DMs
   - `commands` - Add slash commands

### 3. Install App to Workspace

1. Go to "Install App" in sidebar
2. Click "Install to Workspace"
3. Review permissions
4. Click "Allow"
5. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

### 4. Create Slash Commands

Go to "Slash Commands" in sidebar and create these commands:

#### /tokyo-status
- **Command:** `/tokyo-status`
- **Request URL:** `https://your-webhook-url.com/slack/commands` (you'll set this up later)
- **Short Description:** Get Tokyo-IA project status
- **Usage Hint:** (empty)

#### /tokyo-issue
- **Command:** `/tokyo-issue`
- **Request URL:** `https://your-webhook-url.com/slack/commands`
- **Short Description:** Get issue details
- **Usage Hint:** `<issue number>`

#### /tokyo-pr
- **Command:** `/tokyo-pr`
- **Request URL:** `https://your-webhook-url.com/slack/commands`
- **Short Description:** Get PR details
- **Usage Hint:** `<pr number>`

#### /tokyo-search
- **Command:** `/tokyo-search`
- **Request URL:** `https://your-webhook-url.com/slack/commands`
- **Short Description:** Search issues and PRs
- **Usage Hint:** `<search query>`

#### /tokyo-help
- **Command:** `/tokyo-help`
- **Request URL:** `https://your-webhook-url.com/slack/commands`
- **Short Description:** Show bot help
- **Usage Hint:** (empty)

### 5. Get Signing Secret

1. Go to "Basic Information" in sidebar
2. Scroll to "App Credentials"
3. Copy the **Signing Secret**

### 6. Configure GitHub Secrets

Add the following secrets to your GitHub repository:

1. Navigate to: `Settings` → `Secrets and variables` → `Actions`

2. Add these secrets:

   **SLACK_BOT_TOKEN**
   ```
   xoxb-your-bot-token-here
   ```

   **SLACK_SIGNING_SECRET**
   ```
   your-signing-secret-here
   ```

### 7. Configure Integration Settings

Edit `.github/workflows/config/integrations.json`:

```json
{
  "slack": {
    "enabled": true,
    "bot_name": "tokyo-bot",
    "commands_enabled": true,
    "notifications": {
      "issue_opened": true,
      "issue_closed": true,
      "pr_opened": true,
      "pr_merged": true,
      "deployment": true,
      "security_alert": true
    },
    "channels": {
      "general": "#tokyo-general",
      "dev": "#tokyo-dev",
      "alerts": "#tokyo-alerts"
    }
  }
}
```

### 8. Set Up Webhook Endpoint (Optional)

For real-time slash commands, you need a webhook endpoint. Options:

#### Option A: Use GitHub Actions (Manual Trigger)

The current implementation uses manual workflow dispatch. To use a command:

1. Go to GitHub Actions
2. Select "Slack Bot" workflow
3. Click "Run workflow"
4. Enter command (e.g., "status")
5. Click "Run workflow"

#### Option B: Deploy Webhook Server

Deploy a simple webhook server to handle Slack commands:

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/slack/commands', methods=['POST'])
def slack_commands():
    # Verify request is from Slack
    # Parse command
    # Trigger GitHub Action via repository_dispatch
    
    command = request.form.get('command')
    text = request.form.get('text')
    
    # Trigger GitHub Action
    requests.post(
        f'https://api.github.com/repos/YOUR_REPO/dispatches',
        headers={
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        },
        json={
            'event_type': 'slack_command',
            'client_payload': {
                'command': command,
                'text': text
            }
        }
    )
    
    return jsonify({'response_type': 'in_channel', 'text': 'Processing...'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Deploy this to:
- Railway
- Heroku
- AWS Lambda
- Google Cloud Run
- Your own server

### 9. Test the Bot

#### Test Status Command

In Slack:
```
/tokyo-status
```

Expected response:
```
📊 Tokyo-IA Project Status

Issues: 15 open
Pull Requests: 3 open
Recent Commits: 10 in last update

Recent Activity:
• Implement Railway deployment - John Doe
• Add AI provider SDKs - Jane Smith
...
```

#### Test Issue Lookup

In Slack:
```
/tokyo-issue 42
```

Expected response:
```
Issue #42: Implement authentication

Status: open
Author: johndoe
Created: 2025-01-15
Labels: enhancement, security

Description:
We need to implement JWT-based authentication...

View on GitHub
```

## Available Commands

### /tokyo-status

Get project status summary.

**Usage:**
```
/tokyo-status
```

**Returns:**
- Open issues count
- Open PRs count
- Recent commits
- Recent activity

### /tokyo-issue

Get details for a specific issue.

**Usage:**
```
/tokyo-issue <number>
```

**Example:**
```
/tokyo-issue 123
```

**Returns:**
- Issue title and number
- Status and author
- Labels and assignees
- Description excerpt
- GitHub link

### /tokyo-pr

Get details for a specific pull request.

**Usage:**
```
/tokyo-pr <number>
```

**Example:**
```
/tokyo-pr 45
```

**Returns:**
- PR title and number
- Status and author
- Base and head branches
- Changes summary
- Reviewers
- GitHub link

### /tokyo-search

Search for issues and PRs.

**Usage:**
```
/tokyo-search <query>
```

**Example:**
```
/tokyo-search authentication bug
```

**Returns:**
- List of matching issues/PRs
- Title and number
- Status
- Direct links

### /tokyo-help

Show help message with available commands.

**Usage:**
```
/tokyo-help
```

## Automated Notifications

Configure automated notifications for events:

### Issue Notifications

```json
"notifications": {
  "issue_opened": true,
  "issue_closed": true
}
```

Sends message when:
- New issue is created
- Issue is closed

### PR Notifications

```json
"notifications": {
  "pr_opened": true,
  "pr_merged": true
}
```

Sends message when:
- New PR is opened
- PR is merged

### Deployment Notifications

```json
"notifications": {
  "deployment": true
}
```

Sends message when:
- Code is deployed to production
- Deployment succeeds or fails

### Security Alerts

```json
"notifications": {
  "security_alert": true
}
```

Sends message when:
- Security vulnerability detected
- Dependabot alert created

## Channel Configuration

Configure which channels receive notifications:

```json
"channels": {
  "general": "#tokyo-general",
  "dev": "#tokyo-dev",
  "alerts": "#tokyo-alerts"
}
```

- `general` - General project updates
- `dev` - Development activity (PRs, commits)
- `alerts` - Important alerts and failures

## Customization

### Add Custom Commands

Edit `.github/workflows/scripts/slack_bot.py`:

```python
def process_command(command_text: str) -> str:
    cmd, args = parse_command(command_text)
    
    if cmd == 'custom-command':
        # Your custom logic
        return "Custom response"
    
    # ... existing commands
```

### Change Response Format

Customize message formatting:

```python
def get_issue_details(issue_number: int) -> str:
    # ... fetch issue
    
    # Custom formatting
    details = f"🐛 *Issue #{issue['number']}*\n"
    details += f"_{issue['title']}_\n\n"
    # ... more formatting
    
    return details
```

### Add Rich Formatting

Use Slack Block Kit for rich messages:

```python
blocks = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": f"Issue #{issue_number}"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": issue['title']
        }
    }
]
```

## Troubleshooting

### Issue: Commands Not Working

**Symptoms:** Slash commands don't respond

**Solutions:**
1. Verify bot is installed in workspace
2. Check SLACK_BOT_TOKEN is correct
3. Ensure bot has necessary scopes
4. Test with `/tokyo-help` first

### Issue: "Not Authorized" Error

**Symptoms:** Bot can't access channels

**Solutions:**
1. Invite bot to channels: `/invite @tokyo-bot`
2. Check bot token scopes
3. Verify bot is installed

### Issue: Slow Response

**Symptoms:** Commands take long time to respond

**Solutions:**
1. GitHub Actions has cold start time
2. Consider webhook server for real-time
3. Use Slack's delayed response pattern

### Issue: Rate Limiting

**Symptoms:** "Rate limit exceeded" errors

**Solutions:**
1. Implement request throttling
2. Cache frequently requested data
3. Use Slack's rate limit headers

## Security Best Practices

1. **Never commit tokens** to repository
2. **Validate Slack signatures** on webhook requests
3. **Use HTTPS** for webhook endpoints
4. **Rotate tokens** regularly
5. **Monitor bot access logs**
6. **Use least privilege** scopes

## Limitations

Current limitations:
- Commands are not real-time (uses GitHub Actions)
- No interactive components (buttons, dropdowns)
- Limited to text responses
- No file uploads/downloads
- No threading support

## Future Enhancements

Planned features:
- Real-time webhook server
- Interactive buttons and menus
- File sharing capabilities
- Thread support for conversations
- Custom workflows and automations
- AI-powered search and suggestions

## Support

For issues or questions:
1. Check [troubleshooting section](#troubleshooting)
2. Review Slack API logs
3. Check [Slack API documentation](https://api.slack.com/)
4. Open an issue in the Tokyo-IA repository

## Related Documentation

- [Workflow File](.github/workflows/slack-bot.yml)
- [Integration Configuration](../.github/workflows/config/integrations.json)
- [Slack API Documentation](https://api.slack.com/)
- [Slack Block Kit](https://api.slack.com/block-kit)
