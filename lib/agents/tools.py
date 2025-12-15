"""
Custom Tools for Tokyo-IA AI Agents

This module provides custom tools that can be used by CrewAI agents.
"""

import json
import re
from typing import List, Dict, Any
import os

try:
    from crewai_tools import tool
except ImportError:
    # Fallback decorator if crewai_tools is not installed
    def tool(name):
        def decorator(func):
            func.tool_name = name
            return func
        return decorator


@tool("code_analyzer")
def analyze_code(code: str) -> str:
    """
    Analyze code for complexity, structure, and potential issues.
    
    Args:
        code: The code to analyze
        
    Returns:
        Analysis results as a formatted string
    """
    lines = code.split('\n')
    non_empty_lines = [l for l in lines if l.strip()]
    
    # Basic metrics
    metrics = {
        "total_lines": len(lines),
        "code_lines": len(non_empty_lines),
        "blank_lines": len(lines) - len(non_empty_lines),
        "functions": len(re.findall(r'\bdef\s+\w+\s*\(|\bfunction\s+\w+\s*\(', code)),
        "classes": len(re.findall(r'\bclass\s+\w+', code)),
        "comments": len(re.findall(r'#|//|/\*', code))
    }
    
    return json.dumps(metrics, indent=2)


@tool("text_summarizer")
def summarize_text(text: str, max_length: int = 200) -> str:
    """
    Summarize a piece of text to a specified length.
    
    Args:
        text: The text to summarize
        max_length: Maximum length of summary in words
        
    Returns:
        Summarized text
    """
    words = text.split()
    if len(words) <= max_length:
        return text
    
    # Simple extractive summarization: take first and last parts
    first_part = words[:max_length // 2]
    last_part = words[-(max_length // 2):]
    
    return ' '.join(first_part) + " ... " + ' '.join(last_part)


@tool("json_parser")
def parse_json_data(json_str: str) -> Dict[str, Any]:
    """
    Parse and validate JSON data.
    
    Args:
        json_str: JSON string to parse
        
    Returns:
        Parsed JSON as dictionary
    """
    try:
        data = json.loads(json_str)
        return {
            "valid": True,
            "data": data,
            "keys": list(data.keys()) if isinstance(data, dict) else None,
            "type": type(data).__name__
        }
    except json.JSONDecodeError as e:
        return {
            "valid": False,
            "error": str(e)
        }


@tool("word_counter")
def count_words(text: str) -> Dict[str, int]:
    """
    Count words and characters in text.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with counts
    """
    words = text.split()
    unique_words = set(word.lower() for word in words)
    
    return {
        "total_words": len(words),
        "unique_words": len(unique_words),
        "characters": len(text),
        "characters_no_spaces": len(text.replace(" ", "")),
        "sentences": len(re.split(r'[.!?]+', text)),
        "paragraphs": len(text.split('\n\n'))
    }


@tool("url_validator")
def validate_url(url: str) -> Dict[str, Any]:
    """
    Validate URL format and extract components.
    
    Args:
        url: URL to validate
        
    Returns:
        Validation results
    """
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    is_valid = bool(url_pattern.match(url))
    
    result = {"valid": is_valid, "url": url}
    
    if is_valid:
        # Extract components
        match = re.match(r'(https?)://([^/:]+)(?::(\d+))?(/.*)?', url)
        if match:
            result.update({
                "protocol": match.group(1),
                "domain": match.group(2),
                "port": match.group(3) or ("443" if match.group(1) == "https" else "80"),
                "path": match.group(4) or "/"
            })
    
    return result


@tool("data_formatter")
def format_data(data: str, format_type: str = "markdown") -> str:
    """
    Format data into different formats.
    
    Args:
        data: Data to format
        format_type: Output format (markdown, html, plain)
        
    Returns:
        Formatted data
    """
    if format_type == "markdown":
        # Add markdown headers
        lines = data.split('\n')
        formatted = []
        for line in lines:
            if line.strip() and not line.startswith('#'):
                formatted.append(f"* {line}")
            else:
                formatted.append(line)
        return '\n'.join(formatted)
    
    elif format_type == "html":
        lines = data.split('\n')
        html_lines = ['<ul>']
        for line in lines:
            if line.strip():
                html_lines.append(f"  <li>{line}</li>")
        html_lines.append('</ul>')
        return '\n'.join(html_lines)
    
    else:
        return data


@tool("pattern_finder")
def find_patterns(text: str, pattern: str) -> List[str]:
    """
    Find all occurrences of a regex pattern in text.
    
    Args:
        text: Text to search
        pattern: Regex pattern
        
    Returns:
        List of matches
    """
    try:
        matches = re.findall(pattern, text)
        return matches
    except re.error as e:
        return [f"Invalid regex pattern: {str(e)}"]


@tool("file_info")
def get_file_info(filepath: str) -> Dict[str, Any]:
    """
    Get information about a file.
    
    Args:
        filepath: Path to file
        
    Returns:
        File information
    """
    if not os.path.exists(filepath):
        return {"exists": False, "path": filepath}
    
    stat = os.stat(filepath)
    return {
        "exists": True,
        "path": filepath,
        "size_bytes": stat.st_size,
        "size_kb": round(stat.st_size / 1024, 2),
        "is_file": os.path.isfile(filepath),
        "is_directory": os.path.isdir(filepath),
        "extension": os.path.splitext(filepath)[1],
        "basename": os.path.basename(filepath)
    }


@tool("list_splitter")
def split_list(items: str, separator: str = ",") -> List[str]:
    """
    Split a string into a list based on separator.
    
    Args:
        items: String to split
        separator: Separator character
        
    Returns:
        List of items
    """
    result = [item.strip() for item in items.split(separator)]
    return result


# Tool collection for easy access
ALL_TOOLS = [
    analyze_code,
    summarize_text,
    parse_json_data,
    count_words,
    validate_url,
    format_data,
    find_patterns,
    get_file_info,
    split_list
]
