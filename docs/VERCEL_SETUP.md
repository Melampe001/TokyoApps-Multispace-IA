# Vercel Setup Guide - Tokyo IA

Esta guía explica cómo configurar el despliegue automático de la interfaz web de Tokyo IA en Vercel.

## 📋 Requisitos Previos

- Cuenta de GitHub (ya la tienes)
- Código fuente en GitHub (repositorio Tokyo-IA)
- Acceso a configurar GitHub Actions secrets

## 🚀 Paso 1: Crear Cuenta en Vercel

1. Ve a [vercel.com](https://vercel.com)
2. Haz clic en "Sign Up"
3. Selecciona "Continue with GitHub"
4. Autoriza a Vercel a acceder a tu cuenta de GitHub
5. Completa el registro

**Costo:** Plan gratuito incluye:
- Despliegues ilimitados
- 100GB de bandwidth/mes
- SSL automático
- Custom domains

## 🔗 Paso 2: Conectar Repositorio

### Opción A: Desde Vercel Dashboard (Recomendado)

1. En el dashboard de Vercel, haz clic en "Add New Project"
2. Selecciona "Import Git Repository"
3. Busca y selecciona `Melampe001/Tokyo-IA`
4. Configura el proyecto:

```
Framework Preset: Vite
Root Directory: web/
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

5. Haz clic en "Deploy"

### Opción B: Usando Vercel CLI

```bash
# Instalar Vercel CLI globalmente
npm install -g vercel

# Navegar al directorio web
cd web/

# Login a Vercel
vercel login

# Iniciar proyecto (seguir prompts)
vercel

# Deploy a producción
vercel --prod
```

## 🔑 Paso 3: Obtener Tokens y IDs

### Obtener Vercel Token

1. Ve a [vercel.com/account/tokens](https://vercel.com/account/tokens)
2. Haz clic en "Create Token"
3. Nombre sugerido: `Tokyo-IA GitHub Actions`
4. Scope: `Full Account`
5. Expiration: `No Expiration` (o según política de seguridad)
6. Haz clic en "Create Token"
7. **COPIA EL TOKEN INMEDIATAMENTE** (solo se muestra una vez)

### Obtener Organization ID

**Método 1: Desde el Dashboard**
1. Ve a tu [Vercel Dashboard](https://vercel.com/dashboard)
2. En la barra lateral, ve a "Settings" (ícono de engranaje)
3. En la sección "General", encontrarás:
   - **Team ID** (si estás en un team) o
   - **User ID** (si es tu cuenta personal)
4. Copia el ID (empieza con `team_` o `user_`)

**Método 2: Usando Vercel CLI**
```bash
# Ver información de la org actual
vercel teams ls

# El ID aparece en la lista
```

### Obtener Project ID

**Método 1: Desde el Proyecto**
1. Ve a tu proyecto en Vercel
2. Haz clic en "Settings"
3. En "General", encontrarás el **Project ID**
4. Copia el ID (cadena alfanumérica)

**Método 2: Desde `.vercel/project.json`**
Después de hacer tu primer deploy con CLI, este archivo contiene el Project ID:
```bash
cat .vercel/project.json
# Busca "projectId"
```

**Método 3: Desde la URL del Proyecto**
URL típica: `https://vercel.com/melampe001/tokyo-ia-web/settings`
- El segmento `tokyo-ia-web` es el project slug
- Puedes usar el slug directamente en algunos casos

## 🔐 Paso 4: Configurar GitHub Secrets

1. Ve a tu repositorio en GitHub: `https://github.com/Melampe001/Tokyo-IA`
2. Haz clic en "Settings" (en el menú del repositorio)
3. En la barra lateral izquierda: "Secrets and variables" → "Actions"
4. Haz clic en "New repository secret"

Agrega los siguientes secrets:

### VERCEL_TOKEN
```
Name: VERCEL_TOKEN
Secret: [el token que copiaste en el Paso 3]
```

### VERCEL_ORG_ID
```
Name: VERCEL_ORG_ID
Secret: [tu Organization/Team/User ID]
```

### VERCEL_PROJECT_ID
```
Name: VERCEL_PROJECT_ID
Secret: [el Project ID de tu proyecto Tokyo-IA]
```

**Verificación:**
Deberías tener 3 secrets configurados. Aparecerán en la lista como:
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

## ⚙️ Paso 5: Variables de Entorno (Opcional)

Si necesitas configurar variables de entorno para la app:

1. En tu proyecto de Vercel, ve a "Settings" → "Environment Variables"
2. Agrega variables según sea necesario:

```
Variable                Value                Environment
NODE_ENV               production           Production
VITE_API_URL           https://api.tokyo... Production, Preview
```

**Nota:** Variables con prefijo `VITE_` son expuestas al frontend.

## 🔧 Paso 6: Configurar Dominio Personalizado (Opcional)

### Dominio Vercel Gratuito
Tu proyecto automáticamente obtiene:
- `tokyo-ia-web.vercel.app` (dominio principal)
- `tokyo-ia-web-git-main-melampe001.vercel.app` (por rama)
- URLs únicas por despliegue

### Dominio Personalizado
1. En tu proyecto, ve a "Settings" → "Domains"
2. Haz clic en "Add Domain"
3. Ingresa tu dominio (ej: `app.tokyoia.com`)
4. Sigue las instrucciones para configurar DNS:

**Opción A: Dominio principal**
```
Type: A
Name: @
Value: 76.76.21.21
```

**Opción B: Subdominio**
```
Type: CNAME
Name: app
Value: cname.vercel-dns.com
```

5. Vercel automáticamente provisiona SSL (Let's Encrypt)

## 🚦 Paso 7: Verificar Despliegue Automático

1. Haz un cambio en el directorio `web/`:
```bash
# Edita cualquier archivo en web/src/
echo "console.log('test');" >> web/src/App.jsx

# Commit y push
git add web/
git commit -m "test: Verify Vercel auto-deploy"
git push origin main
```

2. Ve a la pestaña "Actions" en GitHub
3. Verifica que el workflow "Deploy Web to Vercel" se ejecute
4. Una vez completado, visita tu URL de Vercel para ver los cambios

## 📱 Paso 8: Configurar Webhooks (Opcional)

Para notificaciones de despliegue:

1. En Vercel, ve a "Settings" → "Git"
2. Configura:
   - ✅ Auto-Deploy: `main` branch
   - ✅ Production Branch: `main`
   - ✅ Deploy Previews: Todos los PRs

## 🐛 Troubleshooting

### Build Falla: "Module not found"
```bash
# Asegurar que package-lock.json esté committeado
cd web/
npm install
git add package-lock.json
git commit -m "chore: Add package-lock.json"
git push
```

### Build Falla: "Vercel Token Invalid"
- Regenera el token en Vercel
- Actualiza el secret `VERCEL_TOKEN` en GitHub

### Deploy Exitoso pero Sitio No Carga
- Verifica que `Output Directory` sea `dist` (no `web/dist`)
- Revisa logs en Vercel Dashboard → tu proyecto → Deployments

### Custom Domain No Funciona
```bash
# Verificar configuración DNS
dig app.tokyoia.com

# Debe retornar IPs de Vercel o CNAME correcto
```

## 🔒 Seguridad

### Rotar Vercel Token
```bash
# En Vercel
1. Ve a Account → Tokens
2. Elimina el token viejo
3. Crea uno nuevo
4. Actualiza VERCEL_TOKEN en GitHub Secrets
```

### Limitar Permisos
- Crea un token con scope mínimo necesario
- Usa tokens específicos por proyecto cuando sea posible
- Configura expiration dates

### Proteger Ramas de Despliegue
En Vercel Settings → Git:
- ✅ Enable Deploy Protection: Solo ramas específicas
- ✅ Require Approval: Para production deploys (team plans)

## 📊 Monitoreo

### Analytics (Vercel Analytics)
```bash
# Instalar @vercel/analytics
cd web/
npm install @vercel/analytics

# En web/src/main.jsx
import { inject } from '@vercel/analytics';
inject();
```

### Logs
- Ver logs en tiempo real: Vercel Dashboard → Functions → Logs
- Download logs: Available en plan Pro

### Métricas
Vercel automáticamente rastrea:
- Page load times
- Web Vitals (LCP, FID, CLS)
- Error rates
- Bandwidth usage

## 🚀 Workflow Completo

### Desarrollo Local
```bash
cd web/
npm install
npm run dev
# Servidor en http://localhost:5173
```

### Deploy Preview (PRs)
```bash
git checkout -b feature/new-ui
# Hacer cambios en web/
git add web/
git commit -m "feat: New UI"
git push origin feature/new-ui
# Crear PR → Vercel crea preview deploy automáticamente
```

### Deploy a Producción
```bash
# Merge PR a main
git checkout main
git pull origin main
# Vercel deploya automáticamente a producción
```

## ✅ Checklist de Configuración

- [ ] ✅ Cuenta de Vercel creada
- [ ] ✅ Proyecto conectado a GitHub repo
- [ ] ✅ VERCEL_TOKEN configurado en GitHub Secrets
- [ ] ✅ VERCEL_ORG_ID configurado en GitHub Secrets
- [ ] ✅ VERCEL_PROJECT_ID configurado en GitHub Secrets
- [ ] ✅ Primer deploy exitoso
- [ ] ✅ Dominio personalizado configurado (opcional)
- [ ] ✅ Variables de entorno configuradas (si aplica)
- [ ] ✅ Deploy automático verificado (push a main)
- [ ] ✅ Preview deploys funcionando (PRs)

## 📚 Recursos Adicionales

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel CLI Reference](https://vercel.com/docs/cli)
- [Vercel + GitHub Integration](https://vercel.com/docs/git/vercel-for-github)
- [Custom Domains Guide](https://vercel.com/docs/custom-domains)
- [Environment Variables](https://vercel.com/docs/environment-variables)

## 💬 Soporte

**Problemas con Vercel:**
- [Vercel Support](https://vercel.com/support)
- [Vercel Community](https://github.com/vercel/vercel/discussions)

**Problemas con GitHub Actions:**
- Revisar logs en Actions tab
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Última actualización:** 23 de diciembre de 2025
