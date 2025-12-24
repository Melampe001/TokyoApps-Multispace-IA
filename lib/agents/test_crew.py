"""
Unit tests for Tokyo-IA agent framework.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from lib.agents.crew_config import (
    AgentConfig,
    CODE_REVIEW_AGENT_CONFIG,
    TEST_GENERATION_AGENT_CONFIG,
    SRE_AGENT_CONFIG,
    DOCUMENTATION_AGENT_CONFIG,
)


class TestAgentConfig(unittest.TestCase):
    """Test AgentConfig class."""

    def test_agent_config_initialization(self):
        """Test that AgentConfig initializes correctly."""
        config = AgentConfig(
            role="Test Role",
            goal="Test Goal",
            backstory="Test Backstory",
            model="test-model",
            provider="test-provider",
            verbose=True,
        )

        self.assertEqual(config.role, "Test Role")
        self.assertEqual(config.goal, "Test Goal")
        self.assertEqual(config.backstory, "Test Backstory")
        self.assertEqual(config.model, "test-model")
        self.assertEqual(config.provider, "test-provider")
        self.assertEqual(config.verbose, True)
        self.assertEqual(config.tools, [])

    def test_agent_config_with_tools(self):
        """Test AgentConfig with tools."""
        tools = [Mock(), Mock()]
        config = AgentConfig(
            role="Test", goal="Test", backstory="Test", model="test", provider="test", tools=tools
        )

        self.assertEqual(len(config.tools), 2)


class TestPredefinedConfigs(unittest.TestCase):
    """Test predefined agent configurations."""

    def test_code_review_agent_config(self):
        """Test code review agent configuration."""
        config = CODE_REVIEW_AGENT_CONFIG

        self.assertIn("Code Reviewer", config.role)
        self.assertIn("code review", config.goal.lower())
        self.assertEqual(config.model, "claude-opus-4.1")
        self.assertEqual(config.provider, "anthropic")

    def test_test_generation_agent_config(self):
        """Test test generation agent configuration."""
        config = TEST_GENERATION_AGENT_CONFIG

        self.assertIn("Test", config.role)
        self.assertIn("test", config.goal.lower())
        self.assertEqual(config.model, "o3")
        self.assertEqual(config.provider, "openai")

    def test_sre_agent_config(self):
        """Test SRE agent configuration."""
        config = SRE_AGENT_CONFIG

        self.assertIn("SRE", config.role)
        self.assertIn("deployment", config.goal.lower())
        self.assertEqual(config.model, "llama-4-405b")
        self.assertEqual(config.provider, "llama")

    def test_documentation_agent_config(self):
        """Test documentation agent configuration."""
        config = DOCUMENTATION_AGENT_CONFIG

        self.assertIn("Documentation", config.role)
        self.assertIn("documentation", config.goal.lower())
        self.assertEqual(config.model, "gemini-3.0-ultra")
        self.assertEqual(config.provider, "gemini")


class TestWorkflows(unittest.TestCase):
    """Test workflow functions."""

    @patch("lib.agents.workflows.create_agent_crew")
    @patch("lib.agents.workflows.create_code_review_agent")
    @patch("lib.agents.workflows.create_test_generation_agent")
    @patch("lib.agents.workflows.create_sre_agent")
    def test_pr_review_workflow_structure(
        self, mock_sre, mock_test_gen, mock_code_review, mock_crew
    ):
        """Test PR review workflow is properly structured."""
        from lib.agents.workflows import pr_review_workflow

        # Mock crew kickoff
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "Mock result"
        mock_crew.return_value = mock_crew_instance

        # Mock agent creation
        mock_code_review.return_value = Mock()
        mock_test_gen.return_value = Mock()
        mock_sre.return_value = Mock()

        # Execute workflow
        pr_data = {"number": 123, "title": "Test PR", "description": "Test description"}

        result = pr_review_workflow(pr_data)

        # Verify result structure
        self.assertEqual(result["workflow"], "pr_review")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["pr_number"], 123)
        self.assertIn("agents_involved", result)

        # Verify agents were created
        mock_code_review.assert_called_once()
        mock_test_gen.assert_called_once()
        mock_sre.assert_called_once()

        # Verify crew was created
        mock_crew.assert_called_once()


class TestTools(unittest.TestCase):
    """Test custom tools."""

    def test_tool_collections_exist(self):
        """Test that tool collections are defined."""
        from lib.agents.tools import (
            CODE_REVIEW_TOOLS,
            TEST_GENERATION_TOOLS,
            SRE_TOOLS,
            DOCUMENTATION_TOOLS,
        )

        self.assertTrue(isinstance(CODE_REVIEW_TOOLS, list))
        self.assertTrue(isinstance(TEST_GENERATION_TOOLS, list))
        self.assertTrue(isinstance(SRE_TOOLS, list))
        self.assertTrue(isinstance(DOCUMENTATION_TOOLS, list))

        # Verify tools are not empty
        self.assertGreater(len(CODE_REVIEW_TOOLS), 0)
        self.assertGreater(len(TEST_GENERATION_TOOLS), 0)
        self.assertGreater(len(SRE_TOOLS), 0)
        self.assertGreater(len(DOCUMENTATION_TOOLS), 0)


if __name__ == "__main__":
    unittest.main()
