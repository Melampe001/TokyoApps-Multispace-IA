# GenAICoordinator (Coordinador de Generación AI)

Bot coordinador Node.js responsable de la generación de contenido multimedia usando IA generativa.

## Descripción

El GenAICoordinator es uno de los dos coordinadores implementados en Node.js. Su función principal es generar imágenes, videos y música de alta calidad usando modelos de IA.

## Responsabilidades

- **Text-to-Image**: Generación de imágenes 4K con Gemini 2.5 Flash
- **Text-to-Video**: Generación de videos con Sora 2 / Veo 3
- **Text-to-Music**: Generación de audio y música
- **Asset Management**: Almacenamiento y optimización de contenido multimedia

## Agentes Especializados

### GenAI_ImageAgent
- Generación de imágenes con Gemini API
- Estilos: fotorealista, artístico, anime, etc.
- Resoluciones hasta 4K

### GenAI_VideoAgent  
- Generación de videos con OpenAI Sora
- Duración: 1-60 segundos
- Calidad: HD, 4K

### GenAI_MusicAgent
- Generación de música y efectos de sonido
- Estilos: múltiples géneros
- Formatos: MP3, WAV, FLAC

### GenAI_StorageAgent
- Upload a Firebase Storage / AWS S3
- Optimización de archivos
- CDN distribution

## Tecnologías

```json
{
  "dependencies": {
    "@google/generative-ai": "^0.2.0",
    "openai": "^4.20.0",
    "fluent-ffmpeg": "^2.1.2",
    "firebase-admin": "^12.0.0",
    "aws-sdk": "^2.1500.0",
    "sharp": "^0.33.0",
    "axios": "^1.6.0"
  }
}
```

## Instalación

```bash
cd agents/node_bots/genai_coordinator
npm install
npm start
```

## API

### HTTP Endpoints

```
POST /api/generate/image
Body: { 
  "prompt": "string", 
  "resolution": "1024x1024",
  "style": "photorealistic" 
}
Response: { "imageUrl": "string", "metadata": {...} }

POST /api/generate/video
Body: { 
  "prompt": "string", 
  "duration": 10,
  "quality": "4K" 
}
Response: { "videoUrl": "string", "metadata": {...} }

POST /api/generate/music
Body: { 
  "prompt": "string", 
  "duration": 30,
  "genre": "lofi" 
}
Response: { "audioUrl": "string", "metadata": {...} }

GET /api/status
Response: { "queue": 5, "processing": 2, "completed": 150 }

GET /api/health
Response: { "status": "ok", "version": "1.0.0" }
```

## Configuración

```bash
# .env
GENAI_COORDINATOR_PORT=3001
GOOGLE_GEMINI_API_KEY=your_key
OPENAI_API_KEY=your_key

# Storage
FIREBASE_CREDENTIALS_PATH=/path/to/firebase-credentials.json
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_S3_BUCKET=tokyo-ia-media

# Processing
MAX_CONCURRENT_GENERATIONS=5
FFMPEG_PATH=/usr/bin/ffmpeg
```

## Ejemplo de Uso

```javascript
import axios from 'axios';

async function generateContent() {
    // Generar imagen
    const imageResult = await axios.post(
        'http://localhost:3001/api/generate/image',
        {
            prompt: 'Tokyo skyline at sunset, cyberpunk style, 4K',
            resolution: '1024x1024',
            style: 'photorealistic'
        }
    );
    
    console.log('Imagen generada:', imageResult.data.imageUrl);
    
    // Generar video
    const videoResult = await axios.post(
        'http://localhost:3001/api/generate/video',
        {
            prompt: 'Flying through Tokyo streets at night',
            duration: 10,
            quality: '4K'
        }
    );
    
    console.log('Video generado:', videoResult.data.videoUrl);
}
```

## Testing

```bash
npm test
npm test -- genai_coordinator
npm run test:coverage
```

## Procesamiento

### Pipeline de Generación

1. **Validación**: Validar prompt y parámetros
2. **Queue**: Agregar a cola de procesamiento
3. **Generate**: Llamar a API correspondiente
4. **Post-process**: Optimizar resultado (resize, compress)
5. **Upload**: Subir a storage
6. **Notify**: Notificar a solicitante

### Optimizaciones

```javascript
// Cache de resultados
const cacheKey = `image:${hash(prompt)}`;
const cached = await redis.get(cacheKey);
if (cached) return cached;

// Compresión de imágenes
await sharp(imageBuffer)
    .resize(1024, 1024)
    .jpeg({ quality: 85 })
    .toFile(outputPath);

// Procesamiento paralelo
const results = await Promise.all([
    generateImage(prompt1),
    generateImage(prompt2),
    generateImage(prompt3)
]);
```

## Logs

Todos los logs se registran en:
- Console: Winston pretty format
- File: `/logs/genai_coordinator.log`
- Firestore: Colección `bot_logs` + `generation_history`

## Comunicación

### Recibe mensajes de:
- App móvil (solicitudes de usuarios)
- KnowledgeCoordinator (generar contenido basado en info)
- SentimentCoordinator (adaptar estilo según mood)

### Envía mensajes a:
- App móvil (contenido generado)
- KnowledgeCoordinator (contenido para embeddings)
- DeploymentCoordinator (assets para incluir en builds)

## Métricas

- Generaciones por minuto
- Tiempo promedio por tipo (image/video/music)
- Tasa de éxito/error
- Costo por generación
- Almacenamiento usado

## Rate Limits

### Gemini API
- 60 requests/minuto (tier gratuito)
- 1,500 requests/día

### OpenAI API
- Varía por plan
- Monitor usage en dashboard

## Estilos Soportados

### Imágenes
- `photorealistic` - Fotorrealista
- `artistic` - Artístico/pintura
- `anime` - Estilo anime/manga
- `cyberpunk` - Cyberpunk/futurista
- `traditional` - Arte tradicional japonés

### Videos
- `cinematic` - Cinemático
- `documentary` - Documental
- `animation` - Animación
- `timelapse` - Timelapse

### Música
- `lofi` - Lo-fi hip hop
- `ambient` - Ambiental
- `electronic` - Electrónica
- `traditional` - Música tradicional japonesa

## Mantenimiento

- Limpiar cache: `npm run clean:cache`
- Optimizar storage: `npm run optimize:storage`
- Analizar métricas: `npm run analyze:metrics`
- Actualizar modelos: `npm run update:models`

## Troubleshooting

### Error: Rate limit exceeded
- Implementar exponential backoff
- Usar cola con delay
- Considerar tier pagado

### Error: Out of memory
- Reducir MAX_CONCURRENT_GENERATIONS
- Aumentar RAM del servidor
- Implementar streaming para videos grandes

### Error: Storage full
- Implementar lifecycle policies
- Comprimir archivos antiguos
- Migrar a storage de largo plazo

## Soporte

Para problemas con este coordinador, abrir issue con etiqueta `genai-coordinator`.
