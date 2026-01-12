"""
Health check endpoint for TokyoApps-Multispace-IA on Vercel.
Returns service health status and system information.
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from datetime import datetime


class handler(BaseHTTPRequestHandler):
    """Health check handler for Vercel serverless function."""

    def do_GET(self):
        """Handle GET requests - return health status."""
        try:
            # Check environment configuration
            has_anthropic = bool(os.environ.get("ANTHROPIC_API_KEY"))
            has_openai = bool(os.environ.get("OPENAI_API_KEY"))
            has_groq = bool(os.environ.get("GROQ_API_KEY"))
            has_google = bool(os.environ.get("GOOGLE_API_KEY"))
            
            # Determine agent availability
            agents_configured = sum([has_anthropic, has_openai, has_groq, has_google])
            agents_status = "fully_configured" if agents_configured == 4 else \
                           "partially_configured" if agents_configured > 0 else \
                           "not_configured"
            
            response_data = {
                "status": "healthy",
                "service": "TokyoApps-Multispace-IA",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "uptime": "serverless",
                "version": "1.0.0",
                "environment": "production",
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "checks": {
                    "api": "operational",
                    "database": "not_configured",
                    "agents": agents_status,
                    "agent_keys": {
                        "anthropic": has_anthropic,
                        "openai": has_openai,
                        "groq": has_groq,
                        "google": has_google
                    }
                }
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            self.wfile.write(json.dumps(response_data, indent=2).encode())
            
        except Exception as e:
            # Log error and return 500
            error_response = {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
