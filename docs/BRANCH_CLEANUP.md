# 🧹 Sistema de Limpieza Automática de Ramas

## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Estrategia de Limpieza](#estrategia-de-limpieza)
- [Ramas Protegidas](#ramas-protegidas)
- [Uso del Script Manual](#uso-del-script-manual)
- [Ejecución Automática](#ejecución-automática)
- [Configuración y Personalización](#configuración-y-personalización)
- [Troubleshooting](#troubleshooting)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [FAQ](#faq)

## Descripción General

El sistema de limpieza automática de ramas mantiene el repositorio organizado eliminando ramas obsoletas que ya han sido mergeadas a la rama principal (`Main`). Este sistema ayuda a:

- ✅ Mantener el repositorio limpio y organizado
- ✅ Reducir la confusión sobre qué ramas están activas
- ✅ Mejorar el rendimiento de operaciones Git
- ✅ Facilitar la navegación en GitHub

### Componentes

1. **Script Manual** (`scripts/cleanup-branches.sh`): Script bash para limpieza manual controlada
2. **Workflow Automático** (`.github/workflows/branch-cleanup.yml`): Limpieza semanal automatizada
3. **Lista de Exclusión** (`.github/branch-cleanup-exclude.txt`): Ramas específicas a proteger
4. **Makefile Targets**: Comandos rápidos para ejecutar limpieza

## Estrategia de Limpieza

### Política de Retención

Por defecto, el sistema:

- 🔍 **Identifica** ramas mergeadas a `Main` usando `git branch --merged`
- ⏱️ **Espera** 14 días después del merge antes de eliminar (configurable)
- 🛡️ **Protege** ramas importantes automáticamente
- 📊 **Reporta** todas las acciones realizadas

### Criterios de Eliminación

Una rama se elimina SOLO si cumple TODOS estos criterios:

1. ✅ Está completamente mergeada a `Main`
2. ✅ Ha pasado el período de retención (14 días por defecto)
3. ✅ NO está en la lista de ramas protegidas
4. ✅ NO coincide con patrones de exclusión
5. ✅ NO está listada en `.github/branch-cleanup-exclude.txt`

## Ramas Protegidas

### Ramas que NUNCA se Eliminan

Las siguientes ramas están **permanentemente protegidas**:

```bash
Main          # Rama principal de producción
Prompt        # Rama de prompts y configuración
main          # Rama principal (lowercase)
develop       # Rama de desarrollo
mela          # Rama especial del proyecto
```

### Patrones Protegidos

Todas las ramas que coincidan con estos patrones están protegidas:

```bash
feature/*     # Ramas de features en desarrollo
hotfix/*      # Parches urgentes
release/*     # Ramas de release
```

### Protección Personalizada

Para proteger ramas adicionales, agrégalas a `.github/branch-cleanup-exclude.txt`:

```bash
# Ejemplo
copilot/important-experiment
experimental/machine-learning
feature/long-term-project
```

## Uso del Script Manual

### Requisitos

- Git instalado
- Bash shell
- Permisos de escritura en el repositorio remoto

### Sintaxis Básica

```bash
./scripts/cleanup-branches.sh [OPCIONES]
```

### Opciones Disponibles

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `--dry-run` | Solo listar, no eliminar (por defecto) | `./scripts/cleanup-branches.sh --dry-run` |
| `--force` | Eliminar sin confirmación | `./scripts/cleanup-branches.sh --force` |
| `--days N` | Solo eliminar ramas mergeadas hace >N días | `./scripts/cleanup-branches.sh --days 7` |
| `--exclude PATTERN` | Agregar patrón de exclusión temporal | `./scripts/cleanup-branches.sh --exclude "test/*"` |
| `-h, --help` | Mostrar ayuda | `./scripts/cleanup-branches.sh --help` |

### Usando Makefile

Para mayor comodidad, usa los targets del Makefile:

```bash
# Dry-run (solo listar)
make clean-branches

# Limpieza real (con confirmación)
make clean-branches-force
```

## Ejecución Automática

### Programación

El workflow se ejecuta automáticamente:

- 📅 **Semanalmente**: Domingos a las 00:00 UTC
- 🕐 **Criterio**: Ramas mergeadas hace más de 14 días
- 📬 **Notificación**: Crea un issue con el reporte

### Ejecución Manual

Puedes ejecutar el workflow manualmente desde GitHub:

1. Ve a **Actions** → **🧹 Branch Cleanup**
2. Click en **Run workflow**
3. Configura las opciones:
   - **Days**: Número de días desde merge (default: 14)
   - **Dry run**: Marcar para solo listar sin eliminar
4. Click en **Run workflow**

### Desactivar Limpieza Automática

Si necesitas desactivar temporalmente la limpieza automática:

**Opción 1: Desactivar el Workflow**

1. Ve a **Actions** → **🧹 Branch Cleanup**
2. Click en los tres puntos (⋯)
3. Selecciona **Disable workflow**

**Opción 2: Modificar el Schedule**

Edita `.github/workflows/branch-cleanup.yml` y comenta la sección `schedule`:

```yaml
on:
  # schedule:
  #   - cron: '0 0 * * 0'
  workflow_dispatch:
    # ...
```

## Configuración y Personalización

### Modificar Período de Retención

Edita el workflow para cambiar el período por defecto:

```yaml
# En .github/workflows/branch-cleanup.yml
inputs:
  days:
    description: 'Días desde merge para eliminar'
    default: '30'  # Cambiar de 14 a 30 días
```

### Agregar Ramas Protegidas

**Método 1: Lista de Exclusión** (Recomendado)

Edita `.github/branch-cleanup-exclude.txt`:

```bash
# Agregar ramas específicas
copilot/experimental-feature
feature/project-xyz
temporary/keep-this-branch
```

**Método 2: Modificar el Script**

Edita `scripts/cleanup-branches.sh`:

```bash
PROTECTED_BRANCHES=(
  "Main"
  "Prompt"
  "main"
  "develop"
  "mela"
  "tu-rama-especial"  # Agregar aquí
)
```

### Agregar Patrones de Exclusión

Edita el script para agregar nuevos patrones:

```bash
PROTECTED_PATTERNS=(
  "feature/*"
  "hotfix/*"
  "release/*"
  "experimental/*"  # Nuevo patrón
)
```

## Troubleshooting

### Problema: "No se encontró rama base"

**Causa**: El repositorio no tiene una rama `Main` o `main`.

**Solución**:
```bash
# Verificar ramas existentes
git branch -a

# Asegúrate de que existe Main o main
git checkout -b Main origin/Main
```

### Problema: "Permission denied" al eliminar ramas

**Causa**: No tienes permisos de escritura en el repositorio remoto.

**Solución**:
1. Verifica tus permisos en GitHub
2. Asegúrate de estar autenticado correctamente:
   ```bash
   git remote -v
   gh auth status
   ```

### Problema: Rama protegida se intenta eliminar

**Causa**: La rama no está correctamente configurada como protegida.

**Solución**:
1. Agrégala a `.github/branch-cleanup-exclude.txt`
2. O modifica `PROTECTED_BRANCHES` en el script

### Problema: Workflow falla con "fetch-depth: 0"

**Causa**: Problema con el checkout de Git.

**Solución**: El workflow ya incluye `fetch-depth: 0`, pero si persiste:
```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0
    token: ${{ secrets.GITHUB_TOKEN }}
```

### Problema: Script no detecta ramas mergeadas

**Causa**: Referencias remotas desactualizadas.

**Solución**:
```bash
# Actualizar referencias
git fetch --prune origin

# Ejecutar el script nuevamente
./scripts/cleanup-branches.sh --dry-run
```

### Problema: "Branch is not fully merged"

**Causa**: La rama tiene commits que no están en `Main`.

**Solución**: Esta es una característica de seguridad. La rama NO se eliminará porque podría contener trabajo importante. Verifica manualmente:
```bash
git log Main..nombre-rama
```

## Ejemplos de Uso

### Ejemplo 1: Limpieza Conservadora

Eliminar solo ramas muy antiguas (30+ días):

```bash
./scripts/cleanup-branches.sh --days 30 --force
```

### Ejemplo 2: Limpieza con Exclusión Temporal

Proteger temporalmente ramas experimentales:

```bash
./scripts/cleanup-branches.sh --exclude "experiment/*" --force
```

### Ejemplo 3: Verificación Antes de Limpieza Masiva

```bash
# 1. Ver qué se eliminaría
./scripts/cleanup-branches.sh --dry-run > cleanup-plan.txt

# 2. Revisar el plan
cat cleanup-plan.txt

# 3. Ejecutar limpieza
./scripts/cleanup-branches.sh --force
```

### Ejemplo 4: Limpieza Gradual

```bash
# Primero ramas muy antiguas
./scripts/cleanup-branches.sh --days 60 --force

# Luego ramas de 30+ días
./scripts/cleanup-branches.sh --days 30 --force

# Finalmente ramas de 14+ días
./scripts/cleanup-branches.sh --days 14 --force
```

### Ejemplo 5: Limpieza Solo de Copilot Branches

```bash
# Ver ramas copilot mergeadas
git branch -r --merged Main | grep copilot

# Usar el script (las ramas copilot no están protegidas por defecto)
./scripts/cleanup-branches.sh --dry-run
```

## FAQ

### ¿Con qué frecuencia debo ejecutar la limpieza?

**Recomendación**: El workflow automático (semanal) es suficiente para la mayoría de proyectos. Ejecuta manualmente si:
- Acabas de mergear muchas ramas
- Necesitas reducir el número de ramas urgentemente
- Estás preparando una release

### ¿Puedo recuperar una rama eliminada?

**Sí**, durante ~90 días:

```bash
# Ver historial de ramas eliminadas
git reflog

# Encontrar el SHA del último commit de la rama
git reflog show origin/nombre-rama

# Recrear la rama
git checkout -b nombre-rama <SHA>
git push origin nombre-rama
```

**Nota**: Después de ~90 días, los commits huérfanos son eliminados por el garbage collector de Git.

### ¿El script elimina ramas locales?

**No por defecto**. El script solo elimina ramas remotas (`origin/*`). Para eliminar locales también:

```bash
# Primero ejecuta el script remoto
./scripts/cleanup-branches.sh --force

# Luego limpia locales
git fetch --prune
git branch -vv | grep ': gone]' | awk '{print $1}' | xargs git branch -d
```

### ¿Puedo modificar las ramas protegidas sin editar el código?

**Sí**, usa el archivo de exclusión:

```bash
# Editar lista de exclusión
vim .github/branch-cleanup-exclude.txt

# Agregar rama
echo "mi-rama-especial" >> .github/branch-cleanup-exclude.txt

# Commit
git add .github/branch-cleanup-exclude.txt
git commit -m "Proteger rama especial de limpieza"
```

### ¿Qué pasa si el workflow falla?

El workflow es **idempotente** y **seguro**:

- ❌ Si falla, no se eliminan ramas
- ✅ Puedes re-ejecutarlo sin problemas
- 📧 Recibirás notificación de fallo en GitHub Actions
- 📋 Los logs completos están disponibles en la pestaña Actions

### ¿Cómo veo el historial de limpiezas?

```bash
# Ver issues de limpieza
gh issue list --label cleanup,automated

# Ver ejecuciones del workflow
gh run list --workflow=branch-cleanup.yml

# Ver detalles de una ejecución
gh run view <run-id>
```

### ¿El script afecta a otros repositorios?

**No**. El script solo opera en el repositorio actual. Es completamente seguro ejecutarlo.

### ¿Puedo usar este script en otros proyectos?

**¡Sí!** El script es genérico y portable. Solo copia:

1. `scripts/cleanup-branches.sh`
2. `.github/workflows/branch-cleanup.yml`
3. `.github/branch-cleanup-exclude.txt`

Ajusta `PROTECTED_BRANCHES` según tu proyecto.

## Métricas y Monitoreo

### Ver Estadísticas

```bash
# Número de ramas remotas
git branch -r | wc -l

# Ramas mergeadas a Main
git branch -r --merged origin/Main | wc -l

# Ramas no mergeadas
git branch -r --no-merged origin/Main | wc -l
```

### Reporte Mensual

El workflow crea issues automáticos con métricas:
- Número de ramas eliminadas
- Fecha de último merge
- Lista completa de ramas procesadas

Filtra por label `cleanup` en la pestaña Issues.

## Referencias

- [Git Branch Documentation](https://git-scm.com/docs/git-branch)
- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Branch Protection Rules](./BRANCH_PROTECTION.md)

## Soporte

Si tienes problemas o preguntas:

1. 📖 Revisa esta documentación
2. 🐛 Busca en [Issues existentes](https://github.com/Melampe001/TokyoApps-Multispace-IA/issues)
3. 💬 Crea un nuevo issue con el label `question`

---

**Última actualización**: 2025-12-27  
**Versión del sistema**: 1.0.0
