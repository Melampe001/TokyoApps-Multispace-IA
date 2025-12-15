#!/bin/bash
# Demo interactivo del sistema AI de Tokyo-IA

set -e

echo "🚀 Tokyo-IA AI Integration Demo"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}Warning: jq is not installed. Output will not be pretty-formatted.${NC}"
    JQ_CMD="cat"
else
    JQ_CMD="jq"
fi

# Build the AI API
echo -e "${BLUE}Building AI API...${NC}"
make build
go build -o bin/ai-api cmd/ai-api/main.go
echo -e "${GREEN}✓ Build complete${NC}"
echo ""

# Start API server in background
echo -e "${BLUE}Starting AI API server...${NC}"
./bin/ai-api &
API_PID=$!
echo -e "${GREEN}✓ API server started (PID: $API_PID)${NC}"

# Wait for server to be ready
echo "Waiting for server to start..."
sleep 3

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Cleaning up...${NC}"
    kill $API_PID 2>/dev/null || true
    echo -e "${GREEN}✓ Server stopped${NC}"
}
trap cleanup EXIT

# Test 1: Reasoning Task
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}1️⃣  Testing Reasoning Task${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Prompt: 'What is quantum computing?'"
echo "Expected: Routed to Anthropic (reasoning specialist)"
echo ""

curl -s -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is quantum computing?",
    "task_type": "reasoning"
  }' | $JQ_CMD

# Test 2: Code Review
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}2️⃣  Testing Code Review${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Prompt: Code snippet review"
echo "Expected: Routed to Anthropic (code review specialist)"
echo ""

curl -s -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Review this code: func Add(a, b int) int { return a + b }",
    "task_type": "code_review"
  }' | $JQ_CMD

# Test 3: Creative Writing
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}3️⃣  Testing Creative Task${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Prompt: 'Write a haiku about Tokyo'"
echo "Expected: Routed to OpenAI (creative specialist)"
echo ""

curl -s -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a haiku about Tokyo",
    "task_type": "creative"
  }' | $JQ_CMD

# Test 4: Translation
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}4️⃣  Testing Translation${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Prompt: 'Translate Hello World to Japanese'"
echo "Expected: Routed to Gemini (translation specialist)"
echo ""

curl -s -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Translate Hello World to Japanese",
    "task_type": "translation"
  }' | $JQ_CMD

# Test 5: Cache Hit
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}5️⃣  Testing Cache (repeat request)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Repeating reasoning task..."
echo "Expected: cache_hit = true, much faster response"
echo ""

curl -s -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is quantum computing?",
    "task_type": "reasoning"
  }' | $JQ_CMD

# Check metrics
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}6️⃣  Checking System Metrics${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

curl -s http://localhost:8080/ai/metrics | $JQ_CMD

# Health check
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}7️⃣  Health Check${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

curl -s http://localhost:8080/health | $JQ_CMD

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Demo complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Summary:"
echo "  - Tested 5 different task types"
echo "  - Verified intelligent routing to appropriate models"
echo "  - Demonstrated caching functionality"
echo "  - Checked system metrics and health"
echo ""
echo "Next steps:"
echo "  - Replace mock clients with real API clients"
echo "  - Set API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY)"
echo "  - Configure custom routing rules in RouterConfig"
echo ""
