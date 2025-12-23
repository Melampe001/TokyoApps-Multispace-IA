#!/bin/bash
# Script to bump version numbers across the project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if version argument is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Version number required${NC}"
    echo "Usage: $0 <version> [build_number]"
    echo "Example: $0 1.0.1 2"
    exit 1
fi

NEW_VERSION=$1
BUILD_NUMBER=${2:-1}

echo -e "${YELLOW}Bumping version to ${NEW_VERSION} (build ${BUILD_NUMBER})${NC}"

# Detect OS for sed compatibility
if [[ "$OSTYPE" == "darwin"* ]]; then
    SED_INPLACE="sed -i ''"
else
    SED_INPLACE="sed -i"
fi

# Update Android app/build.gradle
if [ -f "app/build.gradle" ]; then
    echo "Updating Android version..."
    $SED_INPLACE "s/versionCode .*/versionCode ${BUILD_NUMBER}/" app/build.gradle
    $SED_INPLACE "s/versionName .*/versionName \"${NEW_VERSION}\"/" app/build.gradle
    echo -e "${GREEN}✓ Android version updated${NC}"
fi

# Update web package.json
if [ -f "web/package.json" ]; then
    echo "Updating Web version..."
    $SED_INPLACE "s/\"version\": \".*\"/\"version\": \"${NEW_VERSION}\"/" web/package.json
    echo -e "${GREEN}✓ Web version updated${NC}"
fi

# Update MCP server package.json
if [ -f "server-mcp/package.json" ]; then
    echo "Updating MCP Server version..."
    $SED_INPLACE "s/\"version\": \".*\"/\"version\": \"${NEW_VERSION}\"/" server-mcp/package.json
    echo -e "${GREEN}✓ MCP Server version updated${NC}"
fi

echo -e "${GREEN}Version bump complete!${NC}"
echo "Next steps:"
echo "  1. Review changes: git diff"
echo "  2. Commit: git commit -am 'Bump version to ${NEW_VERSION}'"
echo "  3. Tag: git tag v${NEW_VERSION}"
echo "  4. Push: git push && git push --tags"
