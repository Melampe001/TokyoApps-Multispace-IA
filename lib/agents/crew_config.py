"""
CrewAI Configuration for Tokyo-IA Multi-Agent System

This module defines specialized AI agents for different tasks:
1. Code Review Agent - Deep code analysis using Claude Opus
2. Test Generation Agent - Test generation using OpenAI o3
3. SRE/Deployment Agent - Infrastructure validation using Llama 4
4. Documentation Agent - Documentation generation using Gemini
"""

from crewai import Agent, Crew, Task, Process
from typing import List, Dict, Any


class AgentConfig:
    """Configuration for a single agent."""
    
    def __init__(
        self,
        role: str,
        goal: str,
        backstory: str,
        model: str,
        provider: str,
        tools: List[Any] = None,
        verbose: bool = True
    ):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.model = model
        self.provider = provider
        self.tools = tools or []
        self.verbose = verbose


# Code Review Agent Configuration
CODE_REVIEW_AGENT_CONFIG = AgentConfig(
    role="Senior Code Reviewer",
    goal="Perform comprehensive code reviews with focus on security, performance, and best practices",
    backstory="""You are an expert software engineer with 15+ years of experience.
    You have deep knowledge of multiple programming languages, design patterns, and security best practices.
    You excel at identifying subtle bugs, security vulnerabilities, and performance issues.
    Your reviews are thorough yet constructive, helping developers improve their code quality.""",
    model="claude-opus-4.1",
    provider="anthropic"
)


# Test Generation Agent Configuration
TEST_GENERATION_AGENT_CONFIG = AgentConfig(
    role="Test Engineering Specialist",
    goal="Generate comprehensive test suites with excellent coverage and edge case handling",
    backstory="""You are a test engineering expert specializing in unit tests, integration tests,
    and property-based testing. You have a keen eye for edge cases and boundary conditions.
    You understand testing frameworks across multiple languages and can generate tests that
    are maintainable, readable, and comprehensive. You prioritize test quality over quantity.""",
    model="o3",
    provider="openai"
)


# SRE/Deployment Agent Configuration
SRE_AGENT_CONFIG = AgentConfig(
    role="Site Reliability Engineer",
    goal="Ensure safe deployments and validate infrastructure configurations",
    backstory="""You are an experienced SRE with expertise in Kubernetes, cloud platforms,
    and infrastructure as code. You understand deployment strategies, rollback procedures,
    and incident response. You validate configurations for security, scalability, and reliability.
    Your focus is on preventing production incidents and ensuring system stability.""",
    model="llama-4-405b",
    provider="llama"
)


# Documentation Agent Configuration
DOCUMENTATION_AGENT_CONFIG = AgentConfig(
    role="Technical Documentation Expert",
    goal="Create clear, comprehensive documentation for code, APIs, and systems",
    backstory="""You are a technical writer with strong engineering background.
    You excel at explaining complex concepts in simple terms. You understand code deeply
    and can generate documentation that is accurate, complete, and user-friendly.
    You create diagrams, examples, and tutorials that help users understand and use systems effectively.""",
    model="gemini-3.0-ultra",
    provider="gemini"
)


def create_code_review_agent(tools: List[Any] = None) -> Agent:
    """Create a code review agent instance."""
    config = CODE_REVIEW_AGENT_CONFIG
    return Agent(
        role=config.role,
        goal=config.goal,
        backstory=config.backstory,
        tools=tools or config.tools,
        verbose=config.verbose,
        llm_config={
            "model": config.model,
            "provider": config.provider
        }
    )


def create_test_generation_agent(tools: List[Any] = None) -> Agent:
    """Create a test generation agent instance."""
    config = TEST_GENERATION_AGENT_CONFIG
    return Agent(
        role=config.role,
        goal=config.goal,
        backstory=config.backstory,
        tools=tools or config.tools,
        verbose=config.verbose,
        llm_config={
            "model": config.model,
            "provider": config.provider
        }
    )


def create_sre_agent(tools: List[Any] = None) -> Agent:
    """Create an SRE agent instance."""
    config = SRE_AGENT_CONFIG
    return Agent(
        role=config.role,
        goal=config.goal,
        backstory=config.backstory,
        tools=tools or config.tools,
        verbose=config.verbose,
        llm_config={
            "model": config.model,
            "provider": config.provider
        }
    )


def create_documentation_agent(tools: List[Any] = None) -> Agent:
    """Create a documentation agent instance."""
    config = DOCUMENTATION_AGENT_CONFIG
    return Agent(
        role=config.role,
        goal=config.goal,
        backstory=config.backstory,
        tools=tools or config.tools,
        verbose=config.verbose,
        llm_config={
            "model": config.model,
            "provider": config.provider
        }
    )


def create_agent_crew(
    agents: List[Agent],
    tasks: List[Task],
    process: Process = Process.sequential,
    verbose: bool = True
) -> Crew:
    """
    Create a crew of agents to work together on tasks.
    
    Args:
        agents: List of Agent instances
        tasks: List of Task instances
        process: Process type (sequential or hierarchical)
        verbose: Whether to output detailed logs
        
    Returns:
        Crew instance configured with the agents and tasks
    """
    return Crew(
        agents=agents,
        tasks=tasks,
        process=process,
        verbose=verbose
    )


# Example usage for PR review workflow
def create_pr_review_crew(pr_data: Dict[str, Any], tools: Dict[str, List[Any]]) -> Crew:
    """
    Create a specialized crew for PR review workflow.
    
    Args:
        pr_data: Pull request data (title, description, diff, etc.)
        tools: Dictionary of tools for each agent
        
    Returns:
        Configured Crew for PR review
    """
    # Create agents
    code_reviewer = create_code_review_agent(tools.get("code_review", []))
    test_generator = create_test_generation_agent(tools.get("test_generation", []))
    sre = create_sre_agent(tools.get("sre", []))
    
    # Define tasks
    review_task = Task(
        description=f"""Review the following pull request:
        Title: {pr_data.get('title', 'N/A')}
        Description: {pr_data.get('description', 'N/A')}
        
        Analyze the code changes for:
        1. Code quality and best practices
        2. Security vulnerabilities
        3. Performance issues
        4. Design patterns and architecture
        
        Provide detailed feedback with specific line references.""",
        agent=code_reviewer,
        expected_output="Comprehensive code review with actionable feedback"
    )
    
    test_task = Task(
        description=f"""Based on the code review, generate test cases:
        1. Unit tests for new functions/methods
        2. Integration tests for new features
        3. Edge cases and boundary conditions
        4. Regression tests
        
        Generate actual test code in the appropriate framework.""",
        agent=test_generator,
        expected_output="Test suite code with comprehensive coverage"
    )
    
    sre_task = Task(
        description=f"""Validate deployment safety:
        1. Check for breaking changes
        2. Validate configuration files
        3. Review resource requirements
        4. Assess rollback safety
        
        Provide deployment recommendations and safety checklist.""",
        agent=sre,
        expected_output="Deployment safety analysis and checklist"
    )
    
    # Create and return crew
    return create_agent_crew(
        agents=[code_reviewer, test_generator, sre],
        tasks=[review_task, test_task, sre_task],
        process=Process.sequential,
        verbose=True
    )
