# SentimentCoordinator (Coordinador de Sentimientos)

Bot coordinador Python responsable del análisis emocional y adaptación de respuestas según el estado anímico del usuario.

## Descripción

El SentimentCoordinator es uno de los dos coordinadores implementados en Python. Su función principal es detectar emociones y adaptar la personalidad de la IA según el contexto.

## Responsabilidades

- **Análisis de Sentimientos**: Detección multimodal de emociones (texto, voz, contexto)
- **Adaptación de Respuestas**: Modificación del tono según mood detectado
- **Gestión de Personalidad**: Switch entre género masculino/femenino
- **Contexto Conversacional**: Memoria de estado emocional del usuario

## Agentes Especializados

### Sentiment_AnalysisAgent
- Análisis de texto con transformers
- Detección de emociones múltiples
- Scoring de intensidad emocional

### Sentiment_AdaptationAgent  
- Adaptación de tono de respuestas
- Inserción de elementos empáticos
- Ajuste de formalidad

### Sentiment_PersonalityAgent
- Switch de género de personalidad
- Ajuste de características de respuesta
- Consistencia de personalidad

### Sentiment_ContextAgent
- Memoria de conversaciones previas
- Tracking de evolución emocional
- Predicción de necesidades

## Tecnologías

```python
# requirements.txt
transformers>=4.35.0
torch>=2.1.0
redis>=5.0.0  # Para cache de estados
firebase-admin>=6.2.0
scipy>=1.11.0  # Para análisis estadístico
```

## Instalación

```bash
cd agents/python_bots/sentiment_coordinator
pip install -r requirements.txt
python coordinator.py
```

## API

### HTTP Endpoints

```
POST /api/analyze
Body: { "text": "string", "context": {...} }
Response: { "emotion": "string", "intensity": 0.7, "valence": 0.5 }

POST /api/adapt
Body: { "text": "string", "mood": {...}, "gender": "mujer" }
Response: { "adapted_text": "string", "changes": [...] }

POST /api/personality/switch
Body: { "gender": "mujer" }
Response: { "success": true, "current_gender": "mujer" }

GET /api/health
Response: { "status": "ok", "version": "1.0.0" }
```

## Configuración

```bash
# .env
SENTIMENT_COORDINATOR_PORT=5002
HUGGINGFACE_TOKEN=hf_...
REDIS_URL=redis://localhost:6379
FIREBASE_CREDENTIALS_PATH=/path/to/credentials.json
```

## Ejemplo de Uso

```python
from sentiment_coordinator import SentimentCoordinator

async def main():
    coordinator = SentimentCoordinator()
    
    # Detectar mood
    mood = await coordinator.detect_mood(
        text="Estoy un poco frustrado con este problema",
        user_id="user123"
    )
    
    # Adaptar respuesta
    response = "Aquí está la solución a tu problema"
    adapted = coordinator.adapt_response(
        response=response,
        mood=mood,
        gender="mujer"
    )
    
    print(f"Mood: {mood['emotion']} (intensidad: {mood['intensity']})")
    print(f"Respuesta adaptada: {adapted}")
```

## Testing

```bash
pytest tests/
pytest tests/test_sentiment_analysis.py -v
```

## Modelos

### Sentiment Analysis
- `distilbert-base-uncased-finetuned-sst-2-english` (base)
- `nlptown/bert-base-multilingual-uncased-sentiment` (multilingual)
- Custom fine-tuned model for Spanish

### Emotion Detection
- `j-hartmann/emotion-english-distilroberta-base`
- Custom model trained with conversational data

## Logs

Todos los logs se registran en:
- Console: Formato pretty
- File: `/logs/sentiment_coordinator.log`
- Firestore: Colección `bot_logs` + `sentiment_history`

## Comunicación

### Recibe mensajes de:
- App móvil (input de usuarios)
- Todos los coordinadores (para adaptar sus respuestas)

### Envía mensajes a:
- Todos los coordinadores (contexto emocional)
- App móvil (feedback emocional)

## Métricas

- Emociones detectadas por sesión
- Tiempo de análisis promedio
- Distribución de moods
- Efectividad de adaptaciones (feedback del usuario)

## Estados Emocionales Detectados

- `neutral` - Estado base
- `happy` - Contento, satisfecho
- `sad` - Triste, melancólico
- `angry` - Enojado, frustrado
- `anxious` - Ansioso, preocupado
- `excited` - Emocionado, entusiasmado
- `confused` - Confundido, perdido
- `curious` - Curioso, interesado

## Adaptaciones por Género

### Masculino
- Tono más directo
- Respuestas concisas
- Enfoque en soluciones

### Femenino
- Tono más empático
- Respuestas con contexto emocional
- Enfoque en comprensión

## Mantenimiento

- Reentrenar modelos: `python scripts/retrain_models.py`
- Limpiar cache Redis: `python scripts/clean_sentiment_cache.py`
- Analizar métricas: `python scripts/analyze_sentiment_metrics.py`

## Soporte

Para problemas con este coordinador, abrir issue con etiqueta `sentiment-coordinator`.
