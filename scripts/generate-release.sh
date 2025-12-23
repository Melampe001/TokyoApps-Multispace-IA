#!/bin/bash
# Script to generate a release (build, tag, and push)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if version argument is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Version number required${NC}"
    echo "Usage: $0 <version>"
    echo "Example: $0 1.0.1"
    exit 1
fi

VERSION=$1
TAG="v${VERSION}"

# Get the default branch name dynamically
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
if [ -z "$DEFAULT_BRANCH" ]; then
    echo -e "${YELLOW}Warning: Could not detect default branch, using 'main'${NC}"
    DEFAULT_BRANCH="main"
fi

echo -e "${YELLOW}Generating release ${VERSION} on branch ${DEFAULT_BRANCH}${NC}"

# Check if tag already exists
if git rev-parse "$TAG" >/dev/null 2>&1; then
    echo -e "${RED}Error: Tag ${TAG} already exists${NC}"
    exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${RED}Error: Uncommitted changes detected${NC}"
    echo "Please commit or stash your changes first"
    exit 1
fi

# Build Android app (if gradle wrapper exists)
if [ -f "gradlew" ]; then
    echo "Building Android app..."
    ./gradlew assembleRelease
    echo -e "${GREEN}✓ Android build complete${NC}"
fi

# Build Web app (if package.json exists)
if [ -f "web/package.json" ]; then
    echo "Building Web app..."
    cd web
    npm install
    npm run build
    cd ..
    echo -e "${GREEN}✓ Web build complete${NC}"
fi

# Create git tag
echo "Creating git tag ${TAG}..."
git tag -a "$TAG" -m "Release version ${VERSION}"
echo -e "${GREEN}✓ Tag created${NC}"

# Push changes and tags
echo "Pushing to remote..."
git push origin "$DEFAULT_BRANCH"
git push origin "$TAG"
echo -e "${GREEN}✓ Pushed to remote${NC}"

echo -e "${GREEN}Release ${VERSION} generated successfully!${NC}"
echo "Release artifacts:"
if [ -f "app/build/outputs/apk/release/app-release.apk" ]; then
    echo "  - Android APK: app/build/outputs/apk/release/app-release.apk"
fi
if [ -d "web/dist" ]; then
    echo "  - Web build: web/dist/"
fi
