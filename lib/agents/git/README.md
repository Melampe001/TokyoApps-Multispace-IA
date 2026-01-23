# Git Automation Agents - Usage Guide

## 🤖 Active Agents

Tokyo-IA now includes **working Git automation agents** that you can use right now!

### Available Agents

1. **Pull Analyzer Agent** 🔍
   - Analyzes PR changes and statistics
   - Provides file type breakdown
   - Generates recommendations
   - Uses: GPT-4 Turbo

2. **Commit Composer Agent** 📝
   - Generates conventional commit messages
   - Analyzes staged changes
   - Determines commit type and scope automatically
   - Uses: Claude 3.5 Sonnet

## 🚀 Quick Start

### Using the CLI

```bash
# Analyze the current pull request
python scripts/git_agent_cli.py analyze-pr

# Generate a commit message for staged changes
git add <files>
python scripts/git_agent_cli.py generate-commit
```

### Example Output

#### PR Analysis
```
🔍 Pull Request Analysis

Analysis Timestamp: 2025-12-29T17:33:03Z

📊 Statistics
- Files Changed: 4
- Additions: +234 lines
- Deletions: -12 lines

📁 Changes by File Type
- Python: 3 file(s)
- Markdown: 1 file(s)

📝 Changes by Status
- Added: 4 file(s)
- Modified: 0 file(s)
- Deleted: 0 file(s)

✨ Highlights
- Significant new code added
- Documentation updated (1 files)

💡 Recommendations
- ✅ Small PR: Good size for quick review
- 🧪 Ensure tests are added for new Python code
```

#### Commit Message Generation
```
📝 Commit Message Generator

📁 Staged files: 4
  ➕ lib/agents/git/__init__.py
  ➕ lib/agents/git/commit_composer.py
  ➕ lib/agents/git/pull_analyzer.py
  ➕ scripts/git_agent_cli.py

✨ Generated commit message:
feat(agents): add Git automation agents implementation

Changes:
- Add: lib/agents/git/__init__.py
- Add: lib/agents/git/commit_composer.py
- Add: lib/agents/git/pull_analyzer.py
- Add: scripts/git_agent_cli.py
```

## 📋 Usage in Python

### Pull Analyzer Agent

```python
from lib.agents.git import PullAnalyzerAgent

# Initialize agent
analyzer = PullAnalyzerAgent()

# Analyze current PR
analysis = analyzer.analyze_current_pr()
print(f"Files changed: {analysis['files_changed']}")
print(f"Additions: +{analysis['additions']}")
print(f"Deletions: -{analysis['deletions']}")

# Generate PR summary
summary = analyzer.generate_pr_summary()
print(summary)
```

### Commit Composer Agent

```python
from lib.agents.git import CommitComposerAgent

# Initialize agent
composer = CommitComposerAgent()

# Analyze staged changes
changes = composer.analyze_staged_changes()
print(f"Files staged: {changes['file_count']}")

# Generate commit message
message = composer.generate_commit_message()
print(f"Suggested message: {message}")
```

## 🔧 Configuration

### Environment Variables

```bash
# For Pull Analyzer (optional - uses GPT-4 Turbo)
export OPENAI_API_KEY=your_openai_key

# For Commit Composer (optional - uses Claude 3.5 Sonnet)
export ANTHROPIC_API_KEY=your_anthropic_key
```

**Note:** The agents work without API keys but provide basic analysis. With API keys, they can provide AI-enhanced insights.

## 🎯 Features

### Pull Analyzer Features
- ✅ Automatic file change analysis
- ✅ Statistics calculation (additions, deletions, files changed)
- ✅ File type categorization
- ✅ Smart recommendations based on PR size
- ✅ Documentation completeness check
- ✅ Test coverage suggestions

### Commit Composer Features
- ✅ Conventional commit format (type, scope, subject)
- ✅ Automatic commit type detection
- ✅ Smart scope inference
- ✅ Context-aware subject generation
- ✅ Detailed commit body for large changes
- ✅ Support for all file types

## 📝 Commit Types

The Commit Composer automatically detects and uses these types:

- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions/modifications
- `chore`: Configuration and maintenance

## 🎓 Best Practices

1. **Use for every PR**: Run `analyze-pr` before submitting
2. **Stage incrementally**: Stage related files together for better commit messages
3. **Review suggestions**: Always review generated messages before committing
4. **Keep PRs focused**: Follow size recommendations from analyzer

## 🔮 Future Enhancements

- [ ] Merge conflict resolution (Merge Master agent)
- [ ] Automated dependency updates (Pull Guardian agent)
- [ ] Comprehensive PR review (Review Sentinel agent)
- [ ] AI-powered conflict resolution strategies
- [ ] Integration with GitHub API for automated PR comments

## 📚 Documentation

For complete documentation, see:
- [GIT_AUTOMATION_AGENTS.md](../GIT_AUTOMATION_AGENTS.md) - Full agent specifications
- [IMPERIAL_ELITE_ORCHESTRATION.md](../IMPERIAL_ELITE_ORCHESTRATION.md) - Advanced orchestration patterns

## 🆘 Troubleshooting

### "No files staged for commit"
```bash
# Stage files first
git add <files>

# Then generate commit message
python scripts/git_agent_cli.py generate-commit
```

### "Files Changed: 0" in PR analysis
```bash
# Ensure you're comparing against the correct branch
git fetch origin main

# Check your current branch
git branch

# View actual diff
git diff origin/main...HEAD
```

## 🤝 Contributing

To add new Git agents:

1. Create a new agent file in `lib/agents/git/`
2. Implement the agent class with clear documentation
3. Add to `lib/agents/git/__init__.py`
4. Update CLI in `scripts/git_agent_cli.py`
5. Add tests in `lib/agents/git/test_*.py`

---

**Status:** ✅ Active and Production Ready

*Last Updated: December 29, 2025*
*Version: 1.0.0*
