# GitHub Secrets Setup Guide

Esta guía documenta todos los secrets necesarios para los diferentes workflows de Tokyo IA.

## 🔐 Resumen de Secrets

Tokyo IA requiere configurar los siguientes GitHub Secrets para funcionalidad completa:

| Secret | Propósito | Requerido Para | Prioridad |
|--------|-----------|----------------|-----------|
| `KEYSTORE_FILE` | Firma de release Android | Play Store | 🔴 Alta |
| `KEYSTORE_PASSWORD` | Password del keystore | Play Store | 🔴 Alta |
| `KEY_ALIAS` | Alias de la key | Play Store | 🔴 Alta |
| `KEY_PASSWORD` | Password de la key | Play Store | 🔴 Alta |
| `VERCEL_TOKEN` | Despliegue web | Vercel Deploy | 🔴 Alta |
| `VERCEL_ORG_ID` | ID de organización Vercel | Vercel Deploy | 🔴 Alta |
| `VERCEL_PROJECT_ID` | ID del proyecto Vercel | Vercel Deploy | 🔴 Alta |
| `GOOGLE_PLAY_JSON` | API de Play Console | Auto-deploy Android | 🟡 Media |

## 🎯 Configuración por Componente

### 1️⃣ Android Release Signing

#### ¿Por qué se necesitan?
Para firmar builds de release de la app Android y poder publicarla en Google Play Store.

#### Secrets Requeridos

##### KEYSTORE_FILE
- **Descripción**: Path al archivo del keystore de release
- **Cómo obtener**:
  ```bash
  # Generar keystore (ejecutar localmente)
  keytool -genkey -v -keystore release.keystore \
    -alias key0 \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000
  
  # Subir a GitHub Secrets (método seguro)
  # 1. Codificar en base64
  base64 release.keystore > release.keystore.b64
  
  # 2. Copiar contenido de release.keystore.b64
  # 3. En GitHub Secrets, guardar como KEYSTORE_BASE64
  
  # 4. O especificar path si el keystore está en runner
  # Value: /path/to/release.keystore
  ```
- **Formato**: Path absoluto o contenido base64
- **Ejemplo**: `/home/runner/work/keys/release.keystore`

##### KEYSTORE_PASSWORD
- **Descripción**: Password del keystore
- **Cómo obtener**: El password que especificaste al crear el keystore
- **Formato**: String
- **Ejemplo**: `MySecureKeystorePassword123!`

##### KEY_ALIAS
- **Descripción**: Alias de la key dentro del keystore
- **Cómo obtener**: El alias que especificaste al crear el keystore
- **Formato**: String
- **Ejemplo**: `key0`

##### KEY_PASSWORD
- **Descripción**: Password de la key específica
- **Cómo obtener**: El password que especificaste para la key (puede ser igual al keystore password)
- **Formato**: String
- **Ejemplo**: `MySecureKeyPassword123!`

#### ⚠️ Seguridad Crítica

**NUNCA:**
- ❌ Commitees el keystore al repositorio
- ❌ Compartas los passwords públicamente
- ❌ Uses el mismo password para múltiples proyectos

**SIEMPRE:**
- ✅ Guarda el keystore en múltiples ubicaciones seguras
- ✅ Usa un gestor de contraseñas (1Password, LastPass, Bitwarden)
- ✅ Haz backups encriptados del keystore
- ✅ Documenta dónde están los backups

**Si pierdes el keystore:**
- 💥 NUNCA podrás actualizar la app en Play Store
- 💥 Tendrás que publicar una nueva app con nuevo package name
- 💥 Perderás todos los usuarios e instalaciones

#### Cómo Configurar

```bash
# 1. Generar keystore localmente
cd /secure/location/
keytool -genkey -v -keystore tokyo-ia-release.keystore \
  -alias key0 \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000

# Responder preguntas:
# - Enter keystore password: [CREAR PASSWORD SEGURO]
# - Re-enter password: [REPETIR]
# - First and last name: [Tu nombre o nombre de la app]
# - Organizational unit: [Tu organización]
# - Organization: [Nombre de la compañía]
# - City: [Tu ciudad]
# - State: [Tu estado/provincia]
# - Country code: [XX] (2 letras)
# - Is CN=... correct? yes
# - Enter key password: [PUEDE SER EL MISMO O DIFERENTE]

# 2. Hacer backup del keystore
cp tokyo-ia-release.keystore ~/Dropbox/keys/
cp tokyo-ia-release.keystore /external/drive/

# 3. Configurar en GitHub
# Ve a: https://github.com/Melampe001/Tokyo-IA/settings/secrets/actions
# Add secret → KEYSTORE_FILE → [path o base64]
# Add secret → KEYSTORE_PASSWORD → [password]
# Add secret → KEY_ALIAS → key0
# Add secret → KEY_PASSWORD → [key password]
```

---

### 2️⃣ Vercel Deployment

#### ¿Por qué se necesitan?
Para desplegar automáticamente la interfaz web a Vercel cuando se hace push a main.

#### Secrets Requeridos

##### VERCEL_TOKEN
- **Descripción**: Token de autenticación de Vercel
- **Cómo obtener**:
  1. Ve a [vercel.com/account/tokens](https://vercel.com/account/tokens)
  2. Click "Create Token"
  3. Name: `Tokyo-IA GitHub Actions`
  4. Scope: `Full Account` o scope mínimo necesario
  5. Expiration: Según política de seguridad
  6. Click "Create" y **copia el token inmediatamente**
- **Formato**: String (empieza con `vercel_token_...`)
- **Ejemplo**: `vercel_token_abc123xyz789...`

##### VERCEL_ORG_ID
- **Descripción**: ID de tu organización/cuenta de Vercel
- **Cómo obtener**:
  
  **Opción 1: Desde Dashboard**
  1. Ve a [vercel.com/dashboard](https://vercel.com/dashboard)
  2. Settings (engranaje) → General
  3. Copia "Team ID" o "User ID"
  
  **Opción 2: Desde CLI**
  ```bash
  vercel teams ls
  # Aparece en la lista con formato team_xxx o user_xxx
  ```
  
  **Opción 3: Desde .vercel/project.json**
  ```bash
  # Después del primer deploy
  cat .vercel/project.json | grep orgId
  ```
- **Formato**: String (team_xxx o user_xxx)
- **Ejemplo**: `team_abc123xyz` o `user_abc123xyz`

##### VERCEL_PROJECT_ID
- **Descripción**: ID del proyecto específico en Vercel
- **Cómo obtener**:
  
  **Opción 1: Desde Dashboard**
  1. Ve a tu proyecto en Vercel
  2. Settings → General
  3. Copia "Project ID"
  
  **Opción 2: Desde .vercel/project.json**
  ```bash
  # Después del primer deploy
  cat .vercel/project.json | grep projectId
  ```
  
  **Opción 3: Desde URL**
  - URL del proyecto: `vercel.com/melampe001/tokyo-ia-web`
  - Project slug: `tokyo-ia-web`
- **Formato**: String alfanumérico
- **Ejemplo**: `prj_abc123xyz789`

#### Cómo Configurar

```bash
# 1. Crear cuenta en Vercel (si no existe)
# Ve a: https://vercel.com/signup

# 2. Conectar proyecto
# Ve a: https://vercel.com/new
# Importa: Melampe001/Tokyo-IA
# Root Directory: web/
# Framework: Vite

# 3. Obtener tokens/IDs (ver instrucciones arriba)

# 4. Configurar en GitHub
# Ve a: https://github.com/Melampe001/Tokyo-IA/settings/secrets/actions
# Add secret → VERCEL_TOKEN → [tu token]
# Add secret → VERCEL_ORG_ID → [tu org ID]
# Add secret → VERCEL_PROJECT_ID → [tu project ID]
```

Ver guía completa: [docs/VERCEL_SETUP.md](./VERCEL_SETUP.md)

---

### 3️⃣ Google Play Auto-Deploy (Futuro)

#### ¿Por qué se necesita?
Para publicar automáticamente nuevas versiones de la app Android a Play Store mediante GitHub Actions.

#### Secret Requerido

##### GOOGLE_PLAY_JSON
- **Descripción**: Credenciales JSON de la API de Google Play Developer
- **Cómo obtener**:
  1. Ve a [Google Play Console](https://play.google.com/console)
  2. Settings → API access
  3. Crea una cuenta de servicio:
     - Click "Create service account"
     - Sigue el link a Google Cloud Console
     - Create service account
     - Grant permissions: "Service Account User"
     - Create key → JSON
     - Download JSON file
  4. En Play Console, otorga permisos a la cuenta:
     - "Release to production, exclude devices, and use Play App Signing"
- **Formato**: Contenido completo del archivo JSON
- **Ejemplo**:
  ```json
  {
    "type": "service_account",
    "project_id": "api-123456789",
    "private_key_id": "abc123...",
    "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
    "client_email": "tokyo-ia@api-123456789.iam.gserviceaccount.com",
    "client_id": "123456789",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    ...
  }
  ```

#### ⚠️ Seguridad
- Este JSON contiene credenciales sensibles
- NUNCA lo commitees al repositorio
- Solo guardarlo en GitHub Secrets
- Rotar periódicamente (cada 6-12 meses)

#### Cómo Configurar

```bash
# 1. Obtener JSON (ver pasos arriba)

# 2. Copiar contenido completo del JSON

# 3. Configurar en GitHub
# Ve a: https://github.com/Melampe001/Tokyo-IA/settings/secrets/actions
# Add secret → GOOGLE_PLAY_JSON → [pegar contenido JSON completo]
```

---

## 🔧 Configurar Todos los Secrets

### Via GitHub Web UI

1. Ve a tu repositorio: `https://github.com/Melampe001/Tokyo-IA`
2. Click en "Settings" (menú del repo)
3. En la barra lateral: "Secrets and variables" → "Actions"
4. Click "New repository secret" para cada secret

### Via GitHub CLI (gh)

```bash
# Instalar gh CLI
brew install gh  # macOS
# o descargar desde: https://cli.github.com/

# Autenticar
gh auth login

# Agregar secrets
gh secret set KEYSTORE_PASSWORD --body "YourPassword"
gh secret set KEY_ALIAS --body "key0"
gh secret set KEY_PASSWORD --body "YourKeyPassword"
gh secret set VERCEL_TOKEN --body "vercel_token_..."
gh secret set VERCEL_ORG_ID --body "team_..."
gh secret set VERCEL_PROJECT_ID --body "prj_..."

# Desde archivo
gh secret set GOOGLE_PLAY_JSON < google-play-credentials.json

# Keystore base64
base64 release.keystore | gh secret set KEYSTORE_BASE64
```

---

## ✅ Verificar Configuración

### Listar Secrets Configurados

```bash
# Via GitHub CLI
gh secret list

# Output esperado:
# KEYSTORE_FILE         Updated 2025-12-23
# KEYSTORE_PASSWORD     Updated 2025-12-23
# KEY_ALIAS            Updated 2025-12-23
# KEY_PASSWORD         Updated 2025-12-23
# VERCEL_TOKEN         Updated 2025-12-23
# VERCEL_ORG_ID        Updated 2025-12-23
# VERCEL_PROJECT_ID    Updated 2025-12-23
```

### Probar Workflows

```bash
# Probar workflow de keystore (solo documentación)
gh workflow run generate-keystore.yml

# Probar pre-release tests
gh workflow run pre-release-tests.yml

# Probar deploy Vercel (haz cambio en web/)
echo "console.log('test');" >> web/src/App.jsx
git add web/
git commit -m "test: Verify secrets"
git push origin main
```

---

## 🔄 Rotar Secrets

### ¿Cuándo rotar?

- ✅ Cada 6-12 meses (buena práctica)
- ✅ Si sospecha de compromiso
- ✅ Cuando un miembro del equipo sale
- ✅ Después de exposición accidental

### Cómo Rotar

#### Vercel Token
```bash
# 1. Crear nuevo token en Vercel
# 2. Actualizar secret
gh secret set VERCEL_TOKEN --body "new_token_..."

# 3. Eliminar token viejo en Vercel dashboard
```

#### Android Keystore
```bash
# ⚠️ NO se puede rotar el keystore de una app publicada
# Si el keystore se compromete:
# - Reportar a Google
# - Considerar nueva app con nuevo package name
# - Migrar usuarios si es posible
```

#### Google Play API
```bash
# 1. En Google Cloud Console, desactivar cuenta de servicio vieja
# 2. Crear nueva cuenta de servicio
# 3. Download nuevo JSON
# 4. Actualizar secret
gh secret set GOOGLE_PLAY_JSON < new-credentials.json

# 5. Eliminar cuenta vieja después de verificar
```

---

## 🚨 Troubleshooting

### Secret No Funciona

**Síntomas**: Workflow falla con error de autenticación

**Soluciones**:
```bash
# 1. Verificar que secret existe
gh secret list

# 2. Verificar formato (sin espacios extra)
# NO: " vercel_token_123 "
# SÍ: "vercel_token_123"

# 3. Recrear secret
gh secret delete SECRET_NAME
gh secret set SECRET_NAME --body "value"

# 4. Verificar scope del token (Vercel/GitHub)
```

### Workflow No Ve Secret

**Causa**: Secret no disponible para workflows de forks (PRs externos)

**Solución**:
- Secrets solo disponibles en repo principal
- Para PRs de forks, usar workflow con `pull_request_target` (cuidado con seguridad)

### Keystore Inválido

**Error**: `Keystore was tampered with, or password was incorrect`

**Soluciones**:
```bash
# Verificar password
keytool -list -v -keystore release.keystore
# Enter keystore password: [debe funcionar]

# Verificar alias
keytool -list -v -keystore release.keystore | grep Alias

# Verificar integridad
keytool -list -v -keystore release.keystore -storepass password
```

---

## 📚 Referencias

- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Vercel CLI Documentation](https://vercel.com/docs/cli)
- [Android App Signing](https://developer.android.com/studio/publish/app-signing)
- [Google Play Publishing API](https://developers.google.com/android-publisher)

---

## 📋 Checklist de Configuración

### Android Release (Alta Prioridad)
- [ ] ✅ Keystore generado y respaldado
- [ ] ✅ KEYSTORE_FILE configurado
- [ ] ✅ KEYSTORE_PASSWORD configurado
- [ ] ✅ KEY_ALIAS configurado
- [ ] ✅ KEY_PASSWORD configurado
- [ ] ✅ Build de release probado localmente

### Vercel Deploy (Alta Prioridad)
- [ ] ✅ Cuenta Vercel creada
- [ ] ✅ Proyecto conectado
- [ ] ✅ VERCEL_TOKEN configurado
- [ ] ✅ VERCEL_ORG_ID configurado
- [ ] ✅ VERCEL_PROJECT_ID configurado
- [ ] ✅ Deploy automático verificado

### Google Play Auto-Deploy (Media Prioridad)
- [ ] 🟡 Cuenta de servicio creada
- [ ] 🟡 JSON credentials descargado
- [ ] 🟡 GOOGLE_PLAY_JSON configurado
- [ ] 🟡 Permisos en Play Console otorgados

---

**Última actualización:** 23 de diciembre de 2025
