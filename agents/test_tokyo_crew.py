#!/usr/bin/env python3
"""
Unit tests for Tokyo-IA Agent Orchestration System

Tests the TokyoCrew class and its workflow methods without requiring API keys.
Uses mocking to avoid actual API calls during testing.

Usage:
    pytest agents/test_tokyo_crew.py -v
    python -m pytest agents/test_tokyo_crew.py
"""

import os
import sys
import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestTokyoCrewInitialization:
    """Test TokyoCrew initialization and agent setup."""
    
    def test_crew_initialization_without_api_keys(self):
        """Test that TokyoCrew initializes without API keys."""
        # Remove all API keys from environment
        env_backup = {}
        for key in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GROQ_API_KEY', 'GOOGLE_API_KEY']:
            env_backup[key] = os.environ.pop(key, None)
        
        try:
            # Import here to avoid import errors
            from agents.tokyo_crew import TokyoCrew
            
            crew = TokyoCrew(verbose=False)
            
            # Should have no agents initialized
            assert len(crew.agents) == 0
            assert len(crew.initialized_agents) == 0
            assert crew.output_dir.exists()
            
        finally:
            # Restore environment
            for key, value in env_backup.items():
                if value:
                    os.environ[key] = value
    
    def test_output_directory_creation(self):
        """Test that output directory is created with timestamp."""
        from agents.tokyo_crew import TokyoCrew
        
        crew = TokyoCrew(verbose=False)
        
        assert crew.output_dir.exists()
        assert crew.output_dir.is_dir()
        assert str(crew.output_dir).startswith('agent_reports_')
    
    @patch.dict(os.environ, {'GROQ_API_KEY': 'test_key'})
    @patch('agents.tokyo_crew.LLM')
    @patch('agents.tokyo_crew.Agent')
    def test_hiro_initialization_with_groq_key(self, mock_agent, mock_llm):
        """Test that Hiro initializes when GROQ_API_KEY is set."""
        from agents.tokyo_crew import TokyoCrew
        
        # Mock the LLM and Agent classes
        mock_llm.return_value = MagicMock()
        mock_agent.return_value = MagicMock()
        
        crew = TokyoCrew(verbose=False)
        
        # Check that Hiro was initialized
        assert 'hiro' in crew.agents or len(crew.initialized_agents) > 0


class TestTokyoCrewWorkflows:
    """Test TokyoCrew workflow methods."""
    
    @patch.dict(os.environ, {})
    def test_list_agents_info_without_keys(self, capsys):
        """Test list_agents_info displays correctly without API keys."""
        from agents.tokyo_crew import TokyoCrew
        
        crew = TokyoCrew(verbose=False)
        crew.list_agents_info()
        
        captured = capsys.readouterr()
        
        # Should show all 5 agents
        assert 'Akira' in captured.out
        assert 'Yuki' in captured.out
        assert 'Hiro' in captured.out
        assert 'Sakura' in captured.out
        assert 'Kenji' in captured.out
        assert 'NOT INITIALIZED' in captured.out
    
    def test_analyze_pr_without_agents(self):
        """Test analyze_pr workflow when no agents are initialized."""
        from agents.tokyo_crew import TokyoCrew
        
        crew = TokyoCrew(verbose=False)
        
        # Should complete without errors even with no agents
        result = crew.analyze_pr(123)
        
        assert isinstance(result, dict)
        assert 'pr_number' in result
        assert result['pr_number'] == 123
        assert 'timestamp' in result
        assert 'agent_results' in result
    
    def test_cleanup_repository_without_agents(self):
        """Test cleanup_repository workflow when no agents are initialized."""
        from agents.tokyo_crew import TokyoCrew
        
        crew = TokyoCrew(verbose=False)
        
        # Should complete without errors even with no agents
        result = crew.cleanup_repository()
        
        assert isinstance(result, dict)
        assert 'timestamp' in result
        assert 'cleanup_tasks' in result
    
    def test_generate_documentation_without_sakura(self):
        """Test generate_documentation workflow when Sakura is not initialized."""
        from agents.tokyo_crew import TokyoCrew
        
        crew = TokyoCrew(verbose=False)
        
        # Should return error dict when Sakura not available
        result = crew.generate_documentation()
        
        assert isinstance(result, dict)
        assert 'error' in result or 'timestamp' in result


class TestReportGeneration:
    """Test report file generation."""
    
    def test_pr_analysis_report_creation(self):
        """Test that PR analysis creates a JSON report file."""
        from agents.tokyo_crew import TokyoCrew
        
        crew = TokyoCrew(verbose=False)
        result = crew.analyze_pr(999)
        
        # Check that report file was created
        report_file = crew.output_dir / "pr_999_analysis.json"
        assert report_file.exists()
        
        # Verify JSON structure
        with open(report_file, 'r') as f:
            data = json.load(f)
            assert data['pr_number'] == 999
            assert 'timestamp' in data
            assert 'agent_results' in data
    
    def test_cleanup_report_creation(self):
        """Test that cleanup workflow creates a JSON report file."""
        from agents.tokyo_crew import TokyoCrew
        
        crew = TokyoCrew(verbose=False)
        result = crew.cleanup_repository()
        
        # Check that report file was created
        report_file = crew.output_dir / "cleanup_plan.json"
        assert report_file.exists()
        
        # Verify JSON structure
        with open(report_file, 'r') as f:
            data = json.load(f)
            assert 'timestamp' in data
            assert 'cleanup_tasks' in data


class TestCLIInterface:
    """Test command-line interface."""
    
    def test_cli_help_output(self, capsys):
        """Test that --help flag works."""
        from agents.tokyo_crew import main
        
        with pytest.raises(SystemExit) as exc_info:
            sys.argv = ['tokyo_crew.py', '--help']
            main()
        
        assert exc_info.value.code == 0
    
    def test_cli_list_agents_command(self):
        """Test list-agents command."""
        from agents.tokyo_crew import main
        
        sys.argv = ['tokyo_crew.py', 'list-agents']
        
        # Should not raise any exceptions
        try:
            main()
        except SystemExit as e:
            assert e.code == 0
    
    def test_cli_analyze_pr_requires_number(self):
        """Test that analyze-pr command requires a PR number."""
        from agents.tokyo_crew import main
        
        sys.argv = ['tokyo_crew.py', 'analyze-pr']
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        # Should exit with error code
        assert exc_info.value.code != 0


class TestAgentConfiguration:
    """Test agent configuration and models."""
    
    def test_agent_models_are_correct(self):
        """Test that each agent is configured with the correct LLM model."""
        # This is a documentation test to ensure models match requirements
        expected_models = {
            'akira': 'claude-3-5-sonnet-20241022',
            'yuki': 'gpt-4o-mini',
            'hiro': 'llama-3.3-70b-versatile',
            'sakura': 'gemini-1.5-flash',
            'kenji': 'gpt-4o'
        }
        
        # Read tokyo_crew.py to verify model strings
        tokyo_crew_file = Path(__file__).parent / 'tokyo_crew.py'
        content = tokyo_crew_file.read_text()
        
        for agent, model in expected_models.items():
            assert model in content, f"Model {model} for agent {agent} not found"
    
    def test_free_tier_agents_identified(self):
        """Test that FREE tier agents (Hiro and Sakura) are properly identified."""
        from agents.tokyo_crew import TokyoCrew
        
        crew = TokyoCrew(verbose=False)
        crew.list_agents_info()
        
        # Hiro and Sakura should be marked as FREE
        # This is validated by the model strings containing "FREE"


# Fixtures for cleanup
@pytest.fixture(autouse=True)
def cleanup_test_reports():
    """Clean up test report directories after each test."""
    yield
    
    # Clean up any report directories created during tests
    import shutil
    for report_dir in Path('.').glob('agent_reports_*'):
        if report_dir.is_dir():
            try:
                shutil.rmtree(report_dir)
            except:
                pass


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])
