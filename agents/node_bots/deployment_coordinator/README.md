# DeploymentCoordinator (Coordinador de Despliegue)

Bot coordinador Node.js responsable de la compilación, firmado y despliegue automático de aplicaciones.

## Descripción

El DeploymentCoordinator es uno de los dos coordinadores implementados en Node.js. Su función principal es automatizar todo el proceso de build, release y deployment.

## Responsabilidades

- **Build Automation**: Compilación automática de APK/AAB (Android) e IPA (iOS)
- **Code Signing**: Firmado de aplicaciones con keystores
- **CI/CD Integration**: Integración con GitHub Actions y otros pipelines
- **Version Management**: Gestión automática de versiones y changelogs
- **Store Deployment**: Publicación automática a Play Store / App Store

## Agentes Especializados

### Deployment_BuildAgent
- Compilación de proyectos Android/iOS/Web
- Configuración de build variants
- Optimización de builds (ProGuard, R8)

### Deployment_SignAgent  
- Firmado de APK/AAB con keystore
- Gestión de certificados
- Verificación de integridad

### Deployment_ReleaseAgent
- Creación de releases en GitHub
- Upload de artifacts
- Publicación a stores

### Deployment_VersionAgent
- Bump de versiones (major, minor, patch)
- Generación de changelogs
- Gestión de tags Git

## Tecnologías

```json
{
  "dependencies": {
    "express": "^4.18.0",
    "fastlane": "^2.217.0",
    "@google-cloud/storage": "^7.7.0",
    "simple-git": "^3.21.0",
    "semver": "^7.5.4",
    "node-gradle": "^0.0.6",
    "axios": "^1.6.0",
    "winston": "^3.11.0"
  }
}
```

## Instalación

```bash
cd agents/node_bots/deployment_coordinator
npm install

# Instalar dependencias adicionales
sudo apt-get install gradle fastlane
```

## API

### HTTP Endpoints

```
POST /api/build
Body: { 
  "platform": "android", 
  "buildType": "release",
  "version": "1.2.3" 
}
Response: { "buildPath": "string", "success": true }

POST /api/sign
Body: { 
  "apkPath": "string",
  "keystorePath": "string" 
}
Response: { "signedPath": "string", "verified": true }

POST /api/release
Body: { 
  "version": "1.2.3",
  "changelog": "string",
  "artifacts": [...] 
}
Response: { "releaseUrl": "string", "published": true }

POST /api/version/bump
Body: { "type": "minor" }
Response: { "oldVersion": "1.2.3", "newVersion": "1.3.0" }

GET /api/versions
Response: { "versions": [...], "latest": "1.2.3" }

GET /api/health
Response: { "status": "ok", "version": "1.0.0" }
```

## Configuración

```bash
# .env
DEPLOYMENT_COORDINATOR_PORT=3002

# Build
GRADLE_PATH=/usr/bin/gradle
ANDROID_SDK_ROOT=/path/to/android-sdk

# Signing
ANDROID_KEYSTORE_PATH=/path/to/keystore.jks
ANDROID_KEYSTORE_PASSWORD=your_password
ANDROID_KEY_ALIAS=your_alias
ANDROID_KEY_PASSWORD=your_key_password

# Store Publishing
GOOGLE_PLAY_SERVICE_ACCOUNT=/path/to/play-service-account.json
APP_STORE_CONNECT_KEY=/path/to/appstore-key.json

# Repository
GITHUB_TOKEN=ghp_...
GIT_REPO_PATH=/path/to/repo
```

## Ejemplo de Uso

```javascript
import axios from 'axios';

async function deployApp() {
    // 1. Bump version
    const versionResult = await axios.post(
        'http://localhost:3002/api/version/bump',
        { type: 'minor' }
    );
    
    const newVersion = versionResult.data.newVersion;
    console.log('Nueva versión:', newVersion);
    
    // 2. Build
    const buildResult = await axios.post(
        'http://localhost:3002/api/build',
        {
            platform: 'android',
            buildType: 'release',
            version: newVersion
        }
    );
    
    console.log('Build completado:', buildResult.data.buildPath);
    
    // 3. Sign
    const signResult = await axios.post(
        'http://localhost:3002/api/sign',
        {
            apkPath: buildResult.data.buildPath,
            keystorePath: process.env.ANDROID_KEYSTORE_PATH
        }
    );
    
    console.log('APK firmado:', signResult.data.signedPath);
    
    // 4. Release
    const releaseResult = await axios.post(
        'http://localhost:3002/api/release',
        {
            version: newVersion,
            changelog: 'Bug fixes and improvements',
            artifacts: [signResult.data.signedPath]
        }
    );
    
    console.log('Release publicado:', releaseResult.data.releaseUrl);
}
```

## Testing

```bash
npm test
npm test -- deployment_coordinator
npm run test:integration
```

## Build Pipeline

### Android Build
```javascript
// 1. Clean
await gradle.clean();

// 2. Build
await gradle.assembleRelease();

// 3. Sign
await apksigner.sign(apkPath, keystorePath);

// 4. Align
await zipalign.align(signedApk);

// 5. Verify
await apksigner.verify(finalApk);
```

### iOS Build (Fastlane)
```javascript
// 1. Install dependencies
await exec('pod install');

// 2. Build
await fastlane.build({
    scheme: 'Release',
    exportMethod: 'app-store'
});

// 3. Sign
// Automático con match de Fastlane

// 4. Upload
await fastlane.upload({
    ipa: ipaPath,
    skipMetadata: false
});
```

## Logs

Todos los logs se registran en:
- Console: Winston pretty format
- File: `/logs/deployment_coordinator.log`
- Firestore: Colección `bot_logs` + `deployment_history`
- GitHub: Actions logs

## Comunicación

### Recibe mensajes de:
- GitHub webhooks (push, PR merge)
- Manual triggers (API calls)
- Otros coordinadores (para builds especiales)

### Envía mensajes a:
- GitHub (status updates)
- Slack/Discord (notificaciones)
- Todos los coordinadores (nueva versión disponible)

## Métricas

- Builds por día
- Tiempo promedio de build
- Tasa de éxito/error
- Tamaño de APKs/IPAs
- Tiempo de deploy a stores

## Versionado Semántico

Seguimos [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): Nuevas features (backward compatible)
- **PATCH** (1.0.0 → 1.0.1): Bug fixes

## Changelog Automático

El coordinador genera changelogs basados en:
- Commits convencionales (conventional commits)
- PRs mergeados
- Issues cerrados

Formato:
```markdown
# Changelog

## [1.2.0] - 2025-12-14

### Added
- Nueva feature X
- Nueva feature Y

### Fixed
- Bug Z

### Changed
- Mejora en performance
```

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Trigger deployment
        run: |
          curl -X POST http://deployment-coordinator:3002/api/build \
            -H "Content-Type: application/json" \
            -d '{"platform": "android", "buildType": "release"}'
```

## Seguridad

### Keystores
- **NUNCA** commitear keystores al repo
- Usar GitHub Secrets para CI/CD
- Rotar contraseñas regularmente

### Service Accounts
- Permisos mínimos necesarios
- Rotar keys cada 90 días
- Auditar accesos

## Build Variants

### Android
- `debug` - Debug build con logging
- `release` - Release optimizado
- `beta` - Beta testing con crashlytics

### iOS
- `Debug` - Debug build
- `Release` - Release optimizado
- `TestFlight` - Beta distribution

## Troubleshooting

### Error: Gradle build failed
```bash
# Limpiar cache
./gradlew clean
rm -rf ~/.gradle/caches

# Verificar JDK
java -version  # Debe ser JDK 11 o superior
```

### Error: Signing failed
```bash
# Verificar keystore
keytool -list -v -keystore keystore.jks

# Verificar contraseñas
# Asegurar que ANDROID_KEYSTORE_PASSWORD y ANDROID_KEY_PASSWORD son correctas
```

### Error: Play Store upload failed
```bash
# Verificar service account
# Debe tener permisos de "Release Manager"

# Verificar versionCode
# Debe ser mayor que el último publicado
```

## Automatizaciones

### Deploy automático en merge a main
```javascript
// webhook handler
app.post('/webhook/github', async (req, res) => {
    const { ref, commits } = req.body;
    
    if (ref === 'refs/heads/main') {
        // Trigger build and deploy
        await buildAndDeploy({
            version: 'auto',
            changelog: commits.map(c => c.message).join('\n')
        });
    }
});
```

### Rollback automático
```javascript
async function rollback(version) {
    // 1. Revert to previous version
    await git.checkout(`v${version}`);
    
    // 2. Build
    await build({ version });
    
    // 3. Deploy
    await deploy({ version, isRollback: true });
}
```

## Mantenimiento

- Limpiar builds antiguos: `npm run clean:builds`
- Archivar releases: `npm run archive:releases`
- Actualizar dependencias: `npm run update:deps`
- Verificar keystores: `npm run verify:keystores`

## Soporte

Para problemas con este coordinador, abrir issue con etiqueta `deployment-coordinator`.
