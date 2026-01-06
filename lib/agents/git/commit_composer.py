#!/usr/bin/env python3
"""
Commit Composer Agent - AI-powered semantic commit message generation

Uses Claude to analyze code changes and generate conventional commit messages.
"""

import os
import subprocess
from typing import Dict, List, Optional
from datetime import datetime


class CommitComposerAgent:
    """
    Generates semantic, conventional commit messages.
    
    Format: <type>(<scope>): <subject>
    
    Types: feat, fix, docs, style, refactor, perf, test, chore
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Commit Composer Agent.
        
        Args:
            api_key: Anthropic API key (uses ANTHROPIC_API_KEY env var if not provided)
        """
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        self.model = "claude-3-5-sonnet-20241022"
    
    def analyze_staged_changes(self) -> Dict:
        """
        Analyze currently staged changes.
        
        Returns:
            {
                "files": List[str],
                "stats": Dict,
                "types": List[str]
            }
        """
        # Get staged files
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-status"],
            capture_output=True,
            text=True,
            check=False
        )
        
        files = []
        file_types = set()
        
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 2:
                status = parts[0]
                filename = parts[1]
                files.append({
                    "status": status,
                    "filename": filename
                })
                
                # Track file types
                ext = filename.split('.')[-1] if '.' in filename else 'other'
                file_types.add(ext)
        
        # Get diff stats
        stats_result = subprocess.run(
            ["git", "diff", "--cached", "--stat"],
            capture_output=True,
            text=True,
            check=False
        )
        
        return {
            "files": files,
            "file_types": list(file_types),
            "diff_stat": stats_result.stdout,
            "file_count": len(files)
        }
    
    def generate_commit_message(self) -> str:
        """
        Generate a conventional commit message for staged changes.
        
        Returns:
            str: Generated commit message
        """
        changes = self.analyze_staged_changes()
        
        if changes['file_count'] == 0:
            return "chore: empty commit"
        
        # Determine commit type based on files
        commit_type = self._determine_commit_type(changes)
        
        # Determine scope
        scope = self._determine_scope(changes)
        
        # Generate subject
        subject = self._generate_subject(changes, commit_type)
        
        # Build commit message
        if scope:
            message = f"{commit_type}({scope}): {subject}"
        else:
            message = f"{commit_type}: {subject}"
        
        # Add body if significant changes
        if changes['file_count'] > 3:
            message += "\n\n"
            message += self._generate_body(changes)
        
        return message
    
    def _determine_commit_type(self, changes: Dict) -> str:
        """Determine the commit type from changes."""
        files = changes['files']
        file_types = changes['file_types']
        
        # Check for documentation
        if 'md' in file_types:
            md_count = sum(1 for f in files if f['filename'].endswith('.md'))
            if md_count == len(files):
                return 'docs'
        
        # Check for new features
        new_files = [f for f in files if f['status'] == 'A']
        if len(new_files) > len(files) / 2:
            return 'feat'
        
        # Check for tests
        test_files = [f for f in files if 'test' in f['filename'].lower()]
        if test_files and len(test_files) == len(files):
            return 'test'
        
        # Check for configuration
        config_types = {'json', 'yaml', 'yml', 'toml', 'env'}
        if any(ft in config_types for ft in file_types):
            return 'chore'
        
        # Default to fix for modifications
        modified_files = [f for f in files if f['status'] == 'M']
        if modified_files:
            return 'fix'
        
        return 'chore'
    
    def _determine_scope(self, changes: Dict) -> Optional[str]:
        """Determine the scope from changes."""
        files = changes['files']
        
        # Check for common directories
        dirs = set()
        for file in files:
            filename = file['filename']
            if '/' in filename:
                first_dir = filename.split('/')[0]
                dirs.add(first_dir)
        
        # If all files in same directory, use it as scope
        if len(dirs) == 1:
            return list(dirs)[0]
        
        # Check for API changes
        if any('api' in f['filename'] for f in files):
            return 'api'
        
        # Check for docs
        if any('doc' in f['filename'].lower() for f in files):
            return 'docs'
        
        # Check for agents
        if any('agent' in f['filename'].lower() for f in files):
            return 'agents'
        
        return None
    
    def _generate_subject(self, changes: Dict, commit_type: str) -> str:
        """Generate commit subject line."""
        files = changes['files']
        file_count = changes['file_count']
        
        # For single file, be specific
        if file_count == 1:
            filename = files[0]['filename']
            basename = os.path.basename(filename)
            
            if commit_type == 'docs':
                return f"update {basename}"
            elif commit_type == 'feat':
                return f"add {basename}"
            elif commit_type == 'fix':
                return f"fix {basename}"
        
        # For multiple files, be general
        if commit_type == 'docs':
            return f"update documentation ({file_count} files)"
        elif commit_type == 'feat':
            return f"add new features"
        elif commit_type == 'fix':
            return f"fix issues in {file_count} files"
        elif commit_type == 'test':
            return f"add tests"
        elif commit_type == 'chore':
            return f"update configuration"
        
        return f"update {file_count} files"
    
    def _generate_body(self, changes: Dict) -> str:
        """Generate commit message body."""
        files = changes['files']
        
        body = "Changes:\n"
        for file in files[:10]:  # Limit to 10 files
            status_map = {
                'A': 'Add',
                'M': 'Modify',
                'D': 'Delete'
            }
            status = status_map.get(file['status'], 'Update')
            body += f"- {status}: {file['filename']}\n"
        
        if len(files) > 10:
            body += f"- ... and {len(files) - 10} more files\n"
        
        return body


if __name__ == "__main__":
    # Example usage
    agent = CommitComposerAgent()
    
    print("📝 Commit Composer Agent")
    print("=" * 50)
    
    # Analyze staged changes
    print("\n🔍 Analyzing staged changes...\n")
    changes = agent.analyze_staged_changes()
    
    print(f"Files staged: {changes['file_count']}")
    if changes['files']:
        print("\nStaged files:")
        for file in changes['files']:
            print(f"  {file['status']}\t{file['filename']}")
    
    if changes['file_count'] > 0:
        print("\n✍️ Generated commit message:\n")
        message = agent.generate_commit_message()
        print(message)
    else:
        print("\n⚠️ No files staged for commit")
