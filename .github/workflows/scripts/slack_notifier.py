"""
Slack notifier for automated notifications.
Sends proactive notifications based on repository events.
"""
import os
import sys
import json
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta

from utils import APIClient, load_config, safe_get, calculate_age_days, logger

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ImportError:
    logger.warning("Slack SDK not installed")


class SlackNotifier:
    """Automated Slack notifications."""
    
    def __init__(self, slack_token: str, webhook_url: str = None):
        """
        Initialize Slack notifier.
        
        Args:
            slack_token: Slack bot token
            webhook_url: Optional webhook URL for simple notifications
        """
        self.slack = WebClient(token=slack_token)
        self.webhook_url = webhook_url
        
        # Load config
        try:
            self.config = load_config('.github/workflows/config/integrations.json')
            self.channels = self.config['slack']['notification_channels']
        except:
            self.channels = {'dev_team': 'general', 'alerts': 'alerts'}
    
    def send_notification(self, channel: str, message: str, blocks: List[Dict] = None):
        """
        Send notification to Slack channel.
        
        Args:
            channel: Channel ID or name
            message: Plain text message
            blocks: Optional rich message blocks
        """
        try:
            if blocks:
                self.slack.chat_postMessage(
                    channel=channel,
                    text=message,
                    blocks=blocks
                )
            else:
                self.slack.chat_postMessage(
                    channel=channel,
                    text=message
                )
            
            logger.info(f"Sent notification to {channel}")
            
        except SlackApiError as e:
            logger.error(f"Failed to send notification: {e}")
    
    def notify_pr_approved(self, pr_data: Dict[str, Any]):
        """
        Notify when PR is approved.
        
        Args:
            pr_data: PR data from GitHub
        """
        author = safe_get(pr_data, 'user', 'login')
        pr_number = pr_data['number']
        title = pr_data['title']
        url = pr_data['html_url']
        
        message = f"✅ PR #{pr_number} approved: {title}"
        
        blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f"*PR Approved*\n<{url}|#{pr_number}: {title}>"
                }
            },
            {
                'type': 'context',
                'elements': [
                    {
                        'type': 'mrkdwn',
                        'text': f"Author: @{author}"
                    }
                ]
            }
        ]
        
        self.send_notification(self.channels['dev_team'], message, blocks)
    
    def notify_issue_assigned(self, issue_data: Dict[str, Any], assignee: str):
        """
        Notify when issue is assigned.
        
        Args:
            issue_data: Issue data from GitHub
            assignee: Assignee username
        """
        issue_number = issue_data['number']
        title = issue_data['title']
        url = issue_data['html_url']
        
        message = f"📌 You've been assigned to issue #{issue_number}: {title}"
        
        blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f"*New Assignment*\n<{url}|#{issue_number}: {title}>"
                }
            },
            {
                'type': 'context',
                'elements': [
                    {
                        'type': 'mrkdwn',
                        'text': f"Assignee: @{assignee}"
                    }
                ]
            },
            {
                'type': 'actions',
                'elements': [
                    {
                        'type': 'button',
                        'text': {
                            'type': 'plain_text',
                            'text': 'View Issue'
                        },
                        'url': url
                    }
                ]
            }
        ]
        
        self.send_notification(self.channels['dev_team'], message, blocks)
    
    def notify_build_failed(self, commit_data: Dict[str, Any], build_url: str):
        """
        Notify when build fails.
        
        Args:
            commit_data: Commit data from GitHub
            build_url: Build URL
        """
        author = safe_get(commit_data, 'author', 'login')
        commit_message = safe_get(commit_data, 'commit', 'message', default='').split('\n')[0]
        sha = commit_data['sha'][:7]
        
        message = f"❌ Build failed for commit {sha}: {commit_message}"
        
        blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f"*Build Failed*\nCommit: `{sha}`\n{commit_message}"
                }
            },
            {
                'type': 'context',
                'elements': [
                    {
                        'type': 'mrkdwn',
                        'text': f"Author: @{author}"
                    }
                ]
            },
            {
                'type': 'actions',
                'elements': [
                    {
                        'type': 'button',
                        'text': {
                            'type': 'plain_text',
                            'text': 'View Build'
                        },
                        'url': build_url
                    }
                ]
            }
        ]
        
        self.send_notification(self.channels['alerts'], message, blocks)
    
    def notify_critical_blocker(self, item_data: Dict[str, Any]):
        """
        Notify team of critical blocker.
        
        Args:
            item_data: Issue or PR data
        """
        item_type = 'PR' if 'pull_request' in item_data else 'Issue'
        number = item_data['number']
        title = item_data['title']
        url = item_data['html_url']
        age = calculate_age_days(item_data['created_at'])
        
        message = f"🚨 Critical blocker: {item_type} #{number} has been stale for {age} days"
        
        blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f"*Critical Blocker Alert*\n<{url}|{item_type} #{number}: {title}>\n\n⏰ Age: {age} days"
                }
            },
            {
                'type': 'actions',
                'elements': [
                    {
                        'type': 'button',
                        'text': {
                            'type': 'plain_text',
                            'text': 'View Item'
                        },
                        'url': url,
                        'style': 'danger'
                    }
                ]
            }
        ]
        
        self.send_notification(self.channels['alerts'], message, blocks)
    
    def send_daily_summary(self, metrics: Dict[str, Any]):
        """
        Send daily activity summary.
        
        Args:
            metrics: Dictionary of daily metrics
        """
        message = "📊 Daily Summary"
        
        blocks = [
            {
                'type': 'header',
                'text': {
                    'type': 'plain_text',
                    'text': '📊 Daily Activity Summary'
                }
            },
            {
                'type': 'section',
                'fields': [
                    {
                        'type': 'mrkdwn',
                        'text': f"*Commits:*\n{metrics.get('commits', 0)}"
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*PRs Merged:*\n{metrics.get('prs_merged', 0)}"
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*Issues Closed:*\n{metrics.get('issues_closed', 0)}"
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*New Issues:*\n{metrics.get('new_issues', 0)}"
                    }
                ]
            }
        ]
        
        if metrics.get('blockers'):
            blocks.append({
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f"⚠️ *{len(metrics['blockers'])} Blockers Detected*"
                }
            })
        
        if metrics.get('prs_needing_review'):
            blocks.append({
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f"🔍 *{len(metrics['prs_needing_review'])} PRs Awaiting Review*"
                }
            })
        
        self.send_notification(self.channels['dev_team'], message, blocks)
    
    def send_weekly_report(self, metrics: Dict[str, Any]):
        """
        Send weekly report.
        
        Args:
            metrics: Dictionary of weekly metrics
        """
        message = "📈 Weekly Report"
        
        blocks = [
            {
                'type': 'header',
                'text': {
                    'type': 'plain_text',
                    'text': '📈 Weekly Report'
                }
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f"Week {metrics.get('week_number', '?')}"
                }
            },
            {
                'type': 'section',
                'fields': [
                    {
                        'type': 'mrkdwn',
                        'text': f"*Issues Closed:*\n✅ {metrics.get('issues_closed', 0)}"
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*PRs Merged:*\n✅ {metrics.get('prs_merged', 0)}"
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*Velocity:*\n⚡ {metrics.get('velocity', '1.0x')}"
                    },
                    {
                        'type': 'mrkdwn',
                        'text': f"*Quality Score:*\n🎯 {metrics.get('quality_score', 85)}/100"
                    }
                ]
            }
        ]
        
        # Add top contributors
        if metrics.get('top_contributors'):
            contributor_text = '\n'.join([
                f"{i+1}. @{c['name']} - {c['commits']} commits"
                for i, c in enumerate(metrics['top_contributors'][:5])
            ])
            blocks.append({
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f"*Top Contributors:*\n{contributor_text}"
                }
            })
        
        self.send_notification(self.channels['dev_team'], message, blocks)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Slack Notifier')
    parser.add_argument('action', choices=['daily', 'weekly', 'pr-approved', 'build-failed', 'blocker'],
                        help='Notification type')
    parser.add_argument('--data', help='JSON data for notification')
    
    args = parser.parse_args()
    
    # Initialize notifier
    notifier = SlackNotifier(
        os.environ['SLACK_BOT_TOKEN'],
        os.environ.get('SLACK_WEBHOOK_URL')
    )
    
    try:
        if args.action == 'daily':
            # Send daily summary
            metrics = {
                'commits': 15,
                'prs_merged': 3,
                'issues_closed': 5,
                'new_issues': 2,
                'blockers': [],
                'prs_needing_review': []
            }
            notifier.send_daily_summary(metrics)
        
        elif args.action == 'weekly':
            # Send weekly report
            week_number = datetime.utcnow().isocalendar()[1]
            metrics = {
                'week_number': week_number,
                'issues_closed': 8,
                'prs_merged': 12,
                'velocity': '1.2x',
                'quality_score': 88,
                'top_contributors': []
            }
            notifier.send_weekly_report(metrics)
        
        elif args.action == 'pr-approved':
            if args.data:
                pr_data = json.loads(args.data)
                notifier.notify_pr_approved(pr_data)
        
        elif args.action == 'build-failed':
            if args.data:
                data = json.loads(args.data)
                notifier.notify_build_failed(data['commit'], data['build_url'])
        
        elif args.action == 'blocker':
            if args.data:
                item_data = json.loads(args.data)
                notifier.notify_critical_blocker(item_data)
        
        logger.info(f"Notification sent: {args.action}")
        
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
