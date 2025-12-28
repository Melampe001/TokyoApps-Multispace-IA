"""
Deployment Agent - Specialized in Railway/AWS deployment.

This agent extends the SRE Agent with deployment-specific capabilities.
Falls back to mock implementation if CrewAI is not available.
"""

from typing import Dict, Any, Optional

try:
    from crewai import Agent, Task
    from .crew_config import create_sre_agent
    from .tools import SRE_TOOLS
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


class DeploymentAgent:
    """Agent specialized in deployment to Railway and AWS."""

    def __init__(self, tools: Optional[list] = None):
        """Initialize the deployment agent."""
        if CREWAI_AVAILABLE:
            self.sre_agent = create_sre_agent(tools or SRE_TOOLS)
        else:
            self.sre_agent = MockAgent()
        
        self.TaskClass = Task if CREWAI_AVAILABLE else MockTask

    def validate_railway_config(self, railway_toml_content: str) -> Dict[str, Any]:
        """Validate Railway.toml configuration file."""
        task = self.TaskClass(
            description=f"""
            Validate Railway.toml configuration.
            Content: {railway_toml_content[:200]}...
            
            Check: health checks, env vars, Dockerfile, rollback policy, security.
            """,
            agent=self.sre_agent,
            expected_output="Validation report with recommendations",
        )

        result = task.execute()

        return {
            "status": "completed",
            "validation_result": result,
            "agent": "deployment_agent",
            "mode": "crewai" if CREWAI_AVAILABLE else "mock",
        }

    def generate_railway_config(self, project_spec: Dict[str, Any]) -> Dict[str, str]:
        """Generate optimized railway.toml configuration."""
        task = self.TaskClass(
            description=f"""
            Generate railway.toml for: {project_spec.get('name', 'app')}
            Stack: {project_spec.get('stack', 'Go')}
            Features: {project_spec.get('features', [])}
            
            Include: multi-stage Docker, health checks, env vars, security.
            """,
            agent=self.sre_agent,
            expected_output="Complete railway.toml and Dockerfile",
        )

        result = task.execute()

        return {
            "status": "completed",
            "config_generated": result,
            "agent": "deployment_agent",
            "mode": "crewai" if CREWAI_AVAILABLE else "mock",
        }

    def monitor_deployment_health(
        self, deployment_url: str, expected_status: int = 200
    ) -> Dict[str, Any]:
        """Monitor deployment health after Railway deployment."""
        task = self.TaskClass(
            description=f"""
            Monitor health of deployed application at {deployment_url}
            Expected status: {expected_status}
            
            Check: HTTP response, latency, logs, connections, resources.
            """,
            agent=self.sre_agent,
            expected_output="Health monitoring report",
        )

        result = task.execute()

        return {
            "status": "completed",
            "health_report": result,
            "agent": "deployment_agent",
            "mode": "crewai" if CREWAI_AVAILABLE else "mock",
        }

    def validate_deployment_safety(self, pr_changes: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that PR changes are safe to deploy."""
        task = self.TaskClass(
            description=f"""
            Assess deployment safety for PR: {pr_changes.get('title', '')}
            Files: {len(pr_changes.get('files_changed', []))}
            Changes: +{pr_changes.get('additions', 0)} -{pr_changes.get('deletions', 0)}
            
            Evaluate: breaking changes, config changes, infrastructure, rollback, migrations, security.
            """,
            agent=self.sre_agent,
            expected_output="Deployment safety assessment with risk level",
        )

        result = task.execute()

        return {
            "status": "completed",
            "safety_assessment": result,
            "agent": "deployment_agent",
            "mode": "crewai" if CREWAI_AVAILABLE else "mock",
        }
