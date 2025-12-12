# Tokyo-IA Android App

Android application for Tokyo-IA AI companion.

## Requirements

- Android SDK 24+ (Android 7.0+)
- JDK 17
- Gradle 8.4+

## Building

### Debug Build
```bash
./gradlew assembleDebug
```

### Release Build
```bash
./gradlew assembleRelease
```

### Install on Device
```bash
./gradlew installDebug
```

## Testing

```bash
./gradlew test
```

## Project Structure

- `src/main/java/com/tokyoia/app/` - Application source code
  - `TokyoApp.kt` - Application class
  - `MainActivity.kt` - Main activity
- `src/main/res/` - Resources (layouts, strings, etc.)
- `src/test/` - Unit tests

## Configuration

Configure signing for release builds by setting environment variables:
- `TOKYO_KEYSTORE_PATH` - Path to keystore file
- `TOKYO_KEYSTORE_PASSWORD` - Keystore password
- `TOKYO_KEY_ALIAS` - Key alias
- `TOKYO_KEY_PASSWORD` - Key password
