#!/bin/bash
# Generate release script for Tokyo-IA

set -e

VERSION="${1:-1.0.0}"
echo "Generating release for version $VERSION"

# Build Android APK
echo "Building Android APK..."
if [ -f "./gradlew" ]; then
  ./gradlew assembleRelease
  echo "✓ Android APK built"
else
  echo "⚠ Gradle wrapper not found, skipping Android build"
fi

# Build Web
echo "Building Web application..."
if [ -d "web" ] && [ -f "web/package.json" ]; then
  cd web
  if [ -d "node_modules" ]; then
    npm run build
    echo "✓ Web application built"
  else
    echo "⚠ Web dependencies not installed, skipping web build"
  fi
  cd ..
else
  echo "⚠ Web directory not found, skipping web build"
fi

# Create git tag
echo "Creating git tag v$VERSION..."
git tag -a "v$VERSION" -m "Release version $VERSION"
echo "✓ Tag created"

echo ""
echo "Release $VERSION generated successfully!"
echo "To push the tag, run: git push origin v$VERSION"
