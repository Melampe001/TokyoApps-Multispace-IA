"""
AI Agents endpoint for TokyoApps-Multispace-IA on Vercel.
Provides information about available agents and handles agent task requests.
"""

from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime


class handler(BaseHTTPRequestHandler):
    """AI Agents handler for Vercel serverless function."""

    def do_GET(self):
        """Handle GET requests - list available agents."""
        try:
            # Check which agents are available based on API keys
            agents_status = self._check_agent_availability()
            
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
                        "provider": "Anthropic",
                        "specialties": ["Security", "Performance", "Architecture"],
                        "emoji": "侍",
                        "status": agents_status.get("anthropic", "unavailable")
                    },
                    {
                        "id": "yuki-002",
                        "name": "Yuki",
                        "role": "Test Engineering",
                        "model": "OpenAI o3",
                        "provider": "OpenAI",
                        "specialties": ["Unit Testing", "Integration Testing", "E2E Testing"],
                        "emoji": "❄️",
                        "status": agents_status.get("openai", "unavailable")
                    },
                    {
                        "id": "hiro-003",
                        "name": "Hiro",
                        "role": "SRE & DevOps",
                        "model": "Llama 4 405B",
                        "provider": "Groq",
                        "specialties": ["Kubernetes", "CI/CD", "Monitoring"],
                        "emoji": "🛡️",
                        "status": agents_status.get("groq", "unavailable")
                    },
                    {
                        "id": "sakura-004",
                        "name": "Sakura",
                        "role": "Documentation",
                        "model": "Gemini 3.0 Ultra",
                        "provider": "Google",
                        "specialties": ["Technical Writing", "Diagrams", "User Guides"],
                        "emoji": "🌸",
                        "status": agents_status.get("google", "unavailable")
                    },
                    {
                        "id": "kenji-005",
                        "name": "Kenji",
                        "role": "Architecture",
                        "model": "OpenAI o3",
                        "provider": "OpenAI",
                        "specialties": ["System Design", "Patterns", "Scalability"],
                        "emoji": "🏗️",
                        "status": agents_status.get("openai", "unavailable")
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
            self.send_header("Cache-Control", "public, max-age=60")
            self.end_headers()
            self.wfile.write(json.dumps(agents_data, indent=2).encode())
            
        except Exception as e:
            self._send_error_response(500, f"Internal server error: {str(e)}")

    def do_POST(self):
        """Handle POST requests - start agent task."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            
            if content_length == 0:
                self._send_error_response(400, "Request body required")
                return
            
            if content_length > 10485760:  # 10MB limit
                self._send_error_response(413, "Request entity too large")
                return
            
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode())
            except json.JSONDecodeError as e:
                self._send_error_response(400, f"Invalid JSON: {str(e)}")
                return

            # Validate required fields
            required_fields = ["agent_id", "task_type"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                error_response = {
                    "status": "error",
                    "message": f"Missing required fields: {', '.join(missing_fields)}",
                    "required": required_fields,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Validate agent_id
            valid_agent_ids = ["akira-001", "yuki-002", "hiro-003", "sakura-004", "kenji-005"]
            if data["agent_id"] not in valid_agent_ids:
                self._send_error_response(400, f"Invalid agent_id. Must be one of: {', '.join(valid_agent_ids)}")
                return

            # Create task response
            response_data = {
                "status": "success",
                "message": "Agent task created successfully",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "task": {
                    "task_id": f"task-{int(datetime.utcnow().timestamp() * 1000)}",
                    "agent_id": data["agent_id"],
                    "task_type": data["task_type"],
                    "status": "queued",
                    "created_at": datetime.utcnow().isoformat() + "Z",
                    "note": "This is a demo endpoint. Full agent execution requires API keys and configuration."
                },
                "next_steps": [
                    "Configure environment variables (ANTHROPIC_API_KEY, OPENAI_API_KEY, etc.)",
                    "Deploy full agent orchestration backend",
                    "Monitor task status via Registry API"
                ]
            }

            self.send_response(202)  # 202 Accepted
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data, indent=2).encode())
            
        except Exception as e:
            self._send_error_response(500, f"Internal server error: {str(e)}")

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()
    
    def _check_agent_availability(self):
        """Check which agents are available based on configured API keys."""
        return {
            "anthropic": "available" if os.environ.get("ANTHROPIC_API_KEY") else "unavailable",
            "openai": "available" if os.environ.get("OPENAI_API_KEY") else "unavailable",
            "groq": "available" if os.environ.get("GROQ_API_KEY") else "unavailable",
            "google": "available" if os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY") else "unavailable"
        }
    
    def _send_error_response(self, code: int, message: str):
        """Send a standardized error response."""
        error_response = {
            "status": "error",
            "error": message,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(error_response).encode())
