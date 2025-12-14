# Python Bots - Coordinadores y Agentes

Este directorio contiene todos los bots y agentes implementados en Python para el proyecto Tokyo-IA.

## Coordinadores Python

### 1. KnowledgeCoordinator (Coordinador de Conocimiento)

**Ubicación:** `knowledge_coordinator/`

**Responsabilidades:**
- RAG (Retrieval-Augmented Generation) ilimitado
- Web search en tiempo real
- Gestión de base de datos vectorial (ChromaDB)
- Verificación de fuentes y sinceridad
- Respuestas basadas en evidencia verificable

**Agentes Especializados:**
- `Knowledge_RAGAgent` - Búsqueda en documentos locales
- `Knowledge_WebSearchAgent` - Búsqueda web en tiempo real
- `Knowledge_VectorDBAgent` - Gestión de embeddings
- `Knowledge_VerificationAgent` - Validación de fuentes

**Tecnologías:**
- LangChain para RAG
- ChromaDB para vectores
- Transformers para embeddings
- Requests para web search APIs

**Ejemplo de uso:**
```python
from knowledge_coordinator import KnowledgeCoordinator

coordinator = KnowledgeCoordinator()
result = await coordinator.search_with_sources("¿Cuál es la capital de Japón?")
# Resultado incluye respuesta + fuentes verificadas
```

### 2. SentimentCoordinator (Coordinador de Sentimientos)

**Ubicación:** `sentiment_coordinator/`

**Responsabilidades:**
- Análisis de sentimientos multimodal (texto, voz, contexto)
- Detección de emociones del usuario
- Adaptación de respuestas según mood detectado
- Switch de personalidad (género masculino/femenino)
- Personalización de interacciones

**Agentes Especializados:**
- `Sentiment_AnalysisAgent` - Análisis de emociones
- `Sentiment_AdaptationAgent` - Adaptación de respuestas
- `Sentiment_PersonalityAgent` - Gestión de personalidad
- `Sentiment_ContextAgent` - Análisis de contexto conversacional

**Tecnologías:**
- Transformers (Hugging Face) para sentiment analysis
- Custom models para detección multimodal
- Redis para cache de estados emocionales

**Ejemplo de uso:**
```python
from sentiment_coordinator import SentimentCoordinator

coordinator = SentimentCoordinator()
mood = await coordinator.detect_mood("Estoy un poco frustrado hoy")
# mood: {'emotion': 'frustrated', 'intensity': 0.7}

adapted = coordinator.adapt_response(
    "Aquí está tu respuesta",
    mood=mood,
    gender="mujer"
)
# Respuesta adaptada con empatía
```

## Instalación

### Requisitos
- Python 3.10 o superior
- pip (gestor de paquetes)
- virtualenv (recomendado)

### Setup
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys
```

### Dependencias Principales

```txt
# requirements.txt

# Core ML/AI
transformers>=4.35.0
torch>=2.1.0
sentence-transformers>=2.2.2

# RAG y Vector DB
langchain>=0.1.0
chromadb>=0.4.18
openai>=1.3.0  # Para embeddings

# Web y APIs
requests>=2.31.0
aiohttp>=3.9.0
beautifulsoup4>=4.12.0

# Database
firebase-admin>=6.2.0
redis>=5.0.0

# Utilidades
python-dotenv>=1.0.0
pydantic>=2.5.0
loguru>=0.7.0
```

## Estructura de Archivos

```
python_bots/
├── README.md                           # Este archivo
├── requirements.txt                    # Dependencias Python
├── .env.example                        # Ejemplo de variables de entorno
├── shared/                             # Código compartido
│   ├── __init__.py
│   ├── base_coordinator.py            # Clase base para coordinadores
│   ├── message_queue.py               # Cliente para queue
│   └── utils.py                       # Utilidades comunes
├── knowledge_coordinator/
│   ├── __init__.py
│   ├── coordinator.py                 # Coordinador principal
│   ├── config.py                      # Configuración
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── rag_agent.py
│   │   ├── web_search_agent.py
│   │   ├── vector_db_agent.py
│   │   └── verification_agent.py
│   └── tests/
│       └── test_coordinator.py
└── sentiment_coordinator/
    ├── __init__.py
    ├── coordinator.py                 # Coordinador principal
    ├── config.py                      # Configuración
    ├── agents/
    │   ├── __init__.py
    │   ├── analysis_agent.py
    │   ├── adaptation_agent.py
    │   ├── personality_agent.py
    │   └── context_agent.py
    └── tests/
        └── test_coordinator.py
```

## Convenciones de Código

### Nombres
- Clases: `PascalCase` (ej: `KnowledgeCoordinator`)
- Funciones: `snake_case` (ej: `detect_mood`)
- Constantes: `UPPER_SNAKE_CASE` (ej: `MAX_RETRIES`)
- Archivos: `snake_case` (ej: `rag_agent.py`)

### Documentación
```python
async def process_query(query: str, context: dict) -> dict:
    """
    Procesa una consulta con contexto adicional.
    
    Args:
        query: Texto de la consulta del usuario
        context: Diccionario con contexto adicional
        
    Returns:
        Diccionario con resultado y metadatos
        
    Raises:
        ValueError: Si la consulta está vacía
    """
    pass
```

### Logging
```python
from loguru import logger

logger.info("Iniciando coordinador de conocimiento")
logger.warning("Cache no disponible, usando búsqueda directa")
logger.error("Error al conectar con vector DB", exc_info=True)
```

## Testing

```bash
# Ejecutar todos los tests
pytest python_bots/

# Ejecutar tests de un coordinador específico
pytest python_bots/knowledge_coordinator/tests/

# Con coverage
pytest --cov=python_bots --cov-report=html
```

## Comunicación con Node.js Bots

Los coordinadores Python se comunican con los bots Node.js a través de:

1. **Message Queue** (RabbitMQ/Redis Pub/Sub)
```python
from shared.message_queue import MessageQueue

queue = MessageQueue()
await queue.publish(
    channel="genai_requests",
    message={
        "type": "generate_image",
        "prompt": "Tokyo skyline at night",
        "requester": "knowledge_coordinator"
    }
)
```

2. **REST API**
```python
import aiohttp

async with aiohttp.ClientSession() as session:
    async with session.post(
        "http://genai-coordinator:3000/api/generate",
        json={"prompt": "...", "type": "image"}
    ) as response:
        result = await response.json()
```

## Variables de Entorno

```bash
# .env.example

# Python Coordinators
KNOWLEDGE_COORDINATOR_PORT=5001
SENTIMENT_COORDINATOR_PORT=5002

# APIs
OPENAI_API_KEY=your_openai_key_here
HUGGINGFACE_TOKEN=your_hf_token_here

# Databases
FIREBASE_CREDENTIALS_PATH=/path/to/firebase-credentials.json
REDIS_URL=redis://localhost:6379
CHROMA_PERSIST_DIRECTORY=/data/chromadb

# Message Queue
RABBITMQ_URL=amqp://guest:guest@localhost:5672

# Logging
LOG_LEVEL=INFO
LOG_FILE=/logs/python_bots.log
```

## Desarrollo

### Agregar un Nuevo Agente

1. Crear archivo en `[coordinator]/agents/new_agent.py`
2. Heredar de `BaseAgent` si existe, o crear clase independiente
3. Implementar método `execute()`
4. Registrar en el coordinador
5. Agregar tests en `tests/`

### Debugging

```python
# Activar modo debug
import os
os.environ['DEBUG'] = '1'

# Usar debugger
import pdb; pdb.set_trace()

# O con ipdb
import ipdb; ipdb.set_trace()
```

## Monitoreo

Todos los coordinadores Python registran métricas en:
- **Logs**: `/logs/python_bots.log`
- **Firestore**: Colección `bot_metrics`
- **Prometheus**: Endpoint `/metrics` (si está habilitado)

## Seguridad

- **API Keys**: Nunca hardcodear, usar variables de entorno
- **Autenticación**: Validar tokens de Firebase Auth
- **Rate Limiting**: Implementado en cada coordinador
- **Input Validation**: Usar Pydantic para validar entradas

## Soporte

Para dudas o problemas:
1. Revisar logs en `/logs/`
2. Consultar documentación en `/docs/ARCHITECTURE.md`
3. Abrir issue en GitHub con etiqueta `python-bots`
