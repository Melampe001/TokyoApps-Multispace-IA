#!/usr/bin/env python3
"""
Tokyo-IA Agent Orchestration - Example Usage

This script demonstrates how to use the Tokyo-IA agent orchestration system.

Prerequisites:
1. PostgreSQL database running with schema loaded
2. Registry API server running on localhost:8080
3. API keys set as environment variables

Usage:
    export ANTHROPIC_API_KEY="sk-ant-..."
    export OPENAI_API_KEY="sk-..."
    export GROQ_API_KEY="gsk_..."
    export GOOGLE_API_KEY="..."
    
    python examples/orchestration_demo.py
"""

import os
import sys

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.orchestrator import AgentOrchestrator
from lib.agents.specialized import list_agents


def main():
    """Demonstrate the Tokyo-IA agent orchestration system."""
    
    print("=" * 70)
    print("🗼 Tokyo-IA Agent Orchestration System Demo")
    print("=" * 70)
    print()
    
    # Check environment
    print("📋 Checking environment...")
    registry_url = os.environ.get("REGISTRY_API_URL", "http://localhost:8080")
    print(f"   Registry API: {registry_url}")
    
    api_keys = {
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY"),
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
        "GROQ_API_KEY": os.environ.get("GROQ_API_KEY"),
        "GOOGLE_API_KEY": os.environ.get("GOOGLE_API_KEY"),
    }
    
    available_keys = sum(1 for k, v in api_keys.items() if v)
    print(f"   API Keys: {available_keys}/4 configured")
    
    if available_keys == 0:
        print()
        print("❌ No API keys found!")
        print("   Please set at least one API key:")
        print("   - ANTHROPIC_API_KEY for Akira (Code Review)")
        print("   - OPENAI_API_KEY for Yuki & Kenji (Testing & Architecture)")
        print("   - GROQ_API_KEY for Hiro (SRE/DevOps)")
        print("   - GOOGLE_API_KEY for Sakura (Documentation)")
        return 1
    
    print()
    
    # List available agents
    print("👥 Available Agents:")
    agents_info = list_agents()
    for agent_id, info in agents_info.items():
        print(f"   {info['emoji']} {info['name']} - {info['role']}")
    print()
    
    # Initialize orchestrator
    print("🔧 Initializing orchestrator...")
    orchestrator = AgentOrchestrator(registry_api_url=registry_url)
    
    try:
        orchestrator.initialize_agents(
            anthropic_api_key=api_keys.get("ANTHROPIC_API_KEY"),
            openai_api_key=api_keys.get("OPENAI_API_KEY"),
            groq_api_key=api_keys.get("GROQ_API_KEY"),
            google_api_key=api_keys.get("GOOGLE_API_KEY")
        )
    except Exception as e:
        print(f"⚠️  Warning during initialization: {e}")
    
    print()
    
    # Show initialized agents
    print("✅ Initialized Agents:")
    available = orchestrator.list_available_agents()
    for agent_id, info in available.items():
        status = "✅" if info['initialized'] else "❌"
        print(f"   {status} {info['emoji']} {info['name']}")
    print()
    
    # Example workflow (only if we have agents initialized)
    initialized_count = sum(1 for info in available.values() if info['initialized'])
    
    if initialized_count == 0:
        print("⚠️  No agents initialized - cannot run workflows")
        print("   Please check your API keys and try again")
        return 1
    
    print("=" * 70)
    print("Example: Code Review Workflow")
    print("=" * 70)
    print()
    
    # Example code with security issue
    example_code = '''
def authenticate_user(username, password):
    """Authenticate a user (WARNING: This code has security issues!)"""
    # Security issue: SQL injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    result = database.execute(query)
    
    if result:
        return True
    return False
'''
    
    print("📝 Code to review:")
    print(example_code)
    print()
    
    # Create workflow
    print("🔄 Creating workflow...")
    workflow_id = orchestrator.create_workflow(
        name="Example Code Review",
        description="Demo of security audit on example code",
        workflow_type="demo"
    )
    print(f"   Workflow ID: {workflow_id}")
    print()
    
    # Run tasks based on available agents
    tasks = []
    
    if "akira-001" in orchestrator.agents:
        print("侍 Running Akira's security audit...")
        tasks.append({
            "agent_id": "akira-001",
            "task_type": "security_audit",
            "description": "Security audit of authentication code",
            "method": "security_audit",
            "args": [example_code, "python"]
        })
    
    if "yuki-002" in orchestrator.agents:
        print("❄️ Running Yuki's test generation...")
        tasks.append({
            "agent_id": "yuki-002",
            "task_type": "unit_tests",
            "description": "Generate unit tests",
            "method": "generate_unit_tests",
            "args": [example_code, "python", "pytest"]
        })
    
    if tasks:
        print()
        print("⏳ Executing workflow...")
        print()
        
        result = orchestrator.run_workflow(workflow_id, tasks)
        
        print()
        print("=" * 70)
        print("📊 Workflow Results")
        print("=" * 70)
        print(f"Status: {result['status']}")
        print(f"Total Tasks: {result['total_tasks']}")
        print(f"Completed: {result['completed_tasks']}")
        print(f"Failed: {result['failed_tasks']}")
        print()
        
        for i, task_result in enumerate(result['results'], 1):
            if task_result['success']:
                print(f"✅ Task {i}: {task_result['agent_name']} - Success")
                print(f"   Duration: {task_result['duration_ms']}ms")
                if 'result' in task_result:
                    result_preview = str(task_result['result'].get('result', ''))[:200]
                    print(f"   Result preview: {result_preview}...")
            else:
                print(f"❌ Task {i}: {task_result['agent_name']} - Failed")
                print(f"   Error: {task_result['error']}")
            print()
    else:
        print("⚠️  No tasks could be executed (no agents initialized)")
    
    print("=" * 70)
    print("✨ Demo completed!")
    print()
    print("Next steps:")
    print("- Check the Registry API at http://localhost:8080/api/agents")
    print("- View workflows at http://localhost:8080/api/workflows")
    print("- Read the docs at docs/agents/ORCHESTRATION.md")
    print("- Try other workflows in lib/orchestrator/workflows.py")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
