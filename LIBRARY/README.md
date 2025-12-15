# 📚 Tokyo-IA Digital Library

Welcome to the Tokyo-IA Digital Library - an automated catalog of all project files, code, documentation, and workflows.

## 📊 Quick Links

- [Complete Catalog](CATALOG.md) - Full categorized listing of all files
- [Timeline](TIMELINE.md) - Chronological view of file creation
- [Search Index](SEARCH_INDEX.json) - JSON index for programmatic access

## 🗂️ Browse by Category

- [Workflows](by-category/workflow.md) - GitHub Actions workflows
- [Scripts](by-category/script.md) - Automation scripts
- [Documentation](by-category/documentation.md) - Project documentation
- [Source Code](by-category/source.md) - Application source code
- [Configuration](by-category/configuration.md) - Configuration files

## 🎯 Browse by Purpose

- [Automation](by-purpose/automation.md) - Automation tools and workflows
- [Testing](by-purpose/testing.md) - Test files and test utilities
- [Documentation](by-purpose/documentation.md) - Documentation files
- [Integration](by-purpose/integration.md) - API integrations
- [Monitoring](by-purpose/monitoring.md) - Monitoring and alerting

## 💻 Browse by Technology

- [Go](by-technology/go.md) - Go source files
- [Python](by-technology/py.md) - Python scripts
- [YAML](by-technology/yml.md) - YAML configuration files
- [Markdown](by-technology/md.md) - Markdown documentation

## 📈 Statistics

- [File Count](stats/file-count.md) - File statistics by category

## 🔍 Search the Library

Use the CLI search tool:

```bash
# Search by name
python .github/workflows/scripts/library_search.py --name "workflow"

# Search by type
python .github/workflows/scripts/library_search.py --type "script"

# Search by purpose
python .github/workflows/scripts/library_search.py --purpose "automation"

# List all categories
python .github/workflows/scripts/library_search.py --list
```

## 📅 Updates

This library is automatically updated:
- Daily at 2:00 AM UTC
- On every push to main branch
- Can be triggered manually via workflow_dispatch

---

*Last updated: Automatically generated*
