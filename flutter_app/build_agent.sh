#!/bin/bash
# Build Agent Script for Tokyo-IA Flutter App
# Executes flutter build appbundle --release and verifies output

set -e

echo "========================================="
echo "Tokyo-IA Build Agent"
echo "========================================="
echo ""

# Define paths
PROJECT_DIR="/home/runner/work/Tokyo-IA/Tokyo-IA/flutter_app"
OUTPUT_DIR="$PROJECT_DIR/build/app/outputs/bundle/release"
AAB_FILE="$OUTPUT_DIR/app-release.aab"

# Check if Flutter is available
if ! command -v flutter &> /dev/null; then
    echo "ERROR: Flutter is not installed or not in PATH"
    echo "BUILD FAILED: Flutter not available"
    exit 1
fi

# Navigate to Flutter project
cd "$PROJECT_DIR"

# Verify project structure
if [ ! -f "pubspec.yaml" ]; then
    echo "ERROR: pubspec.yaml not found"
    echo "BUILD FAILED: Invalid Flutter project structure"
    exit 1
fi

echo "Step 1: Getting Flutter dependencies..."
flutter pub get || {
    echo "BUILD FAILED: Could not get dependencies"
    exit 1
}

echo ""
echo "Step 2: Building Android App Bundle (release mode)..."
flutter build appbundle --release || {
    echo "BUILD FAILED: Build command failed"
    exit 1
}

echo ""
echo "Step 3: Verifying .aab output..."
if [ -f "$AAB_FILE" ]; then
    AAB_SIZE=$(stat -f%z "$AAB_FILE" 2>/dev/null || stat -c%s "$AAB_FILE" 2>/dev/null)
    echo "✓ SUCCESS: App bundle generated"
    echo "  Location: $AAB_FILE"
    echo "  Size: $AAB_SIZE bytes"
    echo ""
    echo "========================================="
    echo "BUILD SUCCESS"
    echo "========================================="
    exit 0
else
    echo "BUILD FAILED: .aab file not found at expected location"
    echo "Expected: $AAB_FILE"
    exit 1
fi
