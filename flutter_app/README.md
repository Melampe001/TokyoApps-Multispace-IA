# Tokyo-IA Flutter Application

This directory contains the Flutter mobile application for Tokyo-IA Personal AI Assistant.

## 🏗️ Build Agent

This project includes a BUILD_AGENT role for automated Flutter builds.

### Build Commands

#### Production Build
```bash
# Build Android App Bundle (release)
flutter build appbundle --release
```

#### Development Build
```bash
# Build APK (debug)
flutter build apk --debug

# Build APK (release)
flutter build apk --release
```

### Build Scripts

#### Automated Build Script
```bash
./build_agent.sh
```

This script will:
1. Verify Flutter installation
2. Get dependencies with `flutter pub get`
3. Execute `flutter build appbundle --release`
4. Verify the `.aab` output file exists

#### Mock Build (for testing)
```bash
./build_agent_mock.sh
```

Simulates the build process when Flutter SDK is unavailable.

### Output Location

The Android App Bundle (.aab) file will be generated at:
```
build/app/outputs/bundle/release/app-release.aab
```

### Build Requirements

- Flutter SDK 3.0.0 or higher
- Dart SDK 3.0.0 or higher
- Android SDK with:
  - Min SDK: 24 (Android 7.0)
  - Target SDK: 34 (Android 14)
- Java JDK 17

### CI/CD Integration

The GitHub Actions workflow `.github/workflows/flutter-build-agent.yml` automates the build process:

- Triggers on push to `main` or `develop` branches
- Executes `flutter build appbundle --release`
- Verifies `.aab` output
- Uploads build artifacts
- Reports build status

### Build Verification

After building, verify the output:

```bash
# Check if .aab exists
ls -lh build/app/outputs/bundle/release/app-release.aab

# Get file size
stat -c%s build/app/outputs/bundle/release/app-release.aab
```

### BUILD_AGENT Rules

As per the BUILD_AGENT role requirements:

- ✅ Execute: `flutter build appbundle --release`
- ✅ Verify: `.aab` file output exists
- ❌ Build failed → Exit with FAIL status

### Project Structure

```
flutter_app/
├── lib/
│   └── main.dart           # Application entry point
├── android/                # Android-specific configuration
│   ├── app/
│   │   ├── build.gradle    # Android app build config
│   │   └── src/main/
│   │       ├── AndroidManifest.xml
│   │       └── kotlin/     # MainActivity
│   ├── build.gradle        # Project-level build config
│   └── settings.gradle     # Gradle settings
├── pubspec.yaml            # Flutter dependencies
├── build_agent.sh          # Automated build script
└── README.md              # This file
```

### Troubleshooting

#### Flutter not found
```bash
# Add Flutter to PATH
export PATH="$PATH:/path/to/flutter/bin"

# Verify installation
flutter --version
```

#### Build fails
```bash
# Clean build cache
flutter clean

# Get dependencies
flutter pub get

# Rebuild
flutter build appbundle --release
```

#### Missing Android SDK
```bash
# Check Android SDK setup
flutter doctor -v

# Accept Android licenses
flutter doctor --android-licenses
```

## 📱 Running the App

```bash
# Run in debug mode
flutter run

# Run in release mode
flutter run --release

# Run on specific device
flutter run -d <device-id>
```

## 🧪 Testing

```bash
# Run all tests
flutter test

# Run with coverage
flutter test --coverage
```

## 📦 Distribution

The generated `.aab` file can be:
- Uploaded to Google Play Console for distribution
- Tested locally using `bundletool`
- Distributed via internal channels

## 🔗 Links

- [Flutter Documentation](https://docs.flutter.dev/)
- [Android App Bundle Documentation](https://developer.android.com/guide/app-bundle)
- [Tokyo-IA Main Repository](../README.md)
