# Integration Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Tokyo-IA integrations.

## Table of Contents

- [General Troubleshooting](#general-troubleshooting)
- [Jira Integration Issues](#jira-integration-issues)
- [Google Sheets Issues](#google-sheets-issues)
- [Slack Bot Issues](#slack-bot-issues)
- [Health Check Failures](#health-check-failures)
- [Getting Help](#getting-help)

---

## General Troubleshooting

### Check Integration Health

Run the health check workflow:

```bash
gh workflow run integrations-health-check.yml
```

Or via GitHub UI:
1. Go to **Actions** tab
2. Select **Integrations Health Check**
3. Click **Run workflow**

### View Workflow Logs

1. Go to **Actions** tab
2. Select the relevant workflow
3. Click on a recent run
4. Expand each step to view logs
5. Look for error messages in red

### Verify Secrets

Ensure all required secrets are set:

```bash
# List secrets (won't show values)
gh secret list

# Required secrets:
# - JIRA_BASE_URL
# - JIRA_USER_EMAIL
# - JIRA_API_TOKEN
# - GOOGLE_CREDENTIALS
# - GOOGLE_SHEET_ID
# - SLACK_BOT_TOKEN
# - SLACK_SIGNING_SECRET
```

### Check Configuration Files

Verify configuration files are valid JSON:

```bash
# Validate JSON
python -m json.tool .github/workflows/config/integrations.json
python -m json.tool .github/workflows/config/jira-mappings.json
```

---

## Jira Integration Issues

### Issue: "Authentication failed"

**Symptoms:**
- Workflow fails with 401 Unauthorized
- Error message: "Authentication failed"

**Solutions:**

1. **Verify API token:**
   ```bash
   # Test Jira connection
   curl -u "email@example.com:api_token" \
        "https://yourcompany.atlassian.net/rest/api/2/myself"
   ```

2. **Check token hasn't expired:**
   - Jira API tokens don't expire, but can be revoked
   - Regenerate token if needed

3. **Verify email matches:**
   - `JIRA_USER_EMAIL` must match the account that created the token

4. **Check Base URL format:**
   - Should NOT have trailing slash
   - Correct: `https://yourcompany.atlassian.net`
   - Wrong: `https://yourcompany.atlassian.net/`

### Issue: "Project not found"

**Symptoms:**
- Error: "Project with key TOKYO does not exist"

**Solutions:**

1. **Verify project key:**
   ```python
   # List available projects
   curl -u "email:token" \
        "https://yourcompany.atlassian.net/rest/api/2/project"
   ```

2. **Update configuration:**
   Edit `.github/workflows/config/integrations.json`:
   ```json
   "jira": {
     "projects": ["YOUR_ACTUAL_PROJECT_KEY"]
   }
   ```

### Issue: Jira tickets not syncing

**Symptoms:**
- GitHub issues created but no Jira ticket
- Workflow completes but no sync happens

**Solutions:**

1. **Check issue type mapping:**
   - Verify issue types exist in Jira
   - Edit `.github/workflows/config/jira-mappings.json`
   - Ensure types match exactly (case-sensitive)

2. **Check required fields:**
   - Some Jira projects require additional fields
   - Add them to `custom_fields` in mapping config

3. **Review sync log:**
   - Download artifact from workflow run
   - Check `sync-log.json` for detailed errors

### Issue: Status not syncing

**Symptoms:**
- Tickets created but status doesn't update
- Error: "Transition not found"

**Solutions:**

1. **Check workflow transitions:**
   ```bash
   # Get available transitions for an issue
   curl -u "email:token" \
        "https://yourcompany.atlassian.net/rest/api/2/issue/KEY-123/transitions"
   ```

2. **Update status mapping:**
   - Map to available transition names
   - Transitions are workflow-specific

3. **Verify permissions:**
   - User must have permission to transition issues

### Issue: Comments not syncing

**Symptoms:**
- GitHub comments don't appear in Jira

**Solutions:**

1. **Check sync rules:**
   Edit `.github/workflows/config/jira-mappings.json`:
   ```json
   "sync_rules": {
     "sync_comments": true
   }
   ```

2. **Verify comment permissions:**
   - User must have "Add Comments" permission

---

## Google Sheets Issues

### Issue: "Permission denied"

**Symptoms:**
- Error: "The caller does not have permission"
- 403 Forbidden error

**Solutions:**

1. **Verify sheet is shared:**
   - Check service account email has Editor access
   - Email format: `name@project-id.iam.gserviceaccount.com`

2. **Check Google Sheets API is enabled:**
   - Go to Google Cloud Console
   - Navigate to APIs & Services → Library
   - Search "Google Sheets API"
   - Verify it's enabled

3. **Regenerate credentials:**
   - Create new service account key
   - Update `GOOGLE_CREDENTIALS` secret

### Issue: "Invalid credentials"

**Symptoms:**
- Error: "Unable to parse credentials"
- Authentication fails

**Solutions:**

1. **Verify JSON format:**
   - Ensure entire JSON content is copied
   - No extra spaces or line breaks
   - Valid JSON structure

2. **Test credentials locally:**
   ```python
   import json
   import os
   from google.oauth2 import service_account
   
   creds = service_account.Credentials.from_service_account_info(
       json.loads(os.environ['GOOGLE_CREDENTIALS']),
       scopes=['https://www.googleapis.com/auth/spreadsheets']
   )
   print("Credentials valid!")
   ```

### Issue: Data not updating

**Symptoms:**
- Workflow succeeds but sheet unchanged
- Old data still showing

**Solutions:**

1. **Verify Sheet ID:**
   - Check `GOOGLE_SHEET_ID` matches sheet URL
   - ID should be alphanumeric string

2. **Check tab names:**
   - Tab names are case-sensitive
   - Must match exactly: `Daily_Metrics`, `Weekly_Trends`, etc.

3. **Review write permissions:**
   - Service account needs Editor access
   - Not Viewer or Commenter

### Issue: Formatting not applied

**Symptoms:**
- Data appears but no colors
- Conditional formatting missing

**Solutions:**

1. **Check formatter execution:**
   - Verify formatting step runs in workflow
   - Check for errors in formatting script

2. **Manually trigger formatting:**
   ```bash
   gh workflow run sheets-dashboard-update.yml
   ```

3. **Verify column indices:**
   - Column indices are 0-based
   - Update indices if columns changed

---

## Slack Bot Issues

### Issue: Bot doesn't respond

**Symptoms:**
- @mention doesn't trigger bot
- Slash command times out

**Solutions:**

1. **Verify bot is in channel:**
   ```
   /invite @Tokyo Bot
   ```

2. **Check event subscriptions:**
   - Go to Slack App settings
   - Verify `app_mention` is subscribed
   - Check request URL is correct

3. **Test webhook receiver:**
   - Verify webhook relay is running
   - Check logs for incoming requests

4. **Review workflow logs:**
   - Check GitHub Actions for errors
   - Verify repository_dispatch is triggered

### Issue: "Invalid token" error

**Symptoms:**
- Error: "invalid_auth"
- Bot can't send messages

**Solutions:**

1. **Verify token format:**
   - Bot token should start with `xoxb-`
   - App token should start with `xapp-`

2. **Regenerate token:**
   - Go to Slack App settings
   - OAuth & Permissions → Reinstall to Workspace
   - Update `SLACK_BOT_TOKEN` secret

3. **Check token scope:**
   - Ensure `chat:write` scope is added
   - Reinstall app after scope changes

### Issue: Slash commands timeout

**Symptoms:**
- "timeout" error in Slack
- Command doesn't respond within 3 seconds

**Solutions:**

1. **Use immediate acknowledgment:**
   - Webhook receiver should respond immediately
   - Process command asynchronously

2. **Check webhook performance:**
   - Ensure webhook relay responds quickly
   - Consider using Socket Mode for better performance

### Issue: Notifications not sending

**Symptoms:**
- No daily/weekly reports
- Real-time notifications missing

**Solutions:**

1. **Check channel IDs:**
   - Verify correct channel IDs in config
   - Channel IDs start with 'C'

2. **Verify bot is channel member:**
   ```
   /invite @Tokyo Bot
   ```

3. **Check workflow schedule:**
   - Verify cron expression is correct
   - Workflows run in UTC time

### Issue: "Channel not found" error

**Symptoms:**
- Error: "channel_not_found"

**Solutions:**

1. **Get correct channel ID:**
   - Right-click channel → Copy link
   - Extract ID from URL: `slack.com/archives/C01234567`

2. **Update configuration:**
   Edit `.github/workflows/config/integrations.json`:
   ```json
   "notification_channels": {
     "dev_team": "C01234567",
     "alerts": "C01234568"
   }
   ```

---

## Health Check Failures

### Persistent Health Check Failures

**Symptoms:**
- Health check workflow creates issues repeatedly
- All integrations failing

**Solutions:**

1. **Check service status:**
   - Jira: https://status.atlassian.com/
   - Google: https://www.google.com/appsstatus
   - Slack: https://status.slack.com/

2. **Review rate limits:**
   - Check if API rate limits exceeded
   - Implement backoff strategy

3. **Verify network connectivity:**
   - GitHub Actions runners can reach external services
   - Check for firewall restrictions

### False Positive Health Checks

**Symptoms:**
- Health check fails but integration works

**Solutions:**

1. **Adjust timeout:**
   - Increase timeout in health check script
   - Account for network latency

2. **Review check logic:**
   - Ensure test operations are valid
   - Use appropriate test endpoints

---

## Performance Issues

### Slow Sync Times

**Symptoms:**
- Sync takes longer than expected
- Workflows timeout

**Solutions:**

1. **Increase timeout:**
   Edit workflow file:
   ```yaml
   - name: Sync
     timeout-minutes: 10  # Increase from default 5
   ```

2. **Batch operations:**
   - Process items in batches
   - Use pagination for large result sets

3. **Enable caching:**
   - Cache Python dependencies
   - Reduce setup time

### Rate Limiting

**Symptoms:**
- Error: "Rate limit exceeded"
- 429 Too Many Requests

**Solutions:**

1. **Implement exponential backoff:**
   - Already implemented in `utils.py`
   - Adjust retry parameters if needed

2. **Reduce sync frequency:**
   - Increase cron interval
   - Process fewer items per run

3. **Use conditional requests:**
   - Check `If-Modified-Since` headers
   - Skip unchanged items

---

## Debugging Tips

### Enable Debug Logging

Add to workflow:

```yaml
- name: Enable debug logging
  run: |
    export ACTIONS_STEP_DEBUG=true
    export ACTIONS_RUNNER_DEBUG=true
```

### Test Scripts Locally

```bash
# Test Jira sync
cd .github/workflows/scripts
export JIRA_BASE_URL="..."
export JIRA_USER_EMAIL="..."
export JIRA_API_TOKEN="..."
python jira_sync_manager.py create --issue 123

# Test Sheets update
export GOOGLE_CREDENTIALS='...'
export GOOGLE_SHEET_ID='...'
python sheets_updater.py

# Test Slack bot
export SLACK_BOT_TOKEN='...'
python slack_bot.py --command status --text "" --user test
```

### Check Dependencies

```bash
# Verify Python packages
pip install -r requirements.txt

# Test imports
python -c "import requests; import slack_sdk; print('OK')"
```

### Review Audit Logs

- **Jira**: Settings → System → Audit Log
- **Google**: Cloud Console → IAM → Activity
- **Slack**: App Settings → Event Subscriptions → Recent Events

---

## Common Error Messages

### "Module not found"

**Solution:** Install missing dependencies
```bash
pip install requests slack-sdk google-api-python-client
```

### "Secret not found"

**Solution:** Add missing secret to GitHub repository settings

### "Invalid JSON"

**Solution:** Validate configuration files
```bash
python -m json.tool config.json
```

### "Connection timeout"

**Solution:** 
- Check network connectivity
- Increase timeout values
- Verify service is reachable

---

## Getting Help

### Check Documentation

- [Jira Setup Guide](./JIRA_SETUP.md)
- [Google Sheets Setup Guide](./GOOGLE_SHEETS_SETUP.md)
- [Slack Bot Setup Guide](./SLACK_BOT_SETUP.md)

### Review Workflow Logs

1. Go to Actions tab
2. Select failed workflow
3. Download logs artifact
4. Check for detailed error messages

### Create Issue

If problem persists:

1. Create a GitHub issue
2. Include:
   - Error message
   - Workflow logs
   - Steps to reproduce
   - Expected vs actual behavior

### Contact Information

- **Repository Issues**: Create issue in this repository
- **Jira Support**: https://support.atlassian.com/
- **Google Cloud Support**: https://cloud.google.com/support
- **Slack Support**: https://slack.com/help

---

## Preventive Maintenance

### Regular Tasks

**Weekly:**
- Review integration health checks
- Check for workflow failures
- Monitor rate limit usage

**Monthly:**
- Review and archive old data
- Update dependencies
- Check for API deprecations

**Quarterly:**
- Rotate API tokens/secrets
- Review and optimize workflows
- Update documentation

### Monitoring Checklist

- [ ] All health checks passing
- [ ] No failed workflow runs
- [ ] Sync delays < 5 minutes
- [ ] Error rate < 1%
- [ ] All secrets up to date
- [ ] Documentation current

---

## Advanced Debugging

### Enable Verbose Logging

Add to Python scripts:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Capture Network Requests

```python
import logging
import http.client

http.client.HTTPConnection.debuglevel = 1
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
```

### Profile Performance

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats()
```

---

## FAQ

**Q: How often does sync run?**
A: Jira syncs every 15 minutes, Sheets every 2 hours, Slack notifications are real-time.

**Q: Can I customize sync frequency?**
A: Yes, edit the cron schedule in workflow files.

**Q: What happens if sync fails?**
A: Workflow retries with exponential backoff. After 3 failures, health check creates an issue.

**Q: Are my credentials secure?**
A: Yes, secrets are encrypted and never exposed in logs.

**Q: Can I disable specific integrations?**
A: Yes, set `enabled: false` in `integrations.json`.

**Q: How do I view sync history?**
A: Check workflow artifacts for sync logs, or view Actions tab.

---

## Related Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Jira Cloud REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Slack API](https://api.slack.com/)
