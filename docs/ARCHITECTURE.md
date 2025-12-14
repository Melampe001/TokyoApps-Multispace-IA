# Tokyo-IA Architecture - Bot Separation

## Overview

Tokyo-IA implementa una arquitectura de microservicios basada en bots coordinadores especializados. La arquitectura está diseñada para mantener una **separación clara entre implementaciones Python y Node.js**, evitando cruces de dependencias y facilitando el mantenimiento.

## Principios Arquitectónicos

### 1. Separación por Tecnología
- **Python**: Procesamiento de datos, ML/AI, análisis
- **Node.js**: Servicios web, generación multimedia, automatización

### 2. Autonomía
- Cada coordinador es autónomo y puede funcionar independientemente
- Fallo de un coordinador no afecta a otros

### 3. Comunicación Desacoplada
- Message queues para comunicación asíncrona
- REST APIs para consultas síncronas
- WebSockets para eventos en tiempo real

### 4. Escalabilidad Horizontal
- Cada coordinador puede escalarse independientemente
- Load balancing por coordinador

## Coordinadores Principales

### Coordinadores Python (2)

#### 1. KnowledgeCoordinator
**Puerto**: 5001  
**Responsabilidad**: Gestión de conocimiento y búsqueda

**Stack Tecnológico**:
- LangChain (RAG)
- ChromaDB (Vector DB)
- Transformers (Embeddings)
- aiohttp (Async HTTP)

**Interfaces**:
```python
# REST API
POST /api/search
POST /api/embed
GET  /api/health

# Message Queue
Subscribe: ["knowledge_requests"]
Publish: ["knowledge_responses"]
```

#### 2. SentimentCoordinator
**Puerto**: 5002  
**Responsabilidad**: Análisis emocional y adaptación

**Stack Tecnológico**:
- Transformers (Sentiment Analysis)
- Redis (State caching)
- Firebase (User profiles)

**Interfaces**:
```python
# REST API
POST /api/analyze
POST /api/adapt
POST /api/personality/switch
GET  /api/health

# Message Queue
Subscribe: ["sentiment_requests"]
Publish: ["sentiment_responses", "mood_updates"]
```

### Coordinadores Node.js (2)

#### 3. GenAICoordinator
**Puerto**: 3001  
**Responsabilidad**: Generación de contenido multimedia

**Stack Tecnológico**:
- Google Gemini API
- OpenAI API
- FFmpeg (Processing)
- AWS S3 / Firebase Storage

**Interfaces**:
```javascript
// REST API
POST /api/generate/image
POST /api/generate/video
POST /api/generate/music
GET  /api/status
GET  /api/health

// Message Queue
Subscribe: ["genai_requests"]
Publish: ["genai_responses", "generation_complete"]
```

#### 4. DeploymentCoordinator
**Puerto**: 3002  
**Responsabilidad**: Build, release y deployment

**Stack Tecnológico**:
- Gradle (Android builds)
- Fastlane (iOS automation)
- GitHub API
- Google Play Publishing API

**Interfaces**:
```javascript
// REST API
POST /api/build
POST /api/sign
POST /api/release
POST /api/version/bump
GET  /api/versions
GET  /api/health

// Message Queue
Subscribe: ["deployment_requests"]
Publish: ["deployment_complete", "build_status"]
```

## Flujos de Comunicación

### Ejemplo 1: Usuario hace una pregunta
```
1. Usuario → App → SentimentCoordinator
   └─> Detecta mood: "curioso"

2. App → KnowledgeCoordinator
   └─> Busca información + verifica fuentes

3. KnowledgeCoordinator → GenAICoordinator
   └─> "Genera imagen ilustrativa"

4. SentimentCoordinator → Response Adaptation
   └─> Adapta tono según mood "curioso"

5. App ← Respuesta enriquecida
   └─> Texto + imagen + fuentes + tono adaptado
```

### Ejemplo 2: Deploy automático
```
1. GitHub webhook → DeploymentCoordinator
   └─> "Push to main branch"

2. DeploymentCoordinator → Version bump
   └─> 1.2.3 → 1.3.0

3. DeploymentCoordinator → Build
   └─> Compile APK/AAB

4. DeploymentCoordinator → Sign
   └─> Firma con keystore

5. DeploymentCoordinator → Release
   └─> Publica a Play Store

6. DeploymentCoordinator → Notifica
   └─> Todos los coordinadores + usuarios
```

## Estructura de Directorios

```
agents/
├── README.md                          # Documentación general
├── python_bots/                       # Todos los bots Python
│   ├── README.md
│   ├── requirements.txt               # Dependencias Python compartidas
│   ├── shared/                        # Código compartido
│   │   ├── base_coordinator.py
│   │   ├── message_queue.py
│   │   └── utils.py
│   ├── knowledge_coordinator/
│   │   ├── README.md
│   │   ├── coordinator.py
│   │   ├── config.py
│   │   ├── agents/
│   │   │   ├── rag_agent.py
│   │   │   ├── web_search_agent.py
│   │   │   ├── vector_db_agent.py
│   │   │   └── verification_agent.py
│   │   └── tests/
│   └── sentiment_coordinator/
│       ├── README.md
│       ├── coordinator.py
│       ├── config.py
│       ├── agents/
│       │   ├── analysis_agent.py
│       │   ├── adaptation_agent.py
│       │   ├── personality_agent.py
│       │   └── context_agent.py
│       └── tests/
└── node_bots/                         # Todos los bots Node.js
    ├── README.md
    ├── package.json                   # Dependencias Node compartidas
    ├── shared/                        # Código compartido
    │   ├── baseCoordinator.js
    │   ├── messageQueue.js
    │   ├── logger.js
    │   └── utils.js
    ├── genai_coordinator/
    │   ├── README.md
    │   ├── index.js
    │   ├── coordinator.js
    │   ├── config.js
    │   ├── routes/
    │   ├── agents/
    │   │   ├── imageAgent.js
    │   │   ├── videoAgent.js
    │   │   ├── musicAgent.js
    │   │   └── storageAgent.js
    │   └── __tests__/
    └── deployment_coordinator/
        ├── README.md
        ├── index.js
        ├── coordinator.js
        ├── config.js
        ├── routes/
        ├── agents/
        │   ├── buildAgent.js
        │   ├── signAgent.js
        │   ├── releaseAgent.js
        │   └── versionAgent.js
        └── __tests__/
```

## Convenciones de Nombres

### Coordinadores
- Formato: `[Domain]Coordinator`
- Python: `knowledge_coordinator/coordinator.py` (snake_case)
- Node.js: `genai_coordinator/coordinator.js` (camelCase)

### Agentes
- Formato: `[Coordinator]_[Function]Agent`
- Python: `Knowledge_RAGAgent` (PascalCase en clase, snake_case en archivo)
- Node.js: `GenAI_ImageAgent` (PascalCase)

### APIs
- REST: `/api/[resource]/[action]`
- Message Queue Channels: `[coordinator]_[type]` (ej: `genai_requests`)

## Infraestructura de Comunicación

### Message Queue (RabbitMQ)

**Ventajas**:
- Comunicación asíncrona
- Buffering de mensajes
- Retry automático
- Escalabilidad

**Canales**:
```
knowledge_requests    → KnowledgeCoordinator
knowledge_responses   ← KnowledgeCoordinator
sentiment_requests    → SentimentCoordinator
sentiment_responses   ← SentimentCoordinator
genai_requests        → GenAICoordinator
genai_responses       ← GenAICoordinator
deployment_requests   → DeploymentCoordinator
deployment_complete   ← DeploymentCoordinator
```

### REST APIs

**Ventajas**:
- Comunicación síncrona
- Estándar HTTP
- Fácil debugging
- Compatible con cualquier cliente

**Uso**:
- Consultas que requieren respuesta inmediata
- Health checks
- Status queries

### WebSockets

**Ventajas**:
- Comunicación bidireccional
- Eventos en tiempo real
- Conexión persistente

**Uso**:
- Updates de estado en tiempo real
- Notificaciones push
- Streaming de resultados

### Shared Database (Firebase Firestore)

**Ventajas**:
- Estado compartido
- Persistencia
- Real-time sync
- Escalable

**Colecciones**:
```
users/               → Datos de usuarios
conversations/       → Historial de chats
generations/         → Contenido generado
bot_logs/           → Logs de todos los bots
bot_metrics/        → Métricas y analytics
sentiment_history/  → Evolución emocional
deployment_history/ → Historial de deploys
```

## Dependencias Separadas

### Python (requirements.txt)
```txt
# Core
python>=3.10

# ML/AI
transformers>=4.35.0
torch>=2.1.0
langchain>=0.1.0
chromadb>=0.4.18

# Web
aiohttp>=3.9.0
fastapi>=0.104.0
uvicorn>=0.24.0

# Database
firebase-admin>=6.2.0
redis>=5.0.0

# Message Queue
pika>=1.3.0  # RabbitMQ

# Utilities
python-dotenv>=1.0.0
loguru>=0.7.0
```

### Node.js (package.json)
```json
{
  "dependencies": {
    "@google/generative-ai": "^0.2.0",
    "openai": "^4.20.0",
    "express": "^4.18.0",
    "socket.io": "^4.6.0",
    "firebase-admin": "^12.0.0",
    "redis": "^4.6.0",
    "amqplib": "^0.10.0",
    "axios": "^1.6.0",
    "winston": "^3.11.0",
    "dotenv": "^16.3.0"
  }
}
```

## Deployment

### Desarrollo Local
```bash
# Terminal 1: Python coordinators
cd agents/python_bots
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd knowledge_coordinator && python coordinator.py &
cd ../sentiment_coordinator && python coordinator.py &

# Terminal 2: Node coordinators
cd agents/node_bots
npm install
npm run start:genai &
npm run start:deployment &

# Terminal 3: Infrastructure
docker-compose up -d  # RabbitMQ, Redis, etc.
```

### Producción (Docker)
```yaml
# docker-compose.yml
version: '3.8'

services:
  knowledge-coordinator:
    build: ./agents/python_bots/knowledge_coordinator
    ports:
      - "5001:5001"
    environment:
      - PORT=5001
    depends_on:
      - rabbitmq
      - redis

  sentiment-coordinator:
    build: ./agents/python_bots/sentiment_coordinator
    ports:
      - "5002:5002"
    depends_on:
      - rabbitmq
      - redis

  genai-coordinator:
    build: ./agents/node_bots/genai_coordinator
    ports:
      - "3001:3001"
    depends_on:
      - rabbitmq

  deployment-coordinator:
    build: ./agents/node_bots/deployment_coordinator
    ports:
      - "3002:3002"
    depends_on:
      - rabbitmq

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

## Monitoreo y Observabilidad

### Logs Centralizados
- Formato estructurado (JSON)
- Timestamp + nivel + coordinador + mensaje
- Almacenamiento en Firestore
- Dashboard en tiempo real

### Métricas
- Prometheus para recolección
- Grafana para visualización
- Alertas automáticas

### Health Checks
```bash
# Verificar todos los coordinadores
curl http://knowledge-coordinator:5001/api/health
curl http://sentiment-coordinator:5002/api/health
curl http://genai-coordinator:3001/api/health
curl http://deployment-coordinator:3002/api/health
```

## Seguridad

### Autenticación
- Firebase Auth para usuarios
- API Keys para coordinadores
- JWT tokens para comunicación inter-bot

### Autorización
- Role-based access control (RBAC)
- Permisos por coordinador
- PIN para modo sin restricciones

### Encriptación
- TLS para comunicación HTTP
- Encriptación at-rest para datos sensibles
- Keystores para signing

## Escalabilidad

### Horizontal Scaling
```
Load Balancer
     ├─> KnowledgeCoordinator Instance 1
     ├─> KnowledgeCoordinator Instance 2
     └─> KnowledgeCoordinator Instance 3
```

### Caching Strategy
- Redis para cache de resultados frecuentes
- TTL apropiado por tipo de dato
- Cache invalidation en updates

### Rate Limiting
- Por usuario
- Por coordinador
- Por endpoint

## Testing

### Unit Tests
```bash
# Python
pytest agents/python_bots/*/tests/

# Node.js
npm test --prefix agents/node_bots
```

### Integration Tests
```bash
# Prueba flujo completo
npm run test:integration
```

### Load Tests
```bash
# Artillery para load testing
artillery run load-tests/bot-communication.yml
```

## Troubleshooting

### Coordinador no responde
1. Check health endpoint
2. Verificar logs
3. Verificar dependencias (DB, queue)
4. Restart coordinador

### Message queue atascada
1. Verificar RabbitMQ management
2. Purgar queue si necesario
3. Verificar consumers activos

### Memoria alta
1. Verificar cache Redis
2. Limpiar archivos temporales
3. Restart coordinador con más RAM

## Roadmap

### Fase 1 (Actual)
- 4 coordinadores básicos
- Comunicación message queue
- REST APIs

### Fase 2
- Más agentes especializados
- WebSocket real-time
- Métricas avanzadas

### Fase 3
- Auto-scaling
- Multi-region deployment
- ML model serving optimizado

## Referencias

- [Message Queue Patterns](https://www.enterpriseintegrationpatterns.com/)
- [Microservices Best Practices](https://microservices.io/)
- [Python Async Programming](https://docs.python.org/3/library/asyncio.html)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
