Tokyo-IA

Tokyo-IA is a mobile + web + server project that provides Tokyo-themed AI features and a MCP server.

Repository layout
tokyoia/
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

Agentes implementados mínimo

La carpeta `/agents` contiene las implementaciones base de los siguientes agentes:

| Agente | Archivo | Descripción |
|--------|---------|-------------|
| Agent_CodeMaster | `codemaster.go` | Análisis y generación de código |
| Agent_GenAI | `genai.go` | Generación de contenido con IA |
| Agent_Knowledge | `knowledge.go` | Gestión y recuperación de conocimiento |
| Agent_Sentiment | `sentiment.go` | Análisis de sentimiento |
| Agent_Unrestricted | `unrestricted.go` | Procesamiento sin restricciones |
| Agent_QA | `qa.go` | Aseguramiento de calidad |
| Agent_Deploy | `deploy.go` | Automatización de despliegue |

Para ejecutar los tests de agentes:
```bash
make test-agents
```

Contributing
See docs/CONTRIBUTING.md (if present) or open issues/PRs for proposed changes.

License
See LICENSE