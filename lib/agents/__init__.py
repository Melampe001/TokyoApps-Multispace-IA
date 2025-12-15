"""
Tokyo-IA AI Agents Package

This package provides CrewAI-based agents and workflows for the Tokyo-IA project.
"""

try:
    from .crew_config import (
        get_llm,
        create_research_agent,
        create_code_reviewer_agent,
        create_content_writer_agent,
        create_data_analyst_agent,
        create_translator_agent,
        create_problem_solver_agent
    )
    CREW_CONFIG_AVAILABLE = True
except ImportError:
    CREW_CONFIG_AVAILABLE = False

from .tools import ALL_TOOLS

try:
    from .workflows import WORKFLOWS, run_workflow
    WORKFLOWS_AVAILABLE = True
except ImportError:
    WORKFLOWS_AVAILABLE = False

__all__ = [
    'ALL_TOOLS',
    'CREW_CONFIG_AVAILABLE',
    'WORKFLOWS_AVAILABLE'
]

if CREW_CONFIG_AVAILABLE:
    __all__.extend([
        'get_llm',
        'create_research_agent',
        'create_code_reviewer_agent',
        'create_content_writer_agent',
        'create_data_analyst_agent',
        'create_translator_agent',
        'create_problem_solver_agent',
    ])

if WORKFLOWS_AVAILABLE:
    __all__.extend(['WORKFLOWS', 'run_workflow'])
