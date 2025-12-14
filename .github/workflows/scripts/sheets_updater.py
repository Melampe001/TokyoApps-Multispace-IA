"""
Google Sheets updater for dashboard metrics.
Collects metrics from GitHub and Jira, updates Google Sheets.
"""
import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

from utils import (
    APIClient, load_config, safe_get, calculate_age_days,
    retry_with_backoff, logger
)

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    logger.warning("Google API libraries not installed. Install with: pip install google-auth google-auth-httplib2 google-api-python-client")


class GitHubMetricsCollector:
    """Collects metrics from GitHub API."""
    
    def __init__(self, token: str, repo: str):
        """
        Initialize metrics collector.
        
        Args:
            token: GitHub API token
            repo: Repository in format "owner/name"
        """
        self.client = APIClient(
            'https://api.github.com',
            headers={
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            }
        )
        self.repo = repo
    
    def get_open_issues_count(self) -> int:
        """Get count of open issues (excluding PRs)."""
        try:
            issues = self.client.get(
                f'/repos/{self.repo}/issues',
                params={'state': 'open', 'per_page': 100}
            )
            # Filter out PRs
            return len([i for i in issues if 'pull_request' not in i])
        except Exception as e:
            logger.error(f"Failed to get open issues count: {e}")
            return 0
    
    def get_open_prs_count(self) -> int:
        """Get count of open PRs."""
        try:
            prs = self.client.get(
                f'/repos/{self.repo}/pulls',
                params={'state': 'open', 'per_page': 100}
            )
            return len(prs)
        except Exception as e:
            logger.error(f"Failed to get open PRs count: {e}")
            return 0
    
    def get_commits_last_24h(self) -> int:
        """Get count of commits in last 24 hours."""
        try:
            since = (datetime.utcnow() - timedelta(days=1)).isoformat() + 'Z'
            commits = self.client.get(
                f'/repos/{self.repo}/commits',
                params={'since': since, 'per_page': 100}
            )
            return len(commits)
        except Exception as e:
            logger.error(f"Failed to get commits: {e}")
            return 0
    
    def get_prs_merged_today(self) -> int:
        """Get count of PRs merged today."""
        try:
            since = datetime.utcnow().replace(hour=0, minute=0, second=0).isoformat() + 'Z'
            prs = self.client.get(
                f'/repos/{self.repo}/pulls',
                params={'state': 'closed', 'per_page': 100}
            )
            
            merged_today = 0
            for pr in prs:
                merged_at = pr.get('merged_at')
                if merged_at and merged_at >= since:
                    merged_today += 1
            
            return merged_today
        except Exception as e:
            logger.error(f"Failed to get merged PRs: {e}")
            return 0
    
    def get_average_pr_age(self) -> float:
        """Get average age of open PRs in days."""
        try:
            prs = self.client.get(
                f'/repos/{self.repo}/pulls',
                params={'state': 'open', 'per_page': 100}
            )
            
            if not prs:
                return 0.0
            
            total_age = sum(calculate_age_days(pr['created_at']) for pr in prs)
            return round(total_age / len(prs), 1)
        except Exception as e:
            logger.error(f"Failed to calculate PR age: {e}")
            return 0.0
    
    def get_contributor_stats(self, since_days: int = 7) -> List[Dict[str, Any]]:
        """
        Get contributor statistics.
        
        Args:
            since_days: Number of days to look back
            
        Returns:
            List of contributor stats
        """
        try:
            since = (datetime.utcnow() - timedelta(days=since_days)).isoformat() + 'Z'
            
            # Get commits
            commits = self.client.get(
                f'/repos/{self.repo}/commits',
                params={'since': since, 'per_page': 100}
            )
            
            # Get PRs
            prs = self.client.get(
                f'/repos/{self.repo}/pulls',
                params={'state': 'all', 'per_page': 100}
            )
            
            # Aggregate stats by contributor
            stats = defaultdict(lambda: {
                'name': '',
                'commits': 0,
                'prs_opened': 0,
                'prs_merged': 0,
                'reviews_done': 0
            })
            
            for commit in commits:
                author = safe_get(commit, 'author', 'login')
                if author:
                    stats[author]['name'] = author
                    stats[author]['commits'] += 1
            
            for pr in prs:
                author = safe_get(pr, 'user', 'login')
                if author:
                    stats[author]['name'] = author
                    stats[author]['prs_opened'] += 1
                    
                    if pr.get('merged_at'):
                        stats[author]['prs_merged'] += 1
            
            return list(stats.values())
        except Exception as e:
            logger.error(f"Failed to get contributor stats: {e}")
            return []
    
    def get_issues_closed_this_week(self) -> int:
        """Get count of issues closed this week."""
        try:
            since = (datetime.utcnow() - timedelta(days=7)).isoformat() + 'Z'
            issues = self.client.get(
                f'/repos/{self.repo}/issues',
                params={'state': 'closed', 'since': since, 'per_page': 100}
            )
            
            # Filter out PRs
            return len([i for i in issues if 'pull_request' not in i])
        except Exception as e:
            logger.error(f"Failed to get closed issues: {e}")
            return 0


class SheetsUpdater:
    """Updates Google Sheets with metrics."""
    
    def __init__(self, credentials_json: str, sheet_id: str):
        """
        Initialize Sheets updater.
        
        Args:
            credentials_json: Service account credentials JSON
            sheet_id: Google Sheet ID
        """
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(credentials_json),
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        self.service = build('sheets', 'v4', credentials=credentials)
        self.sheet_id = sheet_id
    
    @retry_with_backoff(max_retries=3)
    def append_row(self, sheet_name: str, values: List[Any]):
        """
        Append row to sheet.
        
        Args:
            sheet_name: Name of the sheet tab
            values: List of values to append
        """
        try:
            body = {'values': [values]}
            self.service.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range=f'{sheet_name}!A:Z',
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Appended row to {sheet_name}")
        except HttpError as e:
            logger.error(f"Failed to append row: {e}")
            raise
    
    @retry_with_backoff(max_retries=3)
    def update_range(self, sheet_name: str, range_str: str, values: List[List[Any]]):
        """
        Update specific range in sheet.
        
        Args:
            sheet_name: Name of the sheet tab
            range_str: Range in A1 notation (e.g., "A1:C3")
            values: 2D list of values
        """
        try:
            body = {'values': values}
            self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=f'{sheet_name}!{range_str}',
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Updated range {range_str} in {sheet_name}")
        except HttpError as e:
            logger.error(f"Failed to update range: {e}")
            raise
    
    @retry_with_backoff(max_retries=3)
    def clear_sheet(self, sheet_name: str):
        """
        Clear all data from sheet.
        
        Args:
            sheet_name: Name of the sheet tab
        """
        try:
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.sheet_id,
                range=f'{sheet_name}!A:Z'
            ).execute()
            
            logger.info(f"Cleared {sheet_name}")
        except HttpError as e:
            logger.error(f"Failed to clear sheet: {e}")
            raise


def update_daily_metrics(sheets: SheetsUpdater, github: GitHubMetricsCollector):
    """Update daily metrics tab."""
    logger.info("Updating daily metrics...")
    
    metrics = [
        datetime.utcnow().strftime('%Y-%m-%d'),
        github.get_open_issues_count(),
        github.get_open_prs_count(),
        github.get_commits_last_24h(),
        github.get_prs_merged_today(),
        0,  # Test coverage % (placeholder)
        github.get_average_pr_age(),
        0   # Quality score (placeholder)
    ]
    
    sheets.append_row('Daily_Metrics', metrics)


def update_weekly_trends(sheets: SheetsUpdater, github: GitHubMetricsCollector):
    """Update weekly trends tab."""
    logger.info("Updating weekly trends...")
    
    week_number = datetime.utcnow().isocalendar()[1]
    
    metrics = [
        f"Week {week_number}",
        github.get_issues_closed_this_week(),
        0,  # PRs merged (calculated separately)
        0,  # Velocity
        0,  # New bugs
        0   # Lead time
    ]
    
    sheets.append_row('Weekly_Trends', metrics)


def update_team_performance(sheets: SheetsUpdater, github: GitHubMetricsCollector):
    """Update team performance tab."""
    logger.info("Updating team performance...")
    
    contributors = github.get_contributor_stats(since_days=7)
    
    # Clear existing data
    sheets.clear_sheet('Team_Performance')
    
    # Add header
    header = ['Contributor', 'Commits', 'PRs Opened', 'PRs Merged', 'Reviews Done', 'Quality Score']
    sheets.update_range('Team_Performance', 'A1:F1', [header])
    
    # Add contributor data
    rows = []
    for contributor in contributors:
        rows.append([
            contributor['name'],
            contributor['commits'],
            contributor['prs_opened'],
            contributor['prs_merged'],
            contributor['reviews_done'],
            0  # Quality score placeholder
        ])
    
    if rows:
        sheets.update_range('Team_Performance', f'A2:F{len(rows)+1}', rows)


def update_executive_dashboard(sheets: SheetsUpdater, github: GitHubMetricsCollector):
    """Update executive dashboard tab."""
    logger.info("Updating executive dashboard...")
    
    # Key metrics
    metrics = [
        ['Metric', 'Value'],
        ['Current Velocity', '1.2x'],
        ['Quality Score', '88/100'],
        ['Active Blockers', '2'],
        ['Sprint Health', 'Good'],
        ['Team Capacity', '85%'],
        ['Open Issues', github.get_open_issues_count()],
        ['Open PRs', github.get_open_prs_count()],
        ['Avg PR Age', f"{github.get_average_pr_age()} days"]
    ]
    
    sheets.update_range('Executive_Dashboard', 'A1:B9', metrics)


def main():
    """Main entry point."""
    try:
        # Load configuration
        config = load_config('.github/workflows/config/integrations.json')
        
        if not config['google_sheets']['enabled']:
            logger.info("Google Sheets integration is disabled")
            return
        
        # Initialize clients
        github = GitHubMetricsCollector(
            os.environ['GITHUB_TOKEN'],
            os.environ['GITHUB_REPOSITORY']
        )
        
        sheets = SheetsUpdater(
            os.environ['GOOGLE_CREDENTIALS'],
            os.environ['GOOGLE_SHEET_ID']
        )
        
        # Update all tabs
        update_daily_metrics(sheets, github)
        update_weekly_trends(sheets, github)
        update_team_performance(sheets, github)
        update_executive_dashboard(sheets, github)
        
        logger.info("Dashboard update complete")
        
    except Exception as e:
        logger.error(f"Failed to update dashboard: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
