"""
Integration Agent - Handles external integrations (Jira, Slack, Google Sheets).

This agent uses the Documentation Agent to generate reports and structures
for external systems.
"""

from typing import Dict, Any, List, Optional
from crewai import Task
from .crew_config import create_documentation_agent, create_sre_agent
from .tools import DOCUMENTATION_TOOLS


class IntegrationAgent:
    """Agent for handling external integrations."""

    def __init__(self, tools: Optional[list] = None):
        """
        Initialize the integration agent.

        Args:
            tools: Optional list of additional tools
        """
        self.doc_agent = create_documentation_agent(tools or DOCUMENTATION_TOOLS)
        self.sre_agent = create_sre_agent()

    def generate_jira_sync_report(self, sync_data: Dict[str, Any]) -> str:
        """
        Generate a comprehensive Jira synchronization report.

        Args:
            sync_data: Synchronization data including:
                - synced_count: Number of issues synced
                - conflicts: List of conflicts encountered
                - errors: List of errors
                - new_issues: Number of new issues created
                - updated_issues: Number of issues updated

        Returns:
            Markdown formatted report
        """
        task = Task(
            description=f"""
            Create a comprehensive Jira synchronization report:
            
            Sync Statistics:
            - Issues Synchronized: {sync_data.get('synced_count', 0)}
            - New Issues Created: {sync_data.get('new_issues', 0)}
            - Issues Updated: {sync_data.get('updated_issues', 0)}
            - Conflicts Encountered: {len(sync_data.get('conflicts', []))}
            - Errors: {len(sync_data.get('errors', []))}
            
            Conflicts:
            {self._format_list(sync_data.get('conflicts', []))}
            
            Errors:
            {self._format_list(sync_data.get('errors', []))}
            
            Generate a professional Markdown report including:
            1. Executive Summary (2-3 sentences)
            2. Sync Statistics (table format)
            3. Detailed Conflict Analysis (if any)
            4. Error Details and Resolution Steps
            5. Recommended Actions
            6. Visual Statistics (using Markdown tables/charts)
            
            The report should be clear, actionable, and suitable for both technical
            and non-technical stakeholders.
            """,
            agent=self.doc_agent,
            expected_output="Professional Markdown report with executive summary and details",
        )

        result = task.execute()
        return result

    def generate_sheets_dashboard(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate structure for Google Sheets dashboard.

        Args:
            metrics: Metrics to include in dashboard:
                - issues_open: Number of open issues
                - issues_closed: Number of closed issues
                - prs_open: Number of open PRs
                - prs_merged: Number of merged PRs
                - velocity: Team velocity
                - quality_score: Code quality score

        Returns:
            Dictionary with sheet structure and formulas
        """
        task = Task(
            description=f"""
            Create a comprehensive Google Sheets dashboard structure for:
            
            Metrics:
            - Open Issues: {metrics.get('issues_open', 0)}
            - Closed Issues: {metrics.get('issues_closed', 0)}
            - Open PRs: {metrics.get('prs_open', 0)}
            - Merged PRs: {metrics.get('prs_merged', 0)}
            - Velocity: {metrics.get('velocity', 0)}
            - Quality Score: {metrics.get('quality_score', 0)}
            
            Generate a complete dashboard structure with 5 tabs:
            
            1. **Daily Tab**:
               - Daily metrics (issues, PRs, commits)
               - Trend charts
               - Today's activity summary
            
            2. **Weekly Tab**:
               - Weekly aggregations
               - Week-over-week comparisons
               - Sprint metrics
            
            3. **Team Tab**:
               - Per-developer metrics
               - Contribution stats
               - Performance indicators
            
            4. **Bots Tab**:
               - Bot activity metrics
               - Automation statistics
               - Bot health status
            
            5. **Executive Tab**:
               - High-level KPIs
               - Executive summary
               - Trend analysis
            
            For each tab, provide:
            - Column headers (A, B, C, etc.)
            - Sample data structure
            - Google Sheets formulas (e.g., =SUM(A2:A10), =AVERAGE(B:B))
            - Conditional formatting rules (e.g., red if < 70, green if > 90)
            - Recommended chart types (line, bar, pie)
            
            Output format: JSON structure with tabs, columns, formulas, and formatting.
            """,
            agent=self.doc_agent,
            expected_output="JSON structure with complete dashboard specification",
        )

        result = task.execute()

        # Parse the result into structured format
        return {
            "status": "generated",
            "dashboard_structure": result,
            "tabs": ["Daily", "Weekly", "Team", "Bots", "Executive"],
            "agent": "integration_agent (Doc-based)",
        }

    def generate_slack_notification(
        self, event_type: str, event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a Slack notification message.

        Args:
            event_type: Type of event (deployment, pr_merged, build_failed, etc.)
            event_data: Event-specific data

        Returns:
            Dictionary with Slack message structure
        """
        task = Task(
            description=f"""
            Generate a Slack notification for event: {event_type}
            
            Event Data:
            {self._format_dict(event_data)}
            
            Create a professional Slack message with:
            1. Clear, concise title
            2. Key information (bullet points)
            3. Action items (if applicable)
            4. Appropriate emoji indicators
            5. Links to relevant resources
            
            Format as Slack Block Kit JSON structure with:
            - Header section with emoji
            - Context section with metadata
            - Main message section
            - Actions section (buttons) if needed
            
            Make it visually appealing and actionable.
            """,
            agent=self.doc_agent,
            expected_output="Slack Block Kit JSON structure",
        )

        result = task.execute()

        return {
            "status": "generated",
            "slack_message": result,
            "event_type": event_type,
        }

    def validate_integration_config(
        self, integration_type: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate configuration for external integration.

        Args:
            integration_type: Type of integration (jira, slack, sheets, etc.)
            config: Configuration to validate

        Returns:
            Dictionary with validation results
        """
        task = Task(
            description=f"""
            Validate configuration for {integration_type} integration:
            
            Configuration:
            {self._format_dict(config)}
            
            Check:
            1. Required fields are present
            2. API keys/credentials are properly formatted
            3. URLs are valid
            4. Permissions are adequate
            5. Security best practices are followed
            
            Provide:
            - List of issues found
            - Recommendations
            - Security warnings
            - Setup checklist
            """,
            agent=self.sre_agent,
            expected_output="Configuration validation report",
        )

        result = task.execute()

        return {
            "status": "validated",
            "validation_result": result,
            "integration_type": integration_type,
        }

    def _format_list(self, items: List[Any]) -> str:
        """Format a list for display in prompts."""
        if not items:
            return "None"
        return "\n".join(f"- {item}" for item in items)

    def _format_dict(self, data: Dict[str, Any]) -> str:
        """Format a dictionary for display in prompts."""
        if not data:
            return "No data provided"
        return "\n".join(f"- {key}: {value}" for key, value in data.items())
