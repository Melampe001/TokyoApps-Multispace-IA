#!/bin/bash
# Entrypoint script for Docker self-hosted runner

set -e

# Configuration
GITHUB_OWNER=${GITHUB_OWNER:-""}
GITHUB_REPO=${GITHUB_REPO:-""}
GITHUB_TOKEN=${GITHUB_TOKEN:-""}
RUNNER_NAME=${RUNNER_NAME:-"tokyo-ia-docker-runner-$(hostname)"}
RUNNER_LABELS=${RUNNER_LABELS:-"self-hosted,linux,x64,docker"}
RUNNER_WORKDIR=${RUNNER_WORKDIR:-"/home/runner/_work"}

echo "🐳 Starting Tokyo IA Docker Runner"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Start Docker daemon in background
echo "🐳 Starting Docker daemon..."
dockerd &

# Wait for Docker to be ready
echo "⏳ Waiting for Docker daemon..."
timeout 60 sh -c 'until docker info > /dev/null 2>&1; do sleep 1; done'
echo "✅ Docker daemon is ready"

# Validate required environment variables
if [ -z "$GITHUB_OWNER" ] || [ -z "$GITHUB_REPO" ] || [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GITHUB_OWNER, GITHUB_REPO, and GITHUB_TOKEN are required"
    exit 1
fi

# Get registration token
echo "🔑 Getting registration token..."
REG_TOKEN=$(curl -s -X POST \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/actions/runners/registration-token" \
    | jq -r '.token')

if [ "$REG_TOKEN" == "null" ] || [ -z "$REG_TOKEN" ]; then
    echo "❌ Failed to get registration token"
    exit 1
fi

echo "✅ Registration token obtained"

# Configure runner
echo "⚙️ Configuring runner..."
cd /home/runner/actions-runner

./config.sh \
    --url "https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}" \
    --token "${REG_TOKEN}" \
    --name "${RUNNER_NAME}" \
    --labels "${RUNNER_LABELS}" \
    --work "${RUNNER_WORKDIR}" \
    --unattended \
    --replace

echo "✅ Runner configured"

# Cleanup function
cleanup() {
    echo "🧹 Cleaning up..."
    
    REMOVE_TOKEN=$(curl -s -X POST \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/actions/runners/remove-token" \
        | jq -r '.token')
    
    if [ "$REMOVE_TOKEN" != "null" ] && [ -n "$REMOVE_TOKEN" ]; then
        ./config.sh remove --token "${REMOVE_TOKEN}"
    fi
}

trap cleanup EXIT SIGTERM SIGINT

# Print info
echo ""
echo "📊 Docker Information"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
docker version
echo ""

# Start runner
echo "🏃 Starting runner..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
./run.sh
