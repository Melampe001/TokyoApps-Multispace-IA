# ¿Qué tengo que hacer? - Guía de Tareas para Tokyo IA

Este documento responde a la pregunta "¿Qué tengo que hacer?" basándose en la documentación existente del proyecto.

## Arquitectura de Bots - ACTUALIZADO

Tokyo-IA ahora implementa una arquitectura de bots coordinadores separados por tecnología:

### Bots Python (2 coordinadores)

#### 1. KnowledgeCoordinator (Puerto 5001)
**Responsable**: Gestión de conocimiento e información
- RAG (Retrieval-Augmented Generation)
- Web search en tiempo real
- Vector database (ChromaDB)
- Verificación de fuentes

**Ubicación**: `agents/python_bots/knowledge_coordinator/`

#### 2. SentimentCoordinator (Puerto 5002)
**Responsable**: Análisis emocional y adaptación
- Análisis de sentimientos multimodal
- Adaptación de respuestas según mood
- Switch de género (masculino/femenino)
- Contexto conversacional

**Ubicación**: `agents/python_bots/sentiment_coordinator/`

### Bots Node.js (2 coordinadores)

#### 3. GenAICoordinator (Puerto 3001)
**Responsable**: Generación de contenido multimedia
- Text-to-image (Gemini 2.5 Flash)
- Text-to-video (Sora 2 / Veo 3)
- Text-to-music
- Gestión de assets multimedia

**Ubicación**: `agents/node_bots/genai_coordinator/`

#### 4. DeploymentCoordinator (Puerto 3002)
**Responsable**: Build y deployment automático
- Compilación de APK/AAB
- Firmado de aplicaciones
- CI/CD automation
- Gestión de versiones

**Ubicación**: `agents/node_bots/deployment_coordinator/`

### Flujo de Trabajo entre Bots

```
Usuario → App
    ↓
    ├─> SentimentCoordinator (detecta mood)
    ├─> KnowledgeCoordinator (busca información)
    └─> GenAICoordinator (genera contenido)
         ↓
    Respuesta enriquecida al usuario
```

## Estado Actual del Repositorio

El repositorio contiene **documentación y especificaciones** pero aún no tiene la implementación completa. Los archivos existentes describen:

- `README.md` - Estructura del proyecto propuesta
- `Setup` - Checklist de configuración inicial
- `Agentes y bots` - Checklist completo de desarrollo
- Archivos de código de ejemplo (Cuerpo, Imitar, Sin limite, etc.)

## Próximos Pasos (Ordenados por Prioridad)

### 1. Implementar Coordinadores de Bots (NUEVO)
- [x] Crear estructura de directorios `/agents/python_bots` y `/agents/node_bots`
- [x] Documentar arquitectura de 4 coordinadores
- [ ] Implementar KnowledgeCoordinator (Python)
  - [ ] Setup base con FastAPI
  - [ ] Integrar LangChain para RAG
  - [ ] Configurar ChromaDB
  - [ ] Implementar agentes especializados
- [ ] Implementar SentimentCoordinator (Python)
  - [ ] Setup base con FastAPI
  - [ ] Integrar Transformers para sentiment analysis
  - [ ] Configurar Redis para cache
  - [ ] Implementar agentes especializados
- [ ] Implementar GenAICoordinator (Node.js)
  - [ ] Setup base con Express
  - [ ] Integrar Gemini API
  - [ ] Integrar OpenAI API
  - [ ] Implementar agentes especializados
- [ ] Implementar DeploymentCoordinator (Node.js)
  - [ ] Setup base con Express
  - [ ] Integrar Gradle para builds Android
  - [ ] Configurar Fastlane
  - [ ] Implementar agentes especializados

### 2. Setup Inicial del Proyecto
- [ ] Crear el proyecto Flutter: `flutter create tokyo_ia_personal --platforms=android,ios --org=com.tokyoia`
- [ ] Configurar Android minSdk 24 / targetSdk 35 y iOS 13.0+
- [ ] Añadir dependencias al `pubspec.yaml` (ver archivo `Fllutter`)
- [ ] Crear archivo `.env` con API Keys y `[PIN_SIN_BLOQUEOS]`
- [ ] Configurar Firebase Project (Auth + Firestore + Storage)

### 2. Setup Inicial del Proyecto
- [ ] Crear el proyecto Flutter: `flutter create tokyo_ia_personal --platforms=android,ios --org=com.tokyoia`
- [ ] Configurar Android minSdk 24 / targetSdk 35 y iOS 13.0+
- [ ] Añadir dependencias al `pubspec.yaml` (ver archivo `Fllutter`)
- [ ] Crear archivo `.env` con API Keys y `[PIN_SIN_BLOQUEOS]`
- [ ] Configurar Firebase Project (Auth + Firestore + Storage)

### 3. Arquitectura de Agentes - Actualizado con Coordinadores
- [x] Crear carpeta `/agents` para agentes autónomos
- [ ] Configurar Message Queue (RabbitMQ) para comunicación entre bots
- [ ] Configurar Redis para caching
- [ ] Implementar agentes especializados bajo cada coordinador:
  - KnowledgeCoordinator:
    - [ ] `Knowledge_RAGAgent`
    - [ ] `Knowledge_WebSearchAgent`
    - [ ] `Knowledge_VectorDBAgent`
    - [ ] `Knowledge_VerificationAgent`
  - SentimentCoordinator:
    - [ ] `Sentiment_AnalysisAgent`
    - [ ] `Sentiment_AdaptationAgent`
    - [ ] `Sentiment_PersonalityAgent`
    - [ ] `Sentiment_ContextAgent`
  - GenAICoordinator:
    - [ ] `GenAI_ImageAgent`
    - [ ] `GenAI_VideoAgent`
    - [ ] `GenAI_MusicAgent`
    - [ ] `GenAI_StorageAgent`
  - DeploymentCoordinator:
    - [ ] `Deployment_BuildAgent`
    - [ ] `Deployment_SignAgent`
    - [ ] `Deployment_ReleaseAgent`
    - [ ] `Deployment_VersionAgent`

### 4. Implementación Técnica
- [ ] Core LLM edge (Gemini Nano / Llama 4)
- [ ] GenAI (Gemini 2.5 Flash Image + Sora 2 / Veo 3)
- [ ] Sistema de conocimiento ilimitado (RAG + web browsing)
- [ ] Modo sin bloqueos con doble confirmación + PIN
- [ ] Switch género hombre/mujer
- [ ] UI principal (chat, voz, galería, AR preview)

### 4. Testing
- [ ] Tests unitarios 100% cobertura
- [ ] Tests de integración
- [ ] Tests de sinceridad
- [ ] Pruebas de estrés

### 5. Despliegue
- [ ] Generar APK firmado
- [ ] Configurar sideload automático
- [ ] Encriptación de datos locales
- [ ] Backup automático en Firebase

## Comandos para Empezar

```bash
# 1. Crear proyecto Flutter
flutter create tokyo_ia_personal --platforms=android,ios --org=com.tokyoia

# 2. Entrar al directorio
cd tokyo_ia_personal

# 3. Añadir Firebase
flutterfire configure

# 4. Ejecutar la app
flutter run
```

## Referencias

- Ver `/agents/README.md` para arquitectura completa de bots
- Ver `/docs/ARCHITECTURE.md` para detalles técnicos de comunicación entre bots
- Ver `/TAREAS.md` para asignación de tareas por bot
- Ver documentación individual en cada carpeta de coordinador:
  - `/agents/python_bots/knowledge_coordinator/README.md`
  - `/agents/python_bots/sentiment_coordinator/README.md`
  - `/agents/node_bots/genai_coordinator/README.md`
  - `/agents/node_bots/deployment_coordinator/README.md`
- Ver `Setup` - Configuración inicial completa
- Ver `Agentes y bots` - Checklist detallado de desarrollo
- Ver `Fllutter` - Dependencias del pubspec.yaml
- Ver `Cuerpo` - Código de ejemplo para GenAI
- Ver `Sin limite` - Código del modo sin bloqueos
- Ver `Imitar` - Código del detector de sentimientos

---

*Documento actualizado con arquitectura de bots separados (Python/Node.js)*
