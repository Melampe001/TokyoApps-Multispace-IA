"""
Tokyo-IA Specialized Agents

Five elite AI agents with unique personalities and expertise:
- Akira (侍) - Code Review Master
- Yuki (❄️) - Test Engineering Specialist
- Hiro (🛡️) - SRE & DevOps Guardian
- Sakura (🌸) - Documentation Artist
- Kenji (🏗️) - Architecture Visionary
"""

from .akira_code_reviewer import AkiraCodeReviewer
from .yuki_test_engineer import YukiTestEngineer
from .hiro_sre import HiroSRE
from .sakura_documentation import SakuraDocumentation
from .kenji_architect import KenjiArchitect

__all__ = [
    'AkiraCodeReviewer',
    'YukiTestEngineer',
    'HiroSRE',
    'SakuraDocumentation',
    'KenjiArchitect',
]

# Agent registry
AGENTS = {
    'akira-001': {
        'class': AkiraCodeReviewer,
        'name': 'Akira',
        'emoji': '侍',
        'role': 'Code Review Master',
        'specialties': ['security', 'performance', 'architecture', 'code-quality']
    },
    'yuki-002': {
        'class': YukiTestEngineer,
        'name': 'Yuki',
        'emoji': '❄️',
        'role': 'Test Engineering Specialist',
        'specialties': ['unit-testing', 'integration-testing', 'e2e-testing', 'test-automation']
    },
    'hiro-003': {
        'class': HiroSRE,
        'name': 'Hiro',
        'emoji': '🛡️',
        'role': 'SRE & DevOps Guardian',
        'specialties': ['kubernetes', 'ci-cd', 'monitoring', 'infrastructure', 'reliability']
    },
    'sakura-004': {
        'class': SakuraDocumentation,
        'name': 'Sakura',
        'emoji': '🌸',
        'role': 'Documentation Artist',
        'specialties': ['technical-writing', 'documentation', 'diagrams', 'api-docs']
    },
    'kenji-005': {
        'class': KenjiArchitect,
        'name': 'Kenji',
        'emoji': '🏗️',
        'role': 'Architecture Visionary',
        'specialties': ['system-design', 'architecture', 'design-patterns', 'scalability']
    }
}


def get_agent(agent_id: str, **kwargs):
    """
    Get an agent instance by ID.
    
    Args:
        agent_id: Agent ID (e.g., 'akira-001')
        **kwargs: Arguments to pass to agent constructor
        
    Returns:
        Agent instance
        
    Raises:
        ValueError: If agent_id is not found
    """
    if agent_id not in AGENTS:
        raise ValueError(f"Unknown agent ID: {agent_id}")
    
    agent_info = AGENTS[agent_id]
    agent_class = agent_info['class']
    
    return agent_class(**kwargs)


def list_agents():
    """
    List all available agents.
    
    Returns:
        Dict of agent information
    """
    return {
        agent_id: {
            'name': info['name'],
            'emoji': info['emoji'],
            'role': info['role'],
            'specialties': info['specialties']
        }
        for agent_id, info in AGENTS.items()
    }
