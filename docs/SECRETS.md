# GitHub Actions Secrets Configuration

This document describes all the secrets that need to be configured in GitHub Actions for the CI/CD pipeline.

## Required Secrets

### Railway Integration

#### `RAILWAY_TOKEN`
- **Description:** Railway API token for deployments
- **How to obtain:**
  1. Login to Railway: https://railway.app
  2. Go to Account Settings → Tokens
  3. Click "Create New Token"
  4. Copy the token (starts with `railway_`)
- **Required for:** CD Pipeline (staging & production deployments)

#### `RAILWAY_PROJECT_ID`
- **Description:** Railway project ID
- **How to obtain:**
  1. Go to Railway Dashboard
  2. Select your Tokyo-IA project
  3. Go to Settings
  4. Copy the Project ID
- **Required for:** CD Pipeline (staging & production deployments)

## Optional Secrets

### Code Coverage

#### `CODECOV_TOKEN`
- **Description:** Codecov.io token for coverage reporting
- **How to obtain:**
  1. Sign up at https://codecov.io
  2. Link your GitHub repository
  3. Copy the token from repository settings
- **Required for:** Private repositories only
- **Used in:** CI Pipeline (coverage reporting)

### Notifications

#### `SLACK_WEBHOOK`
- **Description:** Slack webhook URL for deployment notifications
- **How to obtain:**
  1. Go to your Slack workspace
  2. Create an Incoming Webhook integration
  3. Select the channel for notifications
  4. Copy the webhook URL
- **Required for:** Optional (deployment notifications)
- **Used in:** CD Pipeline (deployment status notifications)

### Testing (Optional)

These are only needed if you want to run integration tests with real API calls. Tests will use mocks if these are not provided.

#### `ANTHROPIC_API_KEY`
- **Description:** Anthropic Claude API key
- **How to obtain:** https://console.anthropic.com
- **Used by:** Akira agent tests

#### `OPENAI_API_KEY`
- **Description:** OpenAI API key
- **How to obtain:** https://platform.openai.com
- **Used by:** Yuki and Kenji agent tests

#### `GROQ_API_KEY`
- **Description:** Groq API key
- **How to obtain:** https://console.groq.com
- **Used by:** Hiro agent tests

#### `GOOGLE_API_KEY`
- **Description:** Google AI API key
- **How to obtain:** https://ai.google.dev
- **Used by:** Sakura agent tests

## How to Add Secrets to GitHub

1. Go to your repository on GitHub
2. Click **Settings**
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Enter the secret name (e.g., `RAILWAY_TOKEN`)
6. Paste the secret value
7. Click **Add secret**

## Security Best Practices

### ✅ DO:
- Rotate tokens regularly
- Use separate tokens for staging and production (if possible)
- Keep secrets in GitHub Secrets, never in code
- Use minimal permissions for tokens
- Document which services use which secrets

### ❌ DON'T:
- Commit secrets to the repository (even in `.env` files)
- Share secrets via chat/email
- Use production secrets for testing
- Give tokens more permissions than needed
- Reuse tokens across different services

## Railway Environment Variables

These should be set in Railway Dashboard, NOT in GitHub Secrets:

### Staging Environment
```
DATABASE_URL=<automatically set by Railway PostgreSQL>
PORT=8080
LOG_LEVEL=info
ANTHROPIC_API_KEY=<your-key>
OPENAI_API_KEY=<your-key>
GROQ_API_KEY=<your-key>
GOOGLE_API_KEY=<your-key>
```

### Production Environment
```
DATABASE_URL=<automatically set by Railway PostgreSQL>
PORT=8080
LOG_LEVEL=info
ANTHROPIC_API_KEY=<your-key>
OPENAI_API_KEY=<your-key>
GROQ_API_KEY=<your-key>
GOOGLE_API_KEY=<your-key>
```

### How to Set Railway Environment Variables

1. Go to Railway Dashboard
2. Select your project
3. Select the environment (staging or production)
4. Click on your service
5. Go to **Variables** tab
6. Add each variable and its value
7. Click **Save**

## Verification

After setting up secrets, verify they work:

1. **Railway Token:**
   ```bash
   # Authenticate with Railway CLI (safer than exporting token)
   railway login
   railway whoami
   ```

2. **Codecov Token:**
   - Push a commit to main
   - Check if coverage report appears on codecov.io

3. **Slack Webhook:**
   ```bash
   curl -X POST -H 'Content-type: application/json' \
     --data '{"text":"Test message from Tokyo-IA"}' \
     YOUR_WEBHOOK_URL
   ```

## Troubleshooting

### "Railway token invalid"
- Regenerate token in Railway dashboard
- Update `RAILWAY_TOKEN` secret in GitHub

### "Codecov upload failed"
- Verify token is correct
- Check if repository is linked in Codecov
- For public repos, token is optional

### "Slack notification not sent"
- Verify webhook URL is correct
- Check Slack app permissions
- Ensure webhook is active

## Support

For issues with:
- **Railway:** https://railway.app/help
- **Codecov:** https://docs.codecov.com
- **GitHub Actions:** https://docs.github.com/actions
- **Slack Webhooks:** https://api.slack.com/messaging/webhooks

---

**Last Updated:** 2025-12-23
