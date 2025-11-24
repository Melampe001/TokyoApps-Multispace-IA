tokyoia/
│
├── app/                                   # Android – Proyecto principal
│   ├── build.gradle                       # Config firmado + release
│   ├── proguard-rules.pro
│   ├── src/
│   │   ├── main/
│   │   │   ├── AndroidManifest.xml
│   │   │   ├── java/com/tokyoia/app/
│   │   │   │   └── TokyoApp.kt
│   │   │   └── res/
│   │   │       ├── layout/activity_main.xml
│   │   │       ├── mipmap-*/              # Íconos de app
│   │   │       └── values/strings.xml
│   │   └── test/
│   │       └── ExampleUnitTest.kt
│   └── gradle.properties
│
├── web/                                   # Sitio web + panel IA
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   └── styles/
│   └── public/
│
├── server-mcp/                            # Servidor Node para TokyoIA MCP
│   ├── index.js
│   ├── package.json
│   ├── tokyo-rules.json
│   └── src/
│       ├── actions/
│       └── context/
│
├── whatsnew/                              # Notas para Google Play
│   ├── en-US/whatsnew.txt
│   └── es-MX/whatsnew.txt
│
├── .github/
│   └── workflows/
│       ├── android-build.yml              # Build AAB
│       ├── tokyoia-release-to-play.yml    # Auto release a Play Store
│       └── security-scan.yml              # Opcional
│
├── scripts/
│   ├── bump-version.sh                    # Incrementa versión
│   └── generate-release.sh                # Compila + tag + push
│
├── tokyoia-keystore.jks (NO subir)        # Local, se convierte a base64
│
├── .gitignore
├── README.md
└── LICENSE
