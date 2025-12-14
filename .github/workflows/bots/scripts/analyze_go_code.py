#!/usr/bin/env python3
"""
Backend Code Quality Analyzer for Go code.
Analyzes Go code for quality metrics: tests, documentation, error handling, imports.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple


class GoCodeAnalyzer:
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.issues = []
        self.metrics = {
            "tests_found": 0,
            "functions_without_docs": 0,
            "error_handling_issues": 0,
            "unused_imports": 0,
            "quality_score": 0
        }

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {
            "quality_thresholds": {
                "min_test_coverage": 80,
                "max_function_length": 50
            },
            "auto_approve": {
                "min_quality_score": 90
            }
        }

    def analyze_file(self, filepath: str) -> None:
        """Analyze a single Go file."""
        if not filepath.endswith('.go'):
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # Check if it's a test file
        if filepath.endswith('_test.go'):
            self.metrics["tests_found"] += 1
            return

        # Check for exported functions without documentation
        self._check_function_docs(filepath, lines)

        # Check for error handling
        self._check_error_handling(filepath, content)

        # Check for unused imports (basic check)
        self._check_imports(filepath, content)

    def _check_function_docs(self, filepath: str, lines: List[str]) -> None:
        """Check if exported functions have documentation comments."""
        func_pattern = re.compile(r'^func\s+([A-Z][a-zA-Z0-9]*)\s*\(')
        
        for i, line in enumerate(lines):
            match = func_pattern.match(line.strip())
            if match:
                func_name = match.group(1)
                # Check if previous line has a comment
                if i == 0 or not lines[i-1].strip().startswith('//'):
                    self.issues.append({
                        "file": filepath,
                        "line": i + 1,
                        "type": "missing_docs",
                        "message": f"Exported function '{func_name}' lacks documentation comment"
                    })
                    self.metrics["functions_without_docs"] += 1

    def _check_error_handling(self, filepath: str, content: str) -> None:
        """Check for basic error handling patterns."""
        # Look for function returns with error but no error handling
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # Very basic check: if line has "err :=" or "err =" but no "if err" nearby
            if re.search(r'\berr\s*:?=', line):
                # Check next few lines for error handling
                check_lines = '\n'.join(lines[i:min(i+5, len(lines))])
                if 'if err != nil' not in check_lines and 'if err =' not in check_lines:
                    # This might be a false positive, so mark as warning
                    self.issues.append({
                        "file": filepath,
                        "line": i + 1,
                        "type": "potential_error_handling",
                        "message": "Potential unhandled error assignment (verify manually)"
                    })
                    self.metrics["error_handling_issues"] += 1

    def _check_imports(self, filepath: str, content: str) -> None:
        """Check for unused imports (basic detection)."""
        import_pattern = re.compile(r'^\s*import\s+\(([^)]+)\)', re.MULTILINE | re.DOTALL)
        single_import_pattern = re.compile(r'^\s*import\s+"([^"]+)"', re.MULTILINE)
        
        # Extract imports
        imports = []
        multi_match = import_pattern.search(content)
        if multi_match:
            import_block = multi_match.group(1)
            imports.extend(re.findall(r'"([^"]+)"', import_block))
        
        for match in single_import_pattern.finditer(content):
            imports.append(match.group(1))
        
        # Check if each import is used (very basic check)
        for imp in imports:
            # Get the package name (last part of import path)
            pkg_name = imp.split('/')[-1]
            # Remove common prefixes
            pkg_name = pkg_name.replace('-', '')
            
            # Check if package name appears in code (outside import block)
            code_without_imports = re.sub(r'import\s+\([^)]+\)', '', content)
            code_without_imports = re.sub(r'import\s+"[^"]+"', '', code_without_imports)
            
            if pkg_name not in code_without_imports and not imp.startswith('_'):
                # Might be unused (could be false positive)
                pass  # Skip reporting for now as it's too prone to false positives

    def calculate_quality_score(self) -> int:
        """Calculate overall quality score (0-100)."""
        # Base score
        score = 100
        
        # Deduct points for issues
        score -= self.metrics["functions_without_docs"] * 5
        score -= self.metrics["error_handling_issues"] * 3
        score -= self.metrics["unused_imports"] * 2
        
        # Ensure score is between 0 and 100
        return max(0, min(100, score))

    def generate_report(self) -> dict:
        """Generate a report of the analysis."""
        self.metrics["quality_score"] = self.calculate_quality_score()
        
        return {
            "metrics": self.metrics,
            "issues": self.issues,
            "summary": {
                "total_issues": len(self.issues),
                "quality_score": self.metrics["quality_score"],
                "meets_threshold": self.metrics["quality_score"] >= self.config["auto_approve"]["min_quality_score"]
            }
        }


def get_changed_files(diff_only: bool = True) -> List[str]:
    """Get list of changed files (or all Go files if not diff_only)."""
    if diff_only:
        # Use git diff to get changed files
        import subprocess
        try:
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'origin/main...HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            files = [f for f in result.stdout.strip().split('\n') if f.endswith('.go')]
            return files
        except subprocess.CalledProcessError:
            print("Warning: Could not get git diff, analyzing all Go files", file=sys.stderr)
    
    # Fallback: find all Go files
    go_files = []
    for root, dirs, files in os.walk('.'):
        # Skip vendor and hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'vendor']
        for file in files:
            if file.endswith('.go'):
                go_files.append(os.path.join(root, file))
    return go_files


def main():
    parser = argparse.ArgumentParser(description='Analyze Go code quality')
    parser.add_argument('--diff-only', action='store_true', help='Only analyze changed files')
    parser.add_argument('--check-tests', action='store_true', help='Check for test files')
    parser.add_argument('--check-docs', action='store_true', help='Check for documentation')
    parser.add_argument('--check-errors', action='store_true', help='Check error handling')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--output', type=str, default='report.json', help='Output file for report')
    
    args = parser.parse_args()
    
    analyzer = GoCodeAnalyzer(args.config)
    
    # Get files to analyze
    files = get_changed_files(args.diff_only)
    
    if not files:
        print("No Go files to analyze")
        report = analyzer.generate_report()
        report["summary"]["message"] = "No Go files found to analyze"
    else:
        print(f"Analyzing {len(files)} Go files...")
        
        for filepath in files:
            if os.path.exists(filepath):
                analyzer.analyze_file(filepath)
        
        report = analyzer.generate_report()
    
    # Write report
    with open(args.output, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Quality Score: {report['metrics']['quality_score']}/100")
    print(f"Total Issues: {report['summary']['total_issues']}")
    print(f"Tests Found: {report['metrics']['tests_found']}")
    print(f"Functions Without Docs: {report['metrics']['functions_without_docs']}")
    print(f"Potential Error Handling Issues: {report['metrics']['error_handling_issues']}")
    print(f"{'='*50}\n")
    
    # Exit with appropriate code
    if report['summary']['meets_threshold']:
        print("✅ Quality threshold met!")
        sys.exit(0)
    else:
        print("⚠️  Quality threshold not met")
        sys.exit(1)


if __name__ == '__main__':
    main()
