#!/usr/bin/env python3
"""
Google Sheets Dashboard Updater

Updates a Google Sheets dashboard with metrics from GitHub:
- Daily metrics (issues, PRs, commits)
- Weekly aggregated metrics
- Team performance metrics
- Bot performance metrics
- Executive summary
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any
import requests

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Google API libraries not installed. Install with:")
    print("pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# Configuration
GOOGLE_CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS')
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')

# Scopes for Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheets_service():
    """Create Google Sheets API service."""
    if not GOOGLE_CREDENTIALS:
        print("GOOGLE_CREDENTIALS not set, skipping sheets update")
        return None
    
    try:
        creds_dict = json.loads(GOOGLE_CREDENTIALS)
        creds = service_account.Credentials.from_service_account_info(
            creds_dict, scopes=SCOPES
        )
        service = build('sheets', 'v4', credentials=creds)
        return service
    except Exception as e:
        print(f"Error creating sheets service: {e}")
        return None

def get_github_headers() -> Dict[str, str]:
    """Get GitHub API headers."""
    return {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

def get_github_issues(state: str = 'all', since: str = None) -> List[Dict]:
    """Get GitHub issues."""
    url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/issues'
    params = {'state': state, 'per_page': 100}
    if since:
        params['since'] = since
    
    try:
        response = requests.get(url, headers=get_github_headers(), params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching issues: {e}")
        return []

def get_github_pulls(state: str = 'all') -> List[Dict]:
    """Get GitHub pull requests."""
    url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls'
    params = {'state': state, 'per_page': 100}
    
    try:
        response = requests.get(url, headers=get_github_headers(), params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching PRs: {e}")
        return []

def get_github_commits(since: str) -> List[Dict]:
    """Get GitHub commits since a date."""
    url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/commits'
    params = {'since': since, 'per_page': 100}
    
    try:
        response = requests.get(url, headers=get_github_headers(), params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching commits: {e}")
        return []

def calculate_daily_metrics() -> Dict[str, Any]:
    """Calculate daily metrics."""
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    
    # Get data from the last 24 hours
    since = yesterday.isoformat() + 'T00:00:00Z'
    
    issues = get_github_issues(since=since)
    pulls = get_github_pulls()
    commits = get_github_commits(since=since)
    
    # Filter to today
    today_issues = [i for i in issues if i['created_at'].startswith(today.isoformat())]
    today_pulls = [p for p in pulls if p['created_at'].startswith(today.isoformat())]
    
    # Count by state
    open_issues = len([i for i in today_issues if i['state'] == 'open'])
    closed_issues = len([i for i in today_issues if i['state'] == 'closed'])
    open_prs = len([p for p in today_pulls if p['state'] == 'open'])
    merged_prs = len([p for p in today_pulls if p.get('merged_at')])
    
    return {
        'date': today.isoformat(),
        'issues_opened': open_issues,
        'issues_closed': closed_issues,
        'prs_opened': open_prs,
        'prs_merged': merged_prs,
        'commits': len(commits),
        'net_issues': open_issues - closed_issues
    }

def calculate_weekly_metrics() -> Dict[str, Any]:
    """Calculate weekly aggregated metrics."""
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    
    since = week_ago.isoformat() + 'T00:00:00Z'
    
    issues = get_github_issues(since=since)
    pulls = get_github_pulls()
    commits = get_github_commits(since=since)
    
    # Filter to this week
    week_issues = [i for i in issues if i['created_at'] >= since]
    week_pulls = [p for p in pulls if p['created_at'] >= since]
    
    open_issues = len([i for i in week_issues if i['state'] == 'open'])
    closed_issues = len([i for i in week_issues if i['state'] == 'closed'])
    open_prs = len([p for p in week_pulls if p['state'] == 'open'])
    merged_prs = len([p for p in week_pulls if p.get('merged_at')])
    
    # Calculate velocity (issues closed per day)
    velocity = closed_issues / 7.0 if closed_issues > 0 else 0
    
    return {
        'week_start': week_ago.isoformat(),
        'week_end': today.isoformat(),
        'issues_opened': open_issues,
        'issues_closed': closed_issues,
        'prs_opened': open_prs,
        'prs_merged': merged_prs,
        'commits': len(commits),
        'velocity': round(velocity, 2)
    }

def calculate_team_metrics() -> List[Dict[str, Any]]:
    """Calculate per-team-member metrics."""
    week_ago = (datetime.utcnow().date() - timedelta(days=7)).isoformat() + 'T00:00:00Z'
    
    issues = get_github_issues(since=week_ago)
    pulls = get_github_pulls()
    commits = get_github_commits(since=week_ago)
    
    # Aggregate by user
    user_metrics = {}
    
    for issue in issues:
        user = issue['user']['login']
        if user not in user_metrics:
            user_metrics[user] = {'issues': 0, 'prs': 0, 'commits': 0}
        user_metrics[user]['issues'] += 1
    
    for pr in pulls:
        user = pr['user']['login']
        if user not in user_metrics:
            user_metrics[user] = {'issues': 0, 'prs': 0, 'commits': 0}
        user_metrics[user]['prs'] += 1
    
    for commit in commits:
        if commit.get('author'):
            user = commit['author'].get('login', 'Unknown')
            if user not in user_metrics:
                user_metrics[user] = {'issues': 0, 'prs': 0, 'commits': 0}
            user_metrics[user]['commits'] += 1
    
    # Convert to list
    team_data = []
    for user, metrics in user_metrics.items():
        team_data.append({
            'user': user,
            'issues': metrics['issues'],
            'prs': metrics['prs'],
            'commits': metrics['commits']
        })
    
    return sorted(team_data, key=lambda x: x['commits'], reverse=True)

def update_daily_tab(service, sheet_id: str, metrics: Dict):
    """Update the Daily metrics tab."""
    try:
        # Prepare data
        values = [[
            metrics['date'],
            metrics['issues_opened'],
            metrics['issues_closed'],
            metrics['prs_opened'],
            metrics['prs_merged'],
            metrics['commits'],
            metrics['net_issues']
        ]]
        
        # Append to sheet
        body = {'values': values}
        result = service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range='Daily!A:G',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"Updated Daily tab: {result.get('updates').get('updatedCells')} cells")
    except HttpError as e:
        print(f"Error updating Daily tab: {e}")

def update_weekly_tab(service, sheet_id: str, metrics: Dict):
    """Update the Weekly metrics tab."""
    try:
        values = [[
            metrics['week_start'],
            metrics['week_end'],
            metrics['issues_opened'],
            metrics['issues_closed'],
            metrics['prs_opened'],
            metrics['prs_merged'],
            metrics['commits'],
            metrics['velocity']
        ]]
        
        body = {'values': values}
        result = service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range='Weekly!A:H',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"Updated Weekly tab: {result.get('updates').get('updatedCells')} cells")
    except HttpError as e:
        print(f"Error updating Weekly tab: {e}")

def update_team_tab(service, sheet_id: str, team_metrics: List[Dict]):
    """Update the Team metrics tab."""
    try:
        # Clear existing data
        service.spreadsheets().values().clear(
            spreadsheetId=sheet_id,
            range='Team!A2:Z1000'
        ).execute()
        
        # Prepare data
        values = []
        for member in team_metrics:
            values.append([
                member['user'],
                member['issues'],
                member['prs'],
                member['commits']
            ])
        
        if values:
            body = {'values': values}
            result = service.spreadsheets().values().update(
                spreadsheetId=sheet_id,
                range='Team!A2',
                valueInputOption='RAW',
                body=body
            ).execute()
            
            print(f"Updated Team tab: {result.get('updatedCells')} cells")
    except HttpError as e:
        print(f"Error updating Team tab: {e}")

def main():
    """Main entry point."""
    print("Starting Google Sheets dashboard update...")
    
    if not GOOGLE_SHEET_ID:
        print("GOOGLE_SHEET_ID not set, skipping update")
        return 0
    
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN not set, cannot fetch metrics")
        return 1
    
    # Get Sheets service
    service = get_sheets_service()
    if not service:
        print("Could not create Sheets service, skipping update")
        return 0
    
    # Calculate metrics
    print("Calculating metrics...")
    daily_metrics = calculate_daily_metrics()
    weekly_metrics = calculate_weekly_metrics()
    team_metrics = calculate_team_metrics()
    
    # Update sheets
    print("Updating sheets...")
    update_daily_tab(service, GOOGLE_SHEET_ID, daily_metrics)
    update_weekly_tab(service, GOOGLE_SHEET_ID, weekly_metrics)
    update_team_tab(service, GOOGLE_SHEET_ID, team_metrics)
    
    print("Dashboard update completed successfully")
    return 0

if __name__ == '__main__':
    sys.exit(main())
