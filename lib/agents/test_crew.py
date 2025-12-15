"""
Tests for Tokyo-IA AI Agents

Run with: pytest lib/agents/test_crew.py -v
"""

import pytest
from unittest.mock import Mock, patch
from lib.agents.crew_config import (
    get_llm,
    create_research_agent,
    create_code_reviewer_agent,
    create_content_writer_agent,
    create_data_analyst_agent,
    create_translator_agent,
    create_problem_solver_agent
)
from lib.agents.tools import (
    analyze_code,
    summarize_text,
    parse_json_data,
    count_words,
    validate_url,
    format_data,
    find_patterns,
    split_list
)


class TestCrewConfig:
    """Test agent configuration."""
    
    def test_get_llm_default(self):
        """Test getting default LLM."""
        # This will fail without API key, but tests the structure
        with pytest.raises(ValueError, match="OPENAI_API_KEY not set"):
            get_llm("gpt-4")
    
    def test_get_llm_anthropic(self):
        """Test getting Anthropic LLM."""
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY not set"):
            get_llm("claude-3-opus-20240229")
    
    def test_get_llm_gemini(self):
        """Test getting Gemini LLM."""
        with pytest.raises(ValueError, match="GEMINI_API_KEY not set"):
            get_llm("gemini-pro")
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_create_research_agent(self):
        """Test creating research agent."""
        # Mock the LLM to avoid actual API calls
        with patch('lib.agents.crew_config.LLM') as mock_llm:
            mock_llm.return_value = Mock()
            agent = create_research_agent(mock_llm.return_value)
            assert agent.role == "Research Specialist"
            assert not agent.allow_delegation
    
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
    def test_create_code_reviewer_agent(self):
        """Test creating code reviewer agent."""
        with patch('lib.agents.crew_config.LLM') as mock_llm:
            mock_llm.return_value = Mock()
            agent = create_code_reviewer_agent(mock_llm.return_value)
            assert agent.role == "Senior Code Reviewer"
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_create_content_writer_agent(self):
        """Test creating content writer agent."""
        with patch('lib.agents.crew_config.LLM') as mock_llm:
            mock_llm.return_value = Mock()
            agent = create_content_writer_agent(mock_llm.return_value)
            assert agent.role == "Content Writer"
    
    @patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'})
    def test_create_data_analyst_agent(self):
        """Test creating data analyst agent."""
        with patch('lib.agents.crew_config.LLM') as mock_llm:
            mock_llm.return_value = Mock()
            agent = create_data_analyst_agent(mock_llm.return_value)
            assert agent.role == "Data Analyst"


class TestTools:
    """Test custom tools."""
    
    def test_analyze_code(self):
        """Test code analysis tool."""
        code = """
def hello():
    # This is a comment
    print("Hello")

class MyClass:
    pass
"""
        result = analyze_code(code)
        assert "total_lines" in result
        assert "functions" in result
        assert "classes" in result
    
    def test_summarize_text_short(self):
        """Test text summarization with short text."""
        text = "This is a short text."
        result = summarize_text(text, max_length=100)
        assert result == text
    
    def test_summarize_text_long(self):
        """Test text summarization with long text."""
        text = " ".join(["word"] * 500)
        result = summarize_text(text, max_length=100)
        assert len(result.split()) <= 105  # Allow for "..."
    
    def test_parse_json_data_valid(self):
        """Test JSON parsing with valid data."""
        json_str = '{"name": "test", "value": 123}'
        result = parse_json_data(json_str)
        assert result["valid"] is True
        assert result["data"]["name"] == "test"
    
    def test_parse_json_data_invalid(self):
        """Test JSON parsing with invalid data."""
        json_str = '{"invalid": json}'
        result = parse_json_data(json_str)
        assert result["valid"] is False
        assert "error" in result
    
    def test_count_words(self):
        """Test word counting."""
        text = "Hello world! Hello everyone. This is a test."
        result = count_words(text)
        assert result["total_words"] == 8
        assert result["unique_words"] == 7  # "Hello" appears twice
    
    def test_validate_url_valid(self):
        """Test URL validation with valid URL."""
        url = "https://example.com/path"
        result = validate_url(url)
        assert result["valid"] is True
        assert result["protocol"] == "https"
        assert result["domain"] == "example.com"
    
    def test_validate_url_invalid(self):
        """Test URL validation with invalid URL."""
        url = "not-a-url"
        result = validate_url(url)
        assert result["valid"] is False
    
    def test_format_data_markdown(self):
        """Test data formatting to markdown."""
        data = "Item 1\nItem 2\nItem 3"
        result = format_data(data, "markdown")
        assert result.count("*") == 3
    
    def test_format_data_html(self):
        """Test data formatting to HTML."""
        data = "Item 1\nItem 2\nItem 3"
        result = format_data(data, "html")
        assert "<ul>" in result
        assert "</ul>" in result
        assert "<li>" in result
    
    def test_find_patterns(self):
        """Test pattern finding."""
        text = "Email me at test@example.com or admin@test.com"
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        result = find_patterns(text, pattern)
        assert len(result) == 2
    
    def test_split_list(self):
        """Test list splitting."""
        items = "apple, banana, orange, grape"
        result = split_list(items, ",")
        assert len(result) == 4
        assert result[0] == "apple"
        assert result[3] == "grape"


class TestWorkflows:
    """Test workflow functionality."""
    
    def test_workflow_registry(self):
        """Test that workflows are registered."""
        from lib.agents.workflows import WORKFLOWS
        assert "research" in WORKFLOWS
        assert "code_review" in WORKFLOWS
        assert "content_creation" in WORKFLOWS
        assert "data_analysis" in WORKFLOWS
    
    def test_run_workflow_unknown(self):
        """Test running unknown workflow."""
        from lib.agents.workflows import run_workflow
        result = run_workflow("unknown_workflow")
        assert "error" in result
        assert "available_workflows" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
