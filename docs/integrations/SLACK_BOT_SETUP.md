# Slack Bot Setup Guide

This guide walks you through setting up the interactive Slack bot for repository queries and automated notifications.

## Overview

The Slack bot provides:
- **Status queries**: Get repository status on demand
- **Issue/PR information**: Quick access to details
- **Semantic search**: Find issues and PRs by keywords
- **Quick actions**: Create issues, assign tasks
- **Reports**: Generate weekly/daily reports
- **Automated notifications**: PR approvals, build failures, daily summaries

## Prerequisites

- Slack workspace with admin access
- GitHub repository admin access
- Basic understanding of Slack Apps

## Step 1: Create Slack App

1. Go to [Slack API](https://api.slack.com/apps)
2. Click **Create New App**
3. Choose **From scratch**
4. Fill in details:
   - **App Name**: `Tokyo Bot` (or your preference)
   - **Workspace**: Select your workspace
5. Click **Create App**

## Step 2: Configure Bot Permissions

### Add OAuth Scopes

1. Go to **OAuth & Permissions** in the left sidebar
2. Scroll to **Scopes** section
3. Under **Bot Token Scopes**, add:

**Required scopes:**
```
chat:write          - Send messages
chat:write.public   - Send messages to public channels
channels:read       - View basic channel info
groups:read         - View private channel info
im:read            - View direct messages
im:write           - Send direct messages
users:read         - View users
app_mentions:read  - Receive @mentions
commands           - Respond to slash commands
```

**Optional scopes (for enhanced features):**
```
reactions:write    - Add reactions to messages
files:read        - Read file information
files:write       - Upload files
```

## Step 3: Install App to Workspace

1. Go to **Install App** in the left sidebar
2. Click **Install to Workspace**
3. Review permissions
4. Click **Allow**
5. Copy the **Bot User OAuth Token** (starts with `xoxb-`)
   - Keep this secure - you'll need it for GitHub Secrets

## Step 4: Configure Slash Commands

1. Go to **Slash Commands** in the left sidebar
2. Click **Create New Command**

### Create `/tokyo` Command

Fill in the details:
- **Command**: `/tokyo`
- **Request URL**: `https://your-webhook-receiver.com/slack/commands`
  - See Step 9 for webhook setup
- **Short Description**: `Interact with GitHub repository`
- **Usage Hint**: `status | issue <num> | pr <num> | search <query> | help`

3. Click **Save**

### Additional Commands (Optional)

Repeat for these convenience commands:
- `/tokyo-status` → Quick status check
- `/tokyo-blockers` → View blockers
- `/tokyo-help` → Show help

## Step 5: Enable Event Subscriptions

1. Go to **Event Subscriptions** in the left sidebar
2. Toggle **Enable Events** to On
3. Set **Request URL**: `https://your-webhook-receiver.com/slack/events`
   - See Step 9 for webhook setup
4. Under **Subscribe to bot events**, add:
   ```
   app_mention       - When bot is @mentioned
   message.im        - Direct messages to bot
   ```
5. Click **Save Changes**

## Step 6: Configure App Settings

### Bot Display Name

1. Go to **App Home**
2. Under **Your App's Presence in Slack**:
   - **Display Name**: `Tokyo Bot`
   - **Default Name**: `tokyo-bot`
3. Enable **Always Show My Bot as Online**

### App Icon (Optional)

1. Go to **Basic Information**
2. Under **Display Information**
3. Upload an icon (256x256 PNG recommended)
4. Set background color

## Step 7: Configure GitHub Secrets

Add these secrets to your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add the following:

| Secret Name | Description | Where to Find |
|-------------|-------------|---------------|
| `SLACK_BOT_TOKEN` | Bot User OAuth Token | OAuth & Permissions page (starts with `xoxb-`) |
| `SLACK_APP_TOKEN` | App-Level Token | Basic Information → App-Level Tokens (for Socket Mode) |
| `SLACK_SIGNING_SECRET` | Signing Secret | Basic Information → App Credentials |
| `SLACK_WEBHOOK_URL` | Incoming Webhook URL | Incoming Webhooks → Add New Webhook |

### Getting Slack Signing Secret

1. Go to **Basic Information**
2. Scroll to **App Credentials**
3. Copy **Signing Secret**

### Creating App-Level Token (Optional, for Socket Mode)

1. Go to **Basic Information**
2. Scroll to **App-Level Tokens**
3. Click **Generate Token and Scopes**
4. Name it `websocket-token`
5. Add scope: `connections:write`
6. Click **Generate**
7. Copy the token (starts with `xapp-`)

### Creating Incoming Webhook

1. Go to **Incoming Webhooks**
2. Toggle **Activate Incoming Webhooks** to On
3. Click **Add New Webhook to Workspace**
4. Select a channel (e.g., `#github-notifications`)
5. Click **Allow**
6. Copy the webhook URL

## Step 8: Configure Notification Channels

Update `.github/workflows/config/integrations.json`:

```json
"slack": {
  "enabled": true,
  "bot_name": "tokyo-bot",
  "notification_channels": {
    "dev_team": "C01234567",      // Replace with your channel ID
    "alerts": "C01234568"          // Replace with your alerts channel ID
  }
}
```

### Finding Channel IDs

1. Open Slack
2. Right-click on channel name
3. Select **Copy link**
4. Channel ID is at the end: `slack.com/archives/C01234567`
                                                  ^^^^^^^^^^

## Step 9: Set Up Webhook Relay

Since GitHub Actions doesn't provide a public endpoint, you need a webhook relay.

### Option A: Use Slack Socket Mode (Recommended)

Socket Mode allows real-time events without a public URL:

1. Go to **Socket Mode** in Slack App settings
2. Enable Socket Mode
3. Use the `SLACK_APP_TOKEN` from Step 7
4. Deploy a lightweight bot listener (example below)

### Option B: Use Webhook Relay Service

Use services like:
- **Smee.io** (free, for development)
- **ngrok** (for local testing)
- **AWS API Gateway** + Lambda (production)
- **Google Cloud Functions** (production)

Example with Smee.io:
1. Go to https://smee.io/
2. Click **Start a new channel**
3. Copy the webhook URL
4. Use this URL in Slack command/event configuration

### Option C: Repository Dispatch (Current Implementation)

The current setup uses GitHub's `repository_dispatch`:

1. Deploy a webhook receiver that:
   - Receives Slack events
   - Triggers GitHub Actions via repository_dispatch
   
2. Example webhook receiver (Node.js):

```javascript
const crypto = require('crypto');
const { Octokit } = require('@octokit/rest');

// Verify Slack signature
function verifySlackSignature(req) {
  const slackSignature = req.headers['x-slack-signature'];
  const timestamp = req.headers['x-slack-request-timestamp'];
  const signingSecret = process.env.SLACK_SIGNING_SECRET;
  
  const hmac = crypto.createHmac('sha256', signingSecret);
  hmac.update(`v0:${timestamp}:${req.rawBody}`);
  const expectedSignature = `v0=${hmac.digest('hex')}`;
  
  return crypto.timingSafeEqual(
    Buffer.from(slackSignature),
    Buffer.from(expectedSignature)
  );
}

// Handle slash command
app.post('/slack/commands', async (req, res) => {
  if (!verifySlackSignature(req)) {
    return res.status(401).send('Invalid signature');
  }
  
  const { command, text, user_id, channel_id } = req.body;
  
  // Trigger GitHub Actions
  const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
  
  await octokit.repos.createDispatchEvent({
    owner: 'OWNER',
    repo: 'REPO',
    event_type: 'slack-command',
    client_payload: {
      command: command.replace('/', ''),
      text: text,
      user: user_id,
      channel: channel_id
    }
  });
  
  res.json({ response_type: 'in_channel', text: 'Processing...' });
});
```

## Step 10: Test the Bot

### Test in Slack

1. Go to your Slack workspace
2. Invite bot to a channel:
   ```
   /invite @Tokyo Bot
   ```

3. Test status command:
   ```
   @Tokyo Bot status
   ```
   or
   ```
   /tokyo status
   ```

4. Test issue query:
   ```
   @Tokyo Bot issue 123
   ```

5. Test search:
   ```
   /tokyo search authentication
   ```

### Test Commands

| Command | Expected Result |
|---------|----------------|
| `@Tokyo Bot status` | Repository status with metrics |
| `@Tokyo Bot issue 123` | Details of issue #123 |
| `@Tokyo Bot pr 456` | Details of PR #456 |
| `@Tokyo Bot search auth` | Search results for "auth" |
| `@Tokyo Bot blockers` | List of stale items |
| `@Tokyo Bot help` | Command help |
| `/tokyo status` | Same as @mention |

### Verify Notifications

1. Create a test PR in GitHub
2. Get it approved
3. Check Slack for approval notification
4. Close an issue
5. Check for notification

## Step 11: Configure Notification Schedule

Automated notifications are sent:

- **Daily at 9 AM UTC**: Activity summary
- **Weekly on Monday at 9 AM UTC**: Weekly report
- **Real-time**: PR approvals, build failures, critical blockers

To adjust schedule, edit `.github/workflows/slack-notifier.yml`:

```yaml
schedule:
  # Daily at 9 AM UTC
  - cron: '0 9 * * *'
  # Weekly on Monday at 9 AM UTC
  - cron: '0 9 * * 1'
```

Adjust to your timezone:
```
'0 9 * * *'   # 9 AM UTC
'0 14 * * *'  # 9 AM EST (UTC-5)
'0 17 * * *'  # 9 AM PST (UTC-8)
```

## Bot Commands Reference

### Status & Information

```
/tokyo status              - Overall repository status
/tokyo issue <number>      - Issue details
/tokyo pr <number>        - PR details
```

### Search & Discovery

```
/tokyo search <query>     - Search issues and PRs
/tokyo blockers           - Show stale items
```

### Actions

```
/tokyo create "<title>"   - Create new issue
/tokyo assign <num> @user - Assign issue to user
```

### Reports

```
/tokyo report             - Generate weekly report
/tokyo report daily       - Generate daily report
/tokyo report weekly      - Generate weekly report
```

### Help

```
/tokyo help               - Show all commands
@Tokyo Bot help           - Same as /tokyo help
```

## Natural Language Support

The bot supports natural language queries:

```
"What's the status?"           → Status query
"Show me issue 123"            → Issue info
"Find authentication PRs"      → Search
"Create issue 'Fix bug'"       → Create issue
"What are the blockers?"       → Show blockers
```

## Customizing Bot Responses

Edit `.github/workflows/scripts/slack_bot.py` to customize:

### Change Response Format

```python
def _handle_status_query(self) -> str:
    # Customize the status message format
    response = f"""📊 *Repository Status*
    
• Issues: {open_issues}
• PRs: {open_prs}
• Your custom metric: {custom_value}
"""
    return response
```

### Add Custom Commands

```python
def _handle_custom_command(self, entities: Dict[str, Any]) -> str:
    # Add your custom logic
    return "Custom response"
```

Update NLP processor in `nlp_processor.py`:

```python
Intent.CUSTOM = 'custom'

self.intent_patterns[Intent.CUSTOM] = [
    r'\bcustom\s+command\b',
    r'\bdo\s+custom\s+thing\b'
]
```

## Monitoring

### View Bot Activity

1. Go to **Actions** tab in GitHub
2. Check **Slack Bot** and **Slack Notifications** workflows
3. Review logs for errors

### Slack App Logs

1. Go to your Slack App settings
2. Navigate to **Event Subscriptions**
3. View recent deliveries and responses
4. Check for failed events

## Troubleshooting

### Common Issues

**Bot doesn't respond to @mentions**
- Verify bot is invited to channel
- Check `app_mention` event is subscribed
- Verify webhook receiver is running
- Check GitHub Actions workflow runs

**Slash commands timeout**
- Slack requires response within 3 seconds
- Use immediate acknowledgment, process async
- Check webhook receiver responds quickly

**Notifications not sending**
- Verify `SLACK_BOT_TOKEN` is correct
- Check channel IDs in config
- Ensure bot is member of notification channels
- Review workflow logs

**"Invalid signature" errors**
- Verify `SLACK_SIGNING_SECRET` matches
- Check timestamp isn't too old (>5 minutes)
- Ensure request body is correctly parsed

For more help, see [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

## Security Best Practices

1. **Validate signatures**: Always verify Slack request signatures
2. **Use environment variables**: Never hardcode tokens
3. **Rotate tokens**: Update tokens periodically
4. **Limit permissions**: Only request necessary OAuth scopes
5. **Monitor usage**: Review Slack app analytics regularly

## Advanced Features

### Interactive Buttons

Add buttons to bot responses:

```python
blocks = [{
    'type': 'actions',
    'elements': [{
        'type': 'button',
        'text': {'type': 'plain_text', 'text': 'View Issue'},
        'url': issue_url
    }]
}]
```

### Scheduled Reminders

Set up custom reminder workflows:
```yaml
schedule:
  - cron: '0 10 * * 1-5'  # Weekdays at 10 AM
```

### Custom Slash Commands

Create additional commands:
- `/tokyo-deploy` - Trigger deployment
- `/tokyo-review` - Find PRs needing review
- `/tokyo-sprint` - Sprint status

## Next Steps

- [Set up Jira Integration](./JIRA_SETUP.md)
- [Configure Google Sheets Dashboard](./GOOGLE_SHEETS_SETUP.md)
- [View Troubleshooting Guide](./TROUBLESHOOTING.md)
