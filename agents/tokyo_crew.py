#!/usr/bin/env python3
"""
Tokyo-IA CrewAI Agent Orchestration System

Main orchestration system using CrewAI to coordinate 5 specialized agents for
repository management, code review, testing, infrastructure, and documentation.

The Five Agents:
- 侍 Akira (akira-001): Code Review Master - Claude 3.5 Sonnet
- ❄️ Yuki (yuki-002): Test Engineering Specialist - GPT-4o mini
- 🛡️ Hiro (hiro-003): SRE & DevOps Expert - Llama 3.3 70B (Groq Free)
- 🌸 Sakura (sakura-004): Documentation Specialist - Gemini 1.5 Flash (Google Free)
- 🏗️ Kenji (kenji-005): Architecture Specialist - GPT-4o

Usage:
    # Analyze a PR
    python agents/tokyo_crew.py analyze-pr 126
    
    # Execute repository cleanup
    python agents/tokyo_crew.py cleanup
    
    # Generate documentation
    python agents/tokyo_crew.py generate-docs
    
    # Show available agents
    python agents/tokyo_crew.py list-agents

Environment Variables:
    ANTHROPIC_API_KEY - For Akira (Claude 3.5 Sonnet)
    OPENAI_API_KEY - For Yuki (GPT-4o mini) and Kenji (GPT-4o)
    GROQ_API_KEY - For Hiro (Llama 3.3 70B) [FREE TIER]
    GOOGLE_API_KEY - For Sakura (Gemini 1.5 Flash) [FREE TIER]
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from crewai import Agent, Task, Crew, LLM
from crewai_tools import FileReadTool, DirectoryReadTool


class TokyoCrew:
    """Main orchestration class for Tokyo-IA agent system."""
    
    def __init__(self, verbose: bool = True):
        """
        Initialize Tokyo Crew orchestration system.
        
        Args:
            verbose: Enable verbose output for debugging
        """
        self.verbose = verbose
        self.agents = {}
        self.initialized_agents = []
        self.output_dir = self._create_output_dir()
        
        # Initialize tools
        self.file_read_tool = FileReadTool()
        self.dir_read_tool = DirectoryReadTool()
        
        # Initialize agents
        self._initialize_agents()
    
    def _create_output_dir(self) -> Path:
        """Create timestamped output directory for reports."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(f"agent_reports_{timestamp}")
        output_dir.mkdir(exist_ok=True)
        return output_dir
    
    def _initialize_agents(self):
        """Initialize all 5 specialized agents."""
        print("🤖 Initializing Tokyo-IA Agent System...")
        print()
        
        # 侍 Akira - Code Review Master (Claude 3.5 Sonnet)
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
        if anthropic_key:
            try:
                akira_llm = LLM(
                    model="anthropic/claude-3-5-sonnet-20241022",
                    api_key=anthropic_key,
                    temperature=0.3
                )
                self.agents["akira"] = Agent(
                    role="Code Review Master",
                    goal="Ensure code quality, security, and performance excellence through thorough reviews",
                    backstory="""You are Akira (侍), a disciplined samurai of code quality. 
                    With decades of experience in software craftsmanship, you have a keen eye for 
                    security vulnerabilities, performance bottlenecks, and architectural flaws. 
                    Every line of code is reviewed with the precision of a master swordsman.""",
                    verbose=self.verbose,
                    allow_delegation=False,
                    llm=akira_llm,
                    tools=[self.file_read_tool]
                )
                self.initialized_agents.append("侍 Akira (Code Review)")
                print("✅ 侍 Akira initialized (Claude 3.5 Sonnet)")
            except Exception as e:
                print(f"⚠️  Could not initialize Akira: {e}")
        else:
            print("⚠️  Akira not initialized (ANTHROPIC_API_KEY not set)")
        
        # ❄️ Yuki - Test Engineering Specialist (GPT-4o mini)
        openai_key = os.environ.get("OPENAI_API_KEY")
        if openai_key:
            try:
                yuki_llm = LLM(
                    model="gpt-4o-mini",
                    api_key=openai_key,
                    temperature=0.4
                )
                self.agents["yuki"] = Agent(
                    role="Test Engineering Specialist",
                    goal="Ensure comprehensive test coverage and quality assurance across all code",
                    backstory="""You are Yuki (❄️), a meticulous test engineer with a passion for quality. 
                    Like falling snow covering every surface, your tests cover every code path. 
                    You believe that great software is built on a foundation of thorough testing.""",
                    verbose=self.verbose,
                    allow_delegation=False,
                    llm=yuki_llm,
                    tools=[self.file_read_tool]
                )
                self.initialized_agents.append("❄️ Yuki (Testing)")
                print("✅ ❄️ Yuki initialized (GPT-4o mini)")
            except Exception as e:
                print(f"⚠️  Could not initialize Yuki: {e}")
        else:
            print("⚠️  Yuki not initialized (OPENAI_API_KEY not set)")
        
        # 🛡️ Hiro - SRE & DevOps Expert (Llama 3.3 70B - Groq Free)
        groq_key = os.environ.get("GROQ_API_KEY")
        if groq_key:
            try:
                hiro_llm = LLM(
                    model="groq/llama-3.3-70b-versatile",
                    api_key=groq_key,
                    temperature=0.4
                )
                self.agents["hiro"] = Agent(
                    role="SRE & DevOps Expert",
                    goal="Ensure infrastructure reliability, optimal CI/CD pipelines, and operational excellence",
                    backstory="""You are Hiro (🛡️), a guardian of infrastructure and reliability. 
                    Like a shield protecting the realm, you ensure systems run smoothly, efficiently, 
                    and securely. Your expertise spans Kubernetes, CI/CD, monitoring, and everything 
                    that keeps software running in production.""",
                    verbose=self.verbose,
                    allow_delegation=False,
                    llm=hiro_llm,
                    tools=[self.file_read_tool, self.dir_read_tool]
                )
                self.initialized_agents.append("🛡️ Hiro (SRE/DevOps)")
                print("✅ 🛡️ Hiro initialized (Llama 3.3 70B - FREE TIER)")
            except Exception as e:
                print(f"⚠️  Could not initialize Hiro: {e}")
        else:
            print("⚠️  Hiro not initialized (GROQ_API_KEY not set)")
        
        # 🌸 Sakura - Documentation Specialist (Gemini 1.5 Flash - Google Free)
        google_key = os.environ.get("GOOGLE_API_KEY")
        if google_key:
            try:
                sakura_llm = LLM(
                    model="gemini/gemini-1.5-flash",
                    api_key=google_key,
                    temperature=0.5
                )
                self.agents["sakura"] = Agent(
                    role="Documentation Specialist",
                    goal="Create beautiful, comprehensive, and user-friendly documentation",
                    backstory="""You are Sakura (🌸), an artist of documentation. Like cherry blossoms 
                    bringing beauty to spring, you bring clarity and elegance to technical documentation. 
                    Your writing transforms complex technical concepts into accessible, engaging content 
                    that developers love to read.""",
                    verbose=self.verbose,
                    allow_delegation=False,
                    llm=sakura_llm,
                    tools=[self.file_read_tool, self.dir_read_tool]
                )
                self.initialized_agents.append("🌸 Sakura (Documentation)")
                print("✅ 🌸 Sakura initialized (Gemini 1.5 Flash - FREE TIER)")
            except Exception as e:
                print(f"⚠️  Could not initialize Sakura: {e}")
        else:
            print("⚠️  Sakura not initialized (GOOGLE_API_KEY not set)")
        
        # 🏗️ Kenji - Architecture Specialist (GPT-4o)
        if openai_key:
            try:
                kenji_llm = LLM(
                    model="gpt-4o",
                    api_key=openai_key,
                    temperature=0.4
                )
                self.agents["kenji"] = Agent(
                    role="Architecture Specialist",
                    goal="Design scalable, maintainable, and elegant system architectures",
                    backstory="""You are Kenji (🏗️), a visionary architect who sees the big picture. 
                    Like a master builder designing magnificent structures, you craft software architectures 
                    that stand the test of time. You understand patterns, scalability, and how to build 
                    systems that grow with their users.""",
                    verbose=self.verbose,
                    allow_delegation=False,
                    llm=kenji_llm,
                    tools=[self.file_read_tool, self.dir_read_tool]
                )
                self.initialized_agents.append("🏗️ Kenji (Architecture)")
                print("✅ 🏗️ Kenji initialized (GPT-4o)")
            except Exception as e:
                print(f"⚠️  Could not initialize Kenji: {e}")
        else:
            print("⚠️  Kenji not initialized (OPENAI_API_KEY not set)")
        
        print()
        print(f"✅ Initialized {len(self.initialized_agents)}/5 agents")
        if self.initialized_agents:
            print("   Active agents:", ", ".join(self.initialized_agents))
        print()
    
    def analyze_pr(self, pr_number: int) -> Dict[str, Any]:
        """
        Analyze a Pull Request with all relevant agents.
        
        Workflow:
        1. Akira: Code review (security, performance, quality)
        2. Yuki: Test coverage analysis
        3. Hiro: Infrastructure impact assessment
        4. Sakura: Documentation review
        5. Kenji: Architectural evaluation
        
        Args:
            pr_number: Pull request number to analyze
            
        Returns:
            Dict with comprehensive PR analysis
        """
        print("=" * 70)
        print(f"📊 PR Analysis Workflow for PR #{pr_number}")
        print("=" * 70)
        print()
        
        results = {
            "pr_number": pr_number,
            "timestamp": datetime.now().isoformat(),
            "agent_results": {}
        }
        
        # Task 1: Akira - Code Review
        if "akira" in self.agents:
            print("侍 Akira analyzing code quality...")
            akira_task = Task(
                description=f"""Review Pull Request #{pr_number} for:
                1. Security vulnerabilities and potential exploits
                2. Performance issues and optimization opportunities
                3. Code quality and maintainability concerns
                4. Best practices compliance
                
                Provide specific line-by-line feedback with severity ratings.""",
                agent=self.agents["akira"],
                expected_output="Detailed code review with security, performance, and quality findings"
            )
            akira_crew = Crew(
                agents=[self.agents["akira"]],
                tasks=[akira_task],
                verbose=self.verbose
            )
            try:
                akira_result = akira_crew.kickoff()
                results["agent_results"]["akira"] = str(akira_result)
                print("✅ Akira analysis complete\n")
            except Exception as e:
                results["agent_results"]["akira"] = f"Error: {str(e)}"
                print(f"❌ Akira analysis failed: {e}\n")
        
        # Task 2: Yuki - Test Coverage
        if "yuki" in self.agents:
            print("❄️ Yuki analyzing test coverage...")
            yuki_task = Task(
                description=f"""Analyze test coverage for PR #{pr_number}:
                1. Identify untested code paths
                2. Review existing test quality
                3. Suggest additional test cases
                4. Check for edge cases and error handling
                
                Provide specific recommendations for improving test coverage.""",
                agent=self.agents["yuki"],
                expected_output="Test coverage analysis with recommendations for improvement"
            )
            yuki_crew = Crew(
                agents=[self.agents["yuki"]],
                tasks=[yuki_task],
                verbose=self.verbose
            )
            try:
                yuki_result = yuki_crew.kickoff()
                results["agent_results"]["yuki"] = str(yuki_result)
                print("✅ Yuki analysis complete\n")
            except Exception as e:
                results["agent_results"]["yuki"] = f"Error: {str(e)}"
                print(f"❌ Yuki analysis failed: {e}\n")
        
        # Task 3: Hiro - Infrastructure Impact
        if "hiro" in self.agents:
            print("🛡️ Hiro analyzing infrastructure impact...")
            hiro_task = Task(
                description=f"""Assess infrastructure impact of PR #{pr_number}:
                1. Review CI/CD pipeline changes
                2. Check deployment configuration updates
                3. Analyze resource usage implications
                4. Identify potential reliability concerns
                
                Provide recommendations for infrastructure improvements.""",
                agent=self.agents["hiro"],
                expected_output="Infrastructure impact assessment with deployment recommendations"
            )
            hiro_crew = Crew(
                agents=[self.agents["hiro"]],
                tasks=[hiro_task],
                verbose=self.verbose
            )
            try:
                hiro_result = hiro_crew.kickoff()
                results["agent_results"]["hiro"] = str(hiro_result)
                print("✅ Hiro analysis complete\n")
            except Exception as e:
                results["agent_results"]["hiro"] = f"Error: {str(e)}"
                print(f"❌ Hiro analysis failed: {e}\n")
        
        # Task 4: Sakura - Documentation Review
        if "sakura" in self.agents:
            print("🌸 Sakura reviewing documentation...")
            sakura_task = Task(
                description=f"""Review documentation for PR #{pr_number}:
                1. Check if code changes are properly documented
                2. Review inline comments and docstrings
                3. Assess README and guide updates
                4. Suggest documentation improvements
                
                Provide specific recommendations for better documentation.""",
                agent=self.agents["sakura"],
                expected_output="Documentation review with improvement suggestions"
            )
            sakura_crew = Crew(
                agents=[self.agents["sakura"]],
                tasks=[sakura_task],
                verbose=self.verbose
            )
            try:
                sakura_result = sakura_crew.kickoff()
                results["agent_results"]["sakura"] = str(sakura_result)
                print("✅ Sakura analysis complete\n")
            except Exception as e:
                results["agent_results"]["sakura"] = f"Error: {str(e)}"
                print(f"❌ Sakura analysis failed: {e}\n")
        
        # Task 5: Kenji - Architecture Evaluation
        if "kenji" in self.agents:
            print("🏗️ Kenji evaluating architecture...")
            kenji_task = Task(
                description=f"""Evaluate architecture changes in PR #{pr_number}:
                1. Review system design modifications
                2. Assess scalability implications
                3. Check design pattern usage
                4. Identify potential architectural improvements
                
                Provide high-level architectural guidance.""",
                agent=self.agents["kenji"],
                expected_output="Architectural evaluation with design recommendations"
            )
            kenji_crew = Crew(
                agents=[self.agents["kenji"]],
                tasks=[kenji_task],
                verbose=self.verbose
            )
            try:
                kenji_result = kenji_crew.kickoff()
                results["agent_results"]["kenji"] = str(kenji_result)
                print("✅ Kenji analysis complete\n")
            except Exception as e:
                results["agent_results"]["kenji"] = f"Error: {str(e)}"
                print(f"❌ Kenji analysis failed: {e}\n")
        
        # Save results
        output_file = self.output_dir / f"pr_{pr_number}_analysis.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        
        print("=" * 70)
        print(f"✅ PR Analysis Complete!")
        print(f"📁 Results saved to: {output_file}")
        print("=" * 70)
        
        return results
    
    def cleanup_repository(self) -> Dict[str, Any]:
        """
        Execute repository cleanup workflow.
        
        Workflow:
        1. Hiro: Branch analysis (identify stale/merged branches)
        2. Akira: PR categorization (ready/needs-review/close)
        3. Sakura: Documentation audit and consolidation
        4. Kenji: Q1 2026 roadmap creation
        
        Returns:
            Dict with cleanup recommendations
        """
        print("=" * 70)
        print("🧹 Repository Cleanup Workflow")
        print("=" * 70)
        print()
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "cleanup_tasks": {}
        }
        
        # Task 1: Hiro - Branch Analysis
        if "hiro" in self.agents:
            print("🛡️ Hiro analyzing branches...")
            hiro_task = Task(
                description="""Analyze repository branches:
                1. Identify stale branches (no activity in 30+ days)
                2. Find merged branches that can be deleted
                3. Review branch naming conventions
                4. Suggest branch cleanup strategy
                
                Provide actionable recommendations with specific branch names.""",
                agent=self.agents["hiro"],
                expected_output="Branch analysis with cleanup recommendations"
            )
            hiro_crew = Crew(
                agents=[self.agents["hiro"]],
                tasks=[hiro_task],
                verbose=self.verbose
            )
            try:
                hiro_result = hiro_crew.kickoff()
                results["cleanup_tasks"]["branch_cleanup"] = str(hiro_result)
                print("✅ Branch analysis complete\n")
            except Exception as e:
                results["cleanup_tasks"]["branch_cleanup"] = f"Error: {str(e)}"
                print(f"❌ Branch analysis failed: {e}\n")
        
        # Task 2: Akira - PR Categorization
        if "akira" in self.agents:
            print("侍 Akira categorizing PRs...")
            akira_task = Task(
                description="""Categorize open Pull Requests:
                1. Identify PRs ready to merge
                2. List PRs needing review/updates
                3. Find PRs that should be closed
                4. Prioritize critical PRs
                
                Provide PR numbers with clear recommendations.""",
                agent=self.agents["akira"],
                expected_output="PR categorization with merge/review/close recommendations"
            )
            akira_crew = Crew(
                agents=[self.agents["akira"]],
                tasks=[akira_task],
                verbose=self.verbose
            )
            try:
                akira_result = akira_crew.kickoff()
                results["cleanup_tasks"]["pr_categorization"] = str(akira_result)
                print("✅ PR categorization complete\n")
            except Exception as e:
                results["cleanup_tasks"]["pr_categorization"] = f"Error: {str(e)}"
                print(f"❌ PR categorization failed: {e}\n")
        
        # Task 3: Sakura - Documentation Audit
        if "sakura" in self.agents:
            print("🌸 Sakura auditing documentation...")
            sakura_task = Task(
                description="""Audit repository documentation:
                1. Review all README files
                2. Check for outdated documentation
                3. Identify missing documentation
                4. Suggest documentation consolidation
                
                Provide specific files and improvements needed.""",
                agent=self.agents["sakura"],
                expected_output="Documentation audit with consolidation recommendations"
            )
            sakura_crew = Crew(
                agents=[self.agents["sakura"]],
                tasks=[sakura_task],
                verbose=self.verbose
            )
            try:
                sakura_result = sakura_crew.kickoff()
                results["cleanup_tasks"]["documentation_audit"] = str(sakura_result)
                print("✅ Documentation audit complete\n")
            except Exception as e:
                results["cleanup_tasks"]["documentation_audit"] = f"Error: {str(e)}"
                print(f"❌ Documentation audit failed: {e}\n")
        
        # Task 4: Kenji - Roadmap Creation
        if "kenji" in self.agents:
            print("🏗️ Kenji creating Q1 2026 roadmap...")
            kenji_task = Task(
                description="""Create Q1 2026 roadmap:
                1. Review current project status
                2. Identify technical debt priorities
                3. Suggest feature development priorities
                4. Create quarterly milestone plan
                
                Provide structured roadmap with timelines.""",
                agent=self.agents["kenji"],
                expected_output="Q1 2026 roadmap with prioritized initiatives"
            )
            kenji_crew = Crew(
                agents=[self.agents["kenji"]],
                tasks=[kenji_task],
                verbose=self.verbose
            )
            try:
                kenji_result = kenji_crew.kickoff()
                results["cleanup_tasks"]["q1_2026_roadmap"] = str(kenji_result)
                print("✅ Roadmap creation complete\n")
            except Exception as e:
                results["cleanup_tasks"]["q1_2026_roadmap"] = f"Error: {str(e)}"
                print(f"❌ Roadmap creation failed: {e}\n")
        
        # Save results
        output_file = self.output_dir / "cleanup_plan.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        
        print("=" * 70)
        print(f"✅ Cleanup Analysis Complete!")
        print(f"📁 Results saved to: {output_file}")
        print("=" * 70)
        
        return results
    
    def generate_documentation(self) -> Dict[str, Any]:
        """
        Generate comprehensive documentation.
        
        Workflow:
        1. Sakura: Scan repository and generate documentation
        
        Returns:
            Dict with documentation generation results
        """
        print("=" * 70)
        print("📚 Documentation Generation Workflow")
        print("=" * 70)
        print()
        
        if "sakura" not in self.agents:
            print("❌ Sakura not initialized - cannot generate documentation")
            return {"error": "Sakura agent not available"}
        
        results = {
            "timestamp": datetime.now().isoformat()
        }
        
        print("🌸 Sakura generating comprehensive documentation...")
        sakura_task = Task(
            description="""Generate comprehensive repository documentation:
            1. Project overview and purpose
            2. Architecture documentation with diagrams
            3. API documentation
            4. Setup and installation guides
            5. Developer contribution guidelines
            6. Agent system documentation
            
            Create well-structured Markdown documentation.""",
            agent=self.agents["sakura"],
            expected_output="Complete repository documentation in Markdown format"
        )
        sakura_crew = Crew(
            agents=[self.agents["sakura"]],
            tasks=[sakura_task],
            verbose=self.verbose
        )
        
        try:
            sakura_result = sakura_crew.kickoff()
            results["documentation"] = str(sakura_result)
            
            # Save as markdown
            output_file = self.output_dir / "consolidated_docs.md"
            with open(output_file, "w") as f:
                f.write(str(sakura_result))
            
            print("✅ Documentation generation complete\n")
            print("=" * 70)
            print(f"✅ Documentation Generated!")
            print(f"📁 Saved to: {output_file}")
            print("=" * 70)
        except Exception as e:
            results["error"] = str(e)
            print(f"❌ Documentation generation failed: {e}")
        
        return results
    
    def list_agents_info(self):
        """Display information about all agents."""
        print("=" * 70)
        print("🤖 Tokyo-IA Agent System")
        print("=" * 70)
        print()
        
        agents_info = [
            {
                "emoji": "侍",
                "name": "Akira",
                "id": "akira-001",
                "role": "Code Review Master",
                "model": "Claude 3.5 Sonnet",
                "specialties": ["Security", "Performance", "Architecture"],
                "initialized": "akira" in self.agents
            },
            {
                "emoji": "❄️",
                "name": "Yuki",
                "id": "yuki-002",
                "role": "Test Engineering Specialist",
                "model": "GPT-4o mini",
                "specialties": ["Unit Testing", "Integration Testing", "E2E Testing"],
                "initialized": "yuki" in self.agents
            },
            {
                "emoji": "🛡️",
                "name": "Hiro",
                "id": "hiro-003",
                "role": "SRE & DevOps Expert",
                "model": "Llama 3.3 70B (Groq FREE)",
                "specialties": ["Kubernetes", "CI/CD", "Monitoring"],
                "initialized": "hiro" in self.agents
            },
            {
                "emoji": "🌸",
                "name": "Sakura",
                "id": "sakura-004",
                "role": "Documentation Specialist",
                "model": "Gemini 1.5 Flash (Google FREE)",
                "specialties": ["Technical Writing", "Diagrams", "User Guides"],
                "initialized": "sakura" in self.agents
            },
            {
                "emoji": "🏗️",
                "name": "Kenji",
                "id": "kenji-005",
                "role": "Architecture Specialist",
                "model": "GPT-4o",
                "specialties": ["System Design", "Patterns", "Scalability"],
                "initialized": "kenji" in self.agents
            }
        ]
        
        for agent in agents_info:
            status = "✅ ACTIVE" if agent["initialized"] else "❌ NOT INITIALIZED"
            print(f"{agent['emoji']} {agent['name']} ({agent['id']})")
            print(f"   Role: {agent['role']}")
            print(f"   Model: {agent['model']}")
            print(f"   Specialties: {', '.join(agent['specialties'])}")
            print(f"   Status: {status}")
            print()
        
        print("=" * 70)
        print(f"Active Agents: {len(self.agents)}/5")
        print("=" * 70)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Tokyo-IA CrewAI Agent Orchestration System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analyze-pr 126        Analyze Pull Request #126
  %(prog)s cleanup               Execute repository cleanup
  %(prog)s generate-docs         Generate comprehensive documentation
  %(prog)s list-agents           Show all available agents

Environment Variables:
  ANTHROPIC_API_KEY    API key for Akira (Claude 3.5 Sonnet)
  OPENAI_API_KEY       API key for Yuki (GPT-4o mini) and Kenji (GPT-4o)
  GROQ_API_KEY         API key for Hiro (Llama 3.3 70B) [FREE TIER]
  GOOGLE_API_KEY       API key for Sakura (Gemini 1.5 Flash) [FREE TIER]
        """
    )
    
    parser.add_argument(
        "command",
        choices=["analyze-pr", "cleanup", "generate-docs", "list-agents"],
        help="Command to execute"
    )
    parser.add_argument(
        "pr_number",
        nargs="?",
        type=int,
        help="PR number (required for analyze-pr)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=True,
        help="Enable verbose output (default: True)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Disable verbose output"
    )
    
    args = parser.parse_args()
    
    # Handle verbose/quiet flags
    verbose = args.verbose and not args.quiet
    
    # Initialize Tokyo Crew
    crew = TokyoCrew(verbose=verbose)
    
    # Execute command
    if args.command == "list-agents":
        crew.list_agents_info()
    elif args.command == "analyze-pr":
        if not args.pr_number:
            print("❌ Error: PR number required for analyze-pr command")
            print("Usage: python agents/tokyo_crew.py analyze-pr <pr_number>")
            sys.exit(1)
        crew.analyze_pr(args.pr_number)
    elif args.command == "cleanup":
        crew.cleanup_repository()
    elif args.command == "generate-docs":
        crew.generate_documentation()
    
    print()
    print("✨ Tokyo-IA Agent System execution complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
