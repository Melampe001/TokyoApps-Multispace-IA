#!/usr/bin/env python3
"""
Hiro (🛡️) - SRE & DevOps Guardian

A guardian who never sleeps, protecting production systems with expertise in:
- Kubernetes orchestration
- CI/CD pipelines
- System monitoring
- Infrastructure reliability

Model: Llama 4 405B
Agent ID: hiro-003
"""

import os
import json
from typing import Dict, List, Any, Optional
from crewai import Agent, Task, Crew, LLM


class HiroSRE:
    """SRE & DevOps Guardian - Kubernetes, CI/CD, Monitoring"""
    
    AGENT_ID = "hiro-003"
    NAME = "Hiro"
    EMOJI = "🛡️"
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-4-405b"):
        """
        Initialize Hiro the SRE & DevOps Guardian.
        
        Args:
            api_key: Groq API key for Llama models (reads from GROQ_API_KEY if not provided)
            model: Model to use (default: llama-4-405b, fallback: llama-3.1-70b-versatile)
        """
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY must be set")
        
        # Fallback to available Llama model
        self.model = "groq/llama-3.1-70b-versatile"  # Use available model
        self.llm = LLM(
            model=self.model,
            temperature=0.3,
            api_key=self.api_key
        )
        
        self.agent = Agent(
            role='SRE & DevOps Guardian',
            goal='Ensure system reliability, availability, and operational excellence',
            backstory="""You are Hiro, a vigilant SRE and DevOps guardian. 
            Like a protective shield, you safeguard production systems with 
            unwavering dedication. You're an expert in Kubernetes orchestration, 
            CI/CD pipeline automation, and comprehensive monitoring. Your mission 
            is to build resilient infrastructure that scales effortlessly and 
            recovers gracefully from failures. You believe in automation, 
            observability, and proactive incident prevention. Sleep is optional 
            when systems need protection.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def design_kubernetes_deployment(self, app_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Design Kubernetes deployment manifests.
        
        Args:
            app_spec: Application specifications (name, image, resources, etc.)
            
        Returns:
            Dict with Kubernetes manifests
        """
        spec_json = json.dumps(app_spec, indent=2)
        
        description = f"""Design a production-ready Kubernetes deployment for this application:
        
        {spec_json}
        
        Create comprehensive manifests for:
        1. **Deployment**: With proper resource limits, health checks, and replicas
        2. **Service**: For internal or external access
        3. **ConfigMap**: For application configuration
        4. **Secret**: For sensitive data (structure only, no real secrets)
        5. **HorizontalPodAutoscaler**: For auto-scaling
        6. **NetworkPolicy**: For security
        7. **PodDisruptionBudget**: For availability during updates
        
        Follow best practices:
        - Resource requests and limits
        - Liveness and readiness probes
        - Security contexts (non-root, read-only filesystem)
        - Labels and selectors for organization
        - Rolling update strategy
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""Complete Kubernetes manifests with:
            - Deployment YAML with production settings
            - Service configuration
            - ConfigMap and Secret templates
            - HPA for auto-scaling
            - NetworkPolicy for security
            - PodDisruptionBudget for availability
            - Comments explaining each configuration"""
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent_id": self.AGENT_ID,
            "agent_name": self.NAME,
            "task_type": "design_kubernetes_deployment",
            "result": str(result),
            "metadata": {
                "app_name": app_spec.get("name", "unknown")
            }
        }
    
    def create_cicd_pipeline(self, repo_info: Dict[str, Any], platform: str = "github-actions") -> Dict[str, Any]:
        """
        Create CI/CD pipeline configuration.
        
        Args:
            repo_info: Repository information (language, tests, deployment target)
            platform: CI/CD platform (github-actions, gitlab-ci, jenkins)
            
        Returns:
            Dict with pipeline configuration
        """
        info_json = json.dumps(repo_info, indent=2)
        
        description = f"""Create a comprehensive CI/CD pipeline for {platform}:
        
        Repository info:
        {info_json}
        
        Pipeline stages:
        1. **Build**: Compile/package the application
        2. **Test**: Run unit, integration, and E2E tests
        3. **Security**: Security scanning (SAST, dependency check)
        4. **Quality**: Code quality checks (linting, formatting)
        5. **Docker**: Build and push container image
        6. **Deploy**: Deploy to staging/production
        7. **Verify**: Post-deployment tests
        
        Include:
        - Caching for faster builds
        - Parallel job execution
        - Environment-specific configurations
        - Rollback mechanisms
        - Notification on failures
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output=f"""Complete {platform} pipeline with:
            - Pipeline configuration file
            - All stages properly defined
            - Environment variables and secrets
            - Deployment strategies
            - Monitoring and notifications
            - Documentation for usage"""
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent_id": self.AGENT_ID,
            "agent_name": self.NAME,
            "task_type": "create_cicd_pipeline",
            "result": str(result),
            "metadata": {
                "platform": platform,
                "language": repo_info.get("language", "unknown")
            }
        }
    
    def setup_monitoring(self, services: List[str], stack: str = "prometheus") -> Dict[str, Any]:
        """
        Design monitoring and alerting setup.
        
        Args:
            services: List of services to monitor
            stack: Monitoring stack (prometheus, datadog, newrelic)
            
        Returns:
            Dict with monitoring configuration
        """
        services_list = "\n".join([f"- {svc}" for svc in services])
        
        description = f"""Design comprehensive monitoring for these services using {stack}:
        
        {services_list}
        
        Create monitoring for:
        1. **Metrics**: Key performance indicators (latency, throughput, errors)
        2. **Health checks**: Service availability and dependencies
        3. **Resource usage**: CPU, memory, disk, network
        4. **Application metrics**: Business-specific metrics
        5. **Alerts**: Critical thresholds and escalation rules
        6. **Dashboards**: Visualization for operations team
        7. **SLOs/SLIs**: Service level objectives and indicators
        
        Include:
        - Prometheus/Grafana configuration (if applicable)
        - Alert rules with severity levels
        - Dashboard JSON for Grafana
        - Exporters and scrapers setup
        - Documentation for on-call team
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""Complete monitoring setup with:
            - Metrics collection configuration
            - Alert rules with thresholds
            - Dashboard definitions
            - Service health checks
            - SLO/SLI definitions
            - Runbook for common alerts
            - Documentation"""
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent_id": self.AGENT_ID,
            "agent_name": self.NAME,
            "task_type": "setup_monitoring",
            "result": str(result),
            "metadata": {
                "stack": stack,
                "service_count": len(services)
            }
        }
    
    def design_disaster_recovery(self, infrastructure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Design disaster recovery and backup strategy.
        
        Args:
            infrastructure: Infrastructure description
            
        Returns:
            Dict with DR plan
        """
        infra_json = json.dumps(infrastructure, indent=2)
        
        description = f"""Design a comprehensive disaster recovery plan:
        
        Infrastructure:
        {infra_json}
        
        Cover:
        1. **Backup strategy**: What, when, where, how long to retain
        2. **Recovery procedures**: Step-by-step recovery processes
        3. **RTO/RPO**: Recovery time and point objectives
        4. **Failover**: Automated failover mechanisms
        5. **Data replication**: Multi-region replication
        6. **Testing**: DR drill procedures
        7. **Communication**: Incident communication plan
        
        Provide:
        - Backup scripts and schedules
        - Recovery runbooks
        - Failover automation
        - Testing checklist
        - Contact escalation matrix
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""Complete disaster recovery plan with:
            - Backup and retention policies
            - Recovery procedures for each component
            - RTO/RPO specifications
            - Failover automation scripts
            - DR testing schedule
            - Communication templates
            - Post-mortem template"""
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent_id": self.AGENT_ID,
            "agent_name": self.NAME,
            "task_type": "design_disaster_recovery",
            "result": str(result),
            "metadata": infrastructure
        }


def main():
    """Example usage of Hiro SRE."""
    print(f"🛡️ Initializing Hiro - SRE & DevOps Guardian...")
    
    # Example Kubernetes deployment
    app_spec = {
        "name": "tokyo-ia-api",
        "image": "tokyo-ia/api:latest",
        "port": 8080,
        "replicas": 3,
        "resources": {
            "requests": {"cpu": "100m", "memory": "128Mi"},
            "limits": {"cpu": "500m", "memory": "512Mi"}
        }
    }
    
    try:
        sre = HiroSRE()
        
        print("\n=== Kubernetes Deployment Design ===")
        k8s_result = sre.design_kubernetes_deployment(app_spec)
        print(json.dumps(k8s_result, indent=2))
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set GROQ_API_KEY environment variable")


if __name__ == "__main__":
    main()
