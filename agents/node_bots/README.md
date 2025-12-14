# Node.js Bots - Coordinadores y Agentes

Este directorio contiene todos los bots y agentes implementados en Node.js para el proyecto Tokyo-IA.

## Coordinadores Node.js

### 1. GenAICoordinator (Coordinador de Generación AI)

**Ubicación:** `genai_coordinator/`

**Responsabilidades:**
- Text-to-image (Gemini 2.5 Flash Image)
- Text-to-video (Sora 2 / Veo 3)
- Text-to-music
- Gestión de contenido multimedia 4K
- Almacenamiento y optimización de assets generados

**Agentes Especializados:**
- `GenAI_ImageAgent` - Generación de imágenes
- `GenAI_VideoAgent` - Generación de videos
- `GenAI_MusicAgent` - Generación de música/audio
- `GenAI_StorageAgent` - Gestión de archivos multimedia

**Tecnologías:**
- Google Gemini API para imágenes
- OpenAI API (Sora) para videos
- FFmpeg para procesamiento multimedia
- AWS S3 / Firebase Storage para almacenamiento

**Ejemplo de uso:**
```javascript
import { GenAICoordinator } from './genai_coordinator';

const coordinator = new GenAICoordinator();
const result = await coordinator.generateImage({
    prompt: "Tokyo skyline at sunset, 4K quality",
    resolution: "1024x1024",
    style: "photorealistic"
});
// result: { imageUrl: "...", metadata: {...} }
```

### 2. DeploymentCoordinator (Coordinador de Despliegue)

**Ubicación:** `deployment_coordinator/`

**Responsabilidades:**
- Compilación automática de APK/AAB (Android)
- Firmado de aplicaciones con keystore
- Gestión de CI/CD pipelines
- Automatización de releases
- Versionado y changelog
- Deploy a Play Store / App Store

**Agentes Especializados:**
- `Deployment_BuildAgent` - Compilación de aplicaciones
- `Deployment_SignAgent` - Firmado de builds
- `Deployment_ReleaseAgent` - Publicación de releases
- `Deployment_VersionAgent` - Gestión de versiones

**Tecnologías:**
- Gradle para builds Android
- Fastlane para automatización
- GitHub Actions API
- Google Play Publishing API

**Ejemplo de uso:**
```javascript
import { DeploymentCoordinator } from './deployment_coordinator';

const coordinator = new DeploymentCoordinator();
const build = await coordinator.buildAndSign({
    platform: "android",
    buildType: "release",
    version: "1.2.3"
});
// build: { apkPath: "...", signed: true, version: "1.2.3" }
```

## Instalación

### Requisitos
- Node.js 18.x o superior
- npm o yarn
- FFmpeg (para GenAICoordinator)

### Setup
```bash
# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys

# Ejecutar en desarrollo
npm run dev

# Ejecutar en producción
npm start
```

### Dependencias Principales

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
    "fluent-ffmpeg": "^2.1.2",
    "dotenv": "^16.3.0",
    "winston": "^3.11.0",
    "joi": "^17.11.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "nodemon": "^3.0.0",
    "eslint": "^8.54.0",
    "prettier": "^3.1.0"
  }
}
```

## Estructura de Archivos

```
node_bots/
├── README.md                           # Este archivo
├── package.json                        # Dependencias y scripts
├── .env.example                        # Ejemplo de variables de entorno
├── .eslintrc.js                        # Configuración ESLint
├── jest.config.js                      # Configuración Jest
├── shared/                             # Código compartido
│   ├── baseCoordinator.js             # Clase base para coordinadores
│   ├── messageQueue.js                # Cliente para queue
│   ├── logger.js                      # Logger configurado
│   └── utils.js                       # Utilidades comunes
├── genai_coordinator/
│   ├── index.js                       # Entry point
│   ├── coordinator.js                 # Coordinador principal
│   ├── config.js                      # Configuración
│   ├── routes/                        # REST API endpoints
│   │   └── api.js
│   ├── agents/
│   │   ├── imageAgent.js
│   │   ├── videoAgent.js
│   │   ├── musicAgent.js
│   │   └── storageAgent.js
│   └── __tests__/
│       └── coordinator.test.js
└── deployment_coordinator/
    ├── index.js                       # Entry point
    ├── coordinator.js                 # Coordinador principal
    ├── config.js                      # Configuración
    ├── routes/                        # REST API endpoints
    │   └── api.js
    ├── agents/
    │   ├── buildAgent.js
    │   ├── signAgent.js
    │   ├── releaseAgent.js
    │   └── versionAgent.js
    └── __tests__/
        └── coordinator.test.js
```

## Convenciones de Código

### Nombres
- Clases: `PascalCase` (ej: `GenAICoordinator`)
- Funciones: `camelCase` (ej: `generateImage`)
- Constantes: `UPPER_SNAKE_CASE` (ej: `MAX_RETRIES`)
- Archivos: `camelCase` (ej: `imageAgent.js`)

### Documentación (JSDoc)
```javascript
/**
 * Genera una imagen a partir de un prompt de texto.
 * 
 * @param {Object} options - Opciones de generación
 * @param {string} options.prompt - Descripción de la imagen
 * @param {string} options.resolution - Resolución deseada
 * @returns {Promise<Object>} Objeto con URL de imagen y metadata
 * @throws {ValidationError} Si el prompt está vacío
 */
async function generateImage(options) {
    // Implementación
}
```

### Logging
```javascript
import logger from '../shared/logger';

logger.info('Iniciando coordinador de GenAI');
logger.warn('API rate limit approaching', { remaining: 10 });
logger.error('Error al generar imagen', { error: err.message });
```

### Manejo de Errores
```javascript
class GenAIError extends Error {
    constructor(message, code) {
        super(message);
        this.name = 'GenAIError';
        this.code = code;
    }
}

// Uso
try {
    const result = await generateImage(prompt);
} catch (error) {
    if (error instanceof GenAIError) {
        logger.error('GenAI error', { code: error.code });
    }
    throw error;
}
```

## Testing

```bash
# Ejecutar todos los tests
npm test

# Ejecutar tests de un coordinador específico
npm test -- genai_coordinator

# Con coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

### Ejemplo de Test
```javascript
import { GenAICoordinator } from '../coordinator';

describe('GenAICoordinator', () => {
    let coordinator;
    
    beforeEach(() => {
        coordinator = new GenAICoordinator();
    });
    
    test('should generate image from prompt', async () => {
        const result = await coordinator.generateImage({
            prompt: 'Test image',
            resolution: '512x512'
        });
        
        expect(result).toHaveProperty('imageUrl');
        expect(result.metadata).toBeDefined();
    });
});
```

## Scripts de npm

```json
{
  "scripts": {
    "start": "node genai_coordinator/index.js & node deployment_coordinator/index.js",
    "dev": "nodemon --watch '**/*.js' genai_coordinator/index.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write '**/*.{js,json,md}'",
    "build": "echo 'No build step required for Node.js'"
  }
}
```

## Comunicación con Python Bots

Los coordinadores Node.js se comunican con los bots Python a través de:

### 1. Message Queue (RabbitMQ)
```javascript
import { MessageQueue } from '../shared/messageQueue';

const queue = new MessageQueue();
await queue.publish('knowledge_requests', {
    type: 'search',
    query: 'Tokyo history',
    requester: 'genai_coordinator'
});
```

### 2. REST API
```javascript
import axios from 'axios';

const response = await axios.post(
    'http://knowledge-coordinator:5001/api/search',
    {
        query: 'Tokyo landmarks',
        includeImages: true
    }
);
```

### 3. WebSockets (para eventos en tiempo real)
```javascript
import { io } from 'socket.io-client';

const socket = io('http://sentiment-coordinator:5002');
socket.on('mood_detected', (data) => {
    console.log('Usuario mood:', data.mood);
    // Adaptar generación según mood
});
```

## Variables de Entorno

```bash
# .env.example

# Node.js Coordinators
GENAI_COORDINATOR_PORT=3001
DEPLOYMENT_COORDINATOR_PORT=3002

# APIs
GOOGLE_GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here

# Storage
FIREBASE_CREDENTIALS_PATH=/path/to/firebase-credentials.json
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=tokyo-ia-media

# Message Queue
RABBITMQ_URL=amqp://guest:guest@localhost:5672
REDIS_URL=redis://localhost:6379

# Build & Deploy
ANDROID_KEYSTORE_PATH=/path/to/keystore.jks
ANDROID_KEYSTORE_PASSWORD=your_password
GOOGLE_PLAY_SERVICE_ACCOUNT=/path/to/play-service-account.json

# Logging
NODE_ENV=production
LOG_LEVEL=info
LOG_FILE=/logs/node_bots.log
```

## Desarrollo

### Agregar un Nuevo Agente

1. Crear archivo en `[coordinator]/agents/newAgent.js`
2. Exportar clase que extiende `BaseAgent` (si existe)
3. Implementar método `execute()`
4. Registrar en el coordinador
5. Agregar tests en `__tests__/`

Ejemplo:
```javascript
// agents/newAgent.js
export class NewAgent {
    constructor(coordinator) {
        this.coordinator = coordinator;
    }
    
    async execute(task) {
        // Implementación
        return result;
    }
}

// coordinator.js
import { NewAgent } from './agents/newAgent';

class Coordinator {
    constructor() {
        this.newAgent = new NewAgent(this);
    }
}
```

### Debugging

```javascript
// Usar debugger de Node.js
node --inspect genai_coordinator/index.js

// O con VSCode, agregar a launch.json:
{
    "type": "node",
    "request": "launch",
    "name": "Debug GenAI Coordinator",
    "program": "${workspaceFolder}/agents/node_bots/genai_coordinator/index.js"
}
```

## API REST

Cada coordinador expone una API REST:

### GenAICoordinator (Puerto 3001)
```
POST /api/generate/image
POST /api/generate/video
POST /api/generate/music
GET  /api/status
GET  /api/health
```

### DeploymentCoordinator (Puerto 3002)
```
POST /api/build
POST /api/sign
POST /api/release
GET  /api/versions
GET  /api/health
```

## Monitoreo

Cada coordinador expone métricas:
- **Logs**: `/logs/node_bots.log` (Winston)
- **Firestore**: Colección `bot_metrics`
- **Prometheus**: Endpoint `/metrics`
- **Health Check**: Endpoint `/api/health`

## Seguridad

- **API Keys**: Usar variables de entorno, nunca hardcodear
- **Autenticación**: JWT tokens o Firebase Auth
- **Rate Limiting**: Express-rate-limit en todas las rutas
- **Input Validation**: Joi para validar requests
- **CORS**: Configurado solo para orígenes autorizados

## Optimización

### Performance
```javascript
// Usar clustering para múltiples workers
import cluster from 'cluster';
import os from 'os';

if (cluster.isPrimary) {
    const numCPUs = os.cpus().length;
    for (let i = 0; i < numCPUs; i++) {
        cluster.fork();
    }
} else {
    // Código del worker
}
```

### Caching
```javascript
import redis from 'redis';

const cache = redis.createClient();
await cache.set(`image:${prompt}`, imageUrl, { EX: 3600 });
```

## Soporte

Para dudas o problemas:
1. Revisar logs en `/logs/node_bots.log`
2. Consultar documentación en `/docs/ARCHITECTURE.md`
3. Abrir issue en GitHub con etiqueta `node-bots`

## Recursos Adicionales

- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [Gemini API Docs](https://ai.google.dev/docs)
- [OpenAI API Docs](https://platform.openai.com/docs)
