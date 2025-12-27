"""
Deployment Agent - Specialized in Railway/AWS deployment.

This agent extends the SRE Agent with deployment-specific capabilities:
- Railway.toml validation
- Dockerfile optimization
- Health check configuration
- Deployment safety checks
"""

from typing import Dict, Any, Optional
from crewai import Agent, Task
from .crew_config import create_sre_agent
from .tools import SRE_TOOLS


class DeploymentAgent:
    """Agent specialized in deployment to Railway and AWS."""

    def __init__(self, tools: Optional[list] = None):
        """
        Initialize the deployment agent.

        Args:
            tools: Optional list of additional tools for the agent
        """
        self.sre_agent = create_sre_agent(tools or SRE_TOOLS)

    def validate_railway_config(self, railway_toml_content: str) -> Dict[str, Any]:
        """
        Validate Railway.toml configuration file.

        Args:
            railway_toml_content: Content of the railway.toml file

        Returns:
            Dictionary with validation results and recommendations
        """
        task = Task(
            description=f"""
            Validate the following Railway.toml configuration:
            
            ```toml
            {railway_toml_content}
            ```
            
            Check the following:
            1. Health check is configured correctly (path, timeout, retry policy)
            2. Required environment variables are documented
            3. Dockerfile build strategy is optimal (multi-stage preferred)
            4. Rollback policy is configured (restart policy type and max retries)
            5. Resource limits are appropriate for the application
            6. Security best practices are followed
            
            Provide:
            - List of issues found (if any)
            - Recommendations for improvements
            - Deployment readiness checklist
            - Security considerations
            """,
            agent=self.sre_agent,
            expected_output="Validation report with issues, recommendations, and checklist",
        )

        result = task.execute()

        return {
            "status": "completed",
            "validation_result": result,
            "agent": "deployment_agent (SRE-based)",
        }

    def generate_railway_config(self, project_spec: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate optimized railway.toml configuration.

        Args:
            project_spec: Project specification including:
                - name: Application name
                - stack: Technology stack (e.g., "Go + PostgreSQL")
                - features: List of features/requirements
                - port: Application port (optional)

        Returns:
            Dictionary with generated railway.toml and Dockerfile
        """
        task = Task(
            description=f"""
            Generate railway.toml configuration for:
            - Application: {project_spec.get('name', 'tokyo-ia')}
            - Stack: {project_spec.get('stack', 'Go + PostgreSQL')}
            - Features: {', '.join(project_spec.get('features', []))}
            - Port: {project_spec.get('port', 8080)}
            
            Requirements:
            1. Multi-stage Docker build for optimal image size
            2. Health checks at /health endpoint with appropriate timeout
            3. Auto-restart on failure with max retries
            4. Environment variables template (with placeholders)
            5. Security best practices (non-root user, minimal base image)
            6. Build caching optimization
            
            Generate:
            1. Complete railway.toml file
            2. Optimized Dockerfile (multi-stage)
            3. .dockerignore file
            4. README section for deployment
            
            Format the output with clear sections for each file.
            """,
            agent=self.sre_agent,
            expected_output="Railway.toml, Dockerfile, and supporting configuration files",
        )

        result = task.execute()

        return {
            "status": "completed",
            "config_generated": result,
            "agent": "deployment_agent (SRE-based)",
        }

    def monitor_deployment_health(
        self, deployment_url: str, expected_status: int = 200
    ) -> Dict[str, Any]:
        """
        Monitor deployment health after Railway deployment.

        Args:
            deployment_url: URL of the deployed application
            expected_status: Expected HTTP status code (default: 200)

        Returns:
            Dictionary with health check results
        """
        task = Task(
            description=f"""
            Monitor the health of deployed application:
            - URL: {deployment_url}
            - Expected Status: {expected_status}
            
            Perform the following checks:
            1. HTTP health endpoint responds correctly
            2. Response time is acceptable (< 1 second)
            3. Application logs show no errors
            4. Database connections are healthy (if applicable)
            5. Memory and CPU usage are within normal ranges
            
            Provide:
            - Health status (healthy/degraded/unhealthy)
            - Response time metrics
            - Any warnings or errors detected
            - Recommendations for monitoring setup
            """,
            agent=self.sre_agent,
            expected_output="Post-deployment health monitoring report",
        )

        result = task.execute()

        return {
            "status": "completed",
            "health_report": result,
            "agent": "deployment_agent (SRE-based)",
        }

    def validate_deployment_safety(self, pr_changes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that PR changes are safe to deploy.

        Args:
            pr_changes: Dictionary with PR information:
                - title: PR title
                - files_changed: List of changed files
                - additions: Number of lines added
                - deletions: Number of lines deleted
                - description: PR description

        Returns:
            Dictionary with safety assessment
        """
        task = Task(
            description=f"""
            Assess deployment safety for the following PR:
            
            Title: {pr_changes.get('title', 'N/A')}
            Files Changed: {pr_changes.get('files_changed', [])}
            +{pr_changes.get('additions', 0)} -{pr_changes.get('deletions', 0)} lines
            
            Description:
            {pr_changes.get('description', 'No description provided')}
            
            Evaluate:
            1. Breaking changes (API changes, schema changes, etc.)
            2. Configuration changes (environment variables, feature flags)
            3. Infrastructure impact (new services, resource requirements)
            4. Rollback feasibility (can we safely rollback if needed?)
            5. Database migrations (are they reversible?)
            6. Security implications (new dependencies, exposed endpoints)
            
            Provide:
            - Deployment risk level (low/medium/high)
            - List of concerns or blockers
            - Pre-deployment checklist
            - Rollback procedure
            - Recommended deployment strategy (blue-green, canary, etc.)
            """,
            agent=self.sre_agent,
            expected_output="Deployment safety assessment with risk level and recommendations",
        )

        result = task.execute()

        return {
            "status": "completed",
            "safety_assessment": result,
            "agent": "deployment_agent (SRE-based)",
        }
