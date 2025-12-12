#!/bin/bash
# Bump version script for Tokyo-IA

set -e

CURRENT_VERSION="1.0.0"
echo "Current version: $CURRENT_VERSION"

# Parse version components
IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR="${VERSION_PARTS[0]}"
MINOR="${VERSION_PARTS[1]}"
PATCH="${VERSION_PARTS[2]}"

# Determine bump type
BUMP_TYPE="${1:-patch}"

case $BUMP_TYPE in
  major)
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    ;;
  minor)
    MINOR=$((MINOR + 1))
    PATCH=0
    ;;
  patch)
    PATCH=$((PATCH + 1))
    ;;
  *)
    echo "Usage: $0 [major|minor|patch]"
    exit 1
    ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
echo "New version: $NEW_VERSION"

# Update version in files
echo "Updating version numbers..."
# Add version update logic here for build.gradle, package.json, etc.

echo "✓ Version bumped to $NEW_VERSION"
