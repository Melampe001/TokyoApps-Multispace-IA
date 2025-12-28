#!/usr/bin/env python3
"""
Jira Sync with Agents

This script synchronizes GitHub issues with Jira using the agent system
for intelligent report generation and validation.
"""

import json
import os
import sys
from pathlib import Path

# Add lib to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "lib"))

from agents.integration_agent import IntegrationAgent


def fetch_github_issues():
    """Fetch GitHub issues (mock implementation)."""
    # In real implementation, this would use GitHub API
    return [
        {
            "number": 1,
            "title": "Implement P1 with agents",
            "state": "open",
            "labels": ["enhancement", "p1"],
        },
        {
            "number": 2,
            "title": "Fix security vulnerability",
            "state": "closed",
            "labels": ["bug", "security"],
        },
    ]


def load_jira_config():
    """Load Jira configuration."""
    return {
        "server": os.environ.get("JIRA_SERVER", "https://jira.example.com"),
        "project": os.environ.get("JIRA_PROJECT", "TOK"),
        "api_key": os.environ.get("JIRA_API_KEY", "placeholder"),
    }


def sync_issues_to_jira(issues, jira_config):
    """Sync issues to Jira (mock implementation)."""
    synced = 0
    conflicts = []
    errors = []
    new_issues = 0
    updated_issues = 0

    for issue in issues:
        # Mock sync logic
        if issue["state"] == "open":
            new_issues += 1
        else:
            updated_issues += 1
        synced += 1

    return {
        "synced_count": synced,
        "new_issues": new_issues,
        "updated_issues": updated_issues,
        "conflicts": conflicts,
        "errors": errors,
    }


def post_to_slack(message):
    """Post message to Slack (mock implementation)."""
    slack_webhook = os.environ.get("SLACK_WEBHOOK_URL")

    if not slack_webhook:
        print("Slack webhook not configured, skipping post")
        return

    print(f"\nWould post to Slack:\n{message}\n")


def main():
    """Main execution function."""
    print("🔄 Jira Sync with Agents")
    print("=" * 50)

    # Step 1: Fetch GitHub issues
    print("\n1. Fetching GitHub issues...")
    issues = fetch_github_issues()
    print(f"   Found {len(issues)} issues")

    # Step 2: Load Jira config
    print("\n2. Loading Jira configuration...")
    jira_config = load_jira_config()
    print(f"   Server: {jira_config['server']}")
    print(f"   Project: {jira_config['project']}")

    # Step 3: Validate config with Integration Agent
    print("\n3. Validating Jira configuration with Integration Agent...")
    agent = IntegrationAgent()
    validation = agent.validate_integration_config("jira", jira_config)
    print(f"   Validation status: {validation['status']}")

    # Step 4: Sync issues to Jira
    print("\n4. Syncing issues to Jira...")
    sync_result = sync_issues_to_jira(issues, jira_config)
    print(f"   Synced: {sync_result['synced_count']} issues")
    print(f"   New: {sync_result['new_issues']}")
    print(f"   Updated: {sync_result['updated_issues']}")

    # Step 5: Generate report with Documentation Agent
    print("\n5. Generating sync report with Documentation Agent...")
    report = agent.generate_jira_sync_report(sync_result)
    print(f"   Report generated ({len(report)} characters)")

    # Save report
    report_file = Path("/tmp/jira_sync_report.md")
    report_file.write_text(report)
    print(f"   Report saved to {report_file}")

    # Step 6: Generate Slack notification
    print("\n6. Generating Slack notification...")
    slack_notification = agent.generate_slack_notification(
        "jira_sync_completed",
        {
            "synced_count": sync_result["synced_count"],
            "new_issues": sync_result["new_issues"],
            "updated_issues": sync_result["updated_issues"],
            "report_url": str(report_file),
        },
    )
    print(f"   Slack notification generated")

    # Step 7: Post to Slack
    print("\n7. Posting to Slack...")
    post_to_slack(slack_notification["slack_message"])

    print("\n✅ Jira sync completed successfully!")
    print(f"\nSummary:")
    print(f"  - Issues synced: {sync_result['synced_count']}")
    print(f"  - New issues: {sync_result['new_issues']}")
    print(f"  - Updated issues: {sync_result['updated_issues']}")
    print(f"  - Conflicts: {len(sync_result['conflicts'])}")
    print(f"  - Errors: {len(sync_result['errors'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
