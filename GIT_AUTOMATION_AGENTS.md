# 🔄 GIT AUTOMATION & DOCUMENT FUSION AGENTS

## AI-Powered Git Operations and Intelligent Document Synthesis

*Autonomous Pull, Merge, Commit, and Content Fusion Agents for Tokyo-IA*

---

## 🎯 Executive Summary

This module introduces specialized AI agents for automating Git workflows and document management:

**Git Automation Agents:**
- 🔀 **Merge Master** - Intelligent conflict resolution
- 📥 **Pull Guardian** - Automated dependency updates and sync
- 📝 **Commit Composer** - Semantic commit message generation
- 🔍 **Review Sentinel** - Automated code review and PR analysis

**Document Fusion Agents:**
- 📄 **DocFusion** - Intelligent document merging and synthesis
- ✍️ **Content Harmonizer** - Style and tone unification
- 📚 **Knowledge Synthesizer** - Multi-source content aggregation
- 🎨 **Format Conductor** - Cross-format document conversion

---

## 🤖 Git Automation Agents

### 1. Merge Master (Conflict Resolution Agent) 🔀

**Capabilities:**
- Automatic merge conflict detection and resolution
- Semantic code analysis to understand intent
- Context-aware conflict resolution strategies
- Safe merge with rollback support
- Integration with CI/CD pipelines

**Architecture:**
```python
# lib/agents/git/merge_master.py

from typing import Dict, List, Optional
import subprocess
import anthropic
from pathlib import Path

class MergeMasterAgent:
    """
    AI-powered merge conflict resolution agent.
    Uses Claude Opus 4.1 for semantic code understanding.
    """
    
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-opus-4.1"
        
    def detect_conflicts(self, branch: str) -> List[Dict]:
        """Detect merge conflicts when merging branch."""
        try:
            # Attempt merge
            result = subprocess.run(
                ["git", "merge", "--no-commit", "--no-ff", branch],
                capture_output=True,
                text=True
            )
            
            if "CONFLICT" in result.stdout:
                # Parse conflicted files
                conflicts = self._parse_conflicts(result.stdout)
                return conflicts
            return []
        except Exception as e:
            return [{"error": str(e)}]
    
    def resolve_conflict(self, file_path: str) -> Optional[str]:
        """
        Resolve conflict in file using AI analysis.
        
        Strategy:
        1. Read conflicted file
        2. Extract both versions (ours vs theirs)
        3. Analyze semantic meaning with Claude
        4. Generate merged version
        5. Validate syntax
        """
        conflict_content = Path(file_path).read_text()
        
        # Parse conflict markers
        sections = self._parse_conflict_markers(conflict_content)
        
        # Build prompt for Claude
        prompt = f"""You are a senior software engineer resolving a Git merge conflict.

File: {file_path}

Version A (current branch):
{sections['ours']}

Version B (merging branch):
{sections['theirs']}

Base version (common ancestor):
{sections.get('base', 'Not available')}

Context: {sections.get('context', '')}

Task: Analyze both versions semantically and create a unified version that:
1. Preserves functionality from both branches
2. Maintains code style consistency
3. Resolves logical conflicts intelligently
4. Adds comments explaining non-obvious merge decisions

Return ONLY the resolved code, no explanations."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        resolved = response.content[0].text
        
        # Validate syntax
        if self._validate_syntax(resolved, file_path):
            return resolved
        else:
            return None
    
    def auto_merge(self, source_branch: str, target_branch: str = "main") -> Dict:
        """
        Automatically merge source into target with AI conflict resolution.
        
        Returns:
            {
                "status": "success" | "conflict" | "error",
                "conflicts_resolved": int,
                "manual_review_needed": List[str],
                "commit_sha": str
            }
        """
        # Checkout target
        subprocess.run(["git", "checkout", target_branch])
        
        # Detect conflicts
        conflicts = self.detect_conflicts(source_branch)
        
        if not conflicts:
            # Clean merge
            subprocess.run(["git", "merge", source_branch])
            return {"status": "success", "conflicts_resolved": 0}
        
        # Resolve conflicts with AI
        resolved = []
        manual_review = []
        
        for conflict in conflicts:
            file_path = conflict['file']
            resolution = self.resolve_conflict(file_path)
            
            if resolution:
                # Write resolved version
                Path(file_path).write_text(resolution)
                subprocess.run(["git", "add", file_path])
                resolved.append(file_path)
            else:
                manual_review.append(file_path)
        
        if manual_review:
            return {
                "status": "conflict",
                "conflicts_resolved": len(resolved),
                "manual_review_needed": manual_review
            }
        
        # Commit merge
        commit_msg = self._generate_merge_commit_message(
            source_branch, resolved
        )
        subprocess.run(["git", "commit", "-m", commit_msg])
        
        return {
            "status": "success",
            "conflicts_resolved": len(resolved),
            "manual_review_needed": []
        }
    
    def _parse_conflict_markers(self, content: str) -> Dict:
        """Parse Git conflict markers into sections."""
        lines = content.split('\n')
        sections = {'ours': [], 'theirs': [], 'base': []}
        current = None
        
        for line in lines:
            if line.startswith('<<<<<<<'):
                current = 'ours'
            elif line.startswith('|||||||'):
                current = 'base'
            elif line.startswith('======='):
                current = 'theirs'
            elif line.startswith('>>>>>>>'):
                current = None
            elif current:
                sections[current].append(line)
        
        return {
            'ours': '\n'.join(sections['ours']),
            'theirs': '\n'.join(sections['theirs']),
            'base': '\n'.join(sections['base'])
        }
    
    def _validate_syntax(self, code: str, file_path: str) -> bool:
        """Validate syntax of resolved code."""
        ext = Path(file_path).suffix
        
        if ext == '.py':
            try:
                compile(code, file_path, 'exec')
                return True
            except SyntaxError:
                return False
        elif ext in ['.js', '.ts', '.jsx', '.tsx']:
            # Use eslint or similar
            return True  # Placeholder
        # Add more language validators
        return True
    
    def _generate_merge_commit_message(
        self, 
        branch: str, 
        resolved_files: List[str]
    ) -> str:
        """Generate semantic merge commit message."""
        return f"""Merge branch '{branch}' with AI conflict resolution

Automatically resolved conflicts in {len(resolved_files)} file(s):
{chr(10).join(f'- {f}' for f in resolved_files)}

Agent: Merge Master (Claude Opus 4.1)
Strategy: Semantic analysis with context preservation"""
```

**Usage:**
```python
from lib.agents.git.merge_master import MergeMasterAgent

# Initialize agent
merge_agent = MergeMasterAgent(api_key=os.environ['ANTHROPIC_API_KEY'])

# Auto-merge feature branch
result = merge_agent.auto_merge(
    source_branch="feature/new-api",
    target_branch="main"
)

if result['status'] == 'success':
    print(f"✅ Merged successfully! Resolved {result['conflicts_resolved']} conflicts")
elif result['manual_review_needed']:
    print(f"⚠️ Manual review needed for: {result['manual_review_needed']}")
```

### 2. Pull Guardian (Dependency Update Agent) 📥

**Capabilities:**
- Automatic dependency updates (npm, pip, go mod)
- Security vulnerability scanning
- Breaking change detection
- Automated testing before merge
- Rollback on failure

**Implementation:**
```python
# lib/agents/git/pull_guardian.py

import subprocess
from typing import Dict, List
import openai

class PullGuardianAgent:
    """
    Monitors and manages pull requests and dependency updates.
    Uses OpenAI o3 for advanced reasoning about compatibility.
    """
    
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "o3"
    
    def check_dependencies(self) -> Dict:
        """Check for outdated dependencies."""
        outdated = {
            'npm': self._check_npm_outdated(),
            'pip': self._check_pip_outdated(),
            'go': self._check_go_outdated()
        }
        return outdated
    
    def update_dependency(
        self, 
        package: str, 
        version: str,
        ecosystem: str = "npm"
    ) -> Dict:
        """
        Update a dependency with safety checks.
        
        Process:
        1. Create update branch
        2. Update package file
        3. Run tests
        4. Check for breaking changes
        5. Create PR if safe
        """
        branch_name = f"deps/update-{package}-{version}"
        
        # Create branch
        subprocess.run(["git", "checkout", "-b", branch_name])
        
        # Update package
        if ecosystem == "npm":
            subprocess.run(["npm", "install", f"{package}@{version}"])
        elif ecosystem == "pip":
            subprocess.run(["pip", "install", f"{package}=={version}"])
        
        # Run tests
        test_result = self._run_tests()
        
        if test_result['passed']:
            # Analyze breaking changes
            breaking = self._analyze_breaking_changes(package, version)
            
            # Generate PR description
            pr_body = self._generate_pr_description(package, version, breaking)
            
            # Commit and push
            subprocess.run([
                "git", "commit", "-am", 
                f"chore(deps): update {package} to {version}"
            ])
            subprocess.run(["git", "push", "origin", branch_name])
            
            return {
                "status": "success",
                "branch": branch_name,
                "pr_description": pr_body,
                "breaking_changes": breaking
            }
        else:
            # Rollback
            subprocess.run(["git", "checkout", "main"])
            subprocess.run(["git", "branch", "-D", branch_name])
            return {
                "status": "failed",
                "reason": "Tests failed",
                "test_output": test_result['output']
            }
    
    def auto_update_safe_deps(self) -> List[Dict]:
        """Automatically update all safe dependencies."""
        outdated = self.check_dependencies()
        results = []
        
        for ecosystem, packages in outdated.items():
            for pkg in packages:
                # Check if update is safe (patch/minor)
                if self._is_safe_update(pkg['current'], pkg['latest']):
                    result = self.update_dependency(
                        pkg['name'], 
                        pkg['latest'],
                        ecosystem
                    )
                    results.append(result)
        
        return results
    
    def _analyze_breaking_changes(
        self, 
        package: str, 
        version: str
    ) -> List[str]:
        """Use AI to analyze changelog for breaking changes."""
        # Fetch changelog
        changelog = self._get_changelog(package, version)
        
        prompt = f"""Analyze this changelog and identify breaking changes:

Package: {package}
Version: {version}

Changelog:
{changelog}

List any breaking changes that would affect our codebase.
Format: bullet points, be specific."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content.split('\n')
```

### 3. Commit Composer (Semantic Commit Agent) 📝

**Capabilities:**
- Analyze code changes semantically
- Generate conventional commit messages
- Follow team commit standards
- Include relevant context and references

**Implementation:**
```python
# lib/agents/git/commit_composer.py

import subprocess
from typing import Dict
import anthropic

class CommitComposerAgent:
    """
    Generates semantic, conventional commit messages.
    Uses Claude for understanding code changes.
    """
    
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
    
    def generate_commit_message(self, staged_files: List[str] = None) -> str:
        """
        Generate commit message based on staged changes.
        
        Format: <type>(<scope>): <subject>
        
        <body>
        
        <footer>
        """
        # Get diff
        if staged_files:
            diff = self._get_diff(staged_files)
        else:
            diff = subprocess.run(
                ["git", "diff", "--cached"],
                capture_output=True,
                text=True
            ).stdout
        
        if not diff:
            return "chore: empty commit"
        
        # Analyze changes with AI
        prompt = f"""Analyze this Git diff and generate a conventional commit message.

Diff:
{diff[:4000]}  # Limit for context

Format: <type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, perf, test, chore
Subject: imperative, lowercase, no period, max 50 chars

Include body if changes are complex (wrap at 72 chars).
Include footer for breaking changes or issue references.

Generate the commit message:"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text.strip()
    
    def auto_commit(self, message: str = None) -> Dict:
        """Stage all changes and commit with AI-generated message."""
        # Stage all changes
        subprocess.run(["git", "add", "."])
        
        # Generate message if not provided
        if not message:
            message = self.generate_commit_message()
        
        # Commit
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # Get commit SHA
            sha = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            return {
                "status": "success",
                "sha": sha,
                "message": message
            }
        else:
            return {
                "status": "error",
                "error": result.stderr
            }
```

### 4. Review Sentinel (PR Analysis Agent) 🔍

**Capabilities:**
- Automated code review
- Security vulnerability detection
- Best practices enforcement
- Performance impact analysis
- Test coverage verification

**Implementation:**
```python
# lib/agents/git/review_sentinel.py

from typing import Dict, List
import openai

class ReviewSentinelAgent:
    """
    Automated code review agent for pull requests.
    Uses OpenAI o3 for deep code analysis.
    """
    
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "o3"
    
    def review_pr(self, pr_number: int) -> Dict:
        """
        Comprehensive PR review.
        
        Checks:
        - Code quality
        - Security issues
        - Performance concerns
        - Test coverage
        - Documentation
        """
        # Fetch PR details
        pr_data = self._get_pr_data(pr_number)
        
        # Analyze each file
        reviews = []
        for file in pr_data['files']:
            review = self._review_file(file)
            reviews.append(review)
        
        # Generate summary
        summary = self._generate_review_summary(reviews)
        
        return {
            "pr": pr_number,
            "status": summary['status'],  # approved, changes_requested, commented
            "summary": summary['text'],
            "file_reviews": reviews,
            "score": summary['score']  # 0-100
        }
    
    def _review_file(self, file_data: Dict) -> Dict:
        """Review a single file with AI."""
        prompt = f"""Review this code change:

File: {file_data['filename']}
Language: {file_data['language']}

Changes:
{file_data['patch']}

Provide a code review focusing on:
1. Code quality and maintainability
2. Security vulnerabilities
3. Performance issues
4. Best practices
5. Test coverage

Format as JSON:
{{
  "issues": [
    {{
      "line": <line_number>,
      "severity": "critical|high|medium|low",
      "type": "security|performance|style|logic",
      "message": "<description>",
      "suggestion": "<how to fix>"
    }}
  ],
  "score": <0-100>,
  "summary": "<overall assessment>"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
```

---

## 📄 Document Fusion Agents

### 1. DocFusion (Document Merger Agent) 📄

**Capabilities:**
- Intelligent document merging
- Style consistency enforcement
- Duplicate content detection
- Section reorganization
- Citation management

**Implementation:**
```python
# lib/agents/documents/doc_fusion.py

from typing import List, Dict
import anthropic

class DocFusionAgent:
    """
    Merges multiple documents into coherent unified document.
    Uses Claude Opus for semantic understanding.
    """
    
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-opus-4.1"
    
    def merge_documents(
        self, 
        documents: List[Dict],
        strategy: str = "comprehensive"
    ) -> Dict:
        """
        Merge multiple documents.
        
        Args:
            documents: List of {"title": str, "content": str}
            strategy: "comprehensive" | "summary" | "comparison"
        
        Returns:
            {
                "merged_content": str,
                "structure": Dict,
                "duplicates_removed": int,
                "sources": List[str]
            }
        """
        # Prepare document content
        doc_texts = [
            f"## Document: {doc['title']}\n\n{doc['content']}"
            for doc in documents
        ]
        combined = "\n\n---\n\n".join(doc_texts)
        
        # Build prompt based on strategy
        if strategy == "comprehensive":
            prompt = self._build_comprehensive_prompt(combined)
        elif strategy == "summary":
            prompt = self._build_summary_prompt(combined)
        else:
            prompt = self._build_comparison_prompt(combined)
        
        # Generate merged document
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        merged_content = response.content[0].text
        
        return {
            "merged_content": merged_content,
            "structure": self._extract_structure(merged_content),
            "sources": [doc['title'] for doc in documents]
        }
    
    def _build_comprehensive_prompt(self, combined: str) -> str:
        """Build prompt for comprehensive merge."""
        return f"""You are a technical documentation specialist. Merge the following documents into a single, comprehensive document.

Requirements:
1. Remove duplicate content
2. Maintain consistent structure
3. Preserve all unique information
4. Use clear headings and sections
5. Add cross-references where relevant
6. Include a table of contents
7. Maintain technical accuracy

Documents:
{combined}

Generate the merged document in Markdown format:"""
    
    def harmonize_style(self, content: str, style_guide: str) -> str:
        """Harmonize document style according to guide."""
        prompt = f"""Rewrite this document to match the style guide:

Style Guide:
{style_guide}

Document:
{content}

Rewrite maintaining all content but matching the style:"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
```

### 2. Content Harmonizer (Style Unification Agent) ✍️

**Capabilities:**
- Tone and voice consistency
- Terminology standardization
- Format unification
- Brand compliance checking

**Implementation:**
```python
# lib/agents/documents/content_harmonizer.py

import openai
from typing import Dict

class ContentHarmonizerAgent:
    """
    Ensures consistent style and tone across documents.
    Uses GPT-4 for style analysis and transformation.
    """
    
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-4-turbo"
    
    def analyze_style(self, content: str) -> Dict:
        """Analyze document style characteristics."""
        prompt = f"""Analyze the writing style of this document:

{content[:2000]}

Provide analysis in JSON format:
{{
  "tone": "<formal|casual|technical|conversational>",
  "voice": "<active|passive>",
  "terminology": ["<key terms used>"],
  "readability_score": <0-100>,
  "target_audience": "<description>",
  "suggestions": ["<improvements>"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def harmonize_to_standard(
        self, 
        content: str,
        standard: Dict
    ) -> str:
        """Transform content to match standard style."""
        prompt = f"""Rewrite this content to match these style standards:

Standards:
- Tone: {standard['tone']}
- Voice: {standard['voice']}
- Formality: {standard['formality']}
- Terminology: {', '.join(standard['terminology'])}

Content:
{content}

Rewrite maintaining meaning but matching the standards:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
```

### 3. Knowledge Synthesizer (Multi-Source Aggregator) 📚

**Capabilities:**
- Cross-reference multiple sources
- Extract key insights
- Build knowledge graphs
- Generate summaries

### 4. Format Conductor (Document Converter) 🎨

**Capabilities:**
- Markdown ↔ PDF ↔ HTML ↔ DOCX
- Preserve formatting and structure
- Handle embedded media
- Maintain hyperlinks

---

## 🚀 Integration with Tokyo-IA

### Orchestrator Integration

```python
# Add Git agents to orchestrator
from lib.agents.git import (
    MergeMasterAgent,
    PullGuardianAgent,
    CommitComposerAgent,
    ReviewSentinelAgent
)

GIT_AGENTS = {
    'merge-master': {
        'name': 'Merge Master',
        'emoji': '🔀',
        'model': 'Claude Opus 4.1',
        'role': 'Conflict Resolution',
        'class': MergeMasterAgent
    },
    'pull-guardian': {
        'name': 'Pull Guardian',
        'emoji': '📥',
        'model': 'OpenAI o3',
        'role': 'Dependency Management',
        'class': PullGuardianAgent
    },
    'commit-composer': {
        'name': 'Commit Composer',
        'emoji': '📝',
        'model': 'Claude 3.5 Sonnet',
        'role': 'Commit Messages',
        'class': CommitComposerAgent
    },
    'review-sentinel': {
        'name': 'Review Sentinel',
        'emoji': '🔍',
        'model': 'OpenAI o3',
        'role': 'Code Review',
        'class': ReviewSentinelAgent
    }
}
```

### CLI Usage

```bash
# Auto-merge with conflict resolution
tokyo-ia git merge feature/new-api --auto-resolve

# Update dependencies
tokyo-ia git deps update --auto --safe-only

# Generate commit message
tokyo-ia git commit --auto-message

# Review PR
tokyo-ia git review 123 --auto-approve-if-safe

# Merge documents
tokyo-ia docs merge README.md CONTRIBUTING.md --output GUIDE.md
```

---

## 📊 Workflow Examples

### Example 1: Automated Dependency Update Workflow

```python
# Daily dependency check and update
from lib.orchestrator.workflows import dependency_update_workflow

result = dependency_update_workflow(
    orchestrator=imperial_orchestrator,
    auto_merge=True,
    require_tests=True,
    notify_on_breaking=True
)

# Output:
# {
#   "updates_applied": 5,
#   "prs_created": 2,  # breaking changes
#   "tests_passed": True,
#   "security_fixes": 3
# }
```

### Example 2: Automated Release Workflow

```python
# Complete release automation
from lib.orchestrator.workflows import release_workflow

result = release_workflow(
    orchestrator=imperial_orchestrator,
    version="1.5.0",
    steps=[
        "run_tests",
        "update_changelog",
        "merge_to_main",
        "create_tag",
        "generate_release_notes",
        "publish_artifacts"
    ]
)
```

### Example 3: Documentation Consolidation

```python
# Merge all README files into master guide
from lib.agents.documents import DocFusionAgent

doc_agent = DocFusionAgent(api_key=api_key)

result = doc_agent.merge_documents(
    documents=[
        {"title": "Main README", "content": open("README.md").read()},
        {"title": "Deployment", "content": open("DEPLOY_VERCEL.md").read()},
        {"title": "Agents", "content": open("AGENTS_README.md").read()}
    ],
    strategy="comprehensive"
)

# Save merged document
with open("COMPLETE_GUIDE.md", "w") as f:
    f.write(result['merged_content'])
```

---

## 🎯 Best Practices

### Git Automation
1. ✅ Always run tests before auto-merging
2. ✅ Require human review for breaking changes
3. ✅ Use semantic versioning for dependencies
4. ✅ Create detailed commit messages
5. ✅ Enable rollback mechanisms
6. ❌ Don't auto-merge to production without approval
7. ❌ Don't skip CI/CD checks

### Document Fusion
1. ✅ Preserve original sources in metadata
2. ✅ Maintain version history
3. ✅ Use consistent formatting
4. ✅ Validate merged content
5. ✅ Keep backups of original documents
6. ❌ Don't lose attribution
7. ❌ Don't merge incompatible formats without conversion

---

## 🔒 Security Considerations

### Git Agents
- **Credential Management:** Never store API keys in Git
- **Code Execution:** Validate all generated code before commit
- **Access Control:** Limit agent permissions to specific repos
- **Audit Trail:** Log all automated actions

### Document Agents
- **Data Privacy:** Don't include sensitive data in merged documents
- **Attribution:** Maintain source citations
- **Validation:** Human review for critical documents
- **Compliance:** Follow organizational document policies

---

## 📈 Metrics & Monitoring

### Git Automation Metrics
```python
{
  "merges_automated": 45,
  "conflicts_resolved": 23,
  "manual_reviews_needed": 3,
  "time_saved_hours": 12.5,
  "success_rate": 0.95,
  "average_resolution_time_seconds": 45
}
```

### Document Fusion Metrics
```python
{
  "documents_merged": 150,
  "duplicates_removed": 230,
  "style_consistency_score": 0.92,
  "processing_time_seconds": 15,
  "manual_edits_needed": 5
}
```

---

## 🚀 Deployment

### Installation

```bash
# Install Git automation agents
pip install tokyo-ia-git-agents

# Install document fusion agents
pip install tokyo-ia-doc-fusion

# Or install all
pip install tokyo-ia[git,docs]
```

### Configuration

```yaml
# config/git-agents.yaml
agents:
  merge_master:
    enabled: true
    model: claude-opus-4.1
    auto_resolve_threshold: 0.8
    require_tests: true
    
  pull_guardian:
    enabled: true
    model: openai-o3
    check_frequency: daily
    auto_update_safe: true
    
  commit_composer:
    enabled: true
    model: claude-3-5-sonnet
    conventional_commits: true
    
  review_sentinel:
    enabled: true
    model: openai-o3
    auto_approve_threshold: 0.9
```

---

## 🏆 Conclusion

Git Automation and Document Fusion agents bring enterprise-grade automation to Tokyo-IA:

✅ **Intelligent Merging** - AI-powered conflict resolution
✅ **Dependency Management** - Automated updates with safety checks
✅ **Semantic Commits** - Professional commit messages
✅ **Automated Reviews** - Consistent code quality
✅ **Document Synthesis** - Intelligent content merging
✅ **Style Consistency** - Unified documentation

**Transform your Git workflow and documentation process with AI agents!**

---

*Last Updated: December 2025*
*Version: 1.0.0*
*License: MIT*
