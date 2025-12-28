"""
AI Agents endpoint for TokyoApps-Multispace-IA on Vercel.
Provides information about available agents and handles agent task requests.
"""

from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime


class handler(BaseHTTPRequestHandler):
    """AI Agents handler for Vercel serverless function."""

    def do_GET(self):
        """Handle GET requests - list available agents."""
        agents_data = {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_agents": 5,
            "agents": [
                {
                    "id": "akira-001",
                    "name": "Akira",
                    "role": "Code Review Master",
                    "model": "Claude Opus 4.1",
                    "specialties": ["Security", "Performance", "Architecture"],
                    "emoji": "侍",
                    "status": "available"
                },
                {
                    "id": "yuki-002",
                    "name": "Yuki",
                    "role": "Test Engineering",
                    "model": "OpenAI o3",
                    "specialties": ["Unit Testing", "Integration Testing", "E2E Testing"],
                    "emoji": "❄️",
                    "status": "available"
                },
                {
                    "id": "hiro-003",
                    "name": "Hiro",
                    "role": "SRE & DevOps",
                    "model": "Llama 4 405B",
                    "specialties": ["Kubernetes", "CI/CD", "Monitoring"],
                    "emoji": "🛡️",
                    "status": "available"
                },
                {
                    "id": "sakura-004",
                    "name": "Sakura",
                    "role": "Documentation",
                    "model": "Gemini 3.0 Ultra",
                    "specialties": ["Technical Writing", "Diagrams", "User Guides"],
                    "emoji": "🌸",
                    "status": "available"
                },
                {
                    "id": "kenji-005",
                    "name": "Kenji",
                    "role": "Architecture",
                    "model": "OpenAI o3",
                    "specialties": ["System Design", "Patterns", "Scalability"],
                    "emoji": "🏗️",
                    "status": "available"
                }
            ],
            "workflows": [
                "full_code_review_workflow",
                "new_feature_workflow",
                "production_deployment_workflow"
            ]
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(agents_data, indent=2).encode())

    def do_POST(self):
        """Handle POST requests - start agent task."""
        content_length = int(self.headers.get("Content-Length", 0))
        
        if content_length > 0:
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode())
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return
        else:
            self.send_error(400, "Request body required")
            return

        # Validate required fields
        required_fields = ["agent_id", "task_type"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            error_response = {
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing_fields)}",
                "required": required_fields
            }
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())
            return

        # Create task response
        response_data = {
            "status": "success",
            "message": "Task created successfully",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "task": {
                "id": f"task-{datetime.utcnow().timestamp()}",
                "agent_id": data.get("agent_id"),
                "task_type": data.get("task_type"),
                "payload": data.get("payload", {}),
                "status": "queued",
                "note": "Full task execution requires API keys configuration in Vercel environment variables"
            }
        }

        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data, indent=2).encode())

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
