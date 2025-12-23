"""
Tools module for agent-based automation.

This module provides various tools that agents can use to perform tasks
such as file operations, data processing, and system interactions.
"""

import os
import json
import subprocess
from typing import Any, Dict, List, Optional
from pathlib import Path
import logging

# Import CrewAI tool decorator
from crewai.tools import tool

logger = logging.getLogger(__name__)


@tool("Read File")
def read_file(file_path: str) -> str:
    """
    Read and return the contents of a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        File contents as string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return f"Error reading file: {str(e)}"


@tool("Write File")
def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        
    Returns:
        Success or error message
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        logger.error(f"Error writing file {file_path}: {e}")
        return f"Error writing file: {str(e)}"


@tool("List Directory")
def list_directory(directory_path: str) -> str:
    """
    List all files and directories in the specified path.
    
    Args:
        directory_path: Path to the directory to list
        
    Returns:
        JSON string with directory contents
    """
    try:
        path = Path(directory_path)
        if not path.exists():
            return f"Directory {directory_path} does not exist"
        
        items = {
            "files": [],
            "directories": []
        }
        
        for item in path.iterdir():
            if item.is_file():
                items["files"].append(str(item.name))
            elif item.is_dir():
                items["directories"].append(str(item.name))
        
        return json.dumps(items, indent=2)
    except Exception as e:
        logger.error(f"Error listing directory {directory_path}: {e}")
        return f"Error listing directory: {str(e)}"


@tool("Execute Command")
def execute_command(command: str) -> str:
    """
    Execute a shell command and return the output.
    
    Args:
        command: Command to execute
        
    Returns:
        Command output or error message
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
        
        return json.dumps(output, indent=2)
    except subprocess.TimeoutExpired:
        return "Error: Command execution timed out"
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        return f"Error executing command: {str(e)}"


@tool("Search Files")
def search_files(directory: str, pattern: str) -> str:
    """
    Search for files matching a pattern in a directory.
    
    Args:
        directory: Directory to search in
        pattern: File pattern to match (e.g., "*.py")
        
    Returns:
        JSON string with matching files
    """
    try:
        path = Path(directory)
        if not path.exists():
            return f"Directory {directory} does not exist"
        
        matches = list(path.rglob(pattern))
        files = [str(match.relative_to(path)) for match in matches if match.is_file()]
        
        return json.dumps({"matches": files, "count": len(files)}, indent=2)
    except Exception as e:
        logger.error(f"Error searching files: {e}")
        return f"Error searching files: {str(e)}"
