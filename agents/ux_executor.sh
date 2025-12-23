#!/bin/bash
set -euo pipefail

# ============================================================================
# Tokyo-IA UX Agent
# Extracts navigation patterns and state management from design model
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INPUT_FILE="$PROJECT_ROOT/simulator/output/design_model.json"
OUTPUT_DIR="$PROJECT_ROOT/simulator/output"
OUTPUT_FILE="$OUTPUT_DIR/ux_flow.json"
FLUTTER_APP_DIR="$PROJECT_ROOT/flutter_app"

echo "🧭 Tokyo-IA UX Agent"
echo "===================="
echo ""

# Check if design model exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Error: design_model.json not found at $INPUT_FILE"
    echo "   Run simulator first: bash simulator/simulate_design.sh"
    exit 1
fi

echo "✓ Found design model"

# Read data from design model
STATE_MANAGEMENT=$(jq -r '.state_management.type' "$INPUT_FILE")
ROUTES=$(jq -c '.routes' "$INPUT_FILE")
ROUTE_COUNT=$(echo "$ROUTES" | jq 'length')

echo "  State Management: $STATE_MANAGEMENT"
echo "  Routes: $ROUTE_COUNT"

# Analyze navigation patterns
echo ""
echo "🔍 Analyzing navigation patterns..."

NAV_PUSH_COUNT=0
NAV_PUSH_NAMED_COUNT=0
NAV_POP_COUNT=0
NAV_REPLACE_COUNT=0

if [ -d "$FLUTTER_APP_DIR/lib" ]; then
    # Temporarily disable pipefail for grep commands that may not find matches
    set +e
    NAV_PUSH_COUNT=$(grep -r "Navigator\.push\|MaterialPageRoute" "$FLUTTER_APP_DIR/lib" 2>/dev/null | wc -l | tr -d ' \n\r')
    NAV_PUSH_NAMED_COUNT=$(grep -r "pushNamed" "$FLUTTER_APP_DIR/lib" 2>/dev/null | wc -l | tr -d ' \n\r')
    NAV_POP_COUNT=$(grep -r "Navigator\.pop" "$FLUTTER_APP_DIR/lib" 2>/dev/null | wc -l | tr -d ' \n\r')
    NAV_REPLACE_COUNT=$(grep -r "pushReplacement" "$FLUTTER_APP_DIR/lib" 2>/dev/null | wc -l | tr -d ' \n\r')
    set -e
fi

# Ensure we have valid numbers
NAV_PUSH_COUNT=${NAV_PUSH_COUNT:-0}
NAV_PUSH_NAMED_COUNT=${NAV_PUSH_NAMED_COUNT:-0}
NAV_POP_COUNT=${NAV_POP_COUNT:-0}
NAV_REPLACE_COUNT=${NAV_REPLACE_COUNT:-0}

echo "  Navigator.push: $NAV_PUSH_COUNT"
echo "  pushNamed: $NAV_PUSH_NAMED_COUNT"
echo "  Navigator.pop: $NAV_POP_COUNT"
echo "  pushReplacement: $NAV_REPLACE_COUNT"

# Determine navigation type
NAV_TYPE="basic"
if [ "$NAV_PUSH_NAMED_COUNT" -gt 0 ]; then
    NAV_TYPE="named_routes"
elif [ "$NAV_PUSH_COUNT" -gt 0 ]; then
    NAV_TYPE="imperative"
fi

# Count stateful widgets
STATEFUL_COUNT=$(jq -r '.metadata.stateful_widget_count' "$INPUT_FILE")
echo "  Stateful widgets: $STATEFUL_COUNT"

# Detect interaction types
echo ""
echo "🎮 Detecting interaction types..."

INTERACTIONS='["tap"]'
if [ -d "$FLUTTER_APP_DIR/lib" ]; then
    INTERACTION_LIST=""
    grep -rq "onPressed\|GestureDetector" "$FLUTTER_APP_DIR/lib" 2>/dev/null && INTERACTION_LIST="${INTERACTION_LIST}tap,"
    grep -rq "onLongPress" "$FLUTTER_APP_DIR/lib" 2>/dev/null && INTERACTION_LIST="${INTERACTION_LIST}long_press,"
    grep -rq "onDoubleTap" "$FLUTTER_APP_DIR/lib" 2>/dev/null && INTERACTION_LIST="${INTERACTION_LIST}double_tap,"
    grep -rq "Draggable\|DragTarget" "$FLUTTER_APP_DIR/lib" 2>/dev/null && INTERACTION_LIST="${INTERACTION_LIST}drag,"
    grep -rq "onPanUpdate\|onScaleUpdate" "$FLUTTER_APP_DIR/lib" 2>/dev/null && INTERACTION_LIST="${INTERACTION_LIST}gesture,"
    grep -rq "TextField\|TextFormField" "$FLUTTER_APP_DIR/lib" 2>/dev/null && INTERACTION_LIST="${INTERACTION_LIST}text_input,"
    
    if [ -n "$INTERACTION_LIST" ]; then
        INTERACTIONS=$(echo "$INTERACTION_LIST" | tr ',' '\n' | grep -v '^$' | sort -u | jq -R -s -c 'split("\n") | map(select(length > 0))')
    fi
fi

echo "  Interactions: $(echo "$INTERACTIONS" | jq -r '.[]' | paste -sd, -)"

# Generate ux_flow.json
echo ""
echo "📝 Generating UX flow..."

cat > "$OUTPUT_FILE" << EOF
{
  "generated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "navigation": {
    "type": "$NAV_TYPE",
    "routes": $ROUTES,
    "patterns": {
      "push_count": $NAV_PUSH_COUNT,
      "push_named_count": $NAV_PUSH_NAMED_COUNT,
      "pop_count": $NAV_POP_COUNT,
      "replace_count": $NAV_REPLACE_COUNT
    }
  },
  "state_management": {
    "type": "$STATE_MANAGEMENT",
    "stateful_widgets": $STATEFUL_COUNT,
    "details": {
      "description": "$([ "$STATE_MANAGEMENT" = "setState" ] && echo "Using built-in setState for state management" || echo "Using $STATE_MANAGEMENT for state management")",
      "complexity": "$([ "$STATEFUL_COUNT" -gt 5 ] && echo "high" || echo "low")"
    }
  },
  "user_flow": {
    "entry_point": "home",
    "primary_actions": [
      "navigate",
      "interact",
      "view_content"
    ],
    "example_flow": [
      "Launch app",
      "View home screen",
      "Navigate to details",
      "Interact with content",
      "Return to home"
    ]
  },
  "state_machine": {
    "states": [
      {
        "name": "initial",
        "description": "App launches and shows home screen"
      },
      {
        "name": "loading",
        "description": "Data is being fetched or processed"
      },
      {
        "name": "content",
        "description": "Content is displayed to user"
      },
      {
        "name": "error",
        "description": "An error has occurred"
      }
    ],
    "transitions": [
      {
        "from": "initial",
        "to": "loading",
        "trigger": "app_start"
      },
      {
        "from": "loading",
        "to": "content",
        "trigger": "data_loaded"
      },
      {
        "from": "loading",
        "to": "error",
        "trigger": "load_failed"
      },
      {
        "from": "error",
        "to": "loading",
        "trigger": "retry"
      }
    ]
  },
  "interactions": $INTERACTIONS
}
EOF

echo "✅ UX flow generated successfully!"
echo "📄 Output: $OUTPUT_FILE"
echo ""

# Display summary
jq '{navigation: .navigation.type, state_management: .state_management.type, interactions: .interactions}' "$OUTPUT_FILE"

echo ""
echo "✨ UX agent complete!"
