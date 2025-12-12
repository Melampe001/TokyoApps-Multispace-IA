# Tokyo-IA - Build and Test Guide

## Project Structure Created

This repository now contains a complete testable project structure:

### ✅ Components Ready for Testing

1. **Android App** (`app/`)
   - Kotlin-based Android application
   - Min SDK 24, Target SDK 35
   - Basic MainActivity with UI
   - Unit tests included
   - ProGuard configuration

2. **Web Application** (`web/`)
   - React 18 + Vite 5
   - Modern development setup
   - Interactive UI components
   - Production build ready

3. **MCP Server** (`server-mcp/`)
   - Node.js Express server
   - Tokyo rules configuration
   - Health check endpoints
   - RESTful API structure

4. **Supporting Files**
   - Release notes (English and Spanish)
   - Build automation scripts
   - Gradle wrapper for Android
   - Git ignore rules

## Build and Test Instructions

### Web Application
```bash
cd web
npm install
npm run dev      # Start development server on port 3000
npm run build    # Build for production
npm test         # Run tests
```

✅ **Status**: Web builds successfully and runs on port 3000

### MCP Server
```bash
cd server-mcp
npm install
npm start        # Start server on port 3001
npm test         # Run tests
```

✅ **Status**: Server starts successfully and responds to health checks at http://localhost:3001/health

### Android App
```bash
./gradlew assembleDebug     # Build debug APK
./gradlew test              # Run unit tests
./gradlew installDebug      # Install on device/emulator
```

⚠️ **Note**: Android build requires Android SDK to be installed. The project structure is ready but needs a proper Android development environment to compile.

## Testing Results

- ✅ Web application builds and runs successfully
- ✅ MCP server starts and responds correctly
- ⏳ Android app structure is ready (requires Android SDK for full build)

## Next Steps

To fully test the Android app:
1. Set up Android SDK (API level 24-35)
2. Install Android Studio or command-line tools
3. Run `./gradlew assembleDebug` to build the APK

## Scripts Available

- `scripts/bump-version.sh [major|minor|patch]` - Bump version numbers
- `scripts/generate-release.sh [version]` - Generate release builds

## Project Ready for Development

The project is now properly structured and ready for:
- Development and testing
- CI/CD integration
- Release builds
- Deployment to production

All components follow the architecture described in README.md and can be independently developed and tested.
