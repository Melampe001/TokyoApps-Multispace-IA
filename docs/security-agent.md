# Security Agent - Android Manifest Auditor

## Overview

The Security Agent is a command-line tool that audits AndroidManifest.xml files to detect forbidden permissions that violate local-first architecture principles. It helps ensure your Android applications respect user privacy and do not collect unnecessary data.

## Role

**SECURITY_AGENT**: Automated security auditing for Android applications

## Features

- 🔍 **Automatic Detection**: Scans directories for AndroidManifest.xml files
- 🚫 **Forbidden Permission Detection**: Identifies privacy-invasive permissions
- ✅ **Local-First Verification**: Ensures applications follow local-first principles
- 📊 **Detailed Reporting**: Clear, formatted output with permission categories
- 🎯 **Exit Codes**: Integration-ready exit codes for CI/CD pipelines

## Installation

### Build from Source

```bash
# Using Make
make security-agent

# Using Go directly
go build -o bin/security-agent ./cmd/security-agent/main.go
```

The binary will be created at `bin/security-agent`.

## Usage

### Basic Usage

```bash
# Audit current directory
./bin/security-agent

# Audit specific directory
./bin/security-agent -path ./app/src/main

# Audit specific file
./bin/security-agent -path ./app/src/main/AndroidManifest.xml

# Verbose output with banner
./bin/security-agent -path . -v
```

### Command Line Options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-path` | string | `.` | Path to directory or AndroidManifest.xml file |
| `-v` | bool | `false` | Verbose output with banner |
| `-h` | bool | `false` | Show help message |

### Exit Codes

- `0`: All audits passed (no forbidden permissions found)
- `1`: One or more audits failed (forbidden permissions detected)

## Forbidden Permissions

The security agent detects the following categories of forbidden permissions:

### 🌍 LOCATION
Permissions that track user location:
- `ACCESS_FINE_LOCATION`
- `ACCESS_COARSE_LOCATION`
- `ACCESS_BACKGROUND_LOCATION`

### 📇 CONTACTS
Permissions that access user contacts:
- `READ_CONTACTS`
- `WRITE_CONTACTS`
- `GET_ACCOUNTS`

### 📷 CAMERA
Permissions that access device camera:
- `CAMERA`

### 📡 TRACKING
Permissions used for tracking and analytics:
- `READ_PHONE_STATE`
- `ACCESS_WIFI_STATE`
- `BLUETOOTH`
- `BLUETOOTH_ADMIN`
- `BLUETOOTH_CONNECT`
- `BLUETOOTH_SCAN`

### 🔄 BACKGROUND_SERVICES
Permissions for background processing:
- `WAKE_LOCK`
- `FOREGROUND_SERVICE`
- `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`
- `SYSTEM_ALERT_WINDOW`

### 🔐 PRIVACY
Additional privacy-invasive permissions:
- `RECORD_AUDIO`
- `READ_SMS` / `SEND_SMS` / `RECEIVE_SMS`
- `READ_CALL_LOG` / `WRITE_CALL_LOG`

## Output Examples

### ✅ Clean Manifest (PASS)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔒 ANDROID MANIFEST SECURITY AUDIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ PASS: /path/to/AndroidManifest.xml
   Total Permissions: 3
   Local-First: true
   All Permissions:
      • android.permission.INTERNET
      • android.permission.WRITE_EXTERNAL_STORAGE
      • android.permission.READ_EXTERNAL_STORAGE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary: 1 passed, 0 failed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ AUDIT PASSED: No forbidden permissions detected
   Local-first architecture verified
```

### ❌ Manifest with Forbidden Permissions (FAIL)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔒 ANDROID MANIFEST SECURITY AUDIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ FAIL: /path/to/AndroidManifest.xml
   Total Permissions: 8
   Local-First: false
   ⚠️  Forbidden Permissions Detected: 7
      • [LOCATION] ACCESS_FINE_LOCATION - Fine location access
      • [LOCATION] ACCESS_COARSE_LOCATION - Coarse location access
      • [CAMERA] CAMERA - Camera access
      • [CONTACTS] READ_CONTACTS - Read contacts
      • [BACKGROUND_SERVICES] WAKE_LOCK - Wake lock for background services
      • [TRACKING] READ_PHONE_STATE - Read phone state (tracking)
      • [TRACKING] BLUETOOTH - Bluetooth (tracking)
   All Permissions:
      • android.permission.INTERNET
      • android.permission.ACCESS_FINE_LOCATION
      • android.permission.ACCESS_COARSE_LOCATION
      • android.permission.CAMERA
      • android.permission.READ_CONTACTS
      • android.permission.WAKE_LOCK
      • android.permission.READ_PHONE_STATE
      • android.permission.BLUETOOTH

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary: 0 passed, 1 failed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ AUDIT FAILED: Forbidden permissions detected
   Local-first architecture violated
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Security Audit

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  android-security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Go
        uses: actions/setup-go@v4
        with:
          go-version: '1.21'
      
      - name: Build Security Agent
        run: make security-agent
      
      - name: Run Security Audit
        run: ./bin/security-agent -path ./app -v
```

### GitLab CI

```yaml
android-security-audit:
  stage: test
  image: golang:1.21
  script:
    - make security-agent
    - ./bin/security-agent -path ./app -v
  only:
    - merge_requests
    - main
```

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Build security agent if not exists
if [ ! -f "./bin/security-agent" ]; then
    make security-agent
fi

# Run security audit
./bin/security-agent -path ./app

# Capture exit code
RESULT=$?

if [ $RESULT -ne 0 ]; then
    echo "❌ Security audit failed. Commit rejected."
    echo "   Please remove forbidden permissions from AndroidManifest.xml"
    exit 1
fi

echo "✅ Security audit passed"
exit 0
```

## Local-First Architecture

Local-first applications prioritize:

1. **Privacy**: No unnecessary data collection
2. **Offline-first**: Works without internet connection
3. **User Control**: Data stays on user's device
4. **No Tracking**: No analytics or telemetry without explicit consent

### Allowed Permissions

Common permissions that are typically acceptable:
- `INTERNET` - For optional features
- `READ_EXTERNAL_STORAGE` / `WRITE_EXTERNAL_STORAGE` - Local file access
- `VIBRATE` - User feedback
- `POST_NOTIFICATIONS` - User-facing notifications

### Why These Permissions are Forbidden

| Permission | Reason |
|------------|--------|
| Location | Tracks user movement, privacy violation |
| Contacts | Accesses private user data |
| Camera | Can capture images without consent |
| Phone State | Used for device fingerprinting |
| Bluetooth/WiFi | Used for location tracking |
| Background Services | Enables persistent tracking |
| SMS/Call Logs | Highly sensitive personal data |

## Development

### Project Structure

```
internal/security/
├── manifest_auditor.go       # Main auditor implementation
└── manifest_auditor_test.go  # Comprehensive tests

cmd/security-agent/
└── main.go                   # CLI implementation
```

### Running Tests

```bash
# Run all tests
go test ./internal/security/... -v

# Run with coverage
go test ./internal/security/... -cover

# Run specific test
go test ./internal/security/... -run TestAuditManifestFile_CleanManifest
```

### Test Coverage

The security package includes comprehensive tests:
- Clean manifest validation
- Forbidden permission detection
- Multiple manifest scanning
- Error handling
- XML parsing validation
- Directory traversal
- Permission categorization

Current test coverage: **100%**

## API Usage

You can also use the security agent as a Go library:

```go
package main

import (
    "fmt"
    "github.com/Melampe001/Tokyo-IA/internal/security"
)

func main() {
    // Create auditor
    auditor := security.NewManifestAuditor()
    
    // Audit single file
    result, err := auditor.AuditManifestFile("path/to/AndroidManifest.xml")
    if err != nil {
        panic(err)
    }
    
    if !result.Passed {
        fmt.Println("❌ Audit failed!")
        for _, forbidden := range result.ForbiddenFound {
            fmt.Printf("  • [%s] %s\n", forbidden.Category, forbidden.Name)
        }
    }
    
    // Audit entire directory
    results, err := auditor.AuditDirectory("./app")
    if err != nil {
        panic(err)
    }
    
    // Print formatted results
    security.PrintResults(results)
    
    // Check for failures
    if security.HasFailures(results) {
        // Handle failure
    }
}
```

## Troubleshooting

### No manifests found

**Problem**: `Error: no AndroidManifest.xml files found`

**Solution**: 
- Verify you're in the correct directory
- Check that AndroidManifest.xml files exist
- Ensure files are not in hidden directories (starting with `.`)

### Permission not detected

**Problem**: Expected permission not flagged as forbidden

**Solution**:
- Check the exact permission name in the manifest
- Verify the permission is in the forbidden list
- Open an issue with the permission details

### XML parsing error

**Problem**: `Error: failed to parse manifest XML`

**Solution**:
- Validate your AndroidManifest.xml syntax
- Check for proper XML structure
- Ensure all tags are properly closed

## Contributing

To add new forbidden permissions:

1. Edit `internal/security/manifest_auditor.go`
2. Add to `ForbiddenPermissions` slice
3. Specify category and description
4. Add tests in `manifest_auditor_test.go`
5. Run tests: `go test ./internal/security/...`

## License

Apache 2.0 - See LICENSE file for details

## Support

For issues or questions:
- Open an issue: https://github.com/Melampe001/Tokyo-IA/issues
- Security concerns: See SECURITY.md

---

**RULE**: Forbidden permission detected → FAIL
