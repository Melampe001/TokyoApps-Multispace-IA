# 🚀 Despliegue en Vercel - TokyoApps-Multispace-IA

Guía completa para desplegar TokyoApps-Multispace-IA en Vercel con serverless functions, API endpoints y automatización.

## 📋 Requisitos Previos

### 1. Cuenta de Vercel
- Crear cuenta en [vercel.com](https://vercel.com)
- Conectar con tu cuenta de GitHub

### 2. Vercel CLI (Opcional, recomendado)
```bash
npm install -g vercel
```

### 3. Variables de Entorno Requeridas

Configure las siguientes variables en el dashboard de Vercel o localmente:

**API Keys (Opcional, para funcionalidad completa de agentes):**
```bash
ANTHROPIC_API_KEY=sk-ant-...      # Para Akira (Claude)
OPENAI_API_KEY=sk-...              # Para Yuki y Kenji (OpenAI)
GROQ_API_KEY=gsk_...               # Para Hiro (Llama)
GOOGLE_API_KEY=...                 # Para Sakura (Gemini)
```

**Base de datos (Opcional):**
```bash
DATABASE_URL=postgresql://...      # PostgreSQL connection string
```

**Configuración:**
```bash
NODE_ENV=production
PYTHON_VERSION=3.11
```

## 🏗️ Estructura del Proyecto en Vercel

```
TokyoApps-Multispace-IA/
├── api/                          # Serverless Functions (Python)
│   ├── index.py                  # Endpoint principal
│   ├── health.py                 # Health check
│   ├── agents.py                 # AI Agents endpoint
│   └── requirements.txt          # Dependencies
├── web/                          # Frontend estático
│   ├── dist/                     # Build output
│   └── package.json
├── vercel.json                   # Configuración de Vercel
└── .vercelignore                 # Archivos excluidos
```

## 🚀 Opciones de Despliegue

### Opción 1: Despliegue Automático con GitHub (Recomendado)

Esta es la forma más sencilla y mantiene tu sitio actualizado automáticamente.

1. **Conectar repositorio a Vercel:**
   - Ve a [vercel.com/new](https://vercel.com/new)
   - Selecciona "Import Git Repository"
   - Autoriza acceso a GitHub
   - Selecciona el repositorio `TokyoApps-Multispace-IA`

2. **Configurar proyecto:**
   - **Framework Preset:** Other
   - **Root Directory:** `./`
   - **Build Command:** (dejar vacío o `npm run build` si tienes web)
   - **Output Directory:** `web/dist`

3. **Agregar variables de entorno:**
   - En el dashboard, ve a Settings → Environment Variables
   - Agrega las API keys necesarias

4. **Deploy:**
   - Click "Deploy"
   - Vercel automáticamente:
     - Detectará `vercel.json`
     - Construirá el frontend
     - Desplegará las serverless functions

5. **Actualizaciones automáticas:**
   - Cada push a `main` → Deploy automático
   - Cada PR → Preview deployment con URL única

### Opción 2: Despliegue con Vercel CLI

Ideal para desarrollo y testing.

#### 2.1 Despliegue a Preview

```bash
# Primera vez: link project
cd TokyoApps-Multispace-IA
vercel

# Subsecuentes despliegues
vercel
```

Esto crea un deployment de preview con URL única para testing.

#### 2.2 Despliegue a Production

```bash
vercel --prod
```

Esto despliega directamente a producción.

#### 2.3 Con variables de entorno

```bash
# Agregar variables de entorno
vercel env add ANTHROPIC_API_KEY
vercel env add OPENAI_API_KEY
vercel env add GROQ_API_KEY
vercel env add GOOGLE_API_KEY

# O importar desde archivo
vercel env pull .env.local
```

### Opción 3: Despliegue con Script Automatizado

Usamos el script incluido que valida todo antes de desplegar.

#### 3.1 Despliegue a Preview

```bash
./scripts/deploy-vercel.sh preview
# o simplemente
./scripts/deploy-vercel.sh
```

#### 3.2 Despliegue a Production

```bash
./scripts/deploy-vercel.sh production
```

El script automáticamente:
- ✅ Verifica instalación de Vercel CLI
- ✅ Valida archivos del proyecto
- ✅ Limpia builds anteriores
- ✅ Ejecuta el despliegue
- ✅ Reporta el estado

## 🌐 Endpoints Desplegados

Una vez desplegado, tendrás acceso a los siguientes endpoints:

### API Principal
```
GET https://your-project.vercel.app/api/index
```
Retorna información del servicio, agentes disponibles y endpoints.

### Health Check
```
GET https://your-project.vercel.app/api/health
```
Retorna el estado de salud del servicio.

### AI Agents
```
GET https://your-project.vercel.app/api/agents
```
Lista todos los agentes AI disponibles (Akira, Yuki, Hiro, Sakura, Kenji).

```
POST https://your-project.vercel.app/api/agents
Content-Type: application/json

{
  "agent_id": "akira-001",
  "task_type": "code_review",
  "payload": {
    "code": "...",
    "language": "python"
  }
}
```
Inicia una tarea para un agente específico.

### Ejemplo de uso con curl:

```bash
# Health check
curl https://your-project.vercel.app/api/health

# Listar agentes
curl https://your-project.vercel.app/api/agents

# Crear tarea
curl -X POST https://your-project.vercel.app/api/agents \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"akira-001","task_type":"code_review"}'
```

## 🧪 Manual Testing Before Deployment

Before deploying to production, it's recommended to test the configuration locally and in preview environments.

### 1. Local Validation

First, run the validation script to ensure all files are properly configured:

```bash
# Run validation script
./scripts/validate-vercel-config.sh

# Expected output: "✅ All Vercel configuration validations passed!"
```

The validation script checks:
- ✅ `vercel.json` is valid JSON with required sections
- ✅ All API endpoints exist (`index.py`, `health.py`, `agents.py`)
- ✅ Python files have valid syntax
- ✅ Dependencies are properly listed in `requirements.txt`
- ✅ Documentation is complete

### 2. Install Vercel CLI (Optional)

For the most accurate local testing, install the Vercel CLI:

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to your Vercel account
vercel login

# Link to your project (first time only)
vercel link
```

### 3. Test Local Development Environment

Test the serverless functions locally using Vercel Dev:

```bash
# Start local development server
vercel dev

# Server will be available at http://localhost:3000
```

**Test the endpoints:**
- Visit: `http://localhost:3000/` - Main page
- Visit: `http://localhost:3000/api` - Main API endpoint
- Visit: `http://localhost:3000/api/health` - Health check
- Visit: `http://localhost:3000/api/agents` - List agents

**Test with curl:**
```bash
# Health check
curl http://localhost:3000/api/health

# List agents
curl http://localhost:3000/api/agents

# Main endpoint
curl http://localhost:3000/api
```

### 4. Deploy to Preview Environment

Before deploying to production, test with a preview deployment:

```bash
# Deploy to preview (does not affect production)
./scripts/deploy-vercel.sh preview

# Or manually with Vercel CLI:
vercel --prod=false
```

Vercel will provide a unique preview URL (e.g., `https://your-project-abc123.vercel.app`).

### 5. Verify Preview Deployment

After preview deployment, test all endpoints with the preview URL:

```bash
# Set your preview URL
export PREVIEW_URL="https://your-project-abc123.vercel.app"

# Test health endpoint
curl $PREVIEW_URL/api/health

# Test agents endpoint
curl $PREVIEW_URL/api/agents

# Test main endpoint
curl $PREVIEW_URL/api

# Test POST request
curl -X POST $PREVIEW_URL/api/agents \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"akira-001","task_type":"code_review","payload":{"test":"data"}}'
```

**Expected responses:**
- Health endpoint: `{"status":"healthy",...}`
- Agents endpoint: List of 5 agents (Akira, Yuki, Hiro, Sakura, Kenji)
- Main endpoint: Service information and available endpoints
- POST request: Task creation confirmation with task ID

### 6. Verify Logs

Check that functions are executing properly:

```bash
# View real-time logs
vercel logs --follow

# Or view logs for specific deployment
vercel logs [deployment-url]
```

### 7. Production Deployment

Once preview testing is successful, deploy to production:

```bash
# Deploy to production
./scripts/deploy-vercel.sh production

# Or manually:
vercel --prod
```

## ✅ Verificación Post-Despliegue

### 1. Verificar endpoints

```bash
# Reemplaza YOUR_PROJECT con tu dominio
export VERCEL_URL="https://your-project.vercel.app"

# Test health
curl $VERCEL_URL/api/health

# Test agents list
curl $VERCEL_URL/api/agents

# Test main endpoint
curl $VERCEL_URL/api/index
```

### 2. Verificar logs

```bash
vercel logs
```

O en el dashboard: Deployments → Select deployment → View Function Logs

### 3. Verificar métricas

En el dashboard de Vercel:
- **Overview:** Requests, bandwidth, function invocations
- **Analytics:** Performance metrics
- **Logs:** Real-time function logs

## 🔧 Desarrollo Local con Vercel

Prueba tu deployment localmente antes de publicar:

```bash
# Instalar dependencias
cd web && npm install && cd ..

# Iniciar servidor local de Vercel
vercel dev

# El servidor estará disponible en:
# http://localhost:3000
```

Esto simula el entorno de Vercel localmente:
- Serverless functions en `http://localhost:3000/api/*`
- Frontend en `http://localhost:3000/`

## 🐛 Troubleshooting

### Error: "vercel: command not found"

**Solución:**
```bash
npm install -g vercel
```

### Error: "No vercel.json found"

**Solución:**
Asegúrate de estar en el directorio raíz del proyecto:
```bash
cd /path/to/TokyoApps-Multispace-IA
```

### Error: "Function exceeded timeout"

**Causa:** Las funciones serverless tienen un límite de 10 segundos en el plan gratuito.

**Solución:**
- Optimizar código de la función
- Upgrade a plan Pro (60 segundos)
- Usar procesamiento asíncrono

### Error: "Module not found"

**Causa:** Dependencias Python faltantes.

**Solución:**
Verifica que `api/requirements.txt` contenga todas las dependencias necesarias.

### Error: "Build failed"

**Pasos de depuración:**
1. Revisar logs en dashboard de Vercel
2. Verificar `vercel.json` es JSON válido
3. Asegurar que `web/package.json` existe si construyes frontend
4. Verificar que archivos Python no tienen errores de sintaxis

### Las funciones retornan 500

**Pasos:**
1. Revisar logs: `vercel logs`
2. Verificar variables de entorno están configuradas
3. Probar localmente: `vercel dev`

## 📊 Monitoreo y Mantenimiento

### Ver logs en tiempo real

```bash
vercel logs --follow
```

### Ver logs de función específica

```bash
vercel logs --output=raw --since=1h
```

### Ver métricas

En el dashboard:
- **Analytics:** Performance, requests, bandwidth
- **Speed Insights:** Core Web Vitals
- **Logs:** Function execution logs

### Rollback a versión anterior

```bash
# Listar deployments
vercel list

# Promover deployment anterior a producción
vercel promote [deployment-url]
```

O en el dashboard:
1. Ve a Deployments
2. Encuentra el deployment deseado
3. Click "Promote to Production"

## 🔄 CI/CD Automático

### GitHub Actions (Ya incluido)

El repositorio ya incluye workflow `.github/workflows/deploy-vercel.yml` que automáticamente:

1. **En cada push a `main`:**
   - Despliega a preview
   - Corre tests
   - Genera preview URL

2. **En cada tag (ej. `v1.0.0`):**
   - Despliega a production
   - Actualiza release notes
   - Notifica en Slack (si está configurado)

### Configurar Secrets en GitHub

Ve a Settings → Secrets and variables → Actions y agrega:

```
VERCEL_TOKEN=<tu-token>           # Token de Vercel
VERCEL_ORG_ID=<org-id>            # ID de organización
VERCEL_PROJECT_ID=<project-id>    # ID del proyecto
```

**Obtener tokens:**

1. **VERCEL_TOKEN:**
   - Ve a [Vercel Settings → Tokens](https://vercel.com/account/tokens)
   - Create Token
   - Scope: Full Access

2. **VERCEL_ORG_ID y VERCEL_PROJECT_ID:**
   ```bash
   vercel link
   cat .vercel/project.json
   ```

## 🔐 Seguridad

### Variables de Entorno

- ❌ **NUNCA** commitear API keys en el código
- ✅ **SIEMPRE** usar variables de entorno en Vercel
- ✅ Rotar keys periódicamente
- ✅ Usar environment-specific keys (dev, prod)

### CORS

Las funciones ya incluyen headers CORS configurados en `vercel.json`:
```json
{
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {"key": "Access-Control-Allow-Origin", "value": "*"}
      ]
    }
  ]
}
```

Para producción, considera restringir origins:
```json
{"key": "Access-Control-Allow-Origin", "value": "https://yourdomain.com"}
```

## 📚 Recursos Adicionales

- **Vercel Docs:** https://vercel.com/docs
- **Python Serverless:** https://vercel.com/docs/functions/serverless-functions/runtimes/python
- **Vercel CLI:** https://vercel.com/docs/cli
- **Environment Variables:** https://vercel.com/docs/concepts/projects/environment-variables
- **Deployment Hooks:** https://vercel.com/docs/concepts/git/deploy-hooks

## 🆘 Soporte

Si tienes problemas:

1. 📖 Revisa esta documentación
2. 🔍 Busca en [Vercel Docs](https://vercel.com/docs)
3. 💬 Abre un issue en el repositorio
4. 🐛 Revisa logs: `vercel logs`

---

**¡Feliz despliegue! 🚀**
