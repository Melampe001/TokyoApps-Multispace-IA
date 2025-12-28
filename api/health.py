"""
Health check endpoint for TokyoApps-Multispace-IA on Vercel.
Returns service health status and system information.
"""

from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime


class handler(BaseHTTPRequestHandler):
    """Health check handler for Vercel serverless function."""

    def do_GET(self):
        """Handle GET requests - return health status."""
        response_data = {
            "status": "healthy",
            "service": "TokyoApps-Multispace-IA",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "uptime": "serverless",
            "version": "1.0.0",
            "environment": "production",
            "checks": {
                "api": "operational",
                "database": "not_configured",
                "agents": "available"
            }
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
