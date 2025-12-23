# 🤖 Sistema de Automatización Inteligente

Sistema completo que utiliza los 5 agentes especializados de Tokyo-IA para automatizar tareas de desarrollo.

## 🎯 Agentes Disponibles

- **侍 Akira** - Code Review Master (Claude Opus 4.1)
- **❄️ Yuki** - Test Engineering Specialist (OpenAI o3)
- **🛡️ Hiro** - SRE & DevOps Guardian (Llama 3.1 70B)
- **🌸 Sakura** - Documentation Artist (Gemini Pro)
- **🏗️ Kenji** - Architecture Visionary (OpenAI o3)

## 📦 Workflows Disponibles

### 1. Auto Review & Improve Code
**Workflow:** Akira (Security) → Akira (Review) → Yuki (Tests) → Hiro (CI/CD) → Sakura (Docs)

```bash
# CLI
python scripts/tokyo-cli.py review my_code.py --language python

# Python
from scripts.intelligent_automation import IntelligentAutomation
automation = IntelligentAutomation()
result = automation.auto_review_and_improve_code(code, "python")
```

### 2. Design & Document Feature
**Workflow:** Kenji (Architecture) → Yuki (Test Strategy) → Sakura (Specification)

```bash
# CLI
python scripts/tokyo-cli.py design \
  --name "User Authentication" \
  --description "OAuth2 + JWT system"

# Python
result = automation.design_and_document_feature({
    "name": "Auth System",
    "description": "OAuth2 implementation",
    "language": "python"
})
```

### 3. Prepare Production Deployment
**Workflow:** Hiro (Kubernetes) → Hiro (Monitoring) → Sakura (Docs)

```bash
# CLI
python scripts/tokyo-cli.py deploy \
  --name myapp \
  --image myapp:latest \
  --port 8080

# Python
result = automation.prepare_production_deployment({
    "name": "myapp",
    "image": "myapp:latest",
    "port": 8080
})
```

## 🚀 Uso con GitHub Actions

El sistema se integra automáticamente con GitHub Actions:

### Ejecución Automática
- **Pull Requests**: Ejecuta review automático de código
- **Push a Main/develop**: Ejecuta validaciones

### Ejecución Manual
1. Ve a la pestaña "Actions"
2. Selecciona "🤖 Agent Automation System"
3. Click en "Run workflow"
4. Elige el tipo de automatización
5. Especifica la ruta objetivo (opcional)

## 🔑 Configuración de API Keys

El sistema requiere las siguientes API keys configuradas como secrets en GitHub:

```
ANTHROPIC_API_KEY  # Para Akira (Claude)
OPENAI_API_KEY     # Para Yuki y Kenji (GPT/o3)
GROQ_API_KEY       # Para Hiro (Llama)
GOOGLE_API_KEY     # Para Sakura (Gemini)
```

Para uso local, exporta las variables de entorno:

```bash
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
export GROQ_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"
```

## 📊 Reportes

Los resultados se generan en dos formatos:

1. **JSON** (`agent_results.json`): Datos estructurados
2. **Markdown** (`AGENT_REPORT.md`): Reporte legible

En PRs, el reporte se publica automáticamente como comentario.

## 🛠️ Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Hacer ejecutable el CLI
chmod +x scripts/tokyo-cli.py

# Probar instalación
python scripts/tokyo-cli.py agents
```

## 📝 Ejemplos

### Ejemplo 1: Review de código Python

```bash
python scripts/tokyo-cli.py review app/main.py \
  --language python \
  --output results.json
```

### Ejemplo 2: Diseñar nueva feature

```bash
python scripts/tokyo-cli.py design \
  --name "Real-time Chat" \
  --description "WebSocket-based chat with message persistence" \
  --language "python" \
  --output design.json
```

### Ejemplo 3: Preparar deployment

```bash
python scripts/tokyo-cli.py deploy \
  --name tokyo-api \
  --image ghcr.io/melampe001/tokyo-api:v1.0.0 \
  --port 8080 \
  --output deployment.json
```

## 🔍 Debugging

Para ver logs detallados:

```bash
# Ejecutar con modo verbose
python scripts/intelligent_automation.py --verbose

# Ver logs de agentes individuales
export CREWAI_VERBOSE=true
python scripts/tokyo-cli.py review code.py
```

## 🤝 Contribuir

Para agregar nuevos workflows:

1. Edita `scripts/intelligent_automation.py`
2. Agrega método a la clase `IntelligentAutomation`
3. Actualiza el CLI en `scripts/tokyo-cli.py`
4. Documenta en este archivo

## 📚 Referencias

- [Agent Orchestration Documentation](./agents/ORCHESTRATION.md)
- [Workflow Examples](../lib/orchestrator/workflows.py)
- [Agent Implementations](../lib/agents/specialized/)
