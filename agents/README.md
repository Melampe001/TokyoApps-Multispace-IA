# Tokyo-IA Agents Architecture

Este directorio contiene la implementación de todos los agentes y bots del proyecto Tokyo-IA, organizados por tecnología para mantener una clara separación de responsabilidades.

## Estructura de Directorios

```
agents/
├── python_bots/          # Bots coordinadores implementados en Python
│   ├── knowledge_coordinator/
│   └── sentiment_coordinator/
└── node_bots/            # Bots coordinadores implementados en Node.js
    ├── genai_coordinator/
    └── deployment_coordinator/
```

## Arquitectura de Coordinadores

El sistema está diseñado con **4 bots coordinadores principales**, cada uno responsable de un dominio específico:

### Bots Python (2 coordinadores)

1. **KnowledgeCoordinator** - Coordinador de Conocimiento
   - RAG (Retrieval-Augmented Generation) ilimitado
   - Web search en tiempo real
   - Gestión de base de datos vectorial
   - Verificación de fuentes y sinceridad

2. **SentimentCoordinator** - Coordinador de Sentimientos
   - Análisis multimodal de emociones
   - Adaptación de respuestas según mood del usuario
   - Switch de género (hombre/mujer)
   - Personalización de interacciones

### Bots Node.js (2 coordinadores)

3. **GenAICoordinator** - Coordinador de Generación AI
   - Text-to-image (Gemini 2.5 Flash)
   - Text-to-video (Sora 2 / Veo 3)
   - Text-to-music
   - Gestión de contenido multimedia 4K

4. **DeploymentCoordinator** - Coordinador de Despliegue
   - Compilación automática de APK/AAB
   - Firmado de aplicaciones
   - CI/CD automation
   - Gestión de versiones y releases

## Convenciones de Nombres

### Para Bots Coordinadores
- Formato: `[Domain]Coordinator`
- Ejemplos: `KnowledgeCoordinator`, `GenAICoordinator`
- Ubicación: Raíz de cada subcarpeta (`python_bots/`, `node_bots/`)

### Para Agentes Especializados
- Formato: `[Coordinator]_[Function]Agent`
- Ejemplos: `Knowledge_RAGAgent`, `GenAI_ImageAgent`
- Ubicación: Dentro de la carpeta del coordinador correspondiente

### Para Archivos
- Python: `snake_case` (ej: `knowledge_coordinator.py`)
- Node.js: `camelCase` (ej: `genaiCoordinator.js`)
- Configuración: `kebab-case` (ej: `bot-config.json`)

## Comunicación entre Bots

### Protocolo de Comunicación
Los bots se comunican a través de:
1. **Message Queue** (RabbitMQ/Redis) para comandos asíncronos
2. **REST API** para consultas síncronas
3. **WebSockets** para eventos en tiempo real
4. **Shared Database** (Firebase Firestore) para estado compartido

### Ejemplo de Flujo
```
Usuario → App → SentimentCoordinator (detecta mood)
              → KnowledgeCoordinator (busca información)
              → GenAICoordinator (genera imagen/video)
              → Respuesta enriquecida al usuario
```

## Separación de Dependencias

### Python Bots
```bash
# Instalación de dependencias
cd agents/python_bots
pip install -r requirements.txt
```

**Dependencias principales:**
- `transformers` - NLP y sentiment analysis
- `langchain` - RAG framework
- `chromadb` - Vector database
- `requests` - HTTP client

### Node.js Bots
```bash
# Instalación de dependencias
cd agents/node_bots
npm install
```

**Dependencias principales:**
- `@google/generative-ai` - Gemini API
- `openai` - OpenAI/Sora API
- `express` - REST API server
- `socket.io` - WebSocket communication

## Principios de Diseño

1. **Separación Clara**: Nunca mezclar código Python y Node.js en el mismo módulo
2. **Autonomía**: Cada coordinador es autónomo y puede funcionar independientemente
3. **Escalabilidad**: Los agentes se pueden agregar sin afectar coordinadores existentes
4. **Trazabilidad**: Todos los logs se registran en Firestore con marca temporal
5. **Sin Bloqueos**: El modo sin restricciones se activa solo con PIN autorizado

## Agregar Nuevos Agentes

### Python Agent
```python
# En agents/python_bots/[coordinator]/new_agent.py
class NewAgent:
    def __init__(self, coordinator):
        self.coordinator = coordinator
    
    async def execute(self, task):
        # Implementación
        pass
```

### Node.js Agent
```javascript
// En agents/node_bots/[coordinator]/newAgent.js
class NewAgent {
    constructor(coordinator) {
        this.coordinator = coordinator;
    }
    
    async execute(task) {
        // Implementación
    }
}
```

## Seguridad

- **API Keys**: Almacenadas en variables de entorno (`.env`)
- **Autenticación**: Firebase Auth para delegados autorizados
- **Encriptación**: Todos los datos sensibles encriptados en tránsito y reposo
- **PIN Protection**: Modo sin bloqueos requiere PIN y confirmación doble

## Referencias

- Ver `/docs/ARCHITECTURE.md` para detalles técnicos completos
- Ver `/TAREAS.md` para asignación de tareas por bot
- Ver documentación individual en cada carpeta de coordinador
