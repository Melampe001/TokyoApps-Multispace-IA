# Tokyo-IA Build Instructions

This document provides detailed instructions for building and running the Tokyo-IA project components.

## Prerequisites

### For Android App
- JDK 17 or higher
- Android SDK with API level 35
- Gradle 8.2 or higher (included via wrapper)

### For Web Application
- Node.js 18+ and npm 9+

### For MCP Server
- Node.js 18+ and npm 9+

## Building the Android App

### Local Debug Build

```bash
# Grant execute permission to gradlew (Unix/Linux/Mac)
chmod +x gradlew

# Build debug APK
./gradlew assembleDebug

# Install debug APK to connected device/emulator
./gradlew installDebug

# Run unit tests
./gradlew test
```

The debug APK will be located at: `app/build/outputs/apk/debug/app-debug.apk`

### Release Build

For release builds, you need to set up signing credentials:

```bash
# Set environment variables
export KEYSTORE_FILE=/path/to/your/keystore.jks
export KEYSTORE_PASSWORD=your_keystore_password
export KEY_ALIAS=your_key_alias
export KEY_PASSWORD=your_key_password

# Build release AAB (Android App Bundle)
./gradlew bundleRelease

# Or build release APK
./gradlew assembleRelease
```

The release AAB will be located at: `app/build/outputs/bundle/release/app-release.aab`
The release APK will be located at: `app/build/outputs/apk/release/app-release.apk`

## Building the Web Application

```bash
cd web

# Install dependencies
npm install

# Development server (with hot reload)
npm run dev
# Server will run on http://localhost:3000

# Production build
npm run build
# Built files will be in web/dist/

# Preview production build
npm run preview

# Run tests
npm test
```

## Running the MCP Server

```bash
cd server-mcp

# Install dependencies
npm install

# Start the server
npm start
# Server will run on http://localhost:3001

# Development mode (with auto-restart)
npm run dev
```

### Testing the MCP Server

```bash
# Health check
curl http://localhost:3001/health

# Get context
curl http://localhost:3001/context

# Test MCP endpoint
curl -X POST http://localhost:3001/mcp \
  -H "Content-Type: application/json" \
  -d '{"action":"ping","payload":{}}'
```

## Using Release Scripts

### Bump Version

```bash
# Bump version to 1.0.1 with build number 2
./scripts/bump-version.sh 1.0.1 2
```

This script updates version numbers in:
- `app/build.gradle` (Android)
- `web/package.json`
- `server-mcp/package.json`

### Generate Release

```bash
# Generate release version 1.0.1
./scripts/generate-release.sh 1.0.1
```

This script:
1. Checks for uncommitted changes
2. Builds all components
3. Creates a git tag
4. Pushes to remote

## CI/CD Workflows

The project includes GitHub Actions workflows:

### Android Build
- **Trigger**: Push to main/develop, or pull requests to main
- **Workflow**: `.github/workflows/android-build.yml`
- **Output**: Debug and release APKs/AABs as artifacts

### Release to Google Play
- **Trigger**: Push tags matching `v*` (e.g., `v1.0.0`)
- **Workflow**: `.github/workflows/tokyoia-release-to-play.yml`
- **Output**: Automatic release to Google Play Internal track

### Security Scan
- **Trigger**: Push to main/develop, pull requests, or daily schedule
- **Workflow**: `.github/workflows/security-scan.yml`
- **Checks**: Dependencies, secrets, and CodeQL analysis

## Setting Up GitHub Secrets

For CI/CD to work, configure these GitHub Secrets:

1. **ANDROID_KEYSTORE_BASE64**: Base64-encoded keystore file
   ```bash
   base64 -i your-keystore.jks | pbcopy  # Mac
   base64 -w 0 your-keystore.jks  # Linux
   ```

2. **KEYSTORE_PASSWORD**: Password for the keystore
3. **KEY_ALIAS**: Key alias in the keystore
4. **KEY_PASSWORD**: Password for the key
5. **GOOGLE_PLAY_JSON**: Google Play service account JSON (as text)

## Troubleshooting

### Android Build Issues

**Problem**: Gradle download fails
```bash
# Try using a different mirror or download manually
./gradlew --refresh-dependencies
```

**Problem**: SDK not found
```bash
# Set ANDROID_HOME environment variable
export ANDROID_HOME=/path/to/android/sdk
```

### Web Build Issues

**Problem**: npm install fails
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### MCP Server Issues

**Problem**: Port already in use
```bash
# Use a different port
PORT=3002 npm start
```

## Development Tips

1. **Android**: Use Android Studio for better IDE support
2. **Web**: Use VS Code with ESLint and Prettier extensions
3. **MCP Server**: Use Postman or curl for API testing
4. **Git**: Always work on feature branches, not directly on main

## Additional Resources

- [Android Developer Guide](https://developer.android.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Express.js Documentation](https://expressjs.com/)
