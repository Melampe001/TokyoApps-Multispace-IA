#!/usr/bin/env python3
"""
Slack Bot for Tokyo-IA

Provides Slack commands to interact with the repository:
- /tokyo-status - Get project status
- /tokyo-issue <number> - Get issue details
- /tokyo-pr <number> - Get PR details
- /tokyo-search <query> - Search issues and PRs
- /tokyo-help - Show help message
"""

import json
import os
import sys
import re
from typing import Dict, List, Optional
import requests

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ImportError:
    print("Slack SDK not installed. Install with: pip install slack-sdk")
    sys.exit(1)

# Configuration
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')
COMMAND_INPUT = os.getenv('COMMAND_INPUT')

def get_github_headers() -> Dict[str, str]:
    """Get GitHub API headers."""
    return {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

def get_repository_status() -> str:
    """Get repository status summary."""
    try:
        # Get open issues
        issues_url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/issues'
        params = {'state': 'open', 'per_page': 100}
        response = requests.get(issues_url, headers=get_github_headers(), params=params, timeout=30)
        response.raise_for_status()
        issues = response.json()
        
        # Separate issues and PRs
        open_issues = [i for i in issues if 'pull_request' not in i]
        open_prs = [i for i in issues if 'pull_request' in i]
        
        # Get recent commits
        commits_url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/commits'
        response = requests.get(commits_url, headers=get_github_headers(), params={'per_page': 10}, timeout=30)
        response.raise_for_status()
        commits = response.json()
        
        # Format status message
        status = f"*Tokyo-IA Project Status*\n\n"
        status += f"📊 *Issues:* {len(open_issues)} open\n"
        status += f"🔀 *Pull Requests:* {len(open_prs)} open\n"
        status += f"💾 *Recent Commits:* {len(commits)} in last update\n\n"
        
        # Add recent commits
        status += "*Recent Activity:*\n"
        for commit in commits[:5]:
            msg = commit['commit']['message'].split('\n')[0][:50]
            author = commit['commit']['author']['name']
            status += f"• {msg} - _{author}_\n"
        
        return status
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching status: {e}"

def get_issue_details(issue_number: int) -> str:
    """Get details for a specific issue."""
    try:
        url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{issue_number}'
        response = requests.get(url, headers=get_github_headers(), timeout=30)
        response.raise_for_status()
        issue = response.json()
        
        # Format issue details
        details = f"*Issue #{issue['number']}: {issue['title']}*\n\n"
        details += f"*Status:* {issue['state']}\n"
        details += f"*Author:* {issue['user']['login']}\n"
        details += f"*Created:* {issue['created_at'][:10]}\n"
        
        if issue.get('assignees'):
            assignees = ', '.join([a['login'] for a in issue['assignees']])
            details += f"*Assignees:* {assignees}\n"
        
        if issue.get('labels'):
            labels = ', '.join([l['name'] for l in issue['labels']])
            details += f"*Labels:* {labels}\n"
        
        details += f"\n*Description:*\n{issue['body'][:500]}"
        details += f"\n\n<{issue['html_url']}|View on GitHub>"
        
        return details
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching issue: {e}"

def get_pr_details(pr_number: int) -> str:
    """Get details for a specific pull request."""
    try:
        url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{pr_number}'
        response = requests.get(url, headers=get_github_headers(), timeout=30)
        response.raise_for_status()
        pr = response.json()
        
        # Format PR details
        details = f"*PR #{pr['number']}: {pr['title']}*\n\n"
        details += f"*Status:* {pr['state']}"
        if pr.get('merged'):
            details += " (merged)"
        details += "\n"
        details += f"*Author:* {pr['user']['login']}\n"
        details += f"*Created:* {pr['created_at'][:10]}\n"
        details += f"*Base:* {pr['base']['ref']} ← *Head:* {pr['head']['ref']}\n"
        
        if pr.get('requested_reviewers'):
            reviewers = ', '.join([r['login'] for r in pr['requested_reviewers']])
            details += f"*Reviewers:* {reviewers}\n"
        
        details += f"\n*Changes:* +{pr['additions']} -{pr['deletions']} lines\n"
        details += f"*Commits:* {pr['commits']}\n"
        
        details += f"\n*Description:*\n{pr['body'][:500] if pr['body'] else 'No description'}"
        details += f"\n\n<{pr['html_url']}|View on GitHub>"
        
        return details
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching PR: {e}"

def search_issues(query: str) -> str:
    """Search for issues and PRs."""
    try:
        # Use GitHub search API
        url = 'https://api.github.com/search/issues'
        params = {
            'q': f'{query} repo:{GITHUB_REPOSITORY}',
            'per_page': 10
        }
        response = requests.get(url, headers=get_github_headers(), params=params, timeout=30)
        response.raise_for_status()
        results = response.json()
        
        if results['total_count'] == 0:
            return f"No results found for: {query}"
        
        # Format results
        output = f"*Search Results for '{query}':* ({results['total_count']} total)\n\n"
        
        for item in results['items'][:10]:
            item_type = "PR" if 'pull_request' in item else "Issue"
            output += f"• *{item_type} #{item['number']}:* {item['title']}\n"
            output += f"  Status: {item['state']} | <{item['html_url']}|View>\n\n"
        
        return output
        
    except requests.exceptions.RequestException as e:
        return f"Error searching: {e}"

def get_help_message() -> str:
    """Get help message."""
    return """*Tokyo-IA Bot Commands*

Available commands:
• `/tokyo-status` - Get project status summary
• `/tokyo-issue <number>` - Get details for an issue
• `/tokyo-pr <number>` - Get details for a pull request
• `/tokyo-search <query>` - Search issues and PRs
• `/tokyo-help` - Show this help message

Examples:
• `/tokyo-status`
• `/tokyo-issue 42`
• `/tokyo-pr 123`
• `/tokyo-search bug authentication`
"""

def parse_command(command_text: str) -> tuple:
    """Parse command text."""
    if not command_text:
        return 'help', []
    
    parts = command_text.strip().split(maxsplit=1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ''
    
    return cmd, args

def process_command(command_text: str) -> str:
    """Process a Slack command."""
    cmd, args = parse_command(command_text)
    
    if cmd in ['status', 'tokyo-status']:
        return get_repository_status()
    
    elif cmd in ['issue', 'tokyo-issue']:
        try:
            issue_num = int(args)
            return get_issue_details(issue_num)
        except ValueError:
            return "Invalid issue number. Usage: `/tokyo-issue <number>`"
    
    elif cmd in ['pr', 'tokyo-pr']:
        try:
            pr_num = int(args)
            return get_pr_details(pr_num)
        except ValueError:
            return "Invalid PR number. Usage: `/tokyo-pr <number>`"
    
    elif cmd in ['search', 'tokyo-search']:
        if not args:
            return "Please provide a search query. Usage: `/tokyo-search <query>`"
        return search_issues(args)
    
    elif cmd in ['help', 'tokyo-help']:
        return get_help_message()
    
    else:
        return f"Unknown command: {cmd}\n\n{get_help_message()}"

def send_slack_message(channel: str, text: str):
    """Send a message to Slack."""
    if not SLACK_BOT_TOKEN:
        print("SLACK_BOT_TOKEN not set, cannot send message")
        return
    
    try:
        client = WebClient(token=SLACK_BOT_TOKEN)
        response = client.chat_postMessage(
            channel=channel,
            text=text
        )
        print(f"Message sent to {channel}: {response['ts']}")
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

def main():
    """Main entry point."""
    print("Starting Slack bot command processor...")
    
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN not set")
        return 1
    
    if not SLACK_BOT_TOKEN:
        print("SLACK_BOT_TOKEN not set, bot features disabled")
        return 0
    
    # Process command from workflow input
    if COMMAND_INPUT:
        print(f"Processing command: {COMMAND_INPUT}")
        response = process_command(COMMAND_INPUT)
        print(f"Response:\n{response}")
    else:
        print("No command to process (use workflow_dispatch with command input)")
    
    print("Slack bot processing completed")
    return 0

if __name__ == '__main__':
    sys.exit(main())
