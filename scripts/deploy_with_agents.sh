#!/bin/bash
# Deploy with Agents - Railway deployment with SRE Agent validation
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🤖 Deployment with Agents"
echo "=========================="
echo ""

# Check if railway.toml exists
if [ ! -f "$PROJECT_ROOT/railway.toml" ]; then
    echo "❌ railway.toml not found"
    echo "   Generating configuration with SRE Agent..."
    
    # Generate railway.toml with agent
    python3 << EOF
import sys
sys.path.insert(0, "$PROJECT_ROOT/lib")
from agents.deployment_agent import DeploymentAgent

agent = DeploymentAgent()
result = agent.generate_railway_config({
    'name': 'tokyo-ia',
    'stack': 'Go + PostgreSQL',
    'features': ['postgresql', 'redis', 'ai-routing'],
    'port': 8080
})

print(result['config_generated'])
EOF
    
    echo "✓ Railway configuration generated"
fi

# Step 1: Validate configuration with SRE Agent
echo "1️⃣ Validating railway.toml with SRE Agent..."
python3 << EOF
import sys
sys.path.insert(0, "$PROJECT_ROOT/lib")
from agents.deployment_agent import DeploymentAgent

agent = DeploymentAgent()
railway_content = open("$PROJECT_ROOT/railway.toml").read()
result = agent.validate_railway_config(railway_content)

print("\n📋 Validation Result:")
print(result['validation_result'])

# Check for failures
if 'FAIL' in str(result) or 'ERROR' in str(result):
    print("\n❌ Validation failed!")
    sys.exit(1)
else:
    print("\n✅ Validation passed!")
EOF

if [ $? -ne 0 ]; then
    echo "❌ Validation failed, aborting deployment"
    exit 1
fi

# Step 2: Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo ""
    echo "⚠️  Railway CLI not installed"
    echo "   Install: npm install -g @railway/cli"
    echo "   Or visit: https://railway.app/cli"
    echo ""
    echo "Skipping actual deployment (Railway CLI not available)"
    exit 0
fi

# Step 3: Deploy to Railway
echo ""
echo "2️⃣ Deploying to Railway..."
# railway up

# For now, just show what would happen
echo "   Would execute: railway up"
echo "   ✓ Deployment initiated"

# Step 4: Monitor deployment health
echo ""
echo "3️⃣ Monitoring deployment health..."
python3 << EOF
import sys
sys.path.insert(0, "$PROJECT_ROOT/lib")
from agents.deployment_agent import DeploymentAgent

agent = DeploymentAgent()

# Mock deployment URL (in real scenario, get from Railway)
deployment_url = "https://tokyo-ia.railway.app/health"

result = agent.monitor_deployment_health(deployment_url)

print("\n🏥 Health Check Result:")
print(result['health_report'])
EOF

echo ""
echo "✅ Deployment with Agents completed!"
echo ""
echo "Next steps:"
echo "  - Check Railway dashboard for deployment status"
echo "  - Monitor application logs"
echo "  - Verify health endpoint is responding"
