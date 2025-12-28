#!/usr/bin/env python3
"""
Tokyo Crew - AI Agent Orchestration System
A multi-agent system leveraging various LLM providers for code analysis and automation.

Agents:
- Hiro: Groq Llama 3.3 70B (Free Tier) - Code Analysis Expert
- Sakura: Google Gemini 1.5 Flash (Free Tier) - Documentation Specialist
- Akira: Claude 3.5 Sonnet - Architecture & Design Expert
- Yuki: GPT-4o mini - Quick Review & Testing Expert
- Kenji: GPT-4o - Senior Lead & Quality Assurance

Workflows:
- cleanup_repository: Analyze and suggest code cleanup
- analyze_pr: Comprehensive pull request analysis
- generate_documentation: Generate comprehensive documentation
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import traceback

# Third-party imports (install via: pip install openai anthropic google-generativeai groq)
try:
    import openai
    from anthropic import Anthropic
    import google.generativeai as genai
    from groq import Groq
except ImportError as e:
    print(f"Error: Missing required package. Install with: pip install openai anthropic google-generativeai groq")
    sys.exit(1)


# =============================================================================
# Configuration & Data Classes
# =============================================================================

@dataclass
class AgentConfig:
    """Configuration for an AI agent"""
    name: str
    role: str
    provider: str  # groq, google, anthropic, openai
    model: str
    is_free_tier: bool
    capabilities: List[str]


@dataclass
class TaskResult:
    """Result from an agent task"""
    agent_name: str
    task: str
    success: bool
    output: str
    error: Optional[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class WorkflowResult:
    """Result from a complete workflow"""
    workflow_name: str
    results: List[TaskResult]
    summary: str
    timestamp: str
    report_path: Optional[str] = None


# =============================================================================
# Agent Implementations
# =============================================================================

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.name = config.name
        self.role = config.role
    
    def execute(self, prompt: str, context: Dict[str, Any] = None) -> TaskResult:
        """Execute a task with the given prompt"""
        raise NotImplementedError("Subclasses must implement execute()")
    
    def _create_result(self, task: str, success: bool, output: str, error: str = None) -> TaskResult:
        """Helper to create a TaskResult"""
        return TaskResult(
            agent_name=self.name,
            task=task,
            success=success,
            output=output,
            error=error
        )


class HiroAgent(BaseAgent):
    """Hiro - Groq Llama 3.3 70B - Code Analysis Expert"""
    
    def __init__(self):
        config = AgentConfig(
            name="Hiro",
            role="Code Analysis Expert",
            provider="groq",
            model="llama-3.3-70b-versatile",
            is_free_tier=True,
            capabilities=["code_analysis", "bug_detection", "performance_review"]
        )
        super().__init__(config)
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        self.client = Groq(api_key=api_key)
    
    def execute(self, prompt: str, context: Dict[str, Any] = None) -> TaskResult:
        """Execute code analysis task"""
        try:
            system_prompt = f"""You are {self.name}, a {self.role}. 
Your expertise includes code quality analysis, bug detection, and performance optimization.
Provide detailed, actionable insights with specific examples and recommendations."""
            
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2048
            )
            
            output = response.choices[0].message.content
            return self._create_result("code_analysis", True, output)
            
        except Exception as e:
            error_msg = f"Error in {self.name}: {str(e)}"
            return self._create_result("code_analysis", False, "", error_msg)


class SakuraAgent(BaseAgent):
    """Sakura - Google Gemini 1.5 Flash - Documentation Specialist"""
    
    def __init__(self):
        config = AgentConfig(
            name="Sakura",
            role="Documentation Specialist",
            provider="google",
            model="gemini-1.5-flash",
            is_free_tier=True,
            capabilities=["documentation", "technical_writing", "tutorials"]
        )
        super().__init__(config)
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.config.model)
    
    def execute(self, prompt: str, context: Dict[str, Any] = None) -> TaskResult:
        """Execute documentation task"""
        try:
            system_instruction = f"""You are {self.name}, a {self.role}.
You excel at creating clear, comprehensive documentation, tutorials, and technical guides.
Focus on clarity, completeness, and practical examples."""
            
            full_prompt = f"{system_instruction}\n\n{prompt}"
            response = self.model.generate_content(full_prompt)
            
            output = response.text
            return self._create_result("documentation", True, output)
            
        except Exception as e:
            error_msg = f"Error in {self.name}: {str(e)}"
            return self._create_result("documentation", False, "", error_msg)


class AkiraAgent(BaseAgent):
    """Akira - Claude 3.5 Sonnet - Architecture & Design Expert"""
    
    def __init__(self):
        config = AgentConfig(
            name="Akira",
            role="Architecture & Design Expert",
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            is_free_tier=False,
            capabilities=["architecture", "design_patterns", "system_design"]
        )
        super().__init__(config)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = Anthropic(api_key=api_key)
    
    def execute(self, prompt: str, context: Dict[str, Any] = None) -> TaskResult:
        """Execute architecture analysis task"""
        try:
            system_prompt = f"""You are {self.name}, a {self.role}.
You specialize in software architecture, design patterns, and system design.
Provide strategic insights, architectural recommendations, and best practices."""
            
            response = self.client.messages.create(
                model=self.config.model,
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            output = response.content[0].text
            return self._create_result("architecture_analysis", True, output)
            
        except Exception as e:
            error_msg = f"Error in {self.name}: {str(e)}"
            return self._create_result("architecture_analysis", False, "", error_msg)


class YukiAgent(BaseAgent):
    """Yuki - GPT-4o mini - Quick Review & Testing Expert"""
    
    def __init__(self):
        config = AgentConfig(
            name="Yuki",
            role="Quick Review & Testing Expert",
            provider="openai",
            model="gpt-4o-mini",
            is_free_tier=False,
            capabilities=["quick_review", "testing", "validation"]
        )
        super().__init__(config)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = openai.OpenAI(api_key=api_key)
    
    def execute(self, prompt: str, context: Dict[str, Any] = None) -> TaskResult:
        """Execute quick review task"""
        try:
            system_prompt = f"""You are {self.name}, a {self.role}.
You specialize in rapid code reviews, test coverage analysis, and validation.
Provide concise, actionable feedback focused on testing and quality."""
            
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2048
            )
            
            output = response.choices[0].message.content
            return self._create_result("quick_review", True, output)
            
        except Exception as e:
            error_msg = f"Error in {self.name}: {str(e)}"
            return self._create_result("quick_review", False, "", error_msg)


class KenjiAgent(BaseAgent):
    """Kenji - GPT-4o - Senior Lead & Quality Assurance"""
    
    def __init__(self):
        config = AgentConfig(
            name="Kenji",
            role="Senior Lead & Quality Assurance",
            provider="openai",
            model="gpt-4o",
            is_free_tier=False,
            capabilities=["leadership", "quality_assurance", "final_review"]
        )
        super().__init__(config)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = openai.OpenAI(api_key=api_key)
    
    def execute(self, prompt: str, context: Dict[str, Any] = None) -> TaskResult:
        """Execute senior review task"""
        try:
            system_prompt = f"""You are {self.name}, a {self.role}.
You are the senior leader providing final quality assurance and strategic direction.
Synthesize inputs from other agents and provide authoritative, comprehensive guidance."""
            
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=4096
            )
            
            output = response.choices[0].message.content
            return self._create_result("senior_review", True, output)
            
        except Exception as e:
            error_msg = f"Error in {self.name}: {str(e)}"
            return self._create_result("senior_review", False, "", error_msg)


# =============================================================================
# Tokyo Crew Orchestrator
# =============================================================================

class TokyoCrew:
    """Main orchestrator for the Tokyo Crew agent system"""
    
    def __init__(self, use_free_tier_only: bool = False):
        self.use_free_tier_only = use_free_tier_only
        self.agents = self._initialize_agents()
        self.report_base_dir = Path("tokyo_crew_reports")
        self.report_base_dir.mkdir(exist_ok=True)
    
    def _initialize_agents(self) -> Dict[str, BaseAgent]:
        """Initialize all agents"""
        agents = {}
        
        try:
            # Always initialize free tier agents
            agents["hiro"] = HiroAgent()
            agents["sakura"] = SakuraAgent()
            
            # Initialize paid agents if not in free-tier-only mode
            if not self.use_free_tier_only:
                agents["akira"] = AkiraAgent()
                agents["yuki"] = YukiAgent()
                agents["kenji"] = KenjiAgent()
            
        except ValueError as e:
            print(f"Warning: {e}")
            print("Some agents may not be available due to missing API keys.")
        
        return agents
    
    def _create_report_directory(self, workflow_name: str) -> Path:
        """Create a timestamped directory for reports"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        report_dir = self.report_base_dir / f"{workflow_name}_{timestamp}"
        report_dir.mkdir(parents=True, exist_ok=True)
        return report_dir
    
    def _save_report(self, workflow_result: WorkflowResult, report_dir: Path):
        """Save workflow results to files"""
        # Save main report
        main_report = report_dir / "report.md"
        with open(main_report, "w", encoding="utf-8") as f:
            f.write(f"# Tokyo Crew Report: {workflow_result.workflow_name}\n\n")
            f.write(f"**Generated:** {workflow_result.timestamp}\n\n")
            f.write(f"## Summary\n\n{workflow_result.summary}\n\n")
            f.write("---\n\n")
            
            for result in workflow_result.results:
                f.write(f"## Agent: {result.agent_name}\n\n")
                f.write(f"**Task:** {result.task}\n\n")
                f.write(f"**Status:** {'✓ Success' if result.success else '✗ Failed'}\n\n")
                f.write(f"**Timestamp:** {result.timestamp}\n\n")
                
                if result.success:
                    f.write(f"### Output\n\n{result.output}\n\n")
                else:
                    f.write(f"### Error\n\n{result.error}\n\n")
                
                f.write("---\n\n")
        
        # Save JSON data
        json_report = report_dir / "report.json"
        with open(json_report, "w", encoding="utf-8") as f:
            json.dump({
                "workflow_name": workflow_result.workflow_name,
                "timestamp": workflow_result.timestamp,
                "summary": workflow_result.summary,
                "results": [asdict(r) for r in workflow_result.results]
            }, f, indent=2)
        
        print(f"\n✓ Report saved to: {report_dir}")
        print(f"  - {main_report.name}")
        print(f"  - {json_report.name}")
    
    # =========================================================================
    # Workflow: Cleanup Repository
    # =========================================================================
    
    def cleanup_repository(self, repo_path: str = ".") -> WorkflowResult:
        """
        Analyze repository and suggest cleanup actions
        
        Workflow:
        1. Hiro: Analyze code quality and identify cleanup opportunities
        2. Sakura: Review documentation and suggest improvements
        3. Akira/Kenji: Provide architectural recommendations (if available)
        """
        print(f"\n{'='*70}")
        print("WORKFLOW: Repository Cleanup Analysis")
        print(f"{'='*70}\n")
        
        results = []
        repo_path_obj = Path(repo_path).resolve()
        
        # Task 1: Code Quality Analysis (Hiro)
        if "hiro" in self.agents:
            print(f"[1/3] {self.agents['hiro'].name} analyzing code quality...")
            prompt = f"""Analyze the repository structure and code quality for cleanup opportunities.

Repository Path: {repo_path_obj}

Please identify:
1. Unused or redundant code files
2. Code duplication issues
3. Deprecated patterns or libraries
4. Files that should be refactored
5. Performance bottlenecks
6. Security concerns

Provide specific file paths and actionable recommendations."""
            
            result = self.agents["hiro"].execute(prompt)
            results.append(result)
            print(f"   Status: {'✓' if result.success else '✗'}")
        
        # Task 2: Documentation Review (Sakura)
        if "sakura" in self.agents:
            print(f"[2/3] {self.agents['sakura'].name} reviewing documentation...")
            prompt = f"""Review the repository documentation and suggest improvements.

Repository Path: {repo_path_obj}

Please evaluate:
1. README completeness and clarity
2. Missing or outdated documentation files
3. Code comments quality
4. API documentation
5. Setup and installation guides
6. Contributing guidelines

Provide specific recommendations for documentation cleanup and enhancement."""
            
            result = self.agents["sakura"].execute(prompt)
            results.append(result)
            print(f"   Status: {'✓' if result.success else '✗'}")
        
        # Task 3: Architectural Review (Akira or Kenji)
        if "akira" in self.agents:
            print(f"[3/3] {self.agents['akira'].name} reviewing architecture...")
            prompt = f"""Provide architectural review and cleanup recommendations.

Repository Path: {repo_path_obj}

Please analyze:
1. Overall project structure
2. Dependency management
3. Module organization
4. Design pattern consistency
5. Scalability concerns
6. Technical debt priorities

Provide strategic recommendations for structural cleanup."""
            
            result = self.agents["akira"].execute(prompt)
            results.append(result)
            print(f"   Status: {'✓' if result.success else '✗'}")
        elif "kenji" in self.agents:
            print(f"[3/3] {self.agents['kenji'].name} providing senior review...")
            prompt = f"""As the senior lead, provide comprehensive cleanup recommendations.

Repository Path: {repo_path_obj}

Synthesize cleanup priorities across:
1. Code quality
2. Documentation
3. Architecture
4. Testing
5. Dependencies
6. Security

Provide a prioritized action plan for repository cleanup."""
            
            result = self.agents["kenji"].execute(prompt)
            results.append(result)
            print(f"   Status: {'✓' if result.success else '✗'}")
        
        # Generate summary
        success_count = sum(1 for r in results if r.success)
        summary = f"""Repository cleanup analysis completed with {success_count}/{len(results)} successful agent tasks.

Agents Involved: {', '.join(r.agent_name for r in results)}
Repository: {repo_path_obj}

This analysis provides comprehensive recommendations for code cleanup, documentation
improvements, and architectural enhancements."""
        
        workflow_result = WorkflowResult(
            workflow_name="cleanup_repository",
            results=results,
            summary=summary,
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Save report
        report_dir = self._create_report_directory("cleanup_repository")
        self._save_report(workflow_result, report_dir)
        workflow_result.report_path = str(report_dir)
        
        return workflow_result
    
    # =========================================================================
    # Workflow: Analyze Pull Request
    # =========================================================================
    
    def analyze_pr(self, pr_number: int, repo_name: str = None) -> WorkflowResult:
        """
        Comprehensive pull request analysis
        
        Workflow:
        1. Hiro: Code quality and bug detection
        2. Yuki: Testing and validation review
        3. Akira: Architecture impact analysis
        4. Kenji: Final approval recommendation
        """
        print(f"\n{'='*70}")
        print(f"WORKFLOW: Pull Request Analysis (PR #{pr_number})")
        print(f"{'='*70}\n")
        
        results = []
        repo_context = f"Repository: {repo_name}" if repo_name else "Current repository"
        
        # Task 1: Code Quality Analysis (Hiro)
        if "hiro" in self.agents:
            print(f"[1/4] {self.agents['hiro'].name} analyzing code quality...")
            prompt = f"""Analyze Pull Request #{pr_number} for code quality and potential bugs.

{repo_context}

Please review:
1. Code quality and adherence to best practices
2. Potential bugs or edge cases
3. Performance implications
4. Security vulnerabilities
5. Code readability and maintainability
6. Breaking changes

Provide detailed feedback with specific line references where possible."""
            
            result = self.agents["hiro"].execute(prompt)
            results.append(result)
            print(f"   Status: {'✓' if result.success else '✗'}")
        
        # Task 2: Testing Review (Yuki if available, else Hiro)
        reviewer = self.agents.get("yuki") or self.agents.get("hiro")
        if reviewer:
            print(f"[2/4] {reviewer.name} reviewing tests and validation...")
            prompt = f"""Review the testing strategy and validation for PR #{pr_number}.

{repo_context}

Please evaluate:
1. Test coverage for new code
2. Test quality and effectiveness
3. Edge cases covered
4. Integration test needs
5. Validation logic
6. Error handling

Provide recommendations for improving test coverage and quality."""
            
            result = reviewer.execute(prompt)
            results.append(result)
            print(f"   Status: {'✓' if result.success else '✗'}")
        
        # Task 3: Architecture Impact (Akira if available)
        if "akira" in self.agents:
            print(f"[3/4] {self.agents['akira'].name} analyzing architecture impact...")
            prompt = f"""Analyze the architectural impact of PR #{pr_number}.

{repo_context}

Please assess:
1. Impact on overall system architecture
2. Design pattern consistency
3. Modularity and coupling
4. Scalability implications
5. Future maintainability
6. Integration considerations

Provide architectural recommendations and concerns."""
            
            result = self.agents["akira"].execute(prompt)
            results.append(result)
            print(f"   Status: {'✓' if result.success else '✗'}")
        
        # Task 4: Final Review (Kenji if available, else Sakura)
        final_reviewer = self.agents.get("kenji") or self.agents.get("sakura")
        if final_reviewer:
            print(f"[4/4] {final_reviewer.name} providing final recommendation...")
            
            # Compile previous results for context
            previous_findings = "\n\n".join([
                f"**{r.agent_name}**: {r.output[:500]}..." 
                for r in results if r.success
            ])
            
            prompt = f"""Provide final recommendation for PR #{pr_number}.

{repo_context}

Previous Agent Findings:
{previous_findings}

Based on all analyses, provide:
1. Overall assessment (Approve/Request Changes/Needs Discussion)
2. Critical issues that must be addressed
3. Suggested improvements
4. Risk assessment
5. Final recommendation and rationale

Synthesize all feedback into clear, actionable guidance."""
            
            result = final_reviewer.execute(prompt)
            results.append(result)
            print(f"   Status: {'✓' if result.success else '✗'}")
        
        # Generate summary
        success_count = sum(1 for r in results if r.success)
        summary = f"""Pull Request #{pr_number} analysis completed with {success_count}/{len(results)} successful agent tasks.

Agents Involved: {', '.join(r.agent_name for r in results)}
{repo_context}

This analysis provides comprehensive review covering code quality, testing,
architecture, and final recommendation for the pull request."""
        
        workflow_result = WorkflowResult(
            workflow_name="analyze_pr",
            results=results,
            summary=summary,
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Save report
        report_dir = self._create_report_directory(f"analyze_pr_{pr_number}")
        self._save_report(workflow_result, report_dir)
        workflow_result.report_path = str(report_dir)
        
        return workflow_result
    
    # =========================================================================
    # Workflow: Generate Documentation
    # =========================================================================
    
    def generate_documentation(self, target: str = "all") -> WorkflowResult:
        """
        Generate comprehensive documentation
        
        Workflow:
        1. Sakura: Create main documentation
        2. Hiro: Add technical code examples
        3. Akira: Add architecture diagrams and design docs
        4. Kenji: Review and finalize documentation
        """
        print(f"\n{'='*70}")
        print(f"WORKFLOW: Documentation Generation (Target: {target})")
        print(f"{'='*70}\n")
        
        results = []
        
        # Task 1: Main Documentation (Sakura)
        if "sakura" in self.agents:
            print(f"[1/4] {self.agents['sakura'].name} generating main documentation...")
            prompt = f"""Generate comprehensive documentation for the project.

Target: {target}

Please create:
1. README.md - Project overview, setup, and usage
2. CONTRIBUTING.md - Contribution guidelines
3. API.md - API documentation
4. ARCHITECTURE.md - System architecture overview
5. GETTING_STARTED.md - Quick start guide
6. FAQ.md - Frequently asked questions

Focus on clarity, completeness, and practical examples."""
            
            result = self.agents["sakura"].execute(prompt)
            results.append(result)
            print(f"   Status: {'✓' if result.success else '✗'}")
        
        # Task 2: Technical Examples (Hiro)
        if "hiro" in self.agents:
            print(f"[2/4] {self.agents['hiro'].name} adding code examples...")
            prompt = f"""Add technical code examples and snippets to the documentation.

Target: {target}

Please provide:
1. Usage examples for key features
2. Code snippets with explanations
3. Common patterns and best practices
4. Integration examples
5. Troubleshooting code samples
6. Performance optimization examples

Make examples practical, well-commented, and copy-pasteable."""
            
            result = self.agents["hiro"].execute(prompt)
            results.append(result)
            print(f"   Status: {'✓' if result.success else '✗'}")
        
        # Task 3: Architecture Documentation (Akira if available)
        if "akira" in self.agents:
            print(f"[3/4] {self.agents['akira'].name} creating architecture docs...")
            prompt = f"""Create architecture and design documentation.

Target: {target}

Please document:
1. System architecture overview
2. Component diagrams (in Mermaid or ASCII)
3. Design patterns used
4. Data flow diagrams
5. Technology stack decisions
6. Scalability considerations

Provide visual representations and clear explanations."""
            
            result = self.agents["akira"].execute(prompt)
            results.append(result)
            print(f"   Status: {'✓' if result.success else '✗'}")
        
        # Task 4: Documentation Review (Kenji if available, else Sakura)
        reviewer = self.agents.get("kenji") or self.agents.get("sakura")
        if reviewer:
            print(f"[4/4] {reviewer.name} reviewing documentation...")
            
            # Compile previous documentation
            previous_docs = "\n\n".join([
                f"**{r.agent_name}'s contribution**:\n{r.output[:800]}..." 
                for r in results if r.success
            ])
            
            prompt = f"""Review and finalize the documentation.

Target: {target}

Previous Documentation:
{previous_docs}

Please:
1. Ensure consistency across all documents
2. Check for completeness and clarity
3. Verify all examples are correct
4. Suggest improvements or missing sections
5. Add table of contents where needed
6. Ensure proper formatting

Provide final polished documentation ready for publication."""
            
            result = reviewer.execute(prompt)
            results.append(result)
            print(f"   Status: {'✓' if result.success else '✗'}")
        
        # Generate summary
        success_count = sum(1 for r in results if r.success)
        summary = f"""Documentation generation completed with {success_count}/{len(results)} successful agent tasks.

Agents Involved: {', '.join(r.agent_name for r in results)}
Target: {target}

This workflow produced comprehensive documentation including README, API docs,
architecture diagrams, code examples, and contribution guidelines."""
        
        workflow_result = WorkflowResult(
            workflow_name="generate_documentation",
            results=results,
            summary=summary,
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Save report
        report_dir = self._create_report_directory("generate_documentation")
        self._save_report(workflow_result, report_dir)
        workflow_result.report_path = str(report_dir)
        
        return workflow_result


# =============================================================================
# CLI Interface
# =============================================================================

def create_cli_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser"""
    parser = argparse.ArgumentParser(
        description="Tokyo Crew - AI Agent Orchestration System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run cleanup analysis with all agents
  python tokyo_crew.py cleanup --path ./my-project
  
  # Analyze PR using only free-tier agents
  python tokyo_crew.py analyze-pr --pr 42 --free-tier
  
  # Generate documentation
  python tokyo_crew.py generate-docs --target api
  
  # List available agents
  python tokyo_crew.py --list-agents

Environment Variables Required:
  GROQ_API_KEY         - For Hiro (Groq Llama 3.3 70B)
  GOOGLE_API_KEY       - For Sakura (Gemini 1.5 Flash)
  ANTHROPIC_API_KEY    - For Akira (Claude 3.5 Sonnet)
  OPENAI_API_KEY       - For Yuki (GPT-4o mini) and Kenji (GPT-4o)
        """
    )
    
    parser.add_argument(
        "--free-tier",
        action="store_true",
        help="Use only free-tier agents (Hiro and Sakura)"
    )
    
    parser.add_argument(
        "--list-agents",
        action="store_true",
        help="List all available agents and exit"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser(
        "cleanup",
        help="Analyze repository and suggest cleanup actions"
    )
    cleanup_parser.add_argument(
        "--path",
        default=".",
        help="Path to repository (default: current directory)"
    )
    
    # Analyze PR command
    pr_parser = subparsers.add_parser(
        "analyze-pr",
        help="Comprehensive pull request analysis"
    )
    pr_parser.add_argument(
        "--pr",
        type=int,
        required=True,
        help="Pull request number"
    )
    pr_parser.add_argument(
        "--repo",
        help="Repository name (optional)"
    )
    
    # Generate docs command
    docs_parser = subparsers.add_parser(
        "generate-docs",
        help="Generate comprehensive documentation"
    )
    docs_parser.add_argument(
        "--target",
        default="all",
        choices=["all", "api", "architecture", "readme", "contributing"],
        help="Documentation target (default: all)"
    )
    
    return parser


def list_agents(crew: TokyoCrew):
    """List all available agents"""
    print("\n" + "="*70)
    print("TOKYO CREW - Available Agents")
    print("="*70 + "\n")
    
    all_agents = [
        ("Hiro", "Code Analysis Expert", "Groq Llama 3.3 70B", True, "hiro"),
        ("Sakura", "Documentation Specialist", "Google Gemini 1.5 Flash", True, "sakura"),
        ("Akira", "Architecture & Design Expert", "Claude 3.5 Sonnet", False, "akira"),
        ("Yuki", "Quick Review & Testing Expert", "GPT-4o mini", False, "yuki"),
        ("Kenji", "Senior Lead & QA", "GPT-4o", False, "kenji"),
    ]
    
    for name, role, model, is_free, key in all_agents:
        status = "✓ ACTIVE" if key in crew.agents else "✗ UNAVAILABLE"
        tier = "FREE" if is_free else "PAID"
        print(f"{status:15} | {name:8} | {tier:4} | {role}")
        print(f"{'':15} | {'':8} | {'':4} | Model: {model}")
        print()
    
    print("="*70)
    print(f"Active Agents: {len(crew.agents)}/{len(all_agents)}")
    print("="*70 + "\n")


def main():
    """Main CLI entry point"""
    parser = create_cli_parser()
    args = parser.parse_args()
    
    # Initialize crew
    try:
        crew = TokyoCrew(use_free_tier_only=args.free_tier)
    except Exception as e:
        print(f"Error initializing Tokyo Crew: {e}")
        sys.exit(1)
    
    # List agents if requested
    if args.list_agents:
        list_agents(crew)
        return
    
    # Check if command was provided
    if not args.command:
        parser.print_help()
        print("\nUse --list-agents to see available agents")
        return
    
    # Execute command
    try:
        if args.command == "cleanup":
            result = crew.cleanup_repository(args.path)
            print(f"\n✓ Cleanup analysis complete!")
            print(f"  Report: {result.report_path}")
            
        elif args.command == "analyze-pr":
            result = crew.analyze_pr(args.pr, args.repo)
            print(f"\n✓ PR analysis complete!")
            print(f"  Report: {result.report_path}")
            
        elif args.command == "generate-docs":
            result = crew.generate_documentation(args.target)
            print(f"\n✓ Documentation generation complete!")
            print(f"  Report: {result.report_path}")
        
        # Print summary
        print(f"\nSummary:")
        print(f"{result.summary}")
        
    except Exception as e:
        print(f"\n✗ Error executing workflow: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
