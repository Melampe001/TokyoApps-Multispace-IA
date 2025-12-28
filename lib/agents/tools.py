"""
Custom tools for Tokyo-IA agents.

This module provides specialized tools for agents to interact with:
- Git repositories and pull requests
- Security scanners
- Test coverage analysis
- Kubernetes resources
- Diagram/image analysis
"""

import os
import subprocess
import json
from typing import Dict, Any
from crewai.tools import tool


@tool("Git Diff Tool")
def git_diff_tool(repo_path: str, base_branch: str = "main", head_branch: str = "HEAD") -> str:
    """
    Fetch git diff between two branches or commits.

    Args:
        repo_path: Path to the git repository
        base_branch: Base branch name (default: main)
        head_branch: Head branch name (default: HEAD)

    Returns:
        Git diff output as string
    """
    try:
        os.chdir(repo_path)
        result = subprocess.run(
            ["git", "diff", f"{base_branch}...{head_branch}"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error fetching git diff: {e.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool("PR Metadata Tool")
def pr_metadata_tool(pr_number: int, repo_owner: str, repo_name: str) -> Dict[str, Any]:
    """
    Fetch pull request metadata from GitHub.

    Args:
        pr_number: Pull request number
        repo_owner: Repository owner
        repo_name: Repository name

    Returns:
        Dictionary with PR metadata
    """
    # This would integrate with GitHub API
    # For now, returning mock data
    return {
        "number": pr_number,
        "title": "Example PR",
        "description": "This is an example pull request",
        "author": "developer",
        "labels": ["feature", "enhancement"],
        "files_changed": 5,
        "additions": 150,
        "deletions": 30,
    }


@tool("Security Scanner Tool")
def security_scanner_tool(file_path: str, scanner: str = "semgrep") -> Dict[str, Any]:
    """
    Run security scanning on code files.

    Args:
        file_path: Path to file or directory to scan
        scanner: Scanner to use (semgrep, snyk, etc.)

    Returns:
        Dictionary with security scan results
    """
    if scanner == "semgrep":
        try:
            result = subprocess.run(
                ["semgrep", "--config=auto", "--json", file_path],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"error": result.stderr, "findings": []}
        except FileNotFoundError:
            return {
                "error": "Semgrep not installed",
                "findings": [],
                "note": "Install with: pip install semgrep",
            }
        except Exception as e:
            return {"error": str(e), "findings": []}

    return {"error": f"Unknown scanner: {scanner}", "findings": []}


@tool("Coverage Analysis Tool")
def coverage_tool(coverage_file: str = "coverage.json") -> Dict[str, Any]:
    """
    Parse and analyze test coverage reports.

    Args:
        coverage_file: Path to coverage report file

    Returns:
        Dictionary with coverage statistics
    """
    try:
        with open(coverage_file, "r") as f:
            data = json.load(f)

        # Extract key metrics
        return {
            "total_coverage": data.get("total_coverage", 0),
            "line_coverage": data.get("line_coverage", 0),
            "branch_coverage": data.get("branch_coverage", 0),
            "files_analyzed": len(data.get("files", [])),
            "uncovered_lines": data.get("uncovered_lines", []),
            "summary": f"Overall coverage: {data.get('total_coverage', 0)}%",
        }
    except FileNotFoundError:
        return {"error": f"Coverage file not found: {coverage_file}", "total_coverage": 0}
    except Exception as e:
        return {"error": str(e), "total_coverage": 0}


@tool("Kubernetes Resource Tool")
def kubectl_tool(action: str, resource_type: str = "pods", namespace: str = "default") -> str:
    """
    Query Kubernetes resources.

    Args:
        action: Action to perform (get, describe, etc.)
        resource_type: Type of resource (pods, deployments, services, etc.)
        namespace: Kubernetes namespace

    Returns:
        Command output as string
    """
    try:
        result = subprocess.run(
            ["kubectl", action, resource_type, "-n", namespace],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout if result.returncode == 0 else result.stderr
    except FileNotFoundError:
        return "Error: kubectl not installed or not in PATH"
    except subprocess.TimeoutExpired:
        return "Error: kubectl command timed out"
    except Exception as e:
        return f"Error: {str(e)}"


@tool("Diagram Parser Tool")
def diagram_parser_tool(image_path: str) -> Dict[str, Any]:
    """
    Analyze diagrams and images to extract information.
    This would integrate with multimodal models.

    Args:
        image_path: Path to image/diagram file

    Returns:
        Dictionary with extracted information
    """
    # This would use a multimodal model (Gemini, GPT-4V, etc.)
    # For now, returning mock analysis
    if not os.path.exists(image_path):
        return {"error": f"Image not found: {image_path}"}

    return {
        "type": "architecture_diagram",
        "components": ["API Gateway", "Service A", "Service B", "Database"],
        "connections": [
            {"from": "API Gateway", "to": "Service A"},
            {"from": "API Gateway", "to": "Service B"},
            {"from": "Service A", "to": "Database"},
        ],
        "description": "Microservices architecture with API gateway pattern",
    }


@tool("Code Quality Tool")
def code_quality_tool(file_path: str, language: str = "auto") -> Dict[str, Any]:
    """
    Analyze code quality metrics.

    Args:
        file_path: Path to source file
        language: Programming language (auto-detect if not specified)

    Returns:
        Dictionary with quality metrics
    """
    try:
        # This would integrate with tools like SonarQube, CodeClimate, etc.
        # For now, basic file analysis
        with open(file_path, "r") as f:
            content = f.read()

        lines = content.split("\n")
        code_lines = [line for line in lines if line.strip() and not line.strip().startswith("#")]

        return {
            "file": file_path,
            "total_lines": len(lines),
            "code_lines": len(code_lines),
            "complexity": "moderate",
            "maintainability_index": 75,
            "issues": [],
        }
    except Exception as e:
        return {"error": str(e), "file": file_path}


@tool("Test Runner Tool")
def test_runner_tool(test_path: str, framework: str = "pytest") -> Dict[str, Any]:
    """
    Run tests and return results.

    Args:
        test_path: Path to test file or directory
        framework: Test framework to use

    Returns:
        Dictionary with test results
    """
    try:
        if framework == "pytest":
            result = subprocess.run(
                ["pytest", test_path, "-v", "--json-report"],
                capture_output=True,
                text=True,
                timeout=300,
            )
            return {
                "passed": result.returncode == 0,
                "output": result.stdout,
                "summary": "Tests completed",
            }
        elif framework == "go":
            result = subprocess.run(
                ["go", "test", "-v", test_path], capture_output=True, text=True, timeout=300
            )
            return {
                "passed": result.returncode == 0,
                "output": result.stdout,
                "summary": "Tests completed",
            }
        else:
            return {"error": f"Unknown framework: {framework}"}
    except Exception as e:
        return {"error": str(e), "passed": False}


# Tool collections for different agent types
CODE_REVIEW_TOOLS = [git_diff_tool, pr_metadata_tool, security_scanner_tool, code_quality_tool]

TEST_GENERATION_TOOLS = [git_diff_tool, coverage_tool, test_runner_tool, code_quality_tool]

SRE_TOOLS = [kubectl_tool, security_scanner_tool, test_runner_tool]

DOCUMENTATION_TOOLS = [git_diff_tool, diagram_parser_tool, code_quality_tool]
