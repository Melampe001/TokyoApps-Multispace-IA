#!/usr/bin/env python3
"""
Tokyo-IA Agent Orchestrator

Multi-agent workflow orchestration system that coordinates the 5 specialized agents:
- Akira (侍) - Code Review Master
- Yuki (❄️) - Test Engineering Specialist
- Hiro (🛡️) - SRE & DevOps Guardian
- Sakura (🌸) - Documentation Artist
- Kenji (🏗️) - Architecture Visionary

Features:
- Workflow management and coordination
- Dependency handling between tasks
- Automatic logging to registry API
- Error handling and retries
- Progress tracking
"""

import os
import time
import requests
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from uuid import UUID, uuid4

from lib.agents.specialized import (
    AGENTS
)


class TaskStatus:
    """Task status constants."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowStatus:
    """Workflow status constants."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentOrchestrator:
    """Orchestrates multiple AI agents in coordinated workflows."""
    
    def __init__(self, registry_api_url: str = None):
        """
        Initialize the agent orchestrator.
        
        Args:
            registry_api_url: URL of the registry API (default: from env or localhost)
        """
        self.registry_api_url = registry_api_url or os.environ.get(
            "REGISTRY_API_URL", 
            "http://localhost:8080"
        )
        self.agents = {}
        self.workflows = {}
        
    def initialize_agents(self, agent_ids: List[str] = None, **api_keys):
        """
        Initialize specified agents.
        
        Args:
            agent_ids: List of agent IDs to initialize (default: all)
            **api_keys: API keys for different services (anthropic_api_key, openai_api_key, etc.)
        """
        if agent_ids is None:
            agent_ids = list(AGENTS.keys())
        
        for agent_id in agent_ids:
            if agent_id not in AGENTS:
                print(f"⚠️  Unknown agent ID: {agent_id}")
                continue
            
            agent_info = AGENTS[agent_id]
            agent_class = agent_info['class']
            
            try:
                # Determine which API key to use based on agent
                api_key = None
                if agent_id == 'akira-001':
                    api_key = api_keys.get('anthropic_api_key') or os.environ.get('ANTHROPIC_API_KEY')
                elif agent_id in ['yuki-002', 'kenji-005']:
                    api_key = api_keys.get('openai_api_key') or os.environ.get('OPENAI_API_KEY')
                elif agent_id == 'hiro-003':
                    api_key = api_keys.get('groq_api_key') or os.environ.get('GROQ_API_KEY')
                elif agent_id == 'sakura-004':
                    api_key = api_keys.get('google_api_key') or os.environ.get('GOOGLE_API_KEY')
                
                if api_key:
                    self.agents[agent_id] = agent_class(api_key=api_key)
                    print(f"✅ {agent_info['emoji']} {agent_info['name']} initialized")
                else:
                    print(f"⚠️  {agent_info['emoji']} {agent_info['name']} - API key not found")
                    
            except Exception as e:
                print(f"❌ Failed to initialize {agent_info['name']}: {e}")
    
    def create_workflow(self, name: str, description: str = "", 
                       workflow_type: str = "custom", initiator: str = "orchestrator") -> UUID:
        """
        Create a new workflow in the registry.
        
        Args:
            name: Workflow name
            description: Workflow description
            workflow_type: Type of workflow
            initiator: Who initiated the workflow
            
        Returns:
            Workflow ID (UUID)
        """
        try:
            response = requests.post(
                f"{self.registry_api_url}/api/workflows",
                json={
                    "name": name,
                    "description": description,
                    "workflow_type": workflow_type,
                    "initiator": initiator
                },
                timeout=10
            )
            response.raise_for_status()
            
            workflow_data = response.json()
            workflow_id = UUID(workflow_data['id'])
            
            self.workflows[workflow_id] = {
                "name": name,
                "status": WorkflowStatus.PENDING,
                "tasks": [],
                "created_at": datetime.now().isoformat()
            }
            
            print(f"🔄 Created workflow: {name} (ID: {workflow_id})")
            return workflow_id
            
        except Exception as e:
            print(f"❌ Failed to create workflow: {e}")
            # Fallback to local tracking
            workflow_id = uuid4()
            self.workflows[workflow_id] = {
                "name": name,
                "status": WorkflowStatus.PENDING,
                "tasks": [],
                "created_at": datetime.now().isoformat()
            }
            return workflow_id
    
    def execute_task(self, agent_id: str, task_func: Callable, 
                    task_type: str, description: str,
                    workflow_id: Optional[UUID] = None, 
                    *args, **kwargs) -> Dict[str, Any]:
        """
        Execute a task with an agent and log to registry.
        
        Args:
            agent_id: Agent ID to execute the task
            task_func: Agent method to call
            task_type: Type of task
            description: Task description
            workflow_id: Optional workflow ID
            *args, **kwargs: Arguments for the task function
            
        Returns:
            Task execution result
        """
        if agent_id not in self.agents:
            return {
                "success": False,
                "error": f"Agent {agent_id} not initialized"
            }
        
        agent_info = AGENTS[agent_id]
        
        # Create task in registry
        task_id = None
        try:
            response = requests.post(
                f"{self.registry_api_url}/api/tasks",
                json={
                    "agent_id": agent_id,
                    "workflow_id": str(workflow_id) if workflow_id else None,
                    "task_type": task_type,
                    "description": description,
                    "input_data": {
                        "args": str(args),
                        "kwargs": {k: str(v) for k, v in kwargs.items()}
                    }
                },
                timeout=10
            )
            
            if response.status_code == 201:
                task_data = response.json()
                task_id = UUID(task_data['id'])
                print(f"📝 Task created: {task_id}")
        except Exception as e:
            print(f"⚠️  Failed to create task in registry: {e}")
        
        # Execute the task
        print(f"\n🚀 Executing: {agent_info['emoji']} {agent_info['name']} - {description}")
        start_time = time.time()
        
        try:
            result = task_func(*args, **kwargs)
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Update task status in registry
            if task_id:
                try:
                    requests.put(
                        f"{self.registry_api_url}/api/tasks/{task_id}",
                        json={
                            "status": TaskStatus.COMPLETED,
                            "output_data": result,
                            "tokens_used": 0,  # Would need to extract from result
                            "cost_usd": 0.0
                        },
                        timeout=10
                    )
                except Exception as e:
                    print(f"⚠️  Failed to update task: {e}")
            
            print(f"✅ Completed in {duration_ms}ms")
            
            return {
                "success": True,
                "task_id": str(task_id) if task_id else None,
                "agent_id": agent_id,
                "agent_name": agent_info['name'],
                "result": result,
                "duration_ms": duration_ms
            }
            
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            error_msg = str(e)
            
            # Update task status in registry
            if task_id:
                try:
                    requests.put(
                        f"{self.registry_api_url}/api/tasks/{task_id}",
                        json={
                            "status": TaskStatus.FAILED,
                            "error_message": error_msg
                        },
                        timeout=10
                    )
                except Exception:
                    pass
            
            print(f"❌ Failed after {duration_ms}ms: {error_msg}")
            
            return {
                "success": False,
                "task_id": str(task_id) if task_id else None,
                "agent_id": agent_id,
                "agent_name": agent_info['name'],
                "error": error_msg,
                "duration_ms": duration_ms
            }
    
    def run_workflow(self, workflow_id: UUID, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute a workflow with multiple coordinated tasks.
        
        Args:
            workflow_id: Workflow ID
            tasks: List of task definitions
            
        Returns:
            Workflow execution results
        """
        if workflow_id not in self.workflows:
            return {"success": False, "error": "Workflow not found"}
        
        workflow = self.workflows[workflow_id]
        workflow["status"] = WorkflowStatus.RUNNING
        
        print(f"\n{'='*70}")
        print(f"🔄 Starting Workflow: {workflow['name']}")
        print(f"{'='*70}\n")
        
        results = []
        failed_tasks = 0
        
        for task_def in tasks:
            agent_id = task_def['agent_id']
            task_type = task_def['task_type']
            description = task_def['description']
            method_name = task_def['method']
            args = task_def.get('args', [])
            kwargs = task_def.get('kwargs', {})
            
            if agent_id not in self.agents:
                print(f"⚠️  Skipping task: Agent {agent_id} not initialized")
                continue
            
            # Get the agent method
            agent = self.agents[agent_id]
            task_func = getattr(agent, method_name)
            
            # Execute the task
            result = self.execute_task(
                agent_id, task_func, task_type, description,
                workflow_id, *args, **kwargs
            )
            
            results.append(result)
            
            if not result['success']:
                failed_tasks += 1
        
        # Update workflow status
        if failed_tasks == 0:
            workflow["status"] = WorkflowStatus.COMPLETED
            print("\n✅ Workflow completed successfully!")
        elif failed_tasks < len(tasks):
            workflow["status"] = WorkflowStatus.COMPLETED
            print(f"\n⚠️  Workflow completed with {failed_tasks} failed tasks")
        else:
            workflow["status"] = WorkflowStatus.FAILED
            print("\n❌ Workflow failed - all tasks failed")
        
        print(f"{'='*70}\n")
        
        return {
            "workflow_id": str(workflow_id),
            "workflow_name": workflow["name"],
            "status": workflow["status"],
            "total_tasks": len(tasks),
            "completed_tasks": len(tasks) - failed_tasks,
            "failed_tasks": failed_tasks,
            "results": results
        }
    
    def get_workflow_status(self, workflow_id: UUID) -> Dict[str, Any]:
        """Get the status of a workflow."""
        if workflow_id not in self.workflows:
            return {"error": "Workflow not found"}
        return self.workflows[workflow_id]
    
    def list_available_agents(self) -> Dict[str, Any]:
        """List all available agents and their status."""
        return {
            agent_id: {
                "name": AGENTS[agent_id]['name'],
                "emoji": AGENTS[agent_id]['emoji'],
                "role": AGENTS[agent_id]['role'],
                "specialties": AGENTS[agent_id]['specialties'],
                "initialized": agent_id in self.agents
            }
            for agent_id in AGENTS.keys()
        }


def main():
    """Example usage of the orchestrator."""
    print("🗼 Tokyo-IA Agent Orchestrator\n")
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator()
    
    # List available agents
    print("Available agents:")
    agents = orchestrator.list_available_agents()
    for agent_id, info in agents.items():
        status = "✅" if info['initialized'] else "❌"
        print(f"  {status} {info['emoji']} {info['name']} - {info['role']}")
    
    print("\n" + "="*70)
    print("Note: Initialize agents with API keys to use them")
    print("Example:")
    print("  orchestrator.initialize_agents(")
    print("      anthropic_api_key='...',")
    print("      openai_api_key='...',")
    print("      groq_api_key='...',")
    print("      google_api_key='...'")
    print("  )")
    print("="*70)


if __name__ == "__main__":
    main()
