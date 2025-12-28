"""
Tests for Deployment Agent.
"""

import pytest
from lib.agents.deployment_agent import DeploymentAgent


def test_deployment_agent_initialization():
    """Test that deployment agent initializes correctly."""
    agent = DeploymentAgent()
    assert agent is not None
    assert agent.sre_agent is not None


def test_validate_railway_config():
    """Test railway.toml validation."""
    agent = DeploymentAgent()

    # Sample railway.toml content
    railway_toml = """
[build]
builder = "DOCKERFILE"

[deploy]
startCommand = "app"
healthcheckPath = "/health"
    """

    result = agent.validate_railway_config(railway_toml)

    assert result is not None
    assert result["status"] == "completed"
    assert "validation_result" in result
    assert result["agent"] == "deployment_agent (SRE-based)"


def test_generate_railway_config():
    """Test railway.toml generation."""
    agent = DeploymentAgent()

    project_spec = {
        "name": "test-app",
        "stack": "Go + PostgreSQL",
        "features": ["postgresql", "redis"],
        "port": 8080,
    }

    result = agent.generate_railway_config(project_spec)

    assert result is not None
    assert result["status"] == "completed"
    assert "config_generated" in result
    assert result["agent"] == "deployment_agent (SRE-based)"


def test_monitor_deployment_health():
    """Test deployment health monitoring."""
    agent = DeploymentAgent()

    result = agent.monitor_deployment_health("https://example.com/health")

    assert result is not None
    assert result["status"] == "completed"
    assert "health_report" in result
    assert result["agent"] == "deployment_agent (SRE-based)"


def test_validate_deployment_safety():
    """Test deployment safety validation."""
    agent = DeploymentAgent()

    pr_changes = {
        "title": "Add new feature",
        "files_changed": ["main.go", "config.yaml"],
        "additions": 150,
        "deletions": 30,
        "description": "Implements new API endpoint",
    }

    result = agent.validate_deployment_safety(pr_changes)

    assert result is not None
    assert result["status"] == "completed"
    assert "safety_assessment" in result
    assert result["agent"] == "deployment_agent (SRE-based)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
