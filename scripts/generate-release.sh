#!/bin/bash
# Script to generate a release: build, tag, and push

set -e

# Check if version is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <version>"
  echo "Example: $0 v1.0.0"
  exit 1
fi

VERSION=$1

# Validate version format
if [[ ! $VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Error: Version must be in format v#.#.#"
  echo "Example: v1.0.0"
  exit 1
fi

echo "Generating release $VERSION..."

# Check if tag already exists
if git rev-parse "$VERSION" >/dev/null 2>&1; then
  echo "Error: Tag $VERSION already exists"
  exit 1
fi

# Build Android app (if gradlew exists)
if [ -f "app/gradlew" ]; then
  echo "Building Android app..."
  cd app
  ./gradlew clean assembleRelease
  cd ..
  echo "Android build completed"
fi

# Build web (if package.json exists)
if [ -f "web/package.json" ]; then
  echo "Building web app..."
  cd web
  npm install
  npm run build
  cd ..
  echo "Web build completed"
fi

# Commit any changes
git add .
git commit -m "Release $VERSION" || echo "No changes to commit"

# Create and push tag
echo "Creating tag $VERSION..."
git tag -a "$VERSION" -m "Release $VERSION"

echo "Pushing to remote..."
git push origin main
git push origin "$VERSION"

echo "Release $VERSION completed successfully!"
echo "GitHub Actions will now build and deploy to Play Store"
