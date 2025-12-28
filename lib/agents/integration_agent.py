"""
Integration Agent - Handles external integrations with mock fallback.

Uses Documentation Agent for report generation when available.
"""

from typing import Dict, Any, List, Optional

try:
    from crewai import Task
    from .crew_config import create_documentation_agent, create_sre_agent
    from .tools import DOCUMENTATION_TOOLS
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False


class MockAgent:
    """Mock Agent when CrewAI not available."""
    pass


class MockTask:
    """Mock Task when CrewAI not available."""
    def __init__(self, description, agent, expected_output):
        self.description = description
        self.expected_output = expected_output
    
    def execute(self):
        return f"[MOCK MODE - CrewAI not installed] {self.expected_output}"


class IntegrationAgent:
    """Agent for handling external integrations."""

    def __init__(self, tools: Optional[list] = None):
        """Initialize the integration agent."""
        if CREWAI_AVAILABLE:
            self.doc_agent = create_documentation_agent(tools or DOCUMENTATION_TOOLS)
            self.sre_agent = create_sre_agent()
        else:
            self.doc_agent = MockAgent()
            self.sre_agent = MockAgent()
        
        self.TaskClass = Task if CREWAI_AVAILABLE else MockTask

    def generate_jira_sync_report(self, sync_data: Dict[str, Any]) -> str:
        """Generate a comprehensive Jira synchronization report."""
        task = self.TaskClass(
            description=f"""
            Create Jira sync report:
            Synced: {sync_data.get('synced_count', 0)}
            New: {sync_data.get('new_issues', 0)}
            Updated: {sync_data.get('updated_issues', 0)}
            Conflicts: {len(sync_data.get('conflicts', []))}
            Errors: {len(sync_data.get('errors', []))}
            
            Generate: Executive summary, statistics table, conflict analysis, recommendations.
            """,
            agent=self.doc_agent,
            expected_output="Professional Markdown report",
        )

        result = task.execute()
        return result

    def generate_sheets_dashboard(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structure for Google Sheets dashboard."""
        task = self.TaskClass(
            description=f"""
            Create Google Sheets dashboard for metrics:
            {self._format_dict(metrics)}
            
            Generate 5 tabs: Daily, Weekly, Team, Bots, Executive
            Include: columns, formulas, conditional formatting, charts.
            """,
            agent=self.doc_agent,
            expected_output="JSON dashboard structure",
        )

        result = task.execute()

        return {
            "status": "generated",
            "dashboard_structure": result,
            "tabs": ["Daily", "Weekly", "Team", "Bots", "Executive"],
            "agent": "integration_agent",
            "mode": "crewai" if CREWAI_AVAILABLE else "mock",
        }

    def generate_slack_notification(
        self, event_type: str, event_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a Slack notification message."""
        task = self.TaskClass(
            description=f"""
            Generate Slack notification for: {event_type}
            Data: {self._format_dict(event_data)}
            
            Create: title, key info, action items, emoji, links.
            Format: Slack Block Kit JSON.
            """,
            agent=self.doc_agent,
            expected_output="Slack Block Kit JSON",
        )

        result = task.execute()

        return {
            "status": "generated",
            "slack_message": result,
            "event_type": event_type,
            "mode": "crewai" if CREWAI_AVAILABLE else "mock",
        }

    def validate_integration_config(
        self, integration_type: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate configuration for external integration."""
        task = self.TaskClass(
            description=f"""
            Validate {integration_type} integration config:
            {self._format_dict(config)}
            
            Check: required fields, credentials, URLs, permissions, security.
            """,
            agent=self.sre_agent,
            expected_output="Configuration validation report",
        )

        result = task.execute()

        return {
            "status": "validated",
            "validation_result": result,
            "integration_type": integration_type,
            "mode": "crewai" if CREWAI_AVAILABLE else "mock",
        }

    def _format_list(self, items: List[Any]) -> str:
        """Format a list for display."""
        if not items:
            return "None"
        return "\n".join(f"- {item}" for item in items)

    def _format_dict(self, data: Dict[str, Any]) -> str:
        """Format a dictionary for display."""
        if not data:
            return "No data provided"
        return "\n".join(f"- {key}: {value}" for key, value in data.items())
