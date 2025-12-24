#!/bin/bash
set -euo pipefail

# ============================================================================
# Tokyo-IA Brand Agent
# Extracts brand tokens (colors, typography, spacing) from design model
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INPUT_FILE="$PROJECT_ROOT/simulator/output/design_model.json"
OUTPUT_DIR="$PROJECT_ROOT/simulator/output"
OUTPUT_FILE="$OUTPUT_DIR/brand_tokens.json"
FLUTTER_APP_DIR="$PROJECT_ROOT/flutter_app"

echo "🎨 Tokyo-IA Brand Agent"
echo "======================="
echo ""

# Check if design model exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Error: design_model.json not found at $INPUT_FILE"
    echo "   Run simulator first: bash simulator/simulate_design.sh"
    exit 1
fi

echo "✓ Found design model"

# Read project name from design model
PROJECT_NAME=$(jq -r '.metadata.project_name' "$INPUT_FILE")
echo "  Project: $PROJECT_NAME"

# Extract theme colors from Flutter main.dart if available
echo ""
echo "🎨 Extracting brand colors..."

PRIMARY_COLOR="#673AB7"
SECONDARY_COLOR="#9C27B0"
ERROR_COLOR="#B00020"
BACKGROUND_COLOR="#FFFFFF"
SURFACE_COLOR="#FFFFFF"

MAIN_DART="$FLUTTER_APP_DIR/lib/main.dart"
if [ -f "$MAIN_DART" ]; then
    # Try to extract seed color
    if grep -q "Colors\\.deepPurple" "$MAIN_DART"; then
        PRIMARY_COLOR="#673AB7"
        SECONDARY_COLOR="#9C27B0"
    elif grep -q "Colors\\.blue" "$MAIN_DART"; then
        PRIMARY_COLOR="#2196F3"
        SECONDARY_COLOR="#03A9F4"
    elif grep -q "Colors\\.red" "$MAIN_DART"; then
        PRIMARY_COLOR="#F44336"
        SECONDARY_COLOR="#E91E63"
    elif grep -q "Colors\\.green" "$MAIN_DART"; then
        PRIMARY_COLOR="#4CAF50"
        SECONDARY_COLOR="#8BC34A"
    fi
    echo "  ✓ Extracted colors from theme"
else
    echo "  ⚠️  Using default colors"
fi

echo "    Primary: $PRIMARY_COLOR"
echo "    Secondary: $SECONDARY_COLOR"

# Generate brand_tokens.json
echo ""
echo "📝 Generating brand tokens..."

cat > "$OUTPUT_FILE" << EOF
{
  "project_name": "$PROJECT_NAME",
  "generated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "colors": {
    "primary": "$PRIMARY_COLOR",
    "secondary": "$SECONDARY_COLOR",
    "error": "$ERROR_COLOR",
    "background": "$BACKGROUND_COLOR",
    "surface": "$SURFACE_COLOR",
    "on_primary": "#FFFFFF",
    "on_secondary": "#FFFFFF",
    "on_error": "#FFFFFF",
    "on_background": "#000000",
    "on_surface": "#000000"
  },
  "typography": {
    "heading1": {
      "font_family": "Roboto",
      "font_weight": "bold",
      "font_size": 32,
      "line_height": 40
    },
    "heading2": {
      "font_family": "Roboto",
      "font_weight": "bold",
      "font_size": 24,
      "line_height": 32
    },
    "heading3": {
      "font_family": "Roboto",
      "font_weight": "medium",
      "font_size": 20,
      "line_height": 28
    },
    "body1": {
      "font_family": "Roboto",
      "font_weight": "normal",
      "font_size": 16,
      "line_height": 24
    },
    "body2": {
      "font_family": "Roboto",
      "font_weight": "normal",
      "font_size": 14,
      "line_height": 20
    },
    "caption": {
      "font_family": "Roboto",
      "font_weight": "normal",
      "font_size": 12,
      "line_height": 16
    }
  },
  "spacing": {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "base": 16,
    "lg": 24,
    "xl": 32,
    "2xl": 48,
    "3xl": 64
  },
  "elevation": {
    "none": 0,
    "low": 2,
    "medium": 4,
    "high": 8,
    "highest": 16
  },
  "border_radius": {
    "sm": 4,
    "md": 8,
    "lg": 16,
    "xl": 24,
    "full": 9999
  }
}
EOF

echo "✅ Brand tokens generated successfully!"
echo "📄 Output: $OUTPUT_FILE"
echo ""

# Display summary
jq '{project_name, colors: .colors | keys, typography: .typography | keys, spacing: .spacing | keys}' "$OUTPUT_FILE"

echo ""
echo "✨ Brand agent complete!"
