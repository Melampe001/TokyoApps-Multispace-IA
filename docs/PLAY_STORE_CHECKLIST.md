# Google Play Store Checklist - Tokyo IA

Esta lista de verificación completa cubre todos los pasos necesarios para publicar Tokyo IA en Google Play Store.

## 📋 Pre-requisitos

### ✅ Cuenta de Google Play Developer
- [ ] Crear cuenta de desarrollador (cuota única de $25 USD)
- [ ] Verificar identidad (puede tomar hasta 48 horas)
- [ ] Configurar información de pago (para recibir pagos de compras)
- [ ] Aceptar el Acuerdo de Distribución para Desarrolladores

### ✅ Requisitos de Firma

#### Generar Keystore de Producción
```bash
keytool -genkey -v -keystore release.keystore -alias key0 -keyalg RSA -keysize 2048 -validity 10000
```

**Información requerida:**
- [ ] Password del keystore (guardar en lugar seguro)
- [ ] Password de la key (puede ser el mismo)
- [ ] Nombre y apellidos
- [ ] Unidad organizacional
- [ ] Organización
- [ ] Ciudad/Localidad
- [ ] Estado/Provincia
- [ ] Código de país (dos letras)

**⚠️ CRÍTICO**: 
- Hacer backup del keystore en múltiples ubicaciones seguras
- Guardar todos los passwords en un gestor de contraseñas
- **Si pierdes el keystore, nunca podrás actualizar la app**

#### Configurar GitHub Secrets
Agregar en `Settings → Secrets → Actions`:
- [ ] `KEYSTORE_FILE` - Path al archivo del keystore
- [ ] `KEYSTORE_PASSWORD` - Password del keystore
- [ ] `KEY_ALIAS` - Alias de la key (ej: `key0`)
- [ ] `KEY_PASSWORD` - Password de la key

## 🎨 Assets Gráficos Requeridos

### Icono de la Aplicación
- [ ] **512x512 px** - Icono de alta resolución (PNG, 32-bit)
  - Sin transparencia
  - Sin esquinas redondeadas (Google las agrega automáticamente)
  - Seguir [Material Design Guidelines](https://material.io/design/iconography/product-icons.html)
- [ ] Generar variantes para Android:
  ```bash
  # Desde flutter_app/
  flutter pub run flutter_launcher_icons:main
  ```

### Gráfico de Función (Feature Graphic)
- [ ] **1024x500 px** (PNG o JPEG, 24-bit)
  - Se muestra en la parte superior de la ficha de Play Store
  - Debe ser visualmente atractivo y representar la app
  - Máximo 1MB

### Capturas de Pantalla
**Teléfono (OBLIGATORIO)**:
- [ ] Mínimo 2 capturas, máximo 8
- [ ] Resolución: 16:9 o 9:16
- [ ] Tamaño mínimo: 320px en lado corto
- [ ] Tamaño máximo: 3840px en lado largo
- [ ] Formatos: PNG o JPEG (24-bit, sin alpha)

**Tablet de 7 pulgadas (OPCIONAL)**:
- [ ] Mínimo 1 captura, máximo 8
- [ ] Recomendado para apps optimizadas para tablet

**Tablet de 10 pulgadas (OPCIONAL)**:
- [ ] Mínimo 1 captura, máximo 8

**Mejores prácticas para capturas**:
- Mostrar las características principales de la app
- Usar texto superpuesto para explicar funcionalidades
- Mantener consistencia visual entre capturas
- Evitar texto excesivo
- Primera captura es la más importante (se muestra en búsqueda)

### Video Promocional (OPCIONAL)
- [ ] Video de YouTube (máximo 1)
- [ ] 30-60 segundos recomendados
- [ ] Mostrar funcionalidades clave

## 📝 Información de Ficha de Play Store

### Título y Descripción
- [ ] **Título de la app**: Máximo 30 caracteres
  - Ejemplo: "Tokyo IA - AI Assistant"
- [ ] **Descripción corta**: Máximo 80 caracteres
  - Primera impresión en resultados de búsqueda
- [ ] **Descripción completa**: Máximo 4000 caracteres
  - Detallar características, beneficios, casos de uso
  - Incluir palabras clave naturalmente (SEO)
  - Usar formato con viñetas y saltos de línea

### Detalles de la Aplicación
- [ ] **Categoría**: Seleccionar apropiada (ej: Productividad, Herramientas)
- [ ] **Tags (etiquetas)**: Hasta 5 tags
- [ ] **Correo electrónico de contacto**: Email público para usuarios
- [ ] **Sitio web** (opcional): URL del sitio web
- [ ] **Política de privacidad**: URL pública (OBLIGATORIO)
  - Publicar `docs/PRIVACY_POLICY.md` en web pública
  - Ejemplo: https://tokyoia.app/privacy

### Calificación de Contenido
- [ ] Completar cuestionario de calificación de contenido
- [ ] Proporcionar información precisa (violaciones pueden resultar en suspensión)
- [ ] Categorías principales:
  - Violencia
  - Contenido sexual
  - Lenguaje
  - Drogas/alcohol
  - Contenido generado por usuarios

### Distribución por País
- [ ] Seleccionar países donde estará disponible la app
- [ ] Considerar restricciones legales locales
- [ ] Por defecto: todos los países disponibles

## 🚀 Builds y Versiones

### Build de Release
```bash
cd flutter_app/

# Limpiar builds anteriores
flutter clean

# Obtener dependencias
flutter pub get

# Build AAB (Android App Bundle) - RECOMENDADO
flutter build appbundle --release

# Build APK (si necesario para testing)
flutter build apk --release
```

**Archivos generados:**
- AAB: `flutter_app/build/app/outputs/bundle/release/app-release.aab`
- APK: `flutter_app/build/app/outputs/apk/release/app-release.apk`

### Versionado
En `flutter_app/pubspec.yaml`:
```yaml
version: 1.0.0+1  # versionName+versionCode
```
- `1.0.0` - Version name (visible para usuarios)
- `1` - Version code (número incremental, usado internamente)

**Reglas:**
- [ ] Cada nueva versión debe incrementar `versionCode`
- [ ] Seguir [Semantic Versioning](https://semver.org/) para `versionName`

### Firma del Build
- [ ] Verificar que el AAB está firmado con keystore de release
- [ ] **NO** subir builds firmados con debug keystore

## 🧪 Pruebas Pre-Publicación

### Pruebas Locales
- [ ] Probar build de release en múltiples dispositivos
- [ ] Verificar funcionalidades principales
- [ ] Probar compras dentro de la app (en modo sandbox)
- [ ] Verificar permisos solicitados

### Pruebas en Play Console
**1. Pista de Pruebas Internas (Internal Testing)**
- [ ] Crear pista de pruebas internas
- [ ] Subir AAB
- [ ] Agregar testers (máximo 100, por email)
- [ ] Distribución inmediata (sin revisión)
- [ ] Ideal para QA del equipo

**2. Pista de Pruebas Cerradas (Closed Testing)**
- [ ] Crear pista cerrada (ej: "beta")
- [ ] Subir AAB
- [ ] Agregar testers (lista de emails o grupos de Google)
- [ ] Distribución tras revisión automatizada (pocas horas)
- [ ] Recopilar feedback de early adopters

**3. Pista de Pruebas Abiertas (Open Testing)**
- [ ] Opcional: hacer beta pública
- [ ] Cualquiera puede unirse con un link
- [ ] Máximo 10,000 testers
- [ ] Feedback público en Play Store

## 📱 Compras Dentro de la App (In-App Purchases)

### Configuración de Productos
- [ ] Ir a "Monetización → Productos"
- [ ] Crear productos:
  - **Consumibles**: Se usan una vez (ej: tokens)
  - **No consumibles**: Se compran una vez (ej: versión premium)
  - **Suscripciones**: Pagos recurrentes

### Información Requerida por Producto
- [ ] ID del producto (único, inmutable)
- [ ] Nombre
- [ ] Descripción
- [ ] Precio (puede variar por país)
- [ ] Estado (activo/inactivo)

### Testing de Compras
- [ ] Agregar testers en "Configuración → Pruebas de licencia"
- [ ] Usar cuentas de prueba para simular compras
- [ ] Verificar flujo completo sin cargos reales

## 🔐 Privacidad y Seguridad

### Declaración de Privacidad
- [ ] Completar "Privacidad de datos" en Play Console
- [ ] Declarar qué datos se recopilan
- [ ] Explicar cómo se usan y comparten los datos
- [ ] Proporcionar link a política de privacidad

### Sección de Seguridad de Datos
- [ ] Datos recopilados (location, personal info, etc.)
- [ ] Propósito de recopilación
- [ ] Si los datos se comparten con terceros
- [ ] Prácticas de seguridad (cifrado en tránsito/reposo)
- [ ] Si el usuario puede solicitar eliminación de datos

### Permisos
En `AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="com.android.vending.BILLING" />
```
- [ ] Solo solicitar permisos necesarios
- [ ] Justificar cada permiso en la descripción

## 📤 Publicación

### Primera Versión (Producción)
1. [ ] Ir a "Producción" en Play Console
2. [ ] Crear nueva versión
3. [ ] Subir AAB firmado
4. [ ] Completar "Notas de la versión" (qué hay de nuevo)
   - Soporte multi-idioma recomendado
5. [ ] Revisar y enviar para revisión

### Tiempos de Revisión
- **Primera app**: 7 días hábiles (puede ser más)
- **Actualizaciones**: 1-3 días
- **Rechazos**: Común en primera publicación, revisar feedback cuidadosamente

### Estados de Publicación
- **Borrador**: No enviado aún
- **En revisión**: Google está revisando
- **Cambios solicitados**: Corregir problemas señalados
- **Aprobado**: Disponible en Play Store
- **Rechazado**: Revisar razones y volver a enviar

## 🔄 Actualizaciones Post-Lanzamiento

### Actualizar la App
```bash
# Incrementar version en pubspec.yaml
version: 1.0.1+2  # Nueva versión

# Build nueva versión
flutter build appbundle --release

# Subir a Play Console en pista de producción
```

### Staged Rollout (Despliegue Gradual)
- [ ] Considerar rollout por etapas (5%, 10%, 25%, 50%, 100%)
- [ ] Monitorear crashes y ANRs (App Not Responding)
- [ ] Pausar rollout si hay problemas críticos
- [ ] Continuar rollout una vez resueltos problemas

### Pre-Lanzamiento Reports
Google automáticamente prueba la app en dispositivos reales:
- [ ] Revisar crashes detectados
- [ ] Revisar screenshots de diferentes dispositivos
- [ ] Corregir problemas antes de lanzamiento completo

## 📊 Post-Lanzamiento

### Monitoreo
- [ ] Configurar alertas para crashes y ANRs
- [ ] Revisar estadísticas de instalación/desinstalación
- [ ] Leer reseñas y responder (aumenta calificación)
- [ ] Monitorear métricas de retención

### Optimización de Ficha (ASO - App Store Optimization)
- [ ] Experimentar con títulos y descripciones
- [ ] A/B testing de íconos y capturas (Play Console Experiments)
- [ ] Analizar palabras clave que traen instalaciones
- [ ] Actualizar capturas con nuevas features

## ⚠️ Problemas Comunes y Soluciones

### App Rechazada
**Razones comunes:**
1. Política de privacidad incompleta o no accesible
2. Descripción engañosa o spammy
3. Permisos no justificados
4. Contenido que viola políticas
5. App se crashea en testing automático

**Solución:**
- Leer cuidadosamente el feedback de rechazo
- Corregir todos los problemas señalados
- Volver a enviar con explicación de cambios

### Problemas de Firma
```bash
# Verificar firma del AAB
jarsigner -verify -verbose -certs build/app/outputs/bundle/release/app-release.aab
```

### App No Visible en Play Store
- Puede tomar 2-3 horas tras aprobación
- Verificar que está publicada en país correcto
- Limpiar caché de Play Store

## 📚 Recursos Adicionales

- [Google Play Console Help](https://support.google.com/googleplay/android-developer)
- [Android Developer Policy](https://play.google.com/about/developer-content-policy/)
- [Launch Checklist](https://developer.android.com/distribute/best-practices/launch/launch-checklist)
- [Play Academy](https://playacademy.exceedlms.com/) - Cursos gratuitos

## ✅ Checklist Final Antes de Submit

- [ ] ✅ Keystore seguro y respaldado
- [ ] ✅ Build AAB firmado y probado
- [ ] ✅ Todos los assets gráficos subidos
- [ ] ✅ Título, descripción, capturas completas
- [ ] ✅ Política de privacidad publicada y linkeada
- [ ] ✅ Calificación de contenido completada
- [ ] ✅ Permisos justificados
- [ ] ✅ Pruebas en múltiples dispositivos
- [ ] ✅ In-app purchases configuradas (si aplica)
- [ ] ✅ Email de contacto válido
- [ ] ✅ Notas de versión escritas
- [ ] ✅ Equipo notificado de publicación

---

**¡Buena suerte con el lanzamiento de Tokyo IA! 🚀**
