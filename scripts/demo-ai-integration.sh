#!/bin/bash

# Tokyo-IA AI Integration Demo Script
# This script demonstrates the AI integration features

set -e

echo "========================================="
echo "Tokyo-IA AI Integration Demo"
echo "========================================="
echo

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Build the project
echo -e "${BLUE}1. Building Tokyo-IA AI services...${NC}"
make build
echo -e "${GREEN}✓ Build complete${NC}"
echo

# Run tests
echo -e "${BLUE}2. Running tests...${NC}"
make test
echo -e "${GREEN}✓ Tests passed${NC}"
echo

# Start the API server in background
echo -e "${BLUE}3. Starting AI API server...${NC}"
./bin/ai-api &
API_PID=$!
echo -e "${GREEN}✓ API server started (PID: $API_PID)${NC}"
echo

# Wait for server to start
echo "Waiting for server to initialize..."
sleep 3

# Test health endpoint
echo -e "${BLUE}4. Testing health endpoint...${NC}"
curl -s http://localhost:8080/health | jq '.'
echo -e "${GREEN}✓ Health check passed${NC}"
echo

# Test completion endpoint with different task types
echo -e "${BLUE}5. Testing AI completion endpoints...${NC}"
echo

echo "  a) Simple reasoning task:"
curl -s -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is 2+2? Explain your reasoning.",
    "task_type": "reasoning",
    "complexity": "simple",
    "max_tokens": 200
  }' | jq -r '.content' | head -c 200
echo "..."
echo

echo "  b) Code generation task:"
curl -s -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Go function to calculate fibonacci numbers",
    "task_type": "code_generation",
    "max_tokens": 300
  }' | jq -r '.content' | head -c 200
echo "..."
echo

echo "  c) Code review task:"
curl -s -X POST http://localhost:8080/ai/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Review this code: func Add(a, b int) int { return a + b }",
    "task_type": "code_review",
    "max_tokens": 200
  }' | jq -r '.content' | head -c 200
echo "..."
echo

echo -e "${GREEN}✓ Completion tests passed${NC}"
echo

# Test metrics endpoint
echo -e "${BLUE}6. Testing metrics endpoint...${NC}"
curl -s http://localhost:8080/ai/metrics | jq '{
  total_requests: .total_requests,
  total_cost: .total_cost_usd,
  budget: .budget
}'
echo -e "${GREEN}✓ Metrics retrieved${NC}"
echo

# Make several cached requests
echo -e "${BLUE}7. Testing caching (making duplicate requests)...${NC}"
for i in {1..3}; do
  echo "  Request $i:"
  RESPONSE=$(curl -s -X POST http://localhost:8080/ai/complete \
    -H "Content-Type: application/json" \
    -d '{
      "prompt": "What is the capital of France?",
      "task_type": "chat",
      "max_tokens": 100
    }')
  echo "$RESPONSE" | jq '{cached: .cached_result, latency_ms: .latency_ms}'
done
echo -e "${GREEN}✓ Caching demonstrated${NC}"
echo

# Show final metrics
echo -e "${BLUE}8. Final metrics after all requests:${NC}"
curl -s http://localhost:8080/ai/metrics | jq '{
  total_requests: .total_requests,
  total_cost_usd: .total_cost_usd,
  providers: .providers | to_entries | map({provider: .key, requests: .value.requests, cost: .value.cost_usd}),
  budget_used_percent: .budget.percent_used
}'
echo

# Cleanup
echo -e "${BLUE}9. Cleaning up...${NC}"
kill $API_PID 2>/dev/null || true
echo -e "${GREEN}✓ Cleanup complete${NC}"
echo

echo "========================================="
echo -e "${GREEN}Demo Complete!${NC}"
echo "========================================="
echo
echo "Next steps:"
echo "  - Read the documentation: docs/guides/ai-model-router-guide.md"
echo "  - Check the API reference: docs/api/ai-api-reference.md"
echo "  - View architecture: docs/architecture/ai-models-integration-architecture.md"
echo "  - Explore agent workflows: lib/agents/workflows.py"
echo
