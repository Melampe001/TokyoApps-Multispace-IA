# 🚀 PR Super Agents Workflow - Documentación

## Descripción General

El workflow `pull_request_super_agents.yml` es un sistema avanzado de validación automática que se ejecuta en cada Pull Request para garantizar calidad, seguridad y cumplimiento de estándares en el código.

## 🎯 Agentes Incluidos

### 1. 📝 Validación de Commits (Conventional Commits)
- **Qué hace**: Valida que todos los commits y el título del PR sigan el formato de Conventional Commits
- **Formato esperado**: `tipo: descripción`
- **Tipos válidos**: 
  - `feat`: Nueva funcionalidad
  - `fix`: Corrección de bugs
  - `docs`: Cambios en documentación
  - `style`: Cambios de formato
  - `refactor`: Refactorización
  - `perf`: Mejoras de rendimiento
  - `test`: Añadir o corregir tests
  - `build`: Cambios en el sistema de build
  - `ci`: Cambios en CI/CD
  - `chore`: Tareas de mantenimiento
  - `revert`: Revertir cambios

**Ejemplo válido**: `feat: Add user authentication`

### 2. 🔍 Linting Go
- **Herramienta**: golangci-lint
- **Qué hace**: Ejecuta múltiples linters para código Go
- **Linters incluidos**:
  - gofmt: Formato de código
  - govet: Análisis estático
  - errcheck: Verificación de errores
  - staticcheck: Análisis avanzado
  - gosec: Seguridad
  - misspell: Errores ortográficos
  - gocyclo: Complejidad ciclomática
  - Y más...

### 3. 🐍 Linting Python
- **Herramientas**: black, flake8, pylint
- **Cuándo se ejecuta**: Solo si hay archivos `.py` modificados
- **Qué hace**: 
  - Verifica formato con black
  - Detecta errores de sintaxis con flake8
  - Análisis de calidad con pylint

### 4. 🎯 Linting Dart/Flutter
- **Herramienta**: dart analyze
- **Cuándo se ejecuta**: Si hay archivos `.dart` o `pubspec.yaml` modificados
- **Qué hace**: Analiza código Dart/Flutter para errores y advertencias

### 5. 🐚 Linting Shell
- **Herramienta**: shellcheck
- **Qué hace**: Valida scripts de shell para errores comunes y mejores prácticas
- **Integración**: ReviewDog para comentarios en línea

### 6. ✅ Tests & CI
- **Comando**: `make ci`
- **Qué hace**:
  - Ejecuta formateo de código
  - Corre todos los tests unitarios
  - Genera reporte de cobertura
  - Sube cobertura a Codecov

### 7. 🔒 Gosec Security Scanner
- **Qué hace**: Escanea vulnerabilidades de seguridad en código Go
- **Formato de salida**: SARIF (subido a GitHub Security)
- **Severidades**: Crítico, Alto, Medio

### 8. 🔒 Bandit Security Scanner
- **Qué hace**: Escanea vulnerabilidades de seguridad en código Python
- **Cuándo se ejecuta**: Solo si hay archivos `.py` modificados
- **Qué detecta**: Problemas comunes de seguridad en Python

### 9. 🔒 Trivy Security Scanner
- **Qué hace**: Escaneo completo de vulnerabilidades
- **Escanea**:
  - Código fuente
  - Dependencias (go.mod, requirements.txt, etc.)
  - Configuraciones
  - Imágenes de contenedor
- **Severidades**: Crítico, Alto, Medio

### 10. 📚 Validación de Documentación
- **Qué hace**: Verifica que cambios en `/lib` o `/internal` incluyan actualizaciones en `/docs`
- **Comportamiento**:
  - Si hay cambios en código sin docs: Crea un comentario de advertencia
  - No falla el PR, solo alerta
  - Fomenta documentación actualizada

### 11. 📦 Alerta de Cambios en Dependencias
- **Archivos monitoreados**:
  - `go.mod`, `go.sum`
  - `requirements.txt`, `requirements-dev.txt`
  - `pyproject.toml`, `Pipfile`
  - `pubspec.yaml`, `pubspec.lock`
  - `package.json`, `package-lock.json`, `yarn.lock`
- **Qué hace**: 
  - Detecta cambios en archivos de dependencias
  - Crea comentario con recomendaciones
  - Lista las mejores prácticas a seguir

### 12. 🐶 ReviewDog
- **Qué hace**: Proporciona sugerencias automáticas de revisión
- **Herramientas integradas**:
  - golangci-lint: Sugerencias de código Go
  - misspell: Corrección de errores ortográficos
- **Formato**: Comentarios en línea en el PR

### 13. 📊 Summary
- **Qué hace**: Genera un resumen final de todos los checks
- **Información incluida**:
  - Estado de cada job (✅ éxito, ❌ fallo, ⏭️ omitido)
  - Lista de jobs fallidos
  - Mensaje de éxito si todos pasan

## 🚀 Estrategia de Ejecución

### Paralelización
- Todos los jobs se ejecutan en **paralelo** para máxima eficiencia
- Solo el job "Summary" espera a que todos terminen
- Tiempo total ≈ tiempo del job más lento

### Optimizaciones
1. **Caché de Dependencias**: 
   - Go modules
   - Python pip
   - Flutter/Dart packages
2. **Ejecución Condicional**: 
   - Linters de Python/Dart solo si hay archivos relevantes
3. **Continue-on-error**: 
   - Algunos checks son informativos, no bloqueantes
4. **Fail-fast desactivado**: 
   - Ver todos los problemas a la vez

### Permisos
- **Principio de menor privilegio**
- Permisos mínimos necesarios:
  - `contents: read` - Leer código
  - `pull-requests: write` - Comentar en PRs
  - `checks: write` - Actualizar estado de checks
  - `security-events: write` - Subir resultados de seguridad

## 📋 Configuración de Archivos

### `.golangci.yml`
Configuración de golangci-lint con:
- 18+ linters habilitados
- Reglas personalizadas
- Exclusiones para tests y vendor
- Timeout de 5 minutos

### `.github/commitlint.config.js`
Configuración de commitlint:
- Basado en `@commitlint/config-conventional`
- Tipos de commit permitidos
- Longitud máxima de header: 100 caracteres
- Sin punto final en el subject

## 🎯 Mejores Prácticas Implementadas

Basado en estándares de empresas líderes:

### Google
- Revisión automática de código
- Tests obligatorios
- Análisis estático exhaustivo

### Microsoft
- Seguridad como prioridad
- Múltiples escaneos de vulnerabilidades
- Validación de dependencias

### Netflix
- Ejecución paralela de checks
- Feedback rápido a desarrolladores
- Optimización de tiempos de CI

### Shopify
- Conventional commits
- Documentación como ciudadano de primera clase
- ReviewDog para sugerencias automáticas

## 🔧 Cómo Usar

### Para Desarrolladores

1. **Crear un PR**:
   ```bash
   git checkout -b feat/nueva-funcionalidad
   git commit -m "feat: Add nueva funcionalidad"
   git push origin feat/nueva-funcionalidad
   ```

2. **El workflow se ejecuta automáticamente**:
   - Se activa al abrir, actualizar o editar el PR
   - Todos los checks se ejecutan en paralelo
   - Recibirás comentarios automáticos si hay problemas

3. **Revisar resultados**:
   - Ve a la pestaña "Checks" en tu PR
   - Revisa los comentarios de ReviewDog
   - Lee las alertas de seguridad y dependencias
   - Corrige los problemas reportados

4. **Actualizar el PR**:
   ```bash
   # Hacer correcciones
   git add .
   git commit -m "fix: Corregir problemas de linting"
   git push
   ```
   - El workflow se ejecuta nuevamente
   - Solo se re-ejecutan los checks afectados (gracias al caché)

### Para Revisores

1. **Revisa los checks automáticos primero**:
   - Todos deben estar en verde antes de aprobar
   - Lee los comentarios de ReviewDog
   - Verifica las alertas de seguridad

2. **Enfócate en lógica de negocio**:
   - Los checks automáticos cubren formato, estilo, seguridad
   - Tú te enfocas en diseño, arquitectura, lógica

## 🛠️ Mantenimiento

### Actualizar versiones de acciones
Las acciones de GitHub se actualizan regularmente. Revisar cada 3-6 meses:
- `actions/checkout@v4` → versión más reciente
- `actions/setup-go@v5` → versión más reciente
- `golangci/golangci-lint-action@v4` → versión más reciente

### Añadir nuevos linters
1. Edita `.golangci.yml` para Go
2. Añade nuevos jobs en el workflow para otros lenguajes
3. Mantén la estructura paralela

### Ajustar severidades
En cada job de seguridad, puedes ajustar:
```yaml
severity: 'CRITICAL,HIGH'  # Solo crítico y alto
# o
severity: 'CRITICAL,HIGH,MEDIUM'  # Incluir medio
```

## ❓ Troubleshooting

### El workflow no se ejecuta
- Verifica que el archivo esté en `.github/workflows/`
- Verifica que la sintaxis YAML sea válida
- Asegúrate de que el trigger incluya tu rama

### Un job falla constantemente
- Revisa los logs del job
- Verifica la configuración del linter
- Considera añadir `continue-on-error: true` temporalmente

### Tiempo de ejecución muy largo
- Revisa qué jobs toman más tiempo
- Aumenta el uso de caché
- Considera hacer algunos checks opcionales con `if` conditions

## 📚 Referencias

- [Conventional Commits](https://www.conventionalcommits.org/)
- [golangci-lint](https://golangci-lint.run/)
- [Trivy](https://aquasecurity.github.io/trivy/)
- [ReviewDog](https://github.com/reviewdog/reviewdog)
- [GitHub Actions Best Practices](https://docs.github.com/en/actions/learn-github-actions/security-hardening-for-github-actions)

## 📝 Licencia

Este workflow es parte del proyecto Tokyo-IA y sigue la misma licencia del proyecto principal.
