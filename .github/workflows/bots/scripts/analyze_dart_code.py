#!/usr/bin/env python3
"""
Frontend Dart/Flutter Code Analyzer.
Analyzes Dart code for naming conventions, hardcoded strings, theme usage.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict


class DartCodeAnalyzer:
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.issues = []
        self.metrics = {
            "files_analyzed": 0,
            "naming_violations": 0,
            "hardcoded_strings": 0,
            "theme_issues": 0,
            "quality_score": 0
        }

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {
            "naming_conventions": {
                "files": "snake_case",
                "classes": "PascalCase"
            },
            "ui_checks": {
                "check_hardcoded_strings": True,
                "check_theme_usage": True
            }
        }

    def analyze_file(self, filepath: str) -> None:
        """Analyze a single Dart file."""
        if not filepath.endswith('.dart'):
            return

        self.metrics["files_analyzed"] += 1

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # Check file naming convention
        self._check_file_naming(filepath)

        # Check for hardcoded strings
        if self.config["ui_checks"]["check_hardcoded_strings"]:
            self._check_hardcoded_strings(filepath, lines)

        # Check theme usage
        if self.config["ui_checks"]["check_theme_usage"]:
            self._check_theme_usage(filepath, content)

    def _check_file_naming(self, filepath: str) -> None:
        """Check if file follows snake_case naming convention."""
        filename = os.path.basename(filepath)
        name_without_ext = filename.replace('.dart', '')
        
        # Check if it's snake_case (lowercase with underscores)
        if not re.match(r'^[a-z][a-z0-9_]*$', name_without_ext):
            self.issues.append({
                "file": filepath,
                "line": 1,
                "type": "naming_convention",
                "message": f"File name '{filename}' should use snake_case convention"
            })
            self.metrics["naming_violations"] += 1

    def _check_hardcoded_strings(self, filepath: str, lines: List[str]) -> None:
        """Check for hardcoded UI strings that should be externalized."""
        # Skip test files
        if '_test.dart' in filepath or 'test/' in filepath:
            return

        # Patterns that might indicate UI strings
        ui_string_pattern = re.compile(r'''['"](.*?)['"]''')
        
        for i, line in enumerate(lines):
            # Skip comments
            if line.strip().startswith('//'):
                continue
            
            # Skip imports and certain declarations
            if 'import ' in line or 'const ' in line or 'final ' in line:
                continue
                
            # Look for string literals in UI contexts
            if any(keyword in line for keyword in ['Text(', 'Text.', 'label:', 'hint:', 'title:']):
                matches = ui_string_pattern.findall(line)
                for match in matches:
                    # Filter out likely non-UI strings
                    if len(match) > 3 and not match.startswith('http') and not match.startswith('/'):
                        self.issues.append({
                            "file": filepath,
                            "line": i + 1,
                            "type": "hardcoded_string",
                            "message": f"Hardcoded UI string detected: '{match[:30]}...' - consider externalizing"
                        })
                        self.metrics["hardcoded_strings"] += 1
                        break  # Only report once per line

    def _check_theme_usage(self, filepath: str, content: str) -> None:
        """Check if colors use theme constants instead of hardcoded values."""
        # Skip test files
        if '_test.dart' in filepath or 'test/' in filepath:
            return

        # Look for hardcoded color values
        color_pattern = re.compile(r'Color\(0x[0-9A-Fa-f]{8}\)|Colors\.\w+')
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'Color(0x' in line or 'Color.fromRGBO' in line:
                # Check if Theme.of(context) is used nearby
                context_start = max(0, i - 5)
                context_end = min(len(lines), i + 5)
                nearby_lines = '\n'.join(lines[context_start:context_end])
                
                if 'Theme.of(context)' not in nearby_lines and 'theme.' not in line.lower():
                    self.issues.append({
                        "file": filepath,
                        "line": i + 1,
                        "type": "theme_usage",
                        "message": "Hardcoded color detected - consider using Theme.of(context)"
                    })
                    self.metrics["theme_issues"] += 1

    def calculate_quality_score(self) -> int:
        """Calculate overall quality score (0-100)."""
        score = 100
        
        # Deduct points for issues
        score -= self.metrics["naming_violations"] * 10
        score -= self.metrics["hardcoded_strings"] * 3
        score -= self.metrics["theme_issues"] * 5
        
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
                "files_analyzed": self.metrics["files_analyzed"]
            }
        }


def get_changed_files(diff_only: bool = True) -> List[str]:
    """Get list of changed Dart files."""
    if diff_only:
        import subprocess
        try:
            # Try to detect the base branch dynamically
            base_branch = 'origin/main'
            try:
                result = subprocess.run(
                    ['git', 'symbolic-ref', 'refs/remotes/origin/HEAD'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                base_branch = result.stdout.strip().replace('refs/remotes/', '')
            except subprocess.CalledProcessError:
                pass  # Use default origin/main
            
            result = subprocess.run(
                ['git', 'diff', '--name-only', f'{base_branch}...HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            files = [f for f in result.stdout.strip().split('\n') if f.endswith('.dart')]
            return files
        except subprocess.CalledProcessError:
            print("Warning: Could not get git diff, analyzing all Dart files", file=sys.stderr)
    
    # Fallback: find all Dart files
    dart_files = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.dart'):
                dart_files.append(os.path.join(root, file))
    return dart_files


def main():
    parser = argparse.ArgumentParser(description='Analyze Dart/Flutter code quality')
    parser.add_argument('--check-naming', action='store_true', help='Check naming conventions')
    parser.add_argument('--check-hardcoded-strings', action='store_true', help='Check for hardcoded strings')
    parser.add_argument('--check-theme-usage', action='store_true', help='Check theme usage')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--output', type=str, default='dart-report.json', help='Output file')
    
    args = parser.parse_args()
    
    analyzer = DartCodeAnalyzer(args.config)
    
    files = get_changed_files(diff_only=True)
    
    if not files:
        print("No Dart files to analyze")
        report = analyzer.generate_report()
        report["summary"]["message"] = "No Dart files found to analyze"
    else:
        print(f"Analyzing {len(files)} Dart files...")
        
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
    print(f"Files Analyzed: {report['metrics']['files_analyzed']}")
    print(f"Naming Violations: {report['metrics']['naming_violations']}")
    print(f"Hardcoded Strings: {report['metrics']['hardcoded_strings']}")
    print(f"Theme Issues: {report['metrics']['theme_issues']}")
    print(f"{'='*50}\n")
    
    sys.exit(0)


if __name__ == '__main__':
    main()
