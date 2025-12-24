# App Icon Generation - Tokyo IA

Este directorio contiene el icono de alta resolución y las instrucciones para generar todas las variantes necesarias.

## 📦 Archivos Requeridos

### Icono Principal
- **ic_launcher.png** (512x512px) - Icono cuadrado completo
  - Este es el icono que se sube a Play Console
  - Sin transparencia (fondo opaco)
  - Sin esquinas redondeadas

### Iconos Adaptativos (Recomendado para Android 8.0+)
- **ic_launcher_foreground.png** (512x512px) - Capa frontal
  - Debe tener transparencia
  - Elemento principal centrado en área segura (308x308px)
  
- **ic_launcher_background.png** (512x512px) - Capa de fondo
  - O especificar color sólido en configuración

## 🛠️ Generar Variantes Automáticamente

### Opción 1: Flutter Launcher Icons (Recomendado)

1. Agregar dependencia en `flutter_app/pubspec.yaml`:
```yaml
dev_dependencies:
  flutter_launcher_icons: ^0.13.1

flutter_icons:
  android: true
  ios: false  # Si también quieres generar para iOS
  image_path: "../assets/play-store/icon/ic_launcher.png"
  adaptive_icon_background: "#667eea"  # Color de fondo Tokyo IA
  adaptive_icon_foreground: "../assets/play-store/icon/ic_launcher_foreground.png"
```

2. Ejecutar generación:
```bash
cd flutter_app/
flutter pub get
flutter pub run flutter_launcher_icons:main
```

3. Resultado:
   - Genera todos los tamaños necesarios en `android/app/src/main/res/`
   - mipmap-mdpi, mipmap-hdpi, mipmap-xhdpi, mipmap-xxhdpi, mipmap-xxxhdpi

### Opción 2: Android Asset Studio (Online)

1. Ve a [Android Asset Studio](https://romannurik.github.io/AndroidAssetStudio/icons-launcher.html)
2. Sube `ic_launcher.png`
3. Configura opciones:
   - Shape: None (ya subimos con forma completa)
   - Color: Transparent (o color de fondo)
4. Download ZIP
5. Extrae los archivos a `flutter_app/android/app/src/main/res/`

### Opción 3: Manual con ImageMagick

```bash
# Instalar ImageMagick
brew install imagemagick  # macOS
# o apt-get install imagemagick  # Linux

# Generar variantes
cd assets/play-store/icon/

# mipmap-mdpi (48x48)
convert ic_launcher.png -resize 48x48 ic_launcher_mdpi.png

# mipmap-hdpi (72x72)
convert ic_launcher.png -resize 72x72 ic_launcher_hdpi.png

# mipmap-xhdpi (96x96)
convert ic_launcher.png -resize 96x96 ic_launcher_xhdpi.png

# mipmap-xxhdpi (144x144)
convert ic_launcher.png -resize 144x144 ic_launcher_xxhdpi.png

# mipmap-xxxhdpi (192x192)
convert ic_launcher.png -resize 192x192 ic_launcher_xxxhdpi.png

# Luego copiar manualmente a las carpetas res/mipmap-*
```

## 📐 Especificaciones de Tamaño

Android requiere múltiples densidades:

| Densidad | Tamaño | Ubicación |
|----------|--------|-----------|
| mdpi | 48x48 | res/mipmap-mdpi/ |
| hdpi | 72x72 | res/mipmap-hdpi/ |
| xhdpi | 96x96 | res/mipmap-xhdpi/ |
| xxhdpi | 144x144 | res/mipmap-xxhdpi/ |
| xxxhdpi | 192x192 | res/mipmap-xxxhdpi/ |

## 🎨 Directrices de Diseño

### Área Segura
- Total: 512x512px
- Área segura: 380x380px (66px padding desde bordes)
- Contenido clave: 308x308px (para iconos adaptativos)

### Formato Adaptativo
Para Android 8.0+ (API 26+):
- Sistema puede cortar el icono en diferentes formas
- Shapes comunes: Circle, Rounded Square, Squircle
- Mantener contenido importante centrado

### Colores
- Usar colores de la marca Tokyo IA
- Principal: #667eea (púrpura/azul)
- Secundario: #764ba2 (púrpura oscuro)
- Contraste suficiente con fondos claros y oscuros

### Simplicidad
- Icono debe ser reconocible a 48x48px
- Evitar texto pequeño
- Evitar detalles finos que se pierden al reducir

## ✅ Checklist de Calidad

Antes de publicar, verificar:

- [ ] Icono se ve bien en todos los tamaños (48px a 512px)
- [ ] Sin transparencia en ic_launcher.png
- [ ] Área segura respetada (66px padding)
- [ ] Se distingue de iconos de apps similares
- [ ] Funciona tanto en fondos claros como oscuros
- [ ] Consistente con la identidad visual de Tokyo IA
- [ ] Probado en dispositivos reales (varios fabricantes)
- [ ] Generadas todas las densidades mipmap

## 🧪 Probar el Icono

### En Emulador
```bash
cd flutter_app/
flutter run
# Verificar icono en launcher y app drawer
```

### En Dispositivo Real
```bash
# Build release APK
flutter build apk --release

# Instalar
adb install build/app/outputs/apk/release/app-release.apk

# Verificar en diferentes launchers:
# - Stock launcher
# - Nova Launcher
# - Samsung One UI
# - Pixel Launcher
```

### Visualizar Todas las Variantes
```bash
# Ver iconos generados
ls -lh flutter_app/android/app/src/main/res/mipmap-*/ic_launcher.png
```

## 🔄 Actualizar Icono

Si necesitas actualizar el icono después:

1. Reemplazar `ic_launcher.png` con nuevo diseño
2. Regenerar variantes (método de preferencia)
3. Rebuild app
4. Probar en dispositivos
5. Subir nuevo icono a Play Console (si ya publicado)

## 📚 Recursos

- [Material Design Product Icons](https://material.io/design/iconography/product-icons.html)
- [Android Adaptive Icons](https://developer.android.com/guide/practices/ui_guidelines/icon_design_adaptive)
- [Flutter Launcher Icons Package](https://pub.dev/packages/flutter_launcher_icons)

---

**Última actualización:** 23 de diciembre de 2025
