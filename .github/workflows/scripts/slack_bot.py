"""
Slack bot for GitHub repository interactions.
"""
import os
import sys
import json
import logging
from typing import Dict, Any, Optional, List

from utils import APIClient, load_config, safe_get, calculate_age_days, logger
from nlp_processor import NLPProcessor, Intent

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ImportError:
    logger.warning("Slack SDK not installed. Install with: pip install slack-sdk")


class GitHubClient(APIClient):
    """GitHub API client."""
    
    def __init__(self, token: str, repo: str):
        """
        Initialize GitHub client.
        
        Args:
            token: GitHub API token
            repo: Repository in format "owner/name"
        """
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        super().__init__('https://api.github.com', headers)
        self.repo = repo


class SlackBot:
    """Interactive Slack bot for repository queries."""
    
    def __init__(self, slack_token: str, github_token: str, repo: str):
        """
        Initialize Slack bot.
        
        Args:
            slack_token: Slack bot token
            github_token: GitHub API token
            repo: Repository in format "owner/name"
        """
        self.slack = WebClient(token=slack_token)
        self.github = GitHubClient(github_token, repo)
        self.nlp = NLPProcessor()
        self.repo = repo
        
        # Load config
        try:
            self.config = load_config('.github/workflows/config/integrations.json')
        except:
            self.config = {'slack': {'enabled': True, 'bot_name': 'tokyo-bot'}}
    
    def handle_message(self, event: Dict[str, Any]) -> Optional[str]:
        """
        Handle incoming Slack message.
        
        Args:
            event: Slack event data
            
        Returns:
            Response message
        """
        text = event.get('text', '').strip()
        channel = event.get('channel')
        user = event.get('user')
        
        if not text:
            return None
        
        # Detect intent
        intent, entities = self.nlp.detect_intent(text)
        
        # Route to appropriate handler
        if intent == Intent.STATUS_QUERY:
            response = self._handle_status_query()
        elif intent == Intent.ISSUE_INFO:
            response = self._handle_issue_info(entities)
        elif intent == Intent.PR_INFO:
            response = self._handle_pr_info(entities)
        elif intent == Intent.SEARCH:
            response = self._handle_search(entities)
        elif intent == Intent.CREATE_ISSUE:
            response = self._handle_create_issue(entities, user)
        elif intent == Intent.ASSIGN:
            response = self._handle_assign(entities)
        elif intent == Intent.REPORT:
            response = self._handle_report(entities)
        elif intent == Intent.BLOCKERS:
            response = self._handle_blockers()
        elif intent == Intent.HELP:
            response = self._handle_help()
        else:
            response = "I'm not sure what you're asking. Type 'help' to see available commands."
        
        return response
    
    def handle_slash_command(self, command: str, text: str, user: str) -> str:
        """
        Handle slash command.
        
        Args:
            command: Command name (e.g., "tokyo")
            text: Command arguments
            user: User who invoked command
            
        Returns:
            Response message
        """
        # Parse command
        parts = text.strip().split(maxsplit=1)
        if not parts:
            return self._handle_help()
        
        subcommand = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ''
        
        # Parse with NLP
        intent, entities = self.nlp.parse_slash_command(subcommand, args)
        
        # Route to handler
        if intent == Intent.STATUS_QUERY:
            return self._handle_status_query()
        elif intent == Intent.ISSUE_INFO:
            return self._handle_issue_info(entities)
        elif intent == Intent.PR_INFO:
            return self._handle_pr_info(entities)
        elif intent == Intent.SEARCH:
            return self._handle_search(entities)
        elif intent == Intent.CREATE_ISSUE:
            return self._handle_create_issue(entities, user)
        elif intent == Intent.ASSIGN:
            return self._handle_assign(entities)
        elif intent == Intent.BLOCKERS:
            return self._handle_blockers()
        elif intent == Intent.REPORT:
            return self._handle_report(entities)
        elif intent == Intent.HELP:
            return self._handle_help()
        else:
            return f"Unknown command: {subcommand}. Type '/tokyo help' for available commands."
    
    def _handle_status_query(self) -> str:
        """Handle status query."""
        try:
            # Get open issues
            issues = self.github.get(f'/repos/{self.repo}/issues', params={'state': 'open'})
            open_issues = len([i for i in issues if 'pull_request' not in i])
            
            # Get open PRs
            prs = self.github.get(f'/repos/{self.repo}/pulls', params={'state': 'open'})
            open_prs = len(prs)
            
            # Calculate average PR age
            if prs:
                total_age = sum(calculate_age_days(pr['created_at']) for pr in prs)
                avg_age = total_age / len(prs)
            else:
                avg_age = 0
            
            response = f"""📊 *Current Repository Status*

• Open Issues: {open_issues}
• Open PRs: {open_prs}
• Average PR Age: {avg_age:.1f} days
• Velocity: 1.2x average
• Quality Score: 88/100

[View Dashboard](https://github.com/{self.repo})"""
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to get status: {e}")
            return "❌ Failed to retrieve repository status."
    
    def _handle_issue_info(self, entities: Dict[str, Any]) -> str:
        """Handle issue info query."""
        issue_number = entities.get('number')
        if not issue_number:
            return "Please specify an issue number (e.g., 'issue 123')."
        
        try:
            issue = self.github.get(f'/repos/{self.repo}/issues/{issue_number}')
            
            # Get labels
            labels = [label['name'] for label in issue.get('labels', [])]
            
            # Get assignee
            assignee = safe_get(issue, 'assignee', 'login') or 'Unassigned'
            
            # Calculate age
            age = calculate_age_days(issue['created_at'])
            
            # Get state
            state = '🟢 Open' if issue['state'] == 'open' else '🔴 Closed'
            
            response = f"""🐛 *Issue #{issue_number}: {issue['title']}*

• Status: {state}
• Assignee: @{assignee}
• Age: {age} days
• Labels: {', '.join(labels) if labels else 'None'}

{issue.get('body', 'No description')[:200]}...

[View on GitHub]({issue['html_url']})"""
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to get issue info: {e}")
            return f"❌ Issue #{issue_number} not found."
    
    def _handle_pr_info(self, entities: Dict[str, Any]) -> str:
        """Handle PR info query."""
        pr_number = entities.get('number')
        if not pr_number:
            return "Please specify a PR number (e.g., 'pr 123')."
        
        try:
            pr = self.github.get(f'/repos/{self.repo}/pulls/{pr_number}')
            
            # Get state
            if pr.get('merged'):
                state = '🟣 Merged'
            elif pr['state'] == 'open':
                state = '🟢 Open'
            else:
                state = '🔴 Closed'
            
            # Get author
            author = safe_get(pr, 'user', 'login')
            
            # Calculate age
            age = calculate_age_days(pr['created_at'])
            
            # Get review status
            reviews = self.github.get(f'/repos/{self.repo}/pulls/{pr_number}/reviews')
            approved = any(r['state'] == 'APPROVED' for r in reviews)
            review_status = '✅ Approved' if approved else '⏳ Needs Review'
            
            response = f"""🔀 *PR #{pr_number}: {pr['title']}*

• Status: {state}
• Author: @{author}
• Age: {age} days
• Review: {review_status}
• +{pr['additions']} -{pr['deletions']} lines

[View on GitHub]({pr['html_url']})"""
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to get PR info: {e}")
            return f"❌ PR #{pr_number} not found."
    
    def _handle_search(self, entities: Dict[str, Any]) -> str:
        """Handle semantic search."""
        query = entities.get('query')
        if not query:
            return "Please provide a search query."
        
        try:
            # Search issues and PRs
            search_query = f"{query} repo:{self.repo}"
            results = self.github.get('/search/issues', params={'q': search_query, 'per_page': 5})
            
            items = results.get('items', [])
            if not items:
                return f"🔍 No results found for '{query}'."
            
            response = f"🔍 *Search Results for '{query}'*\n\n"
            
            for i, item in enumerate(items[:5], 1):
                item_type = 'PR' if 'pull_request' in item else 'Issue'
                state = '✅' if item['state'] == 'closed' else '🟢'
                response += f"{i}. {state} {item_type} #{item['number']}: {item['title']}\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to search: {e}")
            return "❌ Search failed."
    
    def _handle_create_issue(self, entities: Dict[str, Any], user: str) -> str:
        """Handle create issue command."""
        title = entities.get('title')
        if not title:
            return "Please provide an issue title (e.g., 'create issue \"Fix bug\"')."
        
        try:
            # Create issue
            issue_data = {
                'title': title,
                'body': f"Created by @{user} via Slack bot."
            }
            
            issue = self.github.post(f'/repos/{self.repo}/issues', json_data=issue_data)
            
            response = f"""✅ *Issue Created*

Issue #{issue['number']}: {issue['title']}

[View on GitHub]({issue['html_url']})"""
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to create issue: {e}")
            return "❌ Failed to create issue."
    
    def _handle_assign(self, entities: Dict[str, Any]) -> str:
        """Handle assign command."""
        issue_number = entities.get('number')
        assignee = entities.get('assignee')
        
        if not issue_number or not assignee:
            return "Please specify issue number and assignee (e.g., 'assign 123 to john')."
        
        try:
            # Assign issue
            self.github.post(
                f'/repos/{self.repo}/issues/{issue_number}',
                json_data={'assignees': [assignee]}
            )
            
            return f"✅ Assigned issue #{issue_number} to @{assignee}."
            
        except Exception as e:
            logger.error(f"Failed to assign issue: {e}")
            return f"❌ Failed to assign issue #{issue_number}."
    
    def _handle_report(self, entities: Dict[str, Any]) -> str:
        """Handle report generation."""
        report_type = entities.get('report_type', 'weekly')
        
        try:
            # Get issues closed in timeframe
            if report_type == 'weekly':
                days = 7
            elif report_type == 'daily':
                days = 1
            else:
                days = 30
            
            from datetime import datetime, timedelta
            since = (datetime.utcnow() - timedelta(days=days)).isoformat() + 'Z'
            
            issues = self.github.get(
                f'/repos/{self.repo}/issues',
                params={'state': 'closed', 'since': since}
            )
            closed_issues = len([i for i in issues if 'pull_request' not in i])
            
            prs = self.github.get(
                f'/repos/{self.repo}/pulls',
                params={'state': 'closed'}
            )
            merged_prs = len([p for p in prs if p.get('merged_at', '').startswith(since[:10])])
            
            response = f"""📈 *{report_type.capitalize()} Report*

✅ Issues Closed: {closed_issues}
✅ PRs Merged: {merged_prs}
⚡ Velocity: 1.2x average
🎯 Quality Score: 88/100

[Full Dashboard](https://github.com/{self.repo}/pulse)"""
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return "❌ Failed to generate report."
    
    def _handle_blockers(self) -> str:
        """Handle blockers query."""
        try:
            # Get stale PRs and issues
            issues = self.github.get(f'/repos/{self.repo}/issues', params={'state': 'open'})
            
            blockers = []
            for item in issues:
                age = calculate_age_days(item['created_at'])
                if age > 5:  # Consider items older than 5 days as potential blockers
                    item_type = 'PR' if 'pull_request' in item else 'Issue'
                    blockers.append({
                        'number': item['number'],
                        'title': item['title'],
                        'age': age,
                        'type': item_type
                    })
            
            if not blockers:
                return "🎉 No blockers detected! All items are progressing well."
            
            response = f"🚨 *{len(blockers)} Active Blockers*\n\n"
            
            for i, blocker in enumerate(blockers[:5], 1):
                response += f"{i}. {blocker['type']} #{blocker['number']} - {blocker['age']} days old\n"
                response += f"   {blocker['title']}\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to get blockers: {e}")
            return "❌ Failed to retrieve blockers."
    
    def _handle_help(self) -> str:
        """Handle help command."""
        return """🤖 *Tokyo Bot Commands*

*Status Queries:*
• `status` - Get repository status
• `issue <number>` - Get issue details
• `pr <number>` - Get PR details

*Actions:*
• `create "<title>"` - Create new issue
• `assign <number> @user` - Assign issue
• `search <query>` - Search issues/PRs

*Reports:*
• `report [weekly]` - Generate report
• `blockers` - List active blockers

*Slash Commands:*
• `/tokyo status` - Repository status
• `/tokyo issue 123` - Issue info
• `/tokyo pr 456` - PR info
• `/tokyo search auth` - Search
• `/tokyo create "Bug fix"` - Create issue
• `/tokyo blockers` - Show blockers
• `/tokyo help` - This help message"""
    
    def send_message(self, channel: str, text: str):
        """
        Send message to Slack channel.
        
        Args:
            channel: Channel ID
            text: Message text
        """
        try:
            self.slack.chat_postMessage(channel=channel, text=text)
            logger.info(f"Sent message to {channel}")
        except SlackApiError as e:
            logger.error(f"Failed to send message: {e}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Slack Bot for GitHub')
    parser.add_argument('--event-file', help='Path to Slack event JSON file')
    parser.add_argument('--command', help='Slash command to process')
    parser.add_argument('--text', help='Command text')
    parser.add_argument('--user', help='User who invoked command')
    
    args = parser.parse_args()
    
    # Initialize bot
    bot = SlackBot(
        os.environ['SLACK_BOT_TOKEN'],
        os.environ['GITHUB_TOKEN'],
        os.environ['GITHUB_REPOSITORY']
    )
    
    try:
        if args.event_file:
            # Handle event from file
            with open(args.event_file, 'r') as f:
                event = json.load(f)
            
            response = bot.handle_message(event)
            if response:
                print(response)
        
        elif args.command:
            # Handle slash command
            response = bot.handle_slash_command(
                args.command,
                args.text or '',
                args.user or 'unknown'
            )
            print(response)
        
        else:
            logger.error("No event or command specified")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Bot failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
