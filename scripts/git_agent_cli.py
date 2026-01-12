#!/usr/bin/env python3
"""
Tokyo-IA Git Agent CLI

Command-line interface for Git automation agents.

Usage:
    python scripts/git_agent_cli.py analyze-pr
    python scripts/git_agent_cli.py generate-commit
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.agents.git import PullAnalyzerAgent, CommitComposerAgent


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "analyze-pr":
        analyze_pr()
    elif command == "generate-commit":
        generate_commit()
    elif command == "help":
        print_usage()
    else:
        print(f"❌ Unknown command: {command}")
        print_usage()
        sys.exit(1)


def print_usage():
    """Print usage information."""
    print("""
🤖 Tokyo-IA Git Agent CLI
==========================

Commands:
  analyze-pr         Analyze the current pull request
  generate-commit    Generate a commit message for staged changes
  help               Show this help message

Examples:
  python scripts/git_agent_cli.py analyze-pr
  python scripts/git_agent_cli.py generate-commit

Environment Variables:
  OPENAI_API_KEY     Required for PR analysis
  ANTHROPIC_API_KEY  Required for commit generation
""")


def analyze_pr():
    """Analyze current PR."""
    print("\n🔍 Pull Request Analyzer")
    print("=" * 60)
    
    try:
        agent = PullAnalyzerAgent()
        summary = agent.generate_pr_summary()
        print(summary)
    except Exception as e:
        print(f"\n❌ Error analyzing PR: {e}")
        sys.exit(1)


def generate_commit():
    """Generate commit message."""
    print("\n📝 Commit Message Generator")
    print("=" * 60)
    
    try:
        agent = CommitComposerAgent()
        
        # Analyze staged changes
        changes = agent.analyze_staged_changes()
        
        if changes['file_count'] == 0:
            print("\n⚠️  No files staged for commit")
            print("Tip: Use 'git add <files>' to stage changes")
            sys.exit(0)
        
        print(f"\n📁 Staged files: {changes['file_count']}")
        for file in changes['files']:
            status_icon = {
                'A': '➕',
                'M': '✏️',
                'D': '➖'
            }.get(file['status'], '📄')
            print(f"  {status_icon} {file['filename']}")
        
        # Generate message
        print("\n✨ Generated commit message:\n")
        message = agent.generate_commit_message()
        print("-" * 60)
        print(message)
        print("-" * 60)
        
        # Ask to commit
        print("\n💡 To commit with this message, run:")
        print(f'   git commit -m "{message.split(chr(10))[0]}"')
        
    except Exception as e:
        print(f"\n❌ Error generating commit: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
