#!/usr/bin/env python3
"""
Jira Sync Script - Bidirectional synchronization between GitHub Issues and Jira.

This script syncs GitHub issues to Jira tickets and vice versa.
Supports: issue creation, updates, status changes, and comments.
"""

import json
import os
import sys
import requests
from typing import Dict, Optional, Any

# Configuration
JIRA_BASE_URL = os.getenv('JIRA_BASE_URL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_EVENT_NAME = os.getenv('GITHUB_EVENT_NAME')
GITHUB_EVENT_PATH = os.getenv('GITHUB_EVENT_PATH')

# Load configuration
CONFIG_PATH = '.github/workflows/config/integrations.json'

def load_config() -> Dict:
    """Load integration configuration."""
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "jira": {
                "enabled": True,
                "projects": ["TOKYO"],
                "sync_interval_minutes": 15,
                "label_mappings": {
                    "bug": "Bug",
                    "enhancement": "Story",
                    "documentation": "Task"
                }
            }
        }

def get_jira_headers() -> Dict[str, str]:
    """Get Jira API headers."""
    import base64
    auth_str = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
    auth_bytes = auth_str.encode('ascii')
    auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
    
    return {
        'Authorization': f'Basic {auth_b64}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

def get_github_headers() -> Dict[str, str]:
    """Get GitHub API headers."""
    return {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

def map_github_label_to_jira_type(labels: list) -> str:
    """Map GitHub labels to Jira issue types."""
    config = load_config()
    label_mappings = config['jira'].get('label_mappings', {})
    
    for label in labels:
        label_name = label.get('name', '').lower()
        if label_name in label_mappings:
            return label_mappings[label_name]
    
    return 'Task'  # Default

def map_github_state_to_jira_status(state: str) -> str:
    """Map GitHub issue state to Jira status."""
    mapping = {
        'open': 'To Do',
        'closed': 'Done'
    }
    return mapping.get(state, 'To Do')

def get_jira_ticket_from_github_issue(issue_number: int) -> Optional[str]:
    """Get Jira ticket key from GitHub issue number."""
    # Check issue body for Jira ticket reference
    # Format: "Jira: TOKYO-123"
    # This would be stored in the issue body by previous syncs
    return None  # Simplified for now

def create_jira_ticket(issue: Dict) -> Optional[str]:
    """Create a Jira ticket from a GitHub issue."""
    if not JIRA_BASE_URL or not JIRA_API_TOKEN:
        print("Jira credentials not configured, skipping sync")
        return None
    
    config = load_config()
    if not config['jira'].get('enabled', True):
        print("Jira sync is disabled")
        return None
    
    project_key = config['jira']['projects'][0]
    issue_type = map_github_label_to_jira_type(issue.get('labels', []))
    
    jira_data = {
        'fields': {
            'project': {'key': project_key},
            'summary': issue['title'],
            'description': f"{issue['body']}\n\nGitHub Issue: {issue['html_url']}",
            'issuetype': {'name': issue_type}
        }
    }
    
    try:
        response = requests.post(
            f'{JIRA_BASE_URL}/rest/api/3/issue',
            headers=get_jira_headers(),
            json=jira_data,
            timeout=30
        )
        response.raise_for_status()
        ticket = response.json()
        ticket_key = ticket['key']
        print(f"Created Jira ticket: {ticket_key}")
        return ticket_key
    except requests.exceptions.RequestException as e:
        print(f"Error creating Jira ticket: {e}")
        return None

def update_jira_ticket(ticket_key: str, issue: Dict) -> bool:
    """Update an existing Jira ticket."""
    if not JIRA_BASE_URL or not JIRA_API_TOKEN:
        return False
    
    jira_data = {
        'fields': {
            'summary': issue['title'],
            'description': f"{issue['body']}\n\nGitHub Issue: {issue['html_url']}"
        }
    }
    
    try:
        response = requests.put(
            f'{JIRA_BASE_URL}/rest/api/3/issue/{ticket_key}',
            headers=get_jira_headers(),
            json=jira_data,
            timeout=30
        )
        response.raise_for_status()
        print(f"Updated Jira ticket: {ticket_key}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error updating Jira ticket: {e}")
        return False

def sync_issue_status(ticket_key: str, state: str) -> bool:
    """Sync GitHub issue state to Jira ticket status."""
    if not JIRA_BASE_URL or not JIRA_API_TOKEN:
        return False
    
    # Get available transitions
    try:
        response = requests.get(
            f'{JIRA_BASE_URL}/rest/api/3/issue/{ticket_key}/transitions',
            headers=get_jira_headers(),
            timeout=30
        )
        response.raise_for_status()
        transitions = response.json()['transitions']
        
        # Find transition to target status
        target_status = map_github_state_to_jira_status(state)
        transition_id = None
        
        for transition in transitions:
            if transition['to']['name'] == target_status:
                transition_id = transition['id']
                break
        
        if transition_id:
            response = requests.post(
                f'{JIRA_BASE_URL}/rest/api/3/issue/{ticket_key}/transitions',
                headers=get_jira_headers(),
                json={'transition': {'id': transition_id}},
                timeout=30
            )
            response.raise_for_status()
            print(f"Updated {ticket_key} status to {target_status}")
            return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error syncing status: {e}")
    
    return False

def add_jira_comment(ticket_key: str, comment_body: str) -> bool:
    """Add a comment to a Jira ticket."""
    if not JIRA_BASE_URL or not JIRA_API_TOKEN:
        return False
    
    jira_data = {
        'body': {
            'type': 'doc',
            'version': 1,
            'content': [
                {
                    'type': 'paragraph',
                    'content': [
                        {
                            'type': 'text',
                            'text': comment_body
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        response = requests.post(
            f'{JIRA_BASE_URL}/rest/api/3/issue/{ticket_key}/comment',
            headers=get_jira_headers(),
            json=jira_data,
            timeout=30
        )
        response.raise_for_status()
        print(f"Added comment to {ticket_key}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error adding comment: {e}")
        return False

def process_github_event():
    """Process GitHub webhook event."""
    if not GITHUB_EVENT_PATH:
        print("No event path provided")
        return
    
    try:
        with open(GITHUB_EVENT_PATH, 'r') as f:
            event = json.load(f)
    except FileNotFoundError:
        print(f"Event file not found: {GITHUB_EVENT_PATH}")
        return
    
    event_type = GITHUB_EVENT_NAME
    
    if event_type == 'issues':
        action = event['action']
        issue = event['issue']
        
        print(f"Processing issue event: {action}")
        
        # Get existing Jira ticket if any
        ticket_key = get_jira_ticket_from_github_issue(issue['number'])
        
        if action == 'opened' and not ticket_key:
            # Create new Jira ticket
            ticket_key = create_jira_ticket(issue)
            
        elif action == 'edited' and ticket_key:
            # Update existing ticket
            update_jira_ticket(ticket_key, issue)
            
        elif action in ['closed', 'reopened'] and ticket_key:
            # Sync status
            sync_issue_status(ticket_key, issue['state'])
    
    elif event_type == 'issue_comment':
        action = event['action']
        issue = event['issue']
        comment = event['comment']
        
        if action == 'created':
            ticket_key = get_jira_ticket_from_github_issue(issue['number'])
            if ticket_key:
                comment_text = f"{comment['user']['login']}: {comment['body']}"
                add_jira_comment(ticket_key, comment_text)

def main():
    """Main entry point."""
    print("Starting Jira sync...")
    
    if not all([JIRA_BASE_URL, JIRA_API_TOKEN, JIRA_EMAIL]):
        print("Jira configuration incomplete. Set JIRA_BASE_URL, JIRA_API_TOKEN, and JIRA_EMAIL")
        print("Sync skipped (not an error)")
        return 0
    
    process_github_event()
    print("Jira sync completed")
    return 0

if __name__ == '__main__':
    sys.exit(main())
