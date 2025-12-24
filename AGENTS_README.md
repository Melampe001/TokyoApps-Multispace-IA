# 🤖 Tokyo-IA Agent Pipeline System

Complete automated pipeline for translating Flutter designs into native code for Android, iOS, and Web platforms.

## 📐 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         pipeline.sh                              │
│                    (Main Entry Point)                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    orchestrator/run_flow.sh                      │
│                   (Agent Coordination)                           │
└────┬────────┬────────┬────────┬────────┬────────────────────────┘
     │        │        │        │        │
     ▼        ▼        ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌────────┐
│ 1️⃣   │ │ 2️⃣   │ │ 3️⃣   │ │ 4️⃣   │ │  5️⃣    │
│Simu- │ │Brand │ │  UX  │ │Bridge│ │AutoDev │
│lator │ │Agent │ │Agent │ │Agent │ │ Agent  │
└──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └───┬────┘
   │        │        │        │         │
   ▼        ▼        ▼        ▼         ▼
┌──────────────────────────────────────────┐
│        simulator/output/                 │
│  • design_model.json                     │
│  • brand_tokens.json                     │
│  • ux_flow.json                          │
│  • platform_bridge.json                  │
└──────────────────┬───────────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │   output/       │
         │ • android/      │
         │ • ios/          │
         │ • web/          │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │  Emulator       │
         │  (Validation)   │
         └─────────────────┘
```

## 🚀 Usage

### Local Execution

```bash
# Run the complete pipeline
bash pipeline.sh

# Or run individual components
bash simulator/simulate_design.sh
bash orchestrator/run_flow.sh
bash emulator/run_emulator.sh
```

### GitHub Actions

The pipeline runs automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`
- Manual trigger via workflow dispatch

**Manual Trigger with Platform Selection:**

1. Go to Actions tab in GitHub
2. Select "Agent Pipeline" workflow
3. Click "Run workflow"
4. Select target platform: `all`, `android`, `ios`, or `web`

## 📊 Agent Details

| Agent | Function | Input | Output |
|-------|----------|-------|--------|
| **Simulator** | Extracts Flutter metadata | `flutter_app/` directory | `design_model.json` |
| **Brand Agent** | Generates design tokens | `design_model.json` | `brand_tokens.json` |
| **UX Agent** | Analyzes navigation & state | `design_model.json` | `ux_flow.json` |
| **Bridge Agent** | Creates platform mappings | - | `platform_bridge.json` |
| **AutoDev Agent** | Generates native code | All above outputs | Platform code files |
| **Emulator** | Validates & security scans | `output/` directory | `emulator_report.txt` |

## 📁 Output Structure

```
simulator/output/
├── design_model.json          # Flutter project metadata
├── brand_tokens.json          # Colors, typography, spacing
├── ux_flow.json              # Navigation and state patterns
├── platform_bridge.json      # Widget-to-platform mappings
├── emulator_report.txt       # Validation report
├── flutter_doctor.txt        # Flutter doctor output
├── flutter_analyze.txt       # Flutter analyze output
└── pub_get.txt              # Dependency fetch log

output/
├── android/
│   ├── MainActivity.kt       # Main activity class
│   └── activity_main.xml     # Layout XML
├── ios/
│   └── MainViewController.swift  # Main view controller
└── web/
    ├── App.tsx              # React component
    └── App.css              # Styles
```

## 🎯 Generated Code Examples

### Android

**MainActivity.kt**
```kotlin
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        // Setup with Material Design components
    }
}
```

**activity_main.xml**
```xml
<androidx.coordinatorlayout.widget.CoordinatorLayout>
    <com.google.android.material.appbar.AppBarLayout>
        <com.google.android.material.appbar.MaterialToolbar />
    </com.google.android.material.appbar.AppBarLayout>
</androidx.coordinatorlayout.widget.CoordinatorLayout>
```

### iOS

**MainViewController.swift**
```swift
class MainViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        setupConstraints()
    }
}
```

### Web

**App.tsx**
```typescript
const App: React.FC = () => {
  return (
    <main className="scaffold">
      <header className="app-bar">
        <h1>Tokyo-IA</h1>
      </header>
    </main>
  );
};
```

## 🔧 Configuration

### Environment Variables

- `TARGET_PLATFORM`: Set target platform for AutoDev agent
  - Values: `all` (default), `android`, `ios`, `web`
  - Example: `TARGET_PLATFORM=android bash pipeline.sh`

### Requirements

- **Flutter**: 3.0.0+
- **Dart**: 2.17.0+
- **jq**: JSON processor
- **yq**: YAML processor
- **xmllint**: XML validator (optional)
- **tree**: Directory tree viewer (optional)
- **Bash**: 4.0+

### Installation

```bash
# Ubuntu/Debian
sudo apt-get install jq yq xmllint tree

# macOS
brew install jq yq xmllint tree

# Make scripts executable
chmod +x pipeline.sh
chmod +x orchestrator/run_flow.sh
chmod +x simulator/simulate_design.sh
chmod +x agents/*.sh
chmod +x emulator/run_emulator.sh
```

## 🧪 Testing

### Validate Scripts

```bash
# Check syntax with shellcheck
shellcheck *.sh agents/*.sh simulator/*.sh orchestrator/*.sh emulator/*.sh

# Run the pipeline
bash pipeline.sh

# Verify outputs
ls -lah simulator/output/
ls -lah output/android/ output/ios/ output/web/
```

### Check Validation Report

```bash
cat simulator/output/emulator_report.txt
```

## 🔍 Validation Checks

The emulator performs the following validations:

### Android
- ✅ MainActivity.kt exists with valid package
- ✅ Required imports present
- ✅ activity_main.xml is valid XML
- ✅ No deprecated APIs
- ✅ CoordinatorLayout and MaterialToolbar present

### iOS
- ✅ MainViewController.swift exists
- ✅ UIKit import present
- ✅ Valid class declaration
- ✅ viewDidLoad implementation
- ✅ Auto Layout constraints

### Web
- ✅ App.tsx exists with React import
- ✅ Valid React.FC component
- ✅ Semantic HTML elements
- ⚠️  Accessibility attributes (warning if missing)
- ✅ App.css with required classes

### Security
- 🔒 No hardcoded secrets (api_key, password, token)
- 🔒 No SQL injection patterns
- 🔒 No prohibited APIs (ANDROID_ID, etc.)

## 📈 CI/CD Integration

### GitHub Actions Features

- ✅ Automatic execution on push/PR
- ✅ Manual trigger with platform selection
- ✅ Artifact uploads (30-day retention)
- ✅ PR comments with results
- ✅ Workflow summary with metrics
- ✅ Security scanning job
- ✅ Deprecated API detection

### Artifacts

All pipeline runs upload the following artifacts:

1. **simulator-outputs**: JSON files and logs
2. **android-code**: Generated Kotlin and XML
3. **ios-code**: Generated Swift files
4. **web-code**: Generated TypeScript and CSS

## 🎨 Widget Mappings

| Flutter | Android | iOS | Web |
|---------|---------|-----|-----|
| Scaffold | CoordinatorLayout | UIViewController | `<main>` |
| AppBar | MaterialToolbar | UINavigationBar | `<header>` |
| Text | TextView | UILabel | `<span>` |
| Button | MaterialButton | UIButton | `<button>` |
| Container | FrameLayout | UIView | `<div>` |
| Column | LinearLayout (V) | UIStackView (V) | Flexbox column |
| Row | LinearLayout (H) | UIStackView (H) | Flexbox row |
| ListView | RecyclerView | UITableView | `<ul>` |

## 🔄 State Management Mappings

| Flutter | Android | iOS | Web |
|---------|---------|-----|-----|
| setState | LiveData/ViewModel | Property Observers | React useState |
| Provider | ViewModel/Repository | ObservableObject | React Context |
| Riverpod | Hilt/Dagger DI | Environment Objects | Context with Hooks |
| BLoC | LiveData streams | Combine Publishers | Redux/RxJS |

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Basic widget mappings
- ✅ Design token extraction
- ✅ Code generation for 3 platforms
- ✅ Validation and security scanning
- ✅ CI/CD integration

### Phase 2 (Planned)
- 🔜 Advanced widget support (Lists, Forms, etc.)
- 🔜 Animation and transition mapping
- 🔜 API integration code generation
- 🔜 Unit test generation
- 🔜 Platform-specific optimization

### Phase 3 (Future)
- 🔮 AI-powered design recommendations
- 🔮 A/B testing variant generation
- 🔮 Performance profiling
- 🔮 Accessibility compliance checking
- 🔮 Multi-language support

## 🐛 Troubleshooting

### Flutter not found
```bash
# Install Flutter or add to PATH
export PATH="$PATH:/path/to/flutter/bin"
```

### Permission denied
```bash
# Make scripts executable
chmod +x pipeline.sh orchestrator/run_flow.sh simulator/simulate_design.sh agents/*.sh emulator/run_emulator.sh
```

### jq/yq not found
```bash
# Ubuntu/Debian
sudo apt-get install jq yq

# macOS
brew install jq yq
```

### Validation failures
Check the detailed report:
```bash
cat simulator/output/emulator_report.txt
```

## 📚 References

- [Flutter Documentation](https://docs.flutter.dev/)
- [Material Design](https://material.io/design)
- [iOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [React Documentation](https://react.dev/)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

See LICENSE file in the repository root.

## 💬 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section above

---

**Generated by Tokyo-IA Agent Pipeline System** 🚀
