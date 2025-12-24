# 🚀 Tokyo-IA Premium Pipeline & Agent Architecture Guide

Complete guide for the Tokyo-IA automated pipeline system that translates Flutter applications into native code for Android, iOS, and Web platforms.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Detailed Usage](#detailed-usage)
- [Agent System](#agent-system)
- [Output Structure](#output-structure)
- [Integration Guide](#integration-guide)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Advanced Configuration](#advanced-configuration)

## Overview

The Tokyo-IA pipeline is a premium architecture for automating cross-platform code generation. It analyzes Flutter applications and generates production-ready native code following platform best practices.

### Key Features

✅ **Multi-Platform Generation**: Android (Kotlin), iOS (Swift), Web (React/TypeScript)  
✅ **Design Token Extraction**: Automated brand consistency  
✅ **UX Pattern Analysis**: Navigation and state management mapping  
✅ **Security Validation**: Built-in security scanning  
✅ **Compliance Checks**: Platform store policy validation  
✅ **Production Quality**: Follows platform best practices  

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     pipeline.sh                             │
│              (Main Entry Point)                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                orchestrator/run_flow.sh                      │
│              (Agent Coordination)                            │
└──┬────┬────┬────┬────┬───────────────────────────────────────┘
   │    │    │    │    │
   ▼    ▼    ▼    ▼    ▼
┌────┐┌────┐┌────┐┌────┐┌────────┐
│ 1️⃣ ││ 2️⃣ ││ 3️⃣ ││ 4️⃣ ││  5️⃣   │
│Sim ││Brnd││ UX ││Brdg││AutoDev │
└─┬──┘└─┬──┘└─┬──┘└─┬──┘└───┬────┘
  │     │     │     │       │
  └─────┴─────┴─────┴───────┘
                │
                ▼
      ┌──────────────────┐
      │   output/        │
      │ • android/       │
      │ • ios/           │
      │ • web/           │
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │   Emulator       │
      │  (Validation)    │
      └──────────────────┘
```

### Pipeline Phases

**Phase 1: Agent Orchestration**
1. **Simulator** - Extracts Flutter metadata and design model
2. **Brand Agent** - Generates design tokens (colors, typography, spacing)
3. **UX Agent** - Analyzes navigation patterns and user flows
4. **Bridge Agent** - Creates widget-to-platform mappings
5. **AutoDev Agent** - Generates platform-specific code

**Phase 2: Code Validation**
- Platform-specific validation (syntax, structure, APIs)
- Security scanning (secrets, injection risks)
- Compliance checking (store policies)

**Phase 3: Results Summary**
- Execution metrics
- Output structure
- Next steps

## Quick Start

### Basic Usage

```bash
# 1. Ensure Flutter app exists in flutter_app/ directory
ls flutter_app/

# 2. Run the complete pipeline
bash pipeline.sh

# 3. Review generated code
ls output/android/
ls output/ios/
ls output/web/

# 4. Check validation report
cat simulator/output/emulator_report.txt
```

### Platform-Specific Generation

```bash
# Generate only Android code
TARGET_PLATFORM=android bash pipeline.sh

# Generate only iOS code
TARGET_PLATFORM=ios bash pipeline.sh

# Generate only Web code
TARGET_PLATFORM=web bash pipeline.sh

# Generate all platforms (default)
TARGET_PLATFORM=all bash pipeline.sh
```

## Prerequisites

### Required

- **Bash**: Version 4.0 or higher
- **jq**: JSON processor (`apt install jq` or `brew install jq`)
- **Flutter app**: Located in `flutter_app/` directory

### Optional (for enhanced features)

- **Flutter SDK**: For flutter doctor and analyze
- **tree**: For better output visualization
- **xmllint**: For XML validation
- **yq**: For YAML processing

### Installation

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y bash jq tree libxml2-utils

# macOS
brew install bash jq tree

# Verify installation
bash --version  # Should be 4.0+
jq --version
```

## Detailed Usage

### Step-by-Step Workflow

#### 1. Prepare Your Flutter App

```bash
# Ensure flutter_app directory exists with valid Flutter project
flutter_app/
├── lib/
│   ├── main.dart
│   └── ...
├── pubspec.yaml
└── ...
```

#### 2. Run Individual Components (Optional)

```bash
# Run simulator only
bash simulator/simulate_design.sh

# Run orchestrator (all agents)
bash orchestrator/run_flow.sh

# Run emulator validation only
bash emulator/run_emulator.sh
```

#### 3. Run Complete Pipeline

```bash
# Standard execution
bash pipeline.sh

# With verbose output (if you modify scripts)
bash -x pipeline.sh
```

#### 4. Review Outputs

```bash
# View design model
jq . simulator/output/design_model.json

# View brand tokens
jq . simulator/output/brand_tokens.json

# View UX flow
jq . simulator/output/ux_flow.json

# View platform bridge
jq . simulator/output/platform_bridge.json

# View validation report
cat simulator/output/emulator_report.txt
```

## Agent System

### Agent Definitions

Each agent has:
- **Executor Script**: `agents/{name}_executor.sh` - Executable implementation
- **Definition File**: `agents/{name}.agent` - Complete documentation and specification

### Available Agents

#### 1. Brand Agent (`brand.agent` / `brand_executor.sh`)

**Purpose**: Extract design tokens for cross-platform consistency

**Input**: 
- `simulator/output/design_model.json`
- `flutter_app/lib/main.dart` (for theme)

**Output**: `simulator/output/brand_tokens.json`
```json
{
  "colors": { "primary": "#673AB7", ... },
  "typography": { "heading1": {...}, ... },
  "spacing": { "xs": 4, "sm": 8, ... },
  "elevation": { "low": 2, ... },
  "border_radius": { "sm": 4, ... }
}
```

**Key Features**:
- Material Design 3 defaults
- Theme color extraction
- Comprehensive design system

#### 2. UX Agent (`ux.agent` / `ux_executor.sh`)

**Purpose**: Analyze navigation patterns and user experience

**Input**: 
- `simulator/output/design_model.json`
- `flutter_app/lib/` (source code)

**Output**: `simulator/output/ux_flow.json`
```json
{
  "navigation": {
    "type": "named_routes|imperative|basic",
    "routes": [...],
    "patterns": {...}
  },
  "state_management": {
    "type": "setState|provider|riverpod|bloc",
    "complexity": "low|medium|high"
  },
  "interactions": ["tap", "text_input", ...]
}
```

**Key Features**:
- Navigation pattern detection
- State management classification
- Interaction type identification
- User flow documentation

#### 3. Bridge Agent (`bridge.agent` / `bridge_executor.sh`)

**Purpose**: Create widget-to-platform component mappings

**Input**: None (static knowledge base)

**Output**: `simulator/output/platform_bridge.json`
```json
{
  "widget_mappings": {
    "Scaffold": {
      "android": {"component": "CoordinatorLayout", ...},
      "ios": {"component": "UIViewController", ...},
      "web": {"component": "<main>", ...}
    }
  },
  "state_management_mappings": {...},
  "navigation_mappings": {...}
}
```

**Key Features**:
- 10+ core widget mappings
- State management patterns
- Navigation strategies
- Platform best practices

#### 4. AutoDev Agent (`autodev.agent` / `autodev_executor.sh`)

**Purpose**: Generate production-ready native code

**Input**: 
- `simulator/output/platform_bridge.json`
- `simulator/output/brand_tokens.json`
- `simulator/output/ux_flow.json` (optional)

**Output**: 
- `output/android/MainActivity.kt`
- `output/android/activity_main.xml`
- `output/ios/MainViewController.swift`
- `output/web/App.tsx`
- `output/web/App.css`

**Key Features**:
- Platform-specific code generation
- Brand token application
- Modern API usage
- Type safety (Kotlin, Swift, TypeScript)

## Output Structure

```
project/
├── simulator/output/
│   ├── design_model.json       # Flutter project metadata
│   ├── brand_tokens.json       # Design system tokens
│   ├── ux_flow.json           # Navigation and UX patterns
│   ├── platform_bridge.json   # Widget-to-platform mappings
│   ├── emulator_report.txt    # Validation report
│   ├── flutter_doctor.txt     # Flutter environment info
│   ├── flutter_analyze.txt    # Code analysis results
│   └── pub_get.txt           # Dependency fetch log
│
├── output/
│   ├── android/
│   │   ├── MainActivity.kt
│   │   └── activity_main.xml
│   ├── ios/
│   │   └── MainViewController.swift
│   └── web/
│       ├── App.tsx
│       └── App.css
│
└── agents/
    ├── brand.agent            # Brand agent specification
    ├── ux.agent              # UX agent specification
    ├── bridge.agent          # Bridge agent specification
    ├── autodev.agent         # AutoDev agent specification
    ├── brand_executor.sh     # Brand agent implementation
    ├── ux_executor.sh        # UX agent implementation
    ├── bridge_executor.sh    # Bridge agent implementation
    └── autodev_executor.sh   # AutoDev agent implementation
```

## Integration Guide

### Android Integration

```bash
# 1. Copy generated files to your Android project
cp output/android/MainActivity.kt android-project/app/src/main/java/com/tokyoia/app/
cp output/android/activity_main.xml android-project/app/src/main/res/layout/

# 2. Update build.gradle dependencies
cat << 'EOF' >> android-project/app/build.gradle
dependencies {
    implementation 'androidx.coordinatorlayout:coordinatorlayout:1.2.0'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
}
EOF

# 3. Sync and build
cd android-project
./gradlew build
```

### iOS Integration

```bash
# 1. Add to Xcode project
# Open Xcode project
# File > Add Files to "Project"
# Select output/ios/MainViewController.swift

# 2. Set as initial view controller
# In AppDelegate or SceneDelegate:
#   let viewController = MainViewController()
#   navigationController.viewControllers = [viewController]

# 3. Build
xcodebuild -project MyApp.xcodeproj -scheme MyApp build
```

### Web Integration

```bash
# 1. Copy to React project
cp output/web/App.tsx react-project/src/
cp output/web/App.css react-project/src/

# 2. Update index.tsx or main routing
# Import and use the generated App component

# 3. Build
cd react-project
npm install
npm run build
```

## Troubleshooting

### Common Issues

#### Issue: "flutter_app/ directory not found"

**Solution**:
```bash
# Ensure Flutter app exists
ls flutter_app/

# If missing, create or clone your Flutter project
flutter create flutter_app
# OR
git clone <your-flutter-repo> flutter_app
```

#### Issue: "jq: command not found"

**Solution**:
```bash
# Install jq
sudo apt install jq    # Ubuntu/Debian
brew install jq        # macOS
```

#### Issue: "No widgets found" or minimal metadata

**Solution**:
```bash
# Ensure Flutter app has content
ls flutter_app/lib/

# Check main.dart exists
cat flutter_app/lib/main.dart
```

#### Issue: "Validation failed with errors"

**Solution**:
```bash
# Review validation report
cat simulator/output/emulator_report.txt

# Common fixes:
# - Ensure brand_tokens.json has valid hex colors
# - Check generated code for syntax errors
# - Verify platform_bridge.json is complete
```

#### Issue: "Permission denied"

**Solution**:
```bash
# Make scripts executable
chmod +x pipeline.sh
chmod +x orchestrator/run_flow.sh
chmod +x emulator/run_emulator.sh
chmod +x simulator/simulate_design.sh
chmod +x agents/*.sh
```

### Debug Mode

```bash
# Run with verbose output
bash -x pipeline.sh 2>&1 | tee pipeline_debug.log

# Check individual agent
bash -x agents/brand_executor.sh

# Validate JSON outputs
jq empty simulator/output/*.json
```

## Best Practices

### Before Running Pipeline

1. ✅ **Verify Flutter App**: Ensure flutter_app/ has valid Flutter project
2. ✅ **Check Dependencies**: Install jq, bash 4.0+
3. ✅ **Clean Previous Runs**: `rm -rf output/ simulator/output/` (optional)
4. ✅ **Review Flutter Code**: Ensure no syntax errors

### During Execution

1. ✅ **Monitor Output**: Watch for errors or warnings
2. ✅ **Check Logs**: Review agent outputs as they run
3. ✅ **Validate Each Phase**: Ensure each phase completes

### After Execution

1. ✅ **Review Validation Report**: Check `simulator/output/emulator_report.txt`
2. ✅ **Inspect Generated Code**: Review `output/` directory files
3. ✅ **Test Compilation**: Verify generated code compiles
4. ✅ **Customize**: Enhance generated code with business logic

### Code Quality

- **Generated code is a starting point**: Enhance with business logic
- **Review before production**: Generated code should be reviewed
- **Test thoroughly**: Add unit tests and integration tests
- **Follow platform guidelines**: Customize to match platform best practices

## Advanced Configuration

### Environment Variables

```bash
# Platform selection
export TARGET_PLATFORM=android  # android, ios, web, or all (default)

# Custom output directory (modify scripts if needed)
export OUTPUT_BASE=/custom/path/output

# Debug mode
export DEBUG=1
```

### Customization

#### Add Custom Widget Mappings

Edit `agents/bridge_executor.sh` to add new widget mappings:

```bash
# Add to widget_mappings section in platform_bridge.json
"CustomWidget": {
  "android": {
    "component": "CustomAndroidView",
    "package": "com.example.CustomAndroidView",
    "description": "Custom description"
  },
  # ... iOS and Web
}
```

#### Customize Brand Tokens

Modify `agents/brand_executor.sh` to extract custom theme properties:

```bash
# Add custom color extraction
ACCENT_COLOR=$(grep "accentColor" "$MAIN_DART" | ...)
```

#### Extend Code Generation

Modify `agents/autodev_executor.sh` to generate additional components:

```bash
# Add button generation
cat > "$OUTPUT_BASE/android/CustomButton.kt" << EOF
# ... button code
EOF
```

### CI/CD Integration

#### GitHub Actions

```yaml
name: Tokyo-IA Pipeline

on:
  push:
    branches: [main, develop]
  workflow_dispatch:
    inputs:
      platform:
        description: 'Target Platform'
        required: true
        default: 'all'
        type: choice
        options:
          - all
          - android
          - ios
          - web

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install dependencies
        run: sudo apt-get install -y jq tree
      
      - name: Run pipeline
        run: TARGET_PLATFORM=${{ github.event.inputs.platform || 'all' }} bash pipeline.sh
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: generated-code
          path: output/
```

#### GitLab CI

```yaml
tokyo-ia-pipeline:
  image: ubuntu:latest
  before_script:
    - apt-get update
    - apt-get install -y bash jq tree
  script:
    - bash pipeline.sh
  artifacts:
    paths:
      - output/
      - simulator/output/emulator_report.txt
```

### Performance Optimization

```bash
# Parallel agent execution (experimental)
# Modify orchestrator/run_flow.sh to run independent agents in parallel
(bash agents/brand_executor.sh &)
(bash agents/bridge_executor.sh &)
wait
```

## Support & Resources

### Documentation

- **Agent Definitions**: See `agents/*.agent` files for detailed specifications
- **Architecture**: See `AGENTS_README.md` for pipeline architecture
- **API Reference**: See generated code comments for usage

### Getting Help

1. **Check Logs**: Review `simulator/output/` for error messages
2. **Validation Report**: Read `emulator_report.txt` for issues
3. **Agent Specs**: Consult `.agent` files for detailed documentation
4. **Repository Issues**: Open GitHub issue with logs

### Contributing

To extend or improve the pipeline:

1. Study existing agent implementations
2. Follow bash scripting best practices
3. Update corresponding `.agent` documentation
4. Add validation logic to emulator
5. Test with various Flutter apps

## Recommendations

### For Production Use

⚠️ **Important Notes**:

1. **Review Generated Code**: Always review before production
2. **Add Business Logic**: Generated code is structural scaffold
3. **Test Thoroughly**: Add comprehensive tests
4. **Security Review**: Perform security audit on generated code
5. **Platform Guidelines**: Ensure compliance with platform requirements

### Optimization Tips

- **Clean Runs**: Remove `output/` and `simulator/output/` between runs
- **Selective Generation**: Use `TARGET_PLATFORM` for faster iterations
- **Cache Dependencies**: Cache Flutter dependencies for faster analysis
- **Parallel Execution**: Run independent agents in parallel (experimental)

### Future Enhancements

Planned features:

- 🔜 Form component generation
- 🔜 Navigation implementation
- 🔜 State management setup
- 🔜 API integration stubs
- 🔜 Animation generation
- 🔜 Internationalization support

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Maintainer**: Tokyo-IA Team

For more information, visit the project repository or consult `AGENTS_README.md`.
