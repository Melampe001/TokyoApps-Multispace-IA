#!/usr/bin/env python3
"""
Tokyo-IA Agent Dashboard - Real-time Monitoring

Real-time terminal UI for monitoring agent execution progress.
Shows status, progress, and resource usage for all 5 agents.

Usage:
    python agents/agent_dashboard.py

Requirements:
    - rich library for terminal UI
    - At least one API key configured
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

try:
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import box
except ImportError:
    print("❌ Error: 'rich' library not installed")
    print("Install with: pip install rich")
    sys.exit(1)


class AgentDashboard:
    """Real-time monitoring dashboard for Tokyo-IA agents."""
    
    def __init__(self):
        self.console = Console()
        self.agents_status = {
            "akira": {"name": "侍 Akira", "status": "Initializing", "model": "Claude 3.5 Sonnet"},
            "yuki": {"name": "❄️ Yuki", "status": "Initializing", "model": "GPT-4o mini"},
            "hiro": {"name": "🛡️ Hiro", "status": "Initializing", "model": "Llama 3.3 70B [FREE]"},
            "sakura": {"name": "🌸 Sakura", "status": "Initializing", "model": "Gemini 1.5 Flash [FREE]"},
            "kenji": {"name": "🏗️ Kenji", "status": "Initializing", "model": "GPT-4o"}
        }
        self.workflow_status = []
        self.start_time = datetime.now()
    
    def check_api_keys(self) -> Dict[str, bool]:
        """Check which API keys are configured."""
        return {
            "ANTHROPIC_API_KEY": bool(os.environ.get("ANTHROPIC_API_KEY")),
            "OPENAI_API_KEY": bool(os.environ.get("OPENAI_API_KEY")),
            "GROQ_API_KEY": bool(os.environ.get("GROQ_API_KEY")),
            "GOOGLE_API_KEY": bool(os.environ.get("GOOGLE_API_KEY"))
        }
    
    def update_agent_status(self):
        """Update agent status based on API key availability."""
        api_keys = self.check_api_keys()
        
        # Akira needs Anthropic
        if api_keys["ANTHROPIC_API_KEY"]:
            self.agents_status["akira"]["status"] = "✅ Ready"
        else:
            self.agents_status["akira"]["status"] = "❌ No API Key"
        
        # Yuki and Kenji need OpenAI
        if api_keys["OPENAI_API_KEY"]:
            self.agents_status["yuki"]["status"] = "✅ Ready"
            self.agents_status["kenji"]["status"] = "✅ Ready"
        else:
            self.agents_status["yuki"]["status"] = "❌ No API Key"
            self.agents_status["kenji"]["status"] = "❌ No API Key"
        
        # Hiro needs Groq
        if api_keys["GROQ_API_KEY"]:
            self.agents_status["hiro"]["status"] = "✅ Ready"
        else:
            self.agents_status["hiro"]["status"] = "❌ No API Key"
        
        # Sakura needs Google
        if api_keys["GOOGLE_API_KEY"]:
            self.agents_status["sakura"]["status"] = "✅ Ready"
        else:
            self.agents_status["sakura"]["status"] = "❌ No API Key"
    
    def get_report_directories(self) -> List[Path]:
        """Get list of agent report directories."""
        report_dirs = sorted(Path(".").glob("agent_reports_*"), reverse=True)
        return list(report_dirs)[:5]  # Latest 5
    
    def create_agents_table(self) -> Table:
        """Create table showing agent status."""
        table = Table(title="🤖 Tokyo-IA Agents", box=box.ROUNDED, show_header=True)
        
        table.add_column("Agent", style="cyan")
        table.add_column("Model", style="yellow")
        table.add_column("Status", style="green")
        table.add_column("Type", style="magenta")
        
        for agent_id, info in self.agents_status.items():
            is_free = "[FREE]" in info["model"]
            agent_type = "FREE 💚" if is_free else "Paid 💰"
            table.add_row(
                info["name"],
                info["model"],
                info["status"],
                agent_type
            )
        
        return table
    
    def create_api_keys_table(self) -> Table:
        """Create table showing API key configuration."""
        table = Table(title="🔑 API Keys", box=box.ROUNDED)
        
        table.add_column("Provider", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Agents", style="yellow")
        
        api_keys = self.check_api_keys()
        
        configs = [
            ("Anthropic", "ANTHROPIC_API_KEY", "Akira"),
            ("OpenAI", "OPENAI_API_KEY", "Yuki, Kenji"),
            ("Groq [FREE]", "GROQ_API_KEY", "Hiro"),
            ("Google [FREE]", "GOOGLE_API_KEY", "Sakura")
        ]
        
        for provider, key, agents in configs:
            status = "✅ Configured" if api_keys[key] else "❌ Not Set"
            table.add_row(provider, status, agents)
        
        return table
    
    def create_reports_table(self) -> Table:
        """Create table showing recent report directories."""
        table = Table(title="📊 Recent Reports", box=box.ROUNDED)
        
        table.add_column("Directory", style="cyan")
        table.add_column("Files", style="yellow")
        table.add_column("Size", style="green")
        
        report_dirs = self.get_report_directories()
        
        if not report_dirs:
            table.add_row("No reports yet", "-", "-")
        else:
            for report_dir in report_dirs:
                files = list(report_dir.glob("*"))
                file_count = len(files)
                
                # Calculate total size
                total_size = sum(f.stat().st_size for f in files if f.is_file())
                size_str = f"{total_size / 1024:.1f} KB"
                
                table.add_row(report_dir.name, str(file_count), size_str)
        
        return table
    
    def create_system_info(self) -> Panel:
        """Create panel with system information."""
        api_keys = self.check_api_keys()
        active_count = sum(1 for v in api_keys.values() if v)
        
        uptime = datetime.now() - self.start_time
        uptime_str = f"{uptime.seconds // 60}m {uptime.seconds % 60}s"
        
        info_text = f"""
[cyan]System Status[/cyan]
  • Python: {sys.version.split()[0]}
  • Active Agents: {active_count}/4 providers
  • Uptime: {uptime_str}
  • Time: {datetime.now().strftime('%H:%M:%S')}

[cyan]Quick Commands[/cyan]
  • Test APIs: python agents/test_free_apis.py
  • Run cleanup: python agents/tokyo_crew.py cleanup
  • Generate docs: python agents/tokyo_crew.py generate-docs
        """
        
        return Panel(info_text.strip(), title="ℹ️  System Info", box=box.ROUNDED)
    
    def generate_layout(self) -> Layout:
        """Generate the complete dashboard layout."""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=1)
        )
        
        layout["header"].update(
            Panel("[bold]🗼 Tokyo-IA Agent Dashboard[/bold]", style="bold blue")
        )
        
        layout["body"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        layout["left"].split_column(
            Layout(name="agents"),
            Layout(name="api_keys")
        )
        
        layout["right"].split_column(
            Layout(name="system"),
            Layout(name="reports")
        )
        
        # Populate layouts
        layout["agents"].update(self.create_agents_table())
        layout["api_keys"].update(self.create_api_keys_table())
        layout["system"].update(self.create_system_info())
        layout["reports"].update(self.create_reports_table())
        
        layout["footer"].update("[dim]Press Ctrl+C to exit | Updates every 2 seconds[/dim]")
        
        return layout
    
    def run(self):
        """Run the dashboard with live updates."""
        self.console.clear()
        
        with Live(self.generate_layout(), refresh_per_second=0.5, console=self.console) as live:
            try:
                while True:
                    self.update_agent_status()
                    live.update(self.generate_layout())
                    time.sleep(2)
            except KeyboardInterrupt:
                pass


def main():
    """Main entry point."""
    print("🗼 Tokyo-IA Agent Dashboard")
    print("=" * 70)
    print()
    print("Initializing dashboard...")
    print()
    
    # Initialize and run dashboard
    dashboard = AgentDashboard()
    
    try:
        dashboard.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Dashboard stopped by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n✨ Dashboard closed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
