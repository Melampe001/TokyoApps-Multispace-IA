Tokyo-IA

Tokyo-IA is a mobile + web + server project that provides Tokyo-themed AI features and a MCP server.

## Bot Architecture

Tokyo-IA implements a microservices architecture with **4 specialized coordinator bots** (2 Python, 2 Node.js) that manage different aspects of the AI system:

### Python Coordinators
1. **KnowledgeCoordinator** - RAG, web search, and knowledge management
2. **SentimentCoordinator** - Emotion analysis and response adaptation

### Node.js Coordinators
3. **GenAICoordinator** - Multimedia generation (images, videos, music)
4. **DeploymentCoordinator** - Build automation and deployment

See [agents/README.md](agents/README.md) and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

Repository layout
tokyoia/
│
├── agents/                              # AI Bots and Coordinators
│   ├── python_bots/                     # Python coordinators
│   │   ├── knowledge_coordinator/       # RAG + web search
│   │   └── sentiment_coordinator/       # Emotion analysis
│   └── node_bots/                       # Node.js coordinators
│       ├── genai_coordinator/           # Multimedia generation
│       └── deployment_coordinator/      # Build automation
│
├── app/                                   # Android – main project
│   ├── build.gradle                       # Config signed + release
│   ├── proguard-rules.pro
│   ├── src/
│   │   ├── main/
│   │   │   ├── AndroidManifest.xml
│   │   │   ├── java/com/tokyoia/app/
│   │   │   │   └── TokyoApp.kt
│   │   │   └── res/
│   │   │       ├── layout/activity_main.xml
│   │   │       ├── mipmap-*/              # App icons
│   │   │       └── values/strings.xml
│   │   └── test/
│   │       └── ExampleUnitTest.kt
│   └── gradle.properties
│
├── web/                                   # Web site + admin panel
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── src/
│       ├── App.jsx
│       ├── components/
│       └── styles/
│
├── server-mcp/                            # Node server for MCP
│   ├── index.js
│   ├── package.json
│   ├── tokyo-rules.json
│   └── src/
│       ├── actions/
│       └── context/
│
├── whatsnew/                              # Play Store release notes
│   ├── en-US/whatsnew.txt
│   └── es-MX/whatsnew.txt
│
├── .github/
│   └── workflows/
│       ├── android-build.yml              # Build AAB
│       ├── tokyoia-release-to-play.yml    # Auto release to Play Store
│       └── security-scan.yml              # Optional
│
├── scripts/
│   ├── bump-version.sh                    # Increment version
│   └── generate-release.sh                # Build + tag + push
│
├── .gitignore
├── README.md
└── LICENSE

Quick start (high level)
- Bots (development):
  - Python: cd agents/python_bots && pip install -r requirements.txt
  - Node.js: cd agents/node_bots && npm install
  - See [agents/README.md](agents/README.md) for detailed setup
- Android (local debug):
  - ./gradlew assembleDebug
  - ./gradlew installDebug
- Web (dev):
  - cd web && npm install && npm run dev
- Server (local):
  - cd server-mcp && npm install && npm start

Security / Secrets (IMPORTANT)
Do NOT store service account JSONs, keystore files, private keys, or other secrets in the repository. If you need to provide credentials for CI:
- Create the credential (e.g., Google Play service account JSON) locally.
- Encode keystore files or JSON as base64 (or keep them as files) and store them in GitHub Actions Secrets.
- Reference secrets in workflows using: ${{ secrets.GOOGLE_PLAY_JSON }}, ${{ secrets.ANDROID_KEYSTORE_BASE64 }}, etc.

If any secret was ever committed:
1. Rotate the exposed credential immediately (revoke old key).
2. Remove the secret from the repository and history (see docs/SECRETS.md).
3. Notify collaborators and ask them to reclone if history was rewritten.

Where to find release notes
- whatsnew/en-US/whatsnew.txt
- whatsnew/es-MX/whatsnew.txt

Contributing
See docs/CONTRIBUTING.md (if present) or open issues/PRs for proposed changes.

License
See LICENSE