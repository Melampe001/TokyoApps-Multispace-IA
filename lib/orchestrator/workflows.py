#!/usr/bin/env python3
"""
Example workflows demonstrating multi-agent coordination.

These workflows show how the 5 specialized agents work together:
- Full code review workflow (Akira → Yuki → Hiro → Sakura)
- New feature development workflow (Kenji → Akira → Yuki → Sakura)
- Production deployment workflow (Akira → Yuki → Hiro)
"""

from lib.orchestrator import AgentOrchestrator


def full_code_review_workflow(orchestrator: AgentOrchestrator, code: str, language: str = "python"):
    """
    Complete code review workflow involving multiple agents.
    
    Workflow:
    1. Akira: Security audit and code review
    2. Yuki: Generate comprehensive tests
    3. Hiro: Create CI/CD pipeline
    4. Sakura: Generate documentation
    """
    workflow_id = orchestrator.create_workflow(
        name="Full Code Review",
        description=f"Complete review and testing pipeline for {language} code",
        workflow_type="code_review"
    )
    
    tasks = [
        {
            "agent_id": "akira-001",
            "task_type": "security_audit",
            "description": "Security audit and vulnerability scan",
            "method": "security_audit",
            "args": [code, language]
        },
        {
            "agent_id": "akira-001",
            "task_type": "code_review",
            "description": "Comprehensive code review",
            "method": "review_code",
            "args": [code, language],
            "kwargs": {"context": "Production code review"}
        },
        {
            "agent_id": "yuki-002",
            "task_type": "unit_tests",
            "description": "Generate unit tests",
            "method": "generate_unit_tests",
            "args": [code, language, "pytest"]
        },
        {
            "agent_id": "hiro-003",
            "task_type": "ci_cd",
            "description": "Create CI/CD pipeline",
            "method": "create_cicd_pipeline",
            "args": [{"language": language, "tests": True}],
            "kwargs": {"platform": "github-actions"}
        },
        {
            "agent_id": "sakura-004",
            "task_type": "documentation",
            "description": "Generate code documentation",
            "method": "create_readme",
            "args": [{"name": f"{language} Code", "description": "Reviewed code"}]
        }
    ]
    
    return orchestrator.run_workflow(workflow_id, tasks)


def new_feature_workflow(orchestrator: AgentOrchestrator, feature_requirements: dict):
    """
    New feature development workflow.
    
    Workflow:
    1. Kenji: Design system architecture
    2. Akira: Review architecture
    3. Yuki: Plan testing strategy
    4. Sakura: Create technical specification
    """
    workflow_id = orchestrator.create_workflow(
        name="New Feature Development",
        description=f"Design and plan: {feature_requirements.get('name', 'New Feature')}",
        workflow_type="feature_development"
    )
    
    tasks = [
        {
            "agent_id": "kenji-005",
            "task_type": "architecture",
            "description": "Design system architecture",
            "method": "design_system_architecture",
            "args": [feature_requirements]
        },
        {
            "agent_id": "yuki-002",
            "task_type": "test_planning",
            "description": "Generate integration tests plan",
            "method": "generate_integration_tests",
            "args": [[
                "API endpoints",
                "Database layer",
                "Business logic"
            ]],
            "kwargs": {"language": feature_requirements.get("language", "python")}
        },
        {
            "agent_id": "sakura-004",
            "task_type": "specification",
            "description": "Create technical specification",
            "method": "create_user_guide",
            "args": [feature_requirements]
        }
    ]
    
    return orchestrator.run_workflow(workflow_id, tasks)


def production_deployment_workflow(orchestrator: AgentOrchestrator, app_spec: dict):
    """
    Production deployment workflow.
    
    Workflow:
    1. Akira: Final security review
    2. Hiro: Design Kubernetes deployment
    3. Hiro: Setup monitoring
    4. Sakura: Create deployment documentation
    """
    workflow_id = orchestrator.create_workflow(
        name="Production Deployment",
        description=f"Deploy {app_spec.get('name', 'Application')} to production",
        workflow_type="deployment"
    )
    
    tasks = [
        {
            "agent_id": "hiro-003",
            "task_type": "kubernetes",
            "description": "Design Kubernetes deployment",
            "method": "design_kubernetes_deployment",
            "args": [app_spec]
        },
        {
            "agent_id": "hiro-003",
            "task_type": "monitoring",
            "description": "Setup monitoring and alerting",
            "method": "setup_monitoring",
            "args": [[app_spec.get("name", "app")]],
            "kwargs": {"stack": "prometheus"}
        },
        {
            "agent_id": "sakura-004",
            "task_type": "documentation",
            "description": "Create deployment documentation",
            "method": "create_user_guide",
            "args": [{
                "name": f"{app_spec.get('name', 'App')} Deployment",
                "features": ["Kubernetes", "Monitoring", "CI/CD"]
            }]
        }
    ]
    
    return orchestrator.run_workflow(workflow_id, tasks)


def microservices_design_workflow(orchestrator: AgentOrchestrator, monolith_description: str):
    """
    Microservices architecture design workflow.
    
    Workflow:
    1. Kenji: Design microservices architecture
    2. Hiro: Plan infrastructure and deployment
    3. Yuki: Design testing strategy
    4. Sakura: Document architecture
    """
    workflow_id = orchestrator.create_workflow(
        name="Microservices Architecture",
        description="Design microservices architecture from monolith",
        workflow_type="architecture"
    )
    
    tasks = [
        {
            "agent_id": "kenji-005",
            "task_type": "microservices",
            "description": "Design microservices decomposition",
            "method": "design_microservices",
            "args": [monolith_description]
        },
        {
            "agent_id": "hiro-003",
            "task_type": "infrastructure",
            "description": "Plan Kubernetes infrastructure",
            "method": "design_kubernetes_deployment",
            "args": [{
                "name": "microservices-platform",
                "image": "services/*:latest",
                "port": 8080,
                "replicas": 3
            }]
        },
        {
            "agent_id": "yuki-002",
            "task_type": "testing",
            "description": "Design microservices testing strategy",
            "method": "generate_integration_tests",
            "args": [[
                "Service A API",
                "Service B API",
                "Service communication",
                "Database per service"
            ]]
        },
        {
            "agent_id": "sakura-004",
            "task_type": "architecture_docs",
            "description": "Document microservices architecture",
            "method": "document_architecture",
            "args": [
                "Microservices Platform",
                [
                    "API Gateway",
                    "Service A",
                    "Service B",
                    "Service Discovery",
                    "Message Queue"
                ]
            ]
        }
    ]
    
    return orchestrator.run_workflow(workflow_id, tasks)


def main():
    """Demo the workflow examples."""
    print("🗼 Tokyo-IA Workflow Examples\n")
    print("Available workflows:")
    print("1. Full Code Review Workflow")
    print("2. New Feature Development Workflow")
    print("3. Production Deployment Workflow")
    print("4. Microservices Design Workflow")
    print("\nTo run these workflows:")
    print("  - Initialize orchestrator with API keys")
    print("  - Call the workflow functions with appropriate parameters")
    print("\nExample:")
    print("  orchestrator = AgentOrchestrator()")
    print("  orchestrator.initialize_agents(anthropic_api_key='...', ...)")
    print("  result = full_code_review_workflow(orchestrator, code, 'python')")


if __name__ == "__main__":
    main()
