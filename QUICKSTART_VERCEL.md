# 🚀 Quick Start - Vercel Deploy

## Deploy en 3 pasos

### 1️⃣ Conecta tu repositorio
- Ve a [vercel.com/new](https://vercel.com/new)
- Importa `Melampe001/TokyoApps-Multispace-IA`
- Click "Deploy"

### 2️⃣ Configura variables (Opcional)
En Vercel Dashboard → Settings → Environment Variables:
```bash
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
GOOGLE_API_KEY=...
```

### 3️⃣ ¡Listo! 🎉
Tus endpoints están disponibles en:
- `https://tu-proyecto.vercel.app/api/health`
- `https://tu-proyecto.vercel.app/api/agents`
- `https://tu-proyecto.vercel.app/`

## Verificación

```bash
curl https://tu-proyecto.vercel.app/api/health
```

Para más detalles, consulta [DEPLOY_VERCEL.md](./DEPLOY_VERCEL.md)
