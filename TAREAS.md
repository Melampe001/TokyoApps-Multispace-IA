# ¿Qué tengo que hacer? - Guía de Tareas para Tokyo IA

Este documento responde a la pregunta "¿Qué tengo que hacer?" basándose en la documentación existente del proyecto.

## Estado Actual del Repositorio

El repositorio contiene **documentación y especificaciones** pero aún no tiene la implementación completa. Los archivos existentes describen:

- `README.md` - Estructura del proyecto propuesta
- `Setup` - Checklist de configuración inicial
- `Agentes y bots` - Checklist completo de desarrollo
- Archivos de código de ejemplo (Cuerpo, Imitar, Sin limite, etc.)

## Próximos Pasos (Ordenados por Prioridad)

### 1. Setup Inicial del Proyecto
- [ ] Crear el proyecto Flutter: `flutter create tokyo_ia_personal --platforms=android,ios --org=com.tokyoia`
- [ ] Configurar Android minSdk 24 / targetSdk 35 y iOS 13.0+
- [ ] Añadir dependencias al `pubspec.yaml` (ver archivo `Fllutter`)
- [ ] Crear archivo `.env` con API Keys y `[PIN_SIN_BLOQUEOS]`
- [ ] Configurar Firebase Project (Auth + Firestore + Storage)

### 2. Arquitectura de Agentes
- [ ] Crear carpeta `/agents` para agentes autónomos
- [ ] Implementar agentes obligatorios:
  - `Agent_CodeMaster` → genera y revisa código
  - `Agent_GenAI` → text-to-image/video/music
  - `Agent_Knowledge` → RAG + web search
  - `Agent_Sentiment` → análisis de ánimo
  - `Agent_Unrestricted` → modo sin bloqueos
  - `Agent_QA` → comentarios en commits
  - `Agent_Deploy` → compila y firma APK

### 3. Implementación Técnica
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

Para más detalles, consulta los archivos:
- `Setup` - Configuración inicial completa
- `Agentes y bots` - Checklist detallado de desarrollo
- `Fllutter` - Dependencias del pubspec.yaml
- `Cuerpo` - Código de ejemplo para GenAI
- `Sin limite` - Código del modo sin bloqueos
- `Imitar` - Código del detector de sentimientos

---

*Documento generado para clarificar los requisitos del proyecto Tokyo IA Personal*
