#!/bin/bash
set -euo pipefail

# ============================================================================
# Tokyo-IA Design Simulator
# Extracts metadata from Flutter app and generates design model
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
FLUTTER_APP_DIR="$PROJECT_ROOT/flutter_app"
OUTPUT_DIR="$SCRIPT_DIR/output"
OUTPUT_FILE="$OUTPUT_DIR/design_model.json"

echo "🎨 Tokyo-IA Design Simulator"
echo "=============================="
echo ""

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Validate flutter_app directory exists
if [ ! -d "$FLUTTER_APP_DIR" ]; then
    echo "❌ Error: flutter_app/ directory not found at $FLUTTER_APP_DIR"
    exit 1
fi

echo "✓ Found flutter_app directory"
cd "$FLUTTER_APP_DIR"

# Run flutter doctor and save output
echo ""
echo "📋 Running Flutter Doctor..."
if command -v flutter &> /dev/null; then
    flutter doctor -v > "$OUTPUT_DIR/flutter_doctor.txt" 2>&1 || true
    echo "✓ Flutter doctor output saved to: $OUTPUT_DIR/flutter_doctor.txt"
else
    echo "⚠️  Flutter not found in PATH, skipping flutter doctor"
    echo "Flutter not installed" > "$OUTPUT_DIR/flutter_doctor.txt"
fi

# Get Flutter and Dart versions
FLUTTER_VERSION="unknown"
DART_VERSION="unknown"

if command -v flutter &> /dev/null; then
    FLUTTER_VERSION=$(flutter --version 2>/dev/null | grep "Flutter" | head -n 1 | awk '{print $2}' || echo "unknown")
    DART_VERSION=$(flutter --version 2>/dev/null | grep "Dart" | awk '{print $4}' || echo "unknown")
fi

echo "  Flutter: $FLUTTER_VERSION"
echo "  Dart: $DART_VERSION"

# Execute flutter pub get
echo ""
echo "📦 Getting Flutter dependencies..."
if command -v flutter &> /dev/null; then
    flutter pub get > "$OUTPUT_DIR/pub_get.txt" 2>&1 || true
    echo "✓ Dependencies fetched"
else
    echo "⚠️  Flutter not found, skipping pub get"
    echo "Flutter not installed" > "$OUTPUT_DIR/pub_get.txt"
fi

# Run flutter analyze
echo ""
echo "🔍 Running Flutter Analyze..."
if command -v flutter &> /dev/null; then
    flutter analyze > "$OUTPUT_DIR/flutter_analyze.txt" 2>&1 || true
    ANALYZE_RESULT=$(grep -i "no issues found" "$OUTPUT_DIR/flutter_analyze.txt" && echo "clean" || echo "has_issues")
    echo "✓ Analysis complete: $ANALYZE_RESULT"
else
    echo "⚠️  Flutter not found, skipping analyze"
    echo "Flutter not installed" > "$OUTPUT_DIR/flutter_analyze.txt"
fi

# Extract project name from pubspec.yaml
echo ""
echo "📊 Extracting metadata..."
PROJECT_NAME="unknown"
if [ -f "pubspec.yaml" ]; then
    PROJECT_NAME=$(yq e '.name' pubspec.yaml 2>/dev/null || echo "unknown")
fi
echo "  Project: $PROJECT_NAME"

# Count widgets by searching for class definitions extending Widget
WIDGET_COUNT=0
if [ -d "lib" ]; then
    WIDGET_COUNT=$(grep -r "class.*extends.*Widget\|class.*extends.*State" lib/ 2>/dev/null | wc -l || echo "0")
fi
echo "  Widgets found: $WIDGET_COUNT"

# Extract routes from navigation patterns
echo "  Extracting routes..."
ROUTES_JSON="[]"
if [ -d "lib" ]; then
    # Find MaterialPageRoute and pushNamed calls
    ROUTE_FILES=$(mktemp)
    grep -r "MaterialPageRoute\|pushNamed\|Navigator.push" lib/ 2>/dev/null | grep -o "'/[^']*'" | sort -u > "$ROUTE_FILES" || true
    
    # Convert to JSON array
    if [ -s "$ROUTE_FILES" ]; then
        ROUTES_JSON=$(sed "s/'/\"/g" "$ROUTE_FILES" | jq -R -s -c 'split("\n") | map(select(length > 0))')
    fi
    rm -f "$ROUTE_FILES"
fi
echo "  Routes: $(echo "$ROUTES_JSON" | jq 'length' 2>/dev/null || echo "0")"

# Detect state management
STATE_MANAGEMENT="none"
if [ -f "pubspec.yaml" ]; then
    if yq e '.dependencies' pubspec.yaml 2>/dev/null | grep -q "riverpod"; then
        STATE_MANAGEMENT="riverpod"
    elif yq e '.dependencies' pubspec.yaml 2>/dev/null | grep -q "provider"; then
        STATE_MANAGEMENT="provider"
    elif yq e '.dependencies' pubspec.yaml 2>/dev/null | grep -q "bloc"; then
        STATE_MANAGEMENT="bloc"
    elif grep -rq "setState" lib/ 2>/dev/null; then
        STATE_MANAGEMENT="setState"
    fi
fi
echo "  State management: $STATE_MANAGEMENT"

# Parse dependencies from pubspec.yaml
DEPENDENCIES_JSON="[]"
if [ -f "pubspec.yaml" ]; then
    DEPENDENCIES_JSON=$(yq e '.dependencies | keys | .[]' pubspec.yaml 2>/dev/null | grep -v "flutter" | jq -R -s -c 'split("\n") | map(select(length > 0))' || echo "[]")
fi
echo "  Dependencies: $(echo "$DEPENDENCIES_JSON" | jq 'length' 2>/dev/null || echo "0")"

# Determine supported platforms
PLATFORMS_JSON='["android", "ios", "web"]'
echo "  Platforms: android, ios, web"

# Count stateful widgets for UI intent
STATEFUL_COUNT=$(grep -r "class.*extends.*StatefulWidget" lib/ 2>/dev/null | wc -l || echo "0")
HAS_NAVIGATION=$(grep -rq "Navigator" lib/ 2>/dev/null && echo "true" || echo "false")
HAS_RESPONSIVE=$(grep -rq "MediaQuery\|LayoutBuilder" lib/ 2>/dev/null && echo "true" || echo "false")
HAS_ACCESSIBILITY=$(grep -rq "Semantics\|semanticsLabel" lib/ 2>/dev/null && echo "true" || echo "false")

# Generate design_model.json
echo ""
echo "📝 Generating design model..."

cat > "$OUTPUT_FILE" << EOF
{
  "metadata": {
    "flutter_version": "$FLUTTER_VERSION",
    "dart_version": "$DART_VERSION",
    "project_name": "$PROJECT_NAME",
    "generated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "widget_count": $WIDGET_COUNT,
    "stateful_widget_count": $STATEFUL_COUNT
  },
  "routes": $ROUTES_JSON,
  "state_management": {
    "type": "$STATE_MANAGEMENT",
    "detected": $([ "$STATE_MANAGEMENT" != "none" ] && echo "true" || echo "false")
  },
  "dependencies": $DEPENDENCIES_JSON,
  "ui_intent": {
    "has_state": $([ "$STATEFUL_COUNT" -gt 0 ] && echo "true" || echo "false"),
    "has_navigation": $HAS_NAVIGATION,
    "is_responsive": $HAS_RESPONSIVE,
    "has_accessibility": $HAS_ACCESSIBILITY
  },
  "platforms": $PLATFORMS_JSON
}
EOF

echo "✅ Design model generated successfully!"
echo "📄 Output: $OUTPUT_FILE"
echo ""

# Display summary
jq '.' "$OUTPUT_FILE"

echo ""
echo "✨ Simulation complete!"
