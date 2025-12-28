"""
Metrics endpoint for monitoring TokyoApps-Multispace-IA.
"""

from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
import os


class handler(BaseHTTPRequestHandler):
    """Metrics handler for Vercel serverless function."""

    def do_GET(self):
        """Handle GET requests - return metrics."""
        
        # Check which API keys are configured
        api_keys_status = {
            "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "groq": bool(os.getenv("GROQ_API_KEY")),
            "google": bool(os.getenv("GOOGLE_API_KEY"))
        }
        
        response_data = {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "environment": os.getenv("NODE_ENV", "development"),
            "python_version": os.getenv("PYTHON_VERSION", "unknown"),
            "api_keys_configured": api_keys_status,
            "agents_available": sum(api_keys_status.values()),
            "total_agents": 5,
            "deployment_region": os.getenv("VERCEL_REGION", "unknown"),
            "git_commit": os.getenv("VERCEL_GIT_COMMIT_SHA", "unknown")[:7]
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data, indent=2).encode())

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
