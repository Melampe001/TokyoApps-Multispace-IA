#!/bin/bash
# Script to bump version numbers across the project

set -e

# Check if version type is provided
if [ -z "$1" ]; then
  echo "Usage: $0 [major|minor|patch]"
  echo "Example: $0 patch"
  exit 1
fi

VERSION_TYPE=$1

# Get current version from app/build.gradle
CURRENT_VERSION=$(grep "versionName" app/build.gradle | sed 's/.*"\(.*\)".*/\1/')
CURRENT_CODE=$(grep "versionCode" app/build.gradle | sed 's/.*versionCode \(.*\)/\1/')

echo "Current version: $CURRENT_VERSION (code: $CURRENT_CODE)"

# Parse version components
IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

# Bump version
case $VERSION_TYPE in
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
    echo "Invalid version type. Use: major, minor, or patch"
    exit 1
    ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
NEW_CODE=$((CURRENT_CODE + 1))

echo "New version: $NEW_VERSION (code: $NEW_CODE)"

# Update app/build.gradle
sed -i "s/versionCode $CURRENT_CODE/versionCode $NEW_CODE/" app/build.gradle
sed -i "s/versionName \"$CURRENT_VERSION\"/versionName \"$NEW_VERSION\"/" app/build.gradle

# Update web/package.json
sed -i "s/\"version\": \".*\"/\"version\": \"$NEW_VERSION\"/" web/package.json

# Update server-mcp/package.json
sed -i "s/\"version\": \".*\"/\"version\": \"$NEW_VERSION\"/" server-mcp/package.json

echo "Version bumped successfully!"
echo "Updated files:"
echo "  - app/build.gradle"
echo "  - web/package.json"
echo "  - server-mcp/package.json"
