"""
Multi-agent workflows for Tokyo-IA.

This module defines workflows that coordinate multiple agents:
- PR Review Workflow: Code review → Test generation → Deployment check
- Bug Fix Workflow: Debug → Fix → Test → Review
- Feature Development Workflow: Plan → Architecture → Code → Documentation
"""

from typing import Dict, Any
from crewai import Task, Process
from .crew_config import (
    create_code_review_agent,
    create_test_generation_agent,
    create_sre_agent,
    create_documentation_agent,
    create_agent_crew,
)
from .tools import CODE_REVIEW_TOOLS, TEST_GENERATION_TOOLS, SRE_TOOLS, DOCUMENTATION_TOOLS


def pr_review_workflow(pr_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a comprehensive PR review workflow.

    Workflow steps:
    1. Code Review Agent reviews the changes
    2. Test Generation Agent creates tests
    3. SRE Agent validates deployment safety

    Args:
        pr_data: Pull request data including diff, metadata, etc.

    Returns:
        Dictionary with results from all agents
    """
    # Create agents with appropriate tools
    code_reviewer = create_code_review_agent(CODE_REVIEW_TOOLS)
    test_generator = create_test_generation_agent(TEST_GENERATION_TOOLS)
    sre = create_sre_agent(SRE_TOOLS)

    # Define tasks
    tasks = [
        Task(
            description=f"""
            Review pull request #{pr_data.get('number', 'N/A')}:
            Title: {pr_data.get('title', '')}
            
            Perform comprehensive code review covering:
            1. Code quality and style
            2. Security vulnerabilities
            3. Performance considerations
            4. Best practices adherence
            5. Potential bugs
            
            Provide specific, actionable feedback with line references.
            """,
            agent=code_reviewer,
            expected_output="Detailed code review with specific recommendations",
        ),
        Task(
            description="""
            Based on the code review, generate comprehensive tests:
            1. Unit tests for all new functions
            2. Integration tests for new features
            3. Edge cases and error handling
            4. Regression tests
            
            Generate actual test code in the appropriate framework.
            Aim for >80% coverage of new code.
            """,
            agent=test_generator,
            expected_output="Test suite code with high coverage",
        ),
        Task(
            description="""
            Validate deployment safety for this PR:
            1. Check for breaking changes
            2. Review configuration changes
            3. Assess infrastructure impact
            4. Validate rollback procedures
            5. Check security implications
            
            Provide a deployment checklist and safety recommendations.
            """,
            agent=sre,
            expected_output="Deployment safety analysis and checklist",
        ),
    ]

    # Create and run crew
    crew = create_agent_crew(
        agents=[code_reviewer, test_generator, sre],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    return {
        "workflow": "pr_review",
        "status": "completed",
        "results": result,
        "pr_number": pr_data.get("number"),
        "agents_involved": ["code_reviewer", "test_generator", "sre"],
    }


def bug_fix_workflow(bug_report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a bug fix workflow.

    Workflow steps:
    1. Code Review Agent analyzes the bug
    2. Test Generation Agent creates reproduction tests
    3. Code Review Agent validates the fix
    4. Test Generation Agent verifies tests pass

    Args:
        bug_report: Bug report with description, steps to reproduce, etc.

    Returns:
        Dictionary with workflow results
    """
    code_reviewer = create_code_review_agent(CODE_REVIEW_TOOLS)
    test_generator = create_test_generation_agent(TEST_GENERATION_TOOLS)

    tasks = [
        Task(
            description=f"""
            Analyze bug report:
            {bug_report.get('description', '')}
            
            Steps to reproduce:
            {bug_report.get('steps', '')}
            
            Identify:
            1. Root cause
            2. Affected components
            3. Potential fixes
            4. Impact assessment
            """,
            agent=code_reviewer,
            expected_output="Bug analysis with root cause and fix recommendations",
        ),
        Task(
            description="""
            Create tests that reproduce the bug:
            1. Test that fails with current code
            2. Edge cases related to the bug
            3. Regression tests
            
            Tests should verify the fix once implemented.
            """,
            agent=test_generator,
            expected_output="Reproduction tests for the bug",
        ),
    ]

    crew = create_agent_crew(
        agents=[code_reviewer, test_generator],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    return {
        "workflow": "bug_fix",
        "status": "completed",
        "results": result,
        "bug_id": bug_report.get("id"),
        "agents_involved": ["code_reviewer", "test_generator"],
    }


def feature_development_workflow(feature_spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a feature development workflow.

    Workflow steps:
    1. Code Review Agent creates architecture plan
    2. Documentation Agent creates technical design doc
    3. Test Generation Agent creates test strategy
    4. SRE Agent validates operational requirements

    Args:
        feature_spec: Feature specification and requirements

    Returns:
        Dictionary with workflow results
    """
    code_reviewer = create_code_review_agent(CODE_REVIEW_TOOLS)
    doc_agent = create_documentation_agent(DOCUMENTATION_TOOLS)
    test_generator = create_test_generation_agent(TEST_GENERATION_TOOLS)
    sre = create_sre_agent(SRE_TOOLS)

    tasks = [
        Task(
            description=f"""
            Create architecture plan for feature:
            {feature_spec.get('description', '')}
            
            Requirements:
            {feature_spec.get('requirements', '')}
            
            Provide:
            1. High-level architecture
            2. Component design
            3. API contracts
            4. Data models
            5. Integration points
            """,
            agent=code_reviewer,
            expected_output="Detailed architecture plan",
        ),
        Task(
            description="""
            Create technical design document:
            1. Feature overview
            2. Architecture diagrams
            3. API specifications
            4. Implementation guidelines
            5. Usage examples
            """,
            agent=doc_agent,
            expected_output="Comprehensive technical design document",
        ),
        Task(
            description="""
            Create test strategy:
            1. Test levels (unit, integration, e2e)
            2. Test scenarios
            3. Coverage goals
            4. Test data requirements
            5. Performance test criteria
            """,
            agent=test_generator,
            expected_output="Complete test strategy document",
        ),
        Task(
            description="""
            Validate operational requirements:
            1. Infrastructure needs
            2. Scalability considerations
            3. Monitoring requirements
            4. Security requirements
            5. Deployment strategy
            """,
            agent=sre,
            expected_output="Operational requirements document",
        ),
    ]

    crew = create_agent_crew(
        agents=[code_reviewer, doc_agent, test_generator, sre],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    return {
        "workflow": "feature_development",
        "status": "completed",
        "results": result,
        "feature_id": feature_spec.get("id"),
        "agents_involved": ["code_reviewer", "documentation", "test_generator", "sre"],
    }


def documentation_generation_workflow(codebase_path: str) -> Dict[str, Any]:
    """
    Generate comprehensive documentation for a codebase.

    Args:
        codebase_path: Path to the codebase

    Returns:
        Dictionary with generated documentation
    """
    code_reviewer = create_code_review_agent(CODE_REVIEW_TOOLS)
    doc_agent = create_documentation_agent(DOCUMENTATION_TOOLS)

    tasks = [
        Task(
            description=f"""
            Analyze codebase at {codebase_path}:
            1. Identify key components
            2. Map dependencies
            3. Extract API surfaces
            4. Understand architecture
            """,
            agent=code_reviewer,
            expected_output="Codebase analysis report",
        ),
        Task(
            description="""
            Generate documentation:
            1. README with overview
            2. Architecture documentation
            3. API reference
            4. Usage examples
            5. Contributing guidelines
            """,
            agent=doc_agent,
            expected_output="Complete documentation set",
        ),
    ]

    crew = create_agent_crew(
        agents=[code_reviewer, doc_agent], tasks=tasks, process=Process.sequential, verbose=True
    )

    result = crew.kickoff()

    return {
        "workflow": "documentation_generation",
        "status": "completed",
        "results": result,
        "codebase_path": codebase_path,
        "agents_involved": ["code_reviewer", "documentation"],
    }


# Workflow registry for easy access
WORKFLOWS = {
    "pr_review": pr_review_workflow,
    "bug_fix": bug_fix_workflow,
    "feature_development": feature_development_workflow,
    "documentation_generation": documentation_generation_workflow,
}


def execute_workflow(workflow_name: str, **kwargs) -> Dict[str, Any]:
    """
    Execute a named workflow.

    Args:
        workflow_name: Name of the workflow to execute
        **kwargs: Workflow-specific parameters

    Returns:
        Dictionary with workflow results
    """
    if workflow_name not in WORKFLOWS:
        return {
            "error": f"Unknown workflow: {workflow_name}",
            "available_workflows": list(WORKFLOWS.keys()),
        }

    workflow_func = WORKFLOWS[workflow_name]
    return workflow_func(**kwargs)
