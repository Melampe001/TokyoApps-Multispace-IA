"""
Tokyo-IA Agent Framework

This package provides multi-agent AI capabilities using CrewAI.
"""

from .crew_config import (
    create_code_review_agent,
    create_test_generation_agent,
    create_sre_agent,
    create_documentation_agent,
    create_agent_crew,
    create_pr_review_crew
)

from .workflows import (
    pr_review_workflow,
    bug_fix_workflow,
    feature_development_workflow,
    documentation_generation_workflow,
    execute_workflow,
    WORKFLOWS
)

__all__ = [
    'create_code_review_agent',
    'create_test_generation_agent',
    'create_sre_agent',
    'create_documentation_agent',
    'create_agent_crew',
    'create_pr_review_crew',
    'pr_review_workflow',
    'bug_fix_workflow',
    'feature_development_workflow',
    'documentation_generation_workflow',
    'execute_workflow',
    'WORKFLOWS'
]

__version__ = '0.1.0'
