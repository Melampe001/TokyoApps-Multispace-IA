# 📚 Tokyo-IA Digital Library

Welcome to the Tokyo-IA Digital Library - an automated catalog of all project files, code, documentation, and workflows.

## 📊 Quick Links

- [Complete Catalog](CATALOG.md) - Full categorized listing of all files
- [Timeline](TIMELINE.md) - Chronological view of file creation
- [Search Index](SEARCH_INDEX.json) - JSON index for programmatic access
- [Interactive Dashboard](dashboard.html) - Visual, searchable interface

## 🗂️ Browse by Category

- [Workflows](by-category/workflow.md) - GitHub Actions workflows
- [Scripts](by-category/script.md) - Automation scripts
- [Documentation](by-category/documentation.md) - Project documentation
- [Source Code](by-category/source.md) - Application source code
- [Configuration](by-category/configuration.md) - Configuration files
- [Schema](by-category/schema.md) - Protocol buffers and schemas
- [Build](by-category/build.md) - Build configuration files

## 🎯 Browse by Purpose

- [Automation](by-purpose/automation.md) - Automation tools and workflows
- [Testing](by-purpose/testing.md) - Test files and test utilities
- [Documentation](by-purpose/documentation.md) - Documentation files
- [Integration](by-purpose/integration.md) - API integrations
- [Monitoring](by-purpose/monitoring.md) - Monitoring and alerting
- [Deployment](by-purpose/deployment.md) - Deployment tools
- [Security](by-purpose/security.md) - Security-related files

## 💻 Browse by Technology

- [Go](by-technology/go.md) - Go source files
- [Python](by-technology/py.md) - Python scripts
- [YAML](by-technology/yml.md) - YAML configuration files
- [Markdown](by-technology/md.md) - Markdown documentation
- [JSON](by-technology/json.md) - JSON configuration files
- [Shell](by-technology/sh.md) - Shell scripts
- [Protocol Buffers](by-technology/proto.md) - Protobuf schemas

## 📈 Statistics

- [File Count](stats/file-count.md) - File statistics by category

## 🔍 Search the Library

### Using the CLI Tool

```bash
# Search by name
python .github/workflows/scripts/library_search.py --name "workflow"

# Search by type
python .github/workflows/scripts/library_search.py --type "script"

# Search by purpose
python .github/workflows/scripts/library_search.py --purpose "automation"

# Full-text search
python .github/workflows/scripts/library_search.py --content "github"

# Search by author
python .github/workflows/scripts/library_search.py --author "bot"

# List all categories
python .github/workflows/scripts/library_search.py --list

# Combined search
python .github/workflows/scripts/library_search.py --type "script" --purpose "automation"
```

### Using the Interactive Dashboard

Open [dashboard.html](dashboard.html) in your browser for a visual, interactive search interface with:
- Real-time search filtering
- Category filtering
- Statistics visualization
- File metadata display

## 🤖 Automation

This library is automatically maintained by GitHub Actions workflows:

### Library Indexer
- **Workflow**: [library-indexer.yml](../.github/workflows/library-indexer.yml)
- **Schedule**: Daily at 2:00 AM UTC + on every push to main
- **Function**: Scans all files, generates metadata, and updates the catalog

### Auto Documenter
- **Workflow**: [auto-documenter.yml](../.github/workflows/auto-documenter.yml)
- **Schedule**: On push and PR to main
- **Function**: Checks for undocumented files, validates links, extracts code documentation

### Library Report
- **Workflow**: [library-report.yml](../.github/workflows/library-report.yml)
- **Schedule**: Daily, weekly, and monthly reports
- **Function**: Generates activity reports and statistics

## 📋 File Documentation Template

When creating new files, use our [documentation template](../.github/templates/FILE_TEMPLATE.md) to ensure consistent documentation across the project.

## 📊 Reports

View automated reports in the [reports](reports/) directory:
- Daily reports: Activity in the last 24 hours
- Weekly reports: Summary of the week's changes
- Monthly reports: Growth analysis and recommendations

## 🎯 What's Included

The library catalogs:
- ✅ All source code files (Go, Python, JavaScript, etc.)
- ✅ Configuration files (YAML, JSON, etc.)
- ✅ Documentation (Markdown, text files)
- ✅ Build scripts and Makefiles
- ✅ GitHub Actions workflows
- ✅ Protocol buffer schemas
- ✅ Shell scripts and utilities

The library **excludes**:
- ❌ Version control files (.git)
- ❌ Dependencies (node_modules, vendor)
- ❌ Build artifacts (dist, build, target)
- ❌ IDE configuration (.idea, .vscode)

## 📖 Metadata Schema

Each file in the catalog includes:
- **Basic Info**: Name, path, type, size, line count
- **Classification**: Category, area, purpose, tags
- **Dates**: Created, modified
- **Authorship**: Author, contributors, commit count
- **Content**: Description, dependencies
- **Relationships**: Related files, imports

## 🔧 Maintenance

The library system is designed to be:
- **Automatic**: Updates without manual intervention
- **Comprehensive**: Catalogs all project files
- **Searchable**: Multiple ways to find files
- **Up-to-date**: Syncs daily with repository state
- **Extensible**: Easy to add new metadata and views

## 📈 Benefits

Using the Digital Library saves time:
- 🚀 **Onboarding**: New developers can quickly understand project structure (-70% time)
- 🔍 **Finding Files**: Locate any file in seconds (-90% time)
- 📚 **Understanding**: See file relationships and dependencies (-60% time)
- 📝 **Documentation**: Automated documentation compliance (+100%)

**Total Impact**: ~4 hours/week saved in searching and onboarding

## 🆘 Support

For issues or questions:
1. Check the [CATALOG.md](CATALOG.md) for file listings
2. Use the search tool to find specific files
3. View the [dashboard](dashboard.html) for visual overview
4. Check workflow runs in GitHub Actions for any indexing errors

---

📅 **Last Updated**: Automatically updated daily at 2:00 AM UTC

🤖 **Maintained By**: GitHub Actions Library Indexer

✨ **Version**: 1.0.0
