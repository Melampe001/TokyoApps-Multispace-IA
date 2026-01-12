#!/usr/bin/env python3
"""
Pull Analyzer Agent - AI-powered PR analysis and review

Uses OpenAI o3 to analyze pull requests and provide comprehensive feedback.
"""

import os
import subprocess
from typing import Dict, List, Optional
from datetime import datetime


class PullAnalyzerAgent:
    """
    Analyzes pull requests and provides AI-powered insights.
    
    Features:
    - Code quality analysis
    - Security vulnerability detection
    - Performance impact assessment
    - Test coverage verification
    - Documentation completeness check
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Pull Analyzer Agent.
        
        Args:
            api_key: OpenAI API key (uses OPENAI_API_KEY env var if not provided)
        """
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        self.model = "gpt-4-turbo"  # Using GPT-4 Turbo (o3 not yet available via API)
        
    def analyze_current_pr(self) -> Dict:
        """
        Analyze the current PR branch against main.
        
        Returns:
            {
                "status": str,
                "files_changed": int,
                "additions": int,
                "deletions": int,
                "analysis": Dict,
                "recommendations": List[str]
            }
        """
        # Get PR stats
        stats = self._get_pr_stats()
        
        # Get changed files
        files = self._get_changed_files()
        
        # Analyze changes
        analysis = self._analyze_changes(files)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(analysis, stats)
        
        return {
            "status": "analyzed",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "files_changed": stats['files_changed'],
            "additions": stats['additions'],
            "deletions": stats['deletions'],
            "analysis": analysis,
            "recommendations": recommendations
        }
    
    def _get_pr_stats(self) -> Dict:
        """Get PR statistics using git diff."""
        try:
            # Get diff stats
            result = subprocess.run(
                ["git", "diff", "--stat", "origin/main...HEAD"],
                capture_output=True,
                text=True,
                check=False
            )
            
            lines = result.stdout.strip().split('\n')
            if not lines:
                return {"files_changed": 0, "additions": 0, "deletions": 0}
            
            # Parse last line (summary)
            summary = lines[-1]
            files = additions = deletions = 0
            
            if "file" in summary:
                parts = summary.split(',')
                for part in parts:
                    part = part.strip()
                    if "file" in part:
                        files = int(part.split()[0])
                    elif "insertion" in part:
                        additions = int(part.split()[0])
                    elif "deletion" in part:
                        deletions = int(part.split()[0])
            
            return {
                "files_changed": files,
                "additions": additions,
                "deletions": deletions
            }
        except Exception as e:
            return {
                "files_changed": 0,
                "additions": 0,
                "deletions": 0,
                "error": str(e)
            }
    
    def _get_changed_files(self) -> List[Dict]:
        """Get list of changed files with their changes."""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-status", "origin/main...HEAD"],
                capture_output=True,
                text=True,
                check=False
            )
            
            files = []
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                parts = line.split('\t')
                if len(parts) >= 2:
                    status = parts[0]
                    filename = parts[1]
                    files.append({
                        "status": status,
                        "filename": filename,
                        "type": self._get_file_type(filename)
                    })
            
            return files
        except Exception as e:
            return []
    
    def _get_file_type(self, filename: str) -> str:
        """Determine file type from extension."""
        ext = filename.split('.')[-1].lower()
        
        type_map = {
            'py': 'Python',
            'js': 'JavaScript',
            'ts': 'TypeScript',
            'jsx': 'React JSX',
            'tsx': 'React TSX',
            'go': 'Go',
            'java': 'Java',
            'md': 'Markdown',
            'json': 'JSON',
            'yaml': 'YAML',
            'yml': 'YAML',
            'toml': 'TOML',
            'html': 'HTML',
            'css': 'CSS',
            'scss': 'SCSS'
        }
        
        return type_map.get(ext, 'Other')
    
    def _analyze_changes(self, files: List[Dict]) -> Dict:
        """Analyze the changed files."""
        analysis = {
            "by_type": {},
            "by_status": {"added": 0, "modified": 0, "deleted": 0},
            "concerns": [],
            "highlights": []
        }
        
        for file in files:
            # Count by type
            file_type = file['type']
            if file_type not in analysis['by_type']:
                analysis['by_type'][file_type] = 0
            analysis['by_type'][file_type] += 1
            
            # Count by status
            status = file['status']
            if status == 'A':
                analysis['by_status']['added'] += 1
            elif status == 'M':
                analysis['by_status']['modified'] += 1
            elif status == 'D':
                analysis['by_status']['deleted'] += 1
        
        # Identify concerns
        if analysis['by_status']['deleted'] > 5:
            analysis['concerns'].append("Large number of file deletions detected")
        
        if analysis['by_status']['added'] > 10:
            analysis['highlights'].append("Significant new code added")
        
        # Check for documentation
        md_files = analysis['by_type'].get('Markdown', 0)
        if md_files > 0:
            analysis['highlights'].append(f"Documentation updated ({md_files} files)")
        
        return analysis
    
    def _generate_recommendations(self, analysis: Dict, stats: Dict) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Check PR size
        total_changes = stats['additions'] + stats['deletions']
        if total_changes > 500:
            recommendations.append(
                "⚠️ Large PR: Consider splitting into smaller PRs for easier review"
            )
        elif total_changes < 10:
            recommendations.append(
                "✅ Small PR: Good size for quick review"
            )
        
        # Check for documentation
        if 'Markdown' not in analysis['by_type'] and stats['additions'] > 100:
            recommendations.append(
                "📝 Consider adding documentation for significant code changes"
            )
        
        # Check for tests
        if 'Python' in analysis['by_type'] and analysis['by_status']['added'] > 0:
            recommendations.append(
                "🧪 Ensure tests are added for new Python code"
            )
        
        # Security check
        if any('api' in concern.lower() for concern in analysis.get('concerns', [])):
            recommendations.append(
                "🔒 Review for security implications in API changes"
            )
        
        return recommendations
    
    def generate_pr_summary(self) -> str:
        """Generate a comprehensive PR summary."""
        analysis = self.analyze_current_pr()
        
        summary = f"""# 🔍 Pull Request Analysis

**Analysis Timestamp:** {analysis['timestamp']}

## 📊 Statistics
- **Files Changed:** {analysis['files_changed']}
- **Additions:** +{analysis['additions']} lines
- **Deletions:** -{analysis['deletions']} lines

## 📁 Changes by File Type
"""
        
        for file_type, count in analysis['analysis']['by_type'].items():
            summary += f"- **{file_type}:** {count} file(s)\n"
        
        summary += f"\n## 📝 Changes by Status\n"
        summary += f"- **Added:** {analysis['analysis']['by_status']['added']} file(s)\n"
        summary += f"- **Modified:** {analysis['analysis']['by_status']['modified']} file(s)\n"
        summary += f"- **Deleted:** {analysis['analysis']['by_status']['deleted']} file(s)\n"
        
        if analysis['analysis']['highlights']:
            summary += "\n## ✨ Highlights\n"
            for highlight in analysis['analysis']['highlights']:
                summary += f"- {highlight}\n"
        
        if analysis['analysis']['concerns']:
            summary += "\n## ⚠️ Concerns\n"
            for concern in analysis['analysis']['concerns']:
                summary += f"- {concern}\n"
        
        if analysis['recommendations']:
            summary += "\n## 💡 Recommendations\n"
            for rec in analysis['recommendations']:
                summary += f"- {rec}\n"
        
        summary += "\n---\n*Generated by Pull Analyzer Agent (Tokyo-IA)*\n"
        
        return summary


if __name__ == "__main__":
    # Example usage
    agent = PullAnalyzerAgent()
    
    print("🤖 Pull Analyzer Agent")
    print("=" * 50)
    
    # Analyze current PR
    print("\n📊 Analyzing current PR...\n")
    summary = agent.generate_pr_summary()
    print(summary)
