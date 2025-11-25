#!/bin/bash
# Entrypoint script for Python self-hosted runner

set -e

# Configuration
GITHUB_OWNER=${GITHUB_OWNER:-""}
GITHUB_REPO=${GITHUB_REPO:-""}
GITHUB_TOKEN=${GITHUB_TOKEN:-""}
RUNNER_NAME=${RUNNER_NAME:-"tokyo-ia-python-runner-$(hostname)"}
RUNNER_LABELS=${RUNNER_LABELS:-"self-hosted,linux,x64,python"}
RUNNER_WORKDIR=${RUNNER_WORKDIR:-"/home/runner/_work"}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Tokyo IA Python Runner${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Validate required environment variables
if [ -z "$GITHUB_OWNER" ]; then
    echo -e "${RED}❌ Error: GITHUB_OWNER is required${NC}"
    exit 1
fi

if [ -z "$GITHUB_REPO" ]; then
    echo -e "${RED}❌ Error: GITHUB_REPO is required${NC}"
    exit 1
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}❌ Error: GITHUB_TOKEN is required${NC}"
    exit 1
fi

# Get registration token
echo -e "${YELLOW}🔑 Getting registration token...${NC}"
REG_TOKEN=$(curl -s -X POST \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/actions/runners/registration-token" \
    | jq -r '.token')

if [ "$REG_TOKEN" == "null" ] || [ -z "$REG_TOKEN" ]; then
    echo -e "${RED}❌ Failed to get registration token${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Registration token obtained${NC}"

# Configure runner
echo -e "${YELLOW}⚙️ Configuring runner...${NC}"
cd /home/runner/actions-runner

./config.sh \
    --url "https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}" \
    --token "${REG_TOKEN}" \
    --name "${RUNNER_NAME}" \
    --labels "${RUNNER_LABELS}" \
    --work "${RUNNER_WORKDIR}" \
    --unattended \
    --replace

echo -e "${GREEN}✅ Runner configured${NC}"

# Cleanup function
cleanup() {
    echo -e "${YELLOW}🧹 Removing runner...${NC}"
    
    # Get removal token
    REMOVE_TOKEN=$(curl -s -X POST \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/actions/runners/remove-token" \
        | jq -r '.token')
    
    if [ "$REMOVE_TOKEN" != "null" ] && [ -n "$REMOVE_TOKEN" ]; then
        ./config.sh remove --token "${REMOVE_TOKEN}"
        echo -e "${GREEN}✅ Runner removed${NC}"
    fi
}

# Set up signal handlers
trap cleanup EXIT SIGTERM SIGINT

# Print system info
echo ""
echo -e "${GREEN}📊 System Information${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Python versions available:"
for v in 3.9 3.10 3.11 3.12; do
    python3.${v#3.} --version 2>/dev/null || true
done
echo ""
echo "pip version: $(pip3 --version)"
echo "poetry version: $(poetry --version 2>/dev/null || echo 'not installed')"
echo ""

# Start runner
echo -e "${GREEN}🏃 Starting runner...${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
./run.sh
