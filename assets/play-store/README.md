# Play Store Assets - Tokyo IA

Esta carpeta contiene todos los assets gráficos necesarios para la publicación en Google Play Store.

## 📁 Estructura de Directorios

```
assets/play-store/
├── icon/
│   ├── ic_launcher.png (512x512)     # Icono de alta resolución
│   └── README.md                      # Instrucciones para generar variantes
├── screenshots/
│   ├── phone/                         # Capturas para teléfonos (OBLIGATORIO)
│   │   ├── screenshot-1.png
│   │   ├── screenshot-2.png
│   │   ├── screenshot-3.png
│   │   ├── screenshot-4.png
│   │   └── screenshot-5.png
│   └── tablet/                        # Capturas para tablets (OPCIONAL)
│       ├── screenshot-1.png
│       └── screenshot-2.png
├── feature-graphic/
│   └── feature-graphic.png (1024x500) # Gráfico de función
└── README.md (este archivo)
```

## 🎨 Requisitos de Assets

### 1. Icono de Aplicación (App Icon)

**Archivo**: `icon/ic_launcher.png`

**Especificaciones**:
- Tamaño: 512x512 px
- Formato: PNG (32-bit)
- Sin transparencia (fondo opaco)
- Sin esquinas redondeadas (Google las agrega automáticamente)
- Espacio de seguridad: 66px desde los bordes (el icono visible debe estar en el área central de 380x380px)

**Diseño**:
- Seguir [Material Design Icon Guidelines](https://material.io/design/iconography/product-icons.html)
- Mantener consistencia con la identidad visual de Tokyo IA
- Usar colores vibrantes que destaquen en Play Store
- Evitar texto pequeño (debe ser legible a 48x48px)

**Generar Variantes para Android**:
```bash
cd flutter_app/

# Configurar en pubspec.yaml
flutter_icons:
  android: true
  image_path: "../assets/play-store/icon/ic_launcher.png"
  adaptive_icon_background: "#667eea"
  adaptive_icon_foreground: "../assets/play-store/icon/ic_launcher_foreground.png"

# Generar
flutter pub run flutter_launcher_icons:main
```

### 2. Feature Graphic

**Archivo**: `feature-graphic/feature-graphic.png`

**Especificaciones**:
- Tamaño: 1024x500 px
- Formato: PNG o JPEG (24-bit)
- Tamaño máximo: 1 MB
- Se muestra en la parte superior de la ficha de Play Store

**Diseño**:
- Visualmente atractivo y representativo de la app
- Puede incluir logo, personajes (los 5 agentes), o screenshots
- Debe funcionar tanto en móvil como desktop
- Evitar texto excesivo (se corta en algunos dispositivos)

**Ideas para Tokyo IA**:
- Banner con los 5 agentes (侍❄️🛡️🌸🏗️) y sus nombres
- Gradient background (colores de Tokyo IA: #667eea → #764ba2)
- Texto: "Tokyo IA - 5 Specialized AI Agents"

### 3. Screenshots de Teléfono

**Ubicación**: `screenshots/phone/`

**Especificaciones**:
- Cantidad: Mínimo 2, máximo 8 (recomendado: 4-5)
- Aspecto: 16:9 o 9:16 (vertical preferido para apps móviles)
- Tamaño mínimo: 320px en lado corto
- Tamaño máximo: 3840px en lado largo
- Formato: PNG o JPEG (24-bit, sin alpha)
- Tamaño de archivo: Máximo 8 MB por imagen

**Contenido Recomendado**:

1. **screenshot-1.png**: Dashboard principal
   - Mostrar los 5 agentes con iconos
   - Nombre y especialidad de cada uno
   - Interfaz limpia y atractiva

2. **screenshot-2.png**: Chat con Akira (Code Review)
   - Ejemplo de código
   - Respuesta detallada del agente
   - Destacar expertise en seguridad

3. **screenshot-3.png**: Resultados de arquitectura (Kenji)
   - Diagramas o recomendaciones
   - Mostrar profundidad de análisis

4. **screenshot-4.png**: Generación de tests (Yuki)
   - Código de tests generado
   - Cobertura y métricas

5. **screenshot-5.png**: Métricas y estadísticas
   - Gráficos de uso
   - Tokens, costos, latencias

**Mejores Prácticas**:
- ✅ Usar dispositivos reales o emuladores de alta resolución
- ✅ Modo claro (light mode) generalmente funciona mejor
- ✅ Agregar texto superpuesto para explicar funcionalidades
- ✅ Mantener consistencia visual entre capturas
- ✅ Primera captura es la MÁS importante (se muestra en búsqueda)
- ❌ Evitar demasiado texto
- ❌ No incluir información personal o sensible

### 4. Screenshots de Tablet (Opcional)

**Ubicación**: `screenshots/tablet/`

**Especificaciones**: Igual que teléfono, pero con:
- Aspecto: 16:9 o 16:10 (horizontal preferido)
- Mínimo: 1080px en lado corto
- Máximo: 7680px en lado largo

**Cuándo Incluir**:
- Si la app está optimizada para tablets
- Si tienes layouts específicos para pantallas grandes
- Para mostrar funcionalidades adicionales en tablets

## 🛠️ Herramientas para Crear Assets

### Para Iconos
- **Figma/Sketch**: Diseño profesional
- **Canva**: Plantillas prediseñadas
- **Adobe Illustrator**: Diseño vectorial
- **Icon Kitchen**: Generador online específico para Android

### Para Feature Graphic
- **Figma**: Recomendado (template: 1024x500px)
- **Photoshop**: Edición avanzada
- **Canva**: Plantillas de banner
- **GIMP**: Alternativa gratuita

### Para Screenshots
- **Android Studio Emulator**: Capturas de emulador
  ```bash
  # Tomar screenshot
  # En emulador: Camera icon o Ctrl+S (Windows/Linux) / Cmd+S (Mac)
  ```
- **Real Device**: Capturas de dispositivo físico
  ```bash
  # Conectar dispositivo
  adb devices
  
  # Tomar screenshot
  adb shell screencap -p /sdcard/screenshot.png
  adb pull /sdcard/screenshot.png
  ```
- **Flutter Tools**: Capturas desde Flutter
  ```bash
  flutter screenshot
  ```
- **Mockup Tools**: 
  - [Screely](https://screely.com) - Agregar marco de dispositivo
  - [Mockuphone](https://mockuphone.com) - Mockups de múltiples dispositivos
  - [Rotato](https://rotato.app) - Mockups 3D (de pago)

### Para Texto en Screenshots
- **Figma**: Superponer texto en capturas
- **Photoshop**: Capas de texto
- **Screenshot Framer**: Herramientas específicas para ASO

## 📐 Templates y Recursos

### Template Figma (Recomendado)
Crear archivo en Figma con frames:
```
- App Icon: 512x512px
- Feature Graphic: 1024x500px
- Phone Screenshot: 1080x1920px (o resolución de tu dispositivo)
- Tablet Screenshot: 1920x1200px
```

### Paleta de Colores Tokyo IA
```
Primary: #667eea
Secondary: #764ba2
Gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
Text: #ffffff (on dark) / #333333 (on light)
Background: #f5f5f5 (light) / #1a1a1a (dark)
```

### Tipografías Recomendadas
- **Títulos**: Inter Bold, SF Pro Display Bold
- **Cuerpo**: Inter Regular, SF Pro Text Regular
- **Código**: JetBrains Mono, Fira Code

## 📋 Checklist de Creación

### Iconos
- [ ] Crear ic_launcher.png (512x512)
- [ ] Verificar que no tenga transparencia
- [ ] Verificar espacio de seguridad (66px)
- [ ] Generar variantes para Android (mipmap)
- [ ] Probar en dispositivo real

### Feature Graphic
- [ ] Crear feature-graphic.png (1024x500)
- [ ] Incluir branding de Tokyo IA
- [ ] Verificar legibilidad en móvil
- [ ] Optimizar tamaño (<1MB)

### Screenshots
- [ ] Capturar mínimo 2 screenshots de teléfono
- [ ] Agregar texto descriptivo (opcional pero recomendado)
- [ ] Verificar que primera captura es la mejor
- [ ] Optimizar tamaño de archivos
- [ ] Verificar en diferentes densidades de pantalla

## 🚀 Proceso de Subida a Play Console

1. Ve a [Play Console](https://play.google.com/console)
2. Selecciona tu app
3. "Store presence" → "Main store listing"
4. Sección "Graphics":
   - App icon: Subir `icon/ic_launcher.png`
   - Feature graphic: Subir `feature-graphic/feature-graphic.png`
   - Phone screenshots: Subir 2-8 imágenes de `screenshots/phone/`
   - Tablet screenshots (opcional): Subir de `screenshots/tablet/`

## 💡 Tips de ASO (App Store Optimization)

### Para Iconos
- Colores vibrantes funcionan mejor que neutros
- Iconos simples son más memorables
- Probar A/B testing (Play Console Experiments)

### Para Feature Graphic
- Mostrar valor único de la app
- Actualizar con nuevas features
- Usar en anuncios y marketing

### Para Screenshots
- Primera captura debe "vender" la app
- Usar texto superpuesto para explicar beneficios (no solo features)
- Actualizar screenshots con nuevas versiones
- Considerar localización (diferentes idiomas)

## 📊 Métricas de Éxito

Después de publicar, monitorear:
- **CVR (Conversion Rate)**: % visitantes que instalan
- **CTR (Click-Through Rate)**: % que hacen clic en búsqueda
- Comparar con promedios de categoría
- Iterar basándose en datos

## 🔄 Actualización de Assets

**Cuándo actualizar:**
- ✅ Major redesign de la app
- ✅ Nuevas features significativas
- ✅ Cambio de branding
- ✅ Mejorar CVR bajo
- ✅ Cada 6-12 meses (refresh)

**Proceso de actualización:**
1. Crear nuevos assets
2. Subir a Play Console (no reemplaces inmediato)
3. A/B testing con Play Experiments (si disponible)
4. Analizar resultados (2-4 semanas)
5. Implementar versión ganadora

## 📚 Recursos Adicionales

- [Material Design Icons](https://material.io/design/iconography)
- [Android Asset Studio](https://romannurik.github.io/AndroidAssetStudio/)
- [Play Store Listing Guidelines](https://support.google.com/googleplay/android-developer/answer/9866151)
- [ASO Best Practices](https://developer.android.com/distribute/best-practices/launch/store-listing)

---

## ✅ Estado Actual

- [ ] Icono creado
- [ ] Feature graphic creado
- [ ] Screenshots de teléfono creadas
- [ ] Screenshots de tablet creadas (opcional)
- [ ] Assets optimizados
- [ ] Assets subidos a Play Console

**Última actualización:** 23 de diciembre de 2025
