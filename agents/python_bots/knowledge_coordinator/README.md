# KnowledgeCoordinator (Coordinador de Conocimiento)

Bot coordinador Python responsable de la gestión de conocimiento, búsqueda y verificación de información.

## Descripción

El KnowledgeCoordinator es uno de los dos coordinadores implementados en Python. Su función principal es proporcionar respuestas verificadas basadas en múltiples fuentes de información.

## Responsabilidades

- **RAG (Retrieval-Augmented Generation)**: Búsqueda en documentos locales usando vectores
- **Web Search**: Búsqueda en tiempo real en internet
- **Verificación de Fuentes**: Validación de información con sources verificables
- **Vector Database**: Gestión de embeddings y similitud semántica

## Agentes Especializados

### Knowledge_RAGAgent
- Búsqueda en documentos embedidos
- Generación aumentada con retrieval
- Ranking de relevancia

### Knowledge_WebSearchAgent  
- Búsqueda web en tiempo real
- Extracción de información de páginas
- Filtrado de resultados

### Knowledge_VectorDBAgent
- Gestión de ChromaDB
- Creación de embeddings
- Búsqueda por similitud

### Knowledge_VerificationAgent
- Validación de fuentes
- Cross-referencing
- Scoring de confiabilidad

## Tecnologías

```python
# requirements.txt
langchain>=0.1.0
chromadb>=0.4.18
sentence-transformers>=2.2.2
openai>=1.3.0
requests>=2.31.0
aiohttp>=3.9.0
beautifulsoup4>=4.12.0
```

## Instalación

```bash
cd agents/python_bots/knowledge_coordinator
pip install -r requirements.txt
python coordinator.py
```

## API

### HTTP Endpoints

```
POST /api/search
Body: { "query": "string", "sources": ["web", "local"] }
Response: { "answer": "string", "sources": [...], "confidence": 0.9 }

POST /api/embed
Body: { "text": "string" }
Response: { "embedding": [...], "dimension": 768 }

GET /api/health
Response: { "status": "ok", "version": "1.0.0" }
```

## Configuración

```bash
# .env
KNOWLEDGE_COORDINATOR_PORT=5001
OPENAI_API_KEY=sk-...
CHROMA_PERSIST_DIRECTORY=/data/chromadb
WEB_SEARCH_API_KEY=your_key
```

## Ejemplo de Uso

```python
from knowledge_coordinator import KnowledgeCoordinator

async def main():
    coordinator = KnowledgeCoordinator()
    
    # Búsqueda con verificación
    result = await coordinator.search_with_sources(
        query="¿Cuál es la historia del Tokyo Skytree?",
        include_web=True
    )
    
    print(f"Respuesta: {result['answer']}")
    print(f"Fuentes: {result['sources']}")
    print(f"Confianza: {result['confidence']}")
```

## Testing

```bash
pytest tests/
pytest tests/test_rag_agent.py -v
```

## Logs

Todos los logs se registran en:
- Console: Formato pretty
- File: `/logs/knowledge_coordinator.log`
- Firestore: Colección `bot_logs`

## Comunicación

### Recibe mensajes de:
- App móvil (usuarios)
- SentimentCoordinator (contexto emocional)
- GenAICoordinator (necesita info para generar contenido)

### Envía mensajes a:
- App móvil (respuestas)
- GenAICoordinator (datos para generación)
- DeploymentCoordinator (logs de uso)

## Métricas

- Queries por minuto
- Tiempo promedio de respuesta
- Tasa de acierto de cache
- Confianza promedio de respuestas

## Mantenimiento

- Actualizar embeddings: `python scripts/update_embeddings.py`
- Limpiar cache: `python scripts/clean_cache.py`
- Backup vectorDB: `python scripts/backup_chromadb.py`

## Soporte

Para problemas con este coordinador, abrir issue con etiqueta `knowledge-coordinator`.
