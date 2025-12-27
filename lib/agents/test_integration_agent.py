"""
Tests for Integration Agent.
"""

import pytest
from lib.agents.integration_agent import IntegrationAgent


def test_integration_agent_initialization():
    """Test that integration agent initializes correctly."""
    agent = IntegrationAgent()
    assert agent is not None
    assert agent.doc_agent is not None
    assert agent.sre_agent is not None


def test_generate_jira_sync_report():
    """Test Jira sync report generation."""
    agent = IntegrationAgent()

    sync_data = {
        "synced_count": 25,
        "new_issues": 5,
        "updated_issues": 20,
        "conflicts": ["Issue #123 has conflicting labels"],
        "errors": [],
    }

    result = agent.generate_jira_sync_report(sync_data)

    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0


def test_generate_sheets_dashboard():
    """Test Google Sheets dashboard generation."""
    agent = IntegrationAgent()

    metrics = {
        "issues_open": 12,
        "issues_closed": 45,
        "prs_open": 3,
        "prs_merged": 28,
        "velocity": 1.2,
        "quality_score": 87,
    }

    result = agent.generate_sheets_dashboard(metrics)

    assert result is not None
    assert result["status"] == "generated"
    assert "dashboard_structure" in result
    assert "tabs" in result
    assert len(result["tabs"]) == 5
    assert "Daily" in result["tabs"]
    assert "Executive" in result["tabs"]


def test_generate_slack_notification():
    """Test Slack notification generation."""
    agent = IntegrationAgent()

    event_data = {
        "deployment_url": "https://example.com",
        "status": "success",
        "duration": "2m 30s",
    }

    result = agent.generate_slack_notification("deployment", event_data)

    assert result is not None
    assert result["status"] == "generated"
    assert "slack_message" in result
    assert result["event_type"] == "deployment"


def test_validate_integration_config():
    """Test integration configuration validation."""
    agent = IntegrationAgent()

    config = {
        "server": "https://jira.example.com",
        "project": "TOK",
        "api_key": "test-key",
    }

    result = agent.validate_integration_config("jira", config)

    assert result is not None
    assert result["status"] == "validated"
    assert "validation_result" in result
    assert result["integration_type"] == "jira"


def test_format_list():
    """Test list formatting helper."""
    agent = IntegrationAgent()

    items = ["Item 1", "Item 2", "Item 3"]
    formatted = agent._format_list(items)

    assert formatted is not None
    assert "- Item 1" in formatted
    assert "- Item 2" in formatted

    # Test empty list
    empty_formatted = agent._format_list([])
    assert empty_formatted == "None"


def test_format_dict():
    """Test dictionary formatting helper."""
    agent = IntegrationAgent()

    data = {"key1": "value1", "key2": "value2"}
    formatted = agent._format_dict(data)

    assert formatted is not None
    assert "key1: value1" in formatted
    assert "key2: value2" in formatted

    # Test empty dict
    empty_formatted = agent._format_dict({})
    assert empty_formatted == "No data provided"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
