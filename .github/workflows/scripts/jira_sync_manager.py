"""
Jira Synchronization Manager for GitHub Actions.
Handles bidirectional sync between GitHub issues/PRs and Jira tickets.
"""
import os
import sys
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from utils import (
    APIClient, load_config, safe_get, timestamp_to_iso,
    iso_to_timestamp, retry_with_backoff, logger
)

# Configure logging
logger = logging.getLogger(__name__)


class JiraClient(APIClient):
    """Jira API client with authentication."""
    
    def __init__(self, base_url: str, email: str, api_token: str):
        """
        Initialize Jira client.
        
        Args:
            base_url: Jira instance URL
            email: User email
            api_token: API token
        """
        import base64
        auth_string = f"{email}:{api_token}"
        auth_bytes = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
        
        headers = {
            'Authorization': f'Basic {auth_bytes}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        super().__init__(base_url, headers)


class GitHubClient(APIClient):
    """GitHub API client with authentication."""
    
    def __init__(self, token: str):
        """
        Initialize GitHub client.
        
        Args:
            token: GitHub API token
        """
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        super().__init__('https://api.github.com', headers)


class JiraSyncManager:
    """Manages bidirectional synchronization between GitHub and Jira."""
    
    def __init__(self, config_dir: str = '.github/workflows/config'):
        """
        Initialize sync manager.
        
        Args:
            config_dir: Path to configuration directory
        """
        # Load configurations
        self.integrations_config = load_config(f'{config_dir}/integrations.json')
        self.mappings_config = load_config(f'{config_dir}/jira-mappings.json')
        
        # Initialize clients
        self.jira = JiraClient(
            os.environ['JIRA_BASE_URL'],
            os.environ['JIRA_USER_EMAIL'],
            os.environ['JIRA_API_TOKEN']
        )
        self.github = GitHubClient(os.environ['GITHUB_TOKEN'])
        
        # Get repository info
        repo = os.environ['GITHUB_REPOSITORY']
        self.repo_owner, self.repo_name = repo.split('/')
        
        # Sync state tracking
        self.sync_log = []
    
    def github_label_to_jira_type(self, labels: List[str]) -> str:
        """
        Map GitHub labels to Jira issue type.
        
        Args:
            labels: List of GitHub label names
            
        Returns:
            Jira issue type
        """
        label_to_type = self.mappings_config['label_to_type']
        for label in labels:
            if label in label_to_type:
                return label_to_type[label]
        return 'Task'  # Default type
    
    def github_label_to_jira_priority(self, labels: List[str]) -> Optional[str]:
        """
        Map GitHub labels to Jira priority.
        
        Args:
            labels: List of GitHub label names
            
        Returns:
            Jira priority or None
        """
        label_to_priority = self.mappings_config['label_to_priority']
        for label in labels:
            if label in label_to_priority:
                return label_to_priority[label]
        return None
    
    def github_status_to_jira(self, gh_status: str) -> str:
        """
        Map GitHub status to Jira status.
        
        Args:
            gh_status: GitHub status
            
        Returns:
            Jira status
        """
        mapping = self.mappings_config['status_mapping']['github_to_jira']
        return mapping.get(gh_status, 'To Do')
    
    def jira_status_to_github(self, jira_status: str) -> str:
        """
        Map Jira status to GitHub status.
        
        Args:
            jira_status: Jira status
            
        Returns:
            GitHub status
        """
        mapping = self.mappings_config['status_mapping']['jira_to_github']
        return mapping.get(jira_status, 'open')
    
    def create_jira_ticket(self, issue_data: Dict[str, Any]) -> Optional[str]:
        """
        Create Jira ticket from GitHub issue.
        
        Args:
            issue_data: GitHub issue data
            
        Returns:
            Jira ticket key or None
        """
        try:
            labels = [label['name'] for label in issue_data.get('labels', [])]
            issue_type = self.github_label_to_jira_type(labels)
            priority = self.github_label_to_jira_priority(labels)
            
            # Get project key (use first configured project)
            project_key = self.integrations_config['jira']['projects'][0]
            
            # Build Jira ticket data
            ticket_data = {
                'fields': {
                    'project': {'key': project_key},
                    'summary': issue_data['title'],
                    'description': self._format_description_for_jira(issue_data),
                    'issuetype': {'name': issue_type}
                }
            }
            
            if priority:
                ticket_data['fields']['priority'] = {'name': priority}
            
            # Create ticket
            response = self.jira.post('/rest/api/2/issue', json_data=ticket_data)
            jira_key = response['key']
            
            logger.info(f"Created Jira ticket {jira_key} for GitHub issue #{issue_data['number']}")
            
            # Add comment with GitHub link
            self.add_jira_comment(
                jira_key,
                f"Synced from GitHub issue: {issue_data['html_url']}"
            )
            
            # Update GitHub issue with Jira link
            self.add_github_comment(
                issue_data['number'],
                f"Jira ticket created: [{jira_key}]({os.environ['JIRA_BASE_URL']}/browse/{jira_key})"
            )
            
            # Log sync operation
            self.sync_log.append({
                'timestamp': timestamp_to_iso(),
                'action': 'create_jira_ticket',
                'github_issue': issue_data['number'],
                'jira_ticket': jira_key,
                'status': 'success'
            })
            
            return jira_key
            
        except Exception as e:
            logger.error(f"Failed to create Jira ticket: {e}")
            self.sync_log.append({
                'timestamp': timestamp_to_iso(),
                'action': 'create_jira_ticket',
                'github_issue': issue_data['number'],
                'error': str(e),
                'status': 'failed'
            })
            return None
    
    def _format_description_for_jira(self, issue_data: Dict[str, Any]) -> str:
        """Format GitHub issue description for Jira."""
        body = issue_data.get('body', 'No description provided.')
        author = issue_data['user']['login']
        created_at = issue_data['created_at']
        
        return f"""
{body}

---
*Created by @{author} on {created_at}*
*GitHub Issue: {issue_data['html_url']}*
"""
    
    def update_jira_status(self, jira_key: str, new_status: str) -> bool:
        """
        Update Jira ticket status.
        
        Args:
            jira_key: Jira ticket key
            new_status: New status name
            
        Returns:
            True if successful
        """
        try:
            # Get available transitions
            response = self.jira.get(f'/rest/api/2/issue/{jira_key}/transitions')
            transitions = response['transitions']
            
            # Find transition ID for target status
            transition_id = None
            for transition in transitions:
                if transition['to']['name'] == new_status:
                    transition_id = transition['id']
                    break
            
            if transition_id is None:
                logger.warning(f"No transition found to status '{new_status}' for {jira_key}")
                return False
            
            # Execute transition
            self.jira.post(
                f'/rest/api/2/issue/{jira_key}/transitions',
                json_data={'transition': {'id': transition_id}}
            )
            
            logger.info(f"Updated {jira_key} status to '{new_status}'")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update Jira status: {e}")
            return False
    
    def add_jira_comment(self, jira_key: str, comment: str) -> bool:
        """
        Add comment to Jira ticket.
        
        Args:
            jira_key: Jira ticket key
            comment: Comment text
            
        Returns:
            True if successful
        """
        try:
            self.jira.post(
                f'/rest/api/2/issue/{jira_key}/comment',
                json_data={'body': comment}
            )
            logger.debug(f"Added comment to {jira_key}")
            return True
        except Exception as e:
            logger.error(f"Failed to add Jira comment: {e}")
            return False
    
    def add_github_comment(self, issue_number: int, comment: str) -> bool:
        """
        Add comment to GitHub issue.
        
        Args:
            issue_number: GitHub issue number
            comment: Comment text
            
        Returns:
            True if successful
        """
        try:
            self.github.post(
                f'/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}/comments',
                json_data={'body': comment}
            )
            logger.debug(f"Added comment to GitHub issue #{issue_number}")
            return True
        except Exception as e:
            logger.error(f"Failed to add GitHub comment: {e}")
            return False
    
    def sync_github_to_jira(self, issue_number: int) -> Optional[str]:
        """
        Sync GitHub issue to Jira.
        
        Args:
            issue_number: GitHub issue number
            
        Returns:
            Jira ticket key or None
        """
        try:
            # Get GitHub issue
            issue = self.github.get(
                f'/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}'
            )
            
            # Check if Jira ticket already exists (look for Jira key in comments)
            jira_key = self._find_linked_jira_ticket(issue_number)
            
            if jira_key:
                logger.info(f"GitHub issue #{issue_number} already linked to {jira_key}")
                return jira_key
            
            # Create new Jira ticket
            return self.create_jira_ticket(issue)
            
        except Exception as e:
            logger.error(f"Failed to sync GitHub to Jira: {e}")
            return None
    
    def _find_linked_jira_ticket(self, issue_number: int) -> Optional[str]:
        """
        Find Jira ticket linked to GitHub issue.
        
        Args:
            issue_number: GitHub issue number
            
        Returns:
            Jira ticket key or None
        """
        try:
            # Get issue comments
            comments = self.github.get(
                f'/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}/comments'
            )
            
            # Look for Jira ticket key in comments
            import re
            for comment in comments:
                body = comment.get('body', '')
                # Look for pattern like TOKYO-123 or IA-456
                match = re.search(r'\b([A-Z]+-\d+)\b', body)
                if match:
                    return match.group(1)
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to find linked Jira ticket: {e}")
            return None
    
    def sync_jira_to_github(self, jira_key: str, github_issue: int) -> bool:
        """
        Sync Jira ticket changes to GitHub.
        
        Args:
            jira_key: Jira ticket key
            github_issue: GitHub issue number
            
        Returns:
            True if successful
        """
        try:
            # Get Jira ticket
            ticket = self.jira.get(f'/rest/api/2/issue/{jira_key}')
            
            # Map Jira status to GitHub
            jira_status = safe_get(ticket, 'fields', 'status', 'name')
            gh_status = self.jira_status_to_github(jira_status)
            
            # Update GitHub issue state if needed
            if gh_status == 'closed':
                self.github.post(
                    f'/repos/{self.repo_owner}/{self.repo_name}/issues/{github_issue}',
                    json_data={'state': 'closed'}
                )
                logger.info(f"Closed GitHub issue #{github_issue} (synced from {jira_key})")
            elif gh_status == 'open':
                self.github.post(
                    f'/repos/{self.repo_owner}/{self.repo_name}/issues/{github_issue}',
                    json_data={'state': 'open'}
                )
                logger.info(f"Reopened GitHub issue #{github_issue} (synced from {jira_key})")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to sync Jira to GitHub: {e}")
            return False
    
    def handle_conflict(self, github_issue: int, jira_key: str) -> bool:
        """
        Handle sync conflict between GitHub and Jira.
        
        Args:
            github_issue: GitHub issue number
            jira_key: Jira ticket key
            
        Returns:
            True if resolved
        """
        strategy = self.mappings_config['conflict_resolution']['strategy']
        
        if strategy == 'last_write_wins':
            # Compare timestamps and sync from newer to older
            try:
                gh_issue = self.github.get(
                    f'/repos/{self.repo_owner}/{self.repo_name}/issues/{github_issue}'
                )
                jira_ticket = self.jira.get(f'/rest/api/2/issue/{jira_key}')
                
                gh_updated = iso_to_timestamp(gh_issue['updated_at'])
                jira_updated = iso_to_timestamp(safe_get(jira_ticket, 'fields', 'updated'))
                
                if gh_updated > jira_updated:
                    logger.info(f"Conflict: GitHub is newer, syncing to Jira")
                    self.sync_github_to_jira(github_issue)
                else:
                    logger.info(f"Conflict: Jira is newer, syncing to GitHub")
                    self.sync_jira_to_github(jira_key, github_issue)
                
                # Notify if configured
                if self.mappings_config['conflict_resolution']['notify_on_conflict']:
                    self.add_github_comment(
                        github_issue,
                        f"⚠️ Sync conflict detected and resolved using last-write-wins strategy."
                    )
                
                return True
                
            except Exception as e:
                logger.error(f"Failed to resolve conflict: {e}")
                return False
        
        return False
    
    def save_sync_log(self, output_file: str = 'sync-log.json'):
        """
        Save sync log to file.
        
        Args:
            output_file: Output file path
        """
        with open(output_file, 'w') as f:
            json.dump(self.sync_log, f, indent=2)
        logger.info(f"Sync log saved to {output_file}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Jira-GitHub Sync Manager')
    parser.add_argument('action', choices=['create', 'update', 'sync'],
                        help='Action to perform')
    parser.add_argument('--issue', type=int, help='GitHub issue number')
    parser.add_argument('--jira-key', help='Jira ticket key')
    parser.add_argument('--config-dir', default='.github/workflows/config',
                        help='Configuration directory')
    
    args = parser.parse_args()
    
    # Initialize sync manager
    manager = JiraSyncManager(args.config_dir)
    
    try:
        if args.action == 'create':
            if not args.issue:
                logger.error("--issue required for create action")
                sys.exit(1)
            
            jira_key = manager.sync_github_to_jira(args.issue)
            if jira_key:
                print(f"Created Jira ticket: {jira_key}")
            else:
                sys.exit(1)
        
        elif args.action == 'update':
            if not args.issue or not args.jira_key:
                logger.error("--issue and --jira-key required for update action")
                sys.exit(1)
            
            success = manager.sync_jira_to_github(args.jira_key, args.issue)
            if not success:
                sys.exit(1)
        
        elif args.action == 'sync':
            if not args.issue or not args.jira_key:
                logger.error("--issue and --jira-key required for sync action")
                sys.exit(1)
            
            success = manager.handle_conflict(args.issue, args.jira_key)
            if not success:
                sys.exit(1)
        
        # Save sync log
        manager.save_sync_log()
        
    except Exception as e:
        logger.error(f"Sync failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
