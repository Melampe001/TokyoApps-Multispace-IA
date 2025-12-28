"""
Main API endpoint for TokyoApps-Multispace-IA on Vercel.
Handles HTTP GET and POST requests for service information.
"""

from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime


class handler(BaseHTTPRequestHandler):
    """Main API handler for Vercel serverless function."""

    def do_GET(self):
        """Handle GET requests - return service information."""
        response_data = {
            "service": "TokyoApps-Multispace-IA",
            "version": "1.0.0",
            "description": "AI agent orchestration platform with specialized agents",
            "status": "operational",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "endpoints": {
                "health": "/api/health",
                "agents": "/api/agents",
                "main": "/api/index"
            },
            "features": [
                "Multi-agent orchestration",
                "AI-powered code review",
                "Automated testing",
                "DevOps automation",
                "Documentation generation"
            ],
            "agents": {
                "akira": "Code Review Master (Claude Opus 4.1)",
                "yuki": "Test Engineering (OpenAI o3)",
                "hiro": "SRE & DevOps (Llama 4 405B)",
                "sakura": "Documentation (Gemini 3.0 Ultra)",
                "kenji": "Architecture (OpenAI o3)"
            }
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data, indent=2).encode())

    def do_POST(self):
        """Handle POST requests - process incoming data."""
        content_length = int(self.headers.get("Content-Length", 0))
        
        if content_length > 0:
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode())
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return
        else:
            data = {}

        response_data = {
            "status": "success",
            "message": "Data received successfully",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "received": data,
            "note": "This is a demo endpoint. Full implementation requires agent configuration."
        }

        self.send_response(200)
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
