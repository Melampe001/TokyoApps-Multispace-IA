"""
Tests for Tokyo-IA AI Agent Tools (standalone)

These tests can run without CrewAI dependencies.
Run with: pytest lib/agents/test_tools.py -v
"""

import pytest
import json
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
        data = json.loads(result)
        assert "total_lines" in data
        assert "functions" in data
        assert "classes" in data
        assert data["functions"] == 1
        assert data["classes"] == 1
    
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
        assert "..." in result
    
    def test_parse_json_data_valid(self):
        """Test JSON parsing with valid data."""
        json_str = '{"name": "test", "value": 123}'
        result = parse_json_data(json_str)
        assert result["valid"] is True
        assert result["data"]["name"] == "test"
        assert result["data"]["value"] == 123
    
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
        assert result["characters"] > 0
    
    def test_validate_url_valid(self):
        """Test URL validation with valid URL."""
        url = "https://example.com/path"
        result = validate_url(url)
        assert result["valid"] is True
        assert result["protocol"] == "https"
        assert result["domain"] == "example.com"
        assert result["path"] == "/path"
    
    def test_validate_url_invalid(self):
        """Test URL validation with invalid URL."""
        url = "not-a-url"
        result = validate_url(url)
        assert result["valid"] is False
    
    def test_validate_url_localhost(self):
        """Test URL validation with localhost."""
        url = "http://localhost:8080/api"
        result = validate_url(url)
        assert result["valid"] is True
        assert result["protocol"] == "http"
        assert result["port"] == "8080"
    
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
        assert result.count("<li>") == 3
    
    def test_format_data_plain(self):
        """Test data formatting to plain."""
        data = "Item 1\nItem 2"
        result = format_data(data, "plain")
        assert result == data
    
    def test_find_patterns(self):
        """Test pattern finding."""
        text = "Email me at test@example.com or admin@test.com"
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        result = find_patterns(text, pattern)
        assert len(result) == 2
        assert "test@example.com" in result
        assert "admin@test.com" in result
    
    def test_find_patterns_invalid_regex(self):
        """Test pattern finding with invalid regex."""
        text = "Some text"
        pattern = r'[invalid'
        result = find_patterns(text, pattern)
        assert len(result) == 1
        assert "Invalid regex pattern" in result[0]
    
    def test_split_list(self):
        """Test list splitting."""
        items = "apple, banana, orange, grape"
        result = split_list(items, ",")
        assert len(result) == 4
        assert result[0] == "apple"
        assert result[3] == "grape"
    
    def test_split_list_custom_separator(self):
        """Test list splitting with custom separator."""
        items = "apple|banana|orange"
        result = split_list(items, "|")
        assert len(result) == 3
        assert result[1] == "banana"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
