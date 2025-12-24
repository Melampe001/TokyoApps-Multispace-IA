# Imperial Cleaner Workflow

## 🏰 Overview

El **Imperial Cleaner** es un workflow automatizado de GitHub Actions que implementa gestión de Pull Requests de nivel empresarial premium. Proporciona limpieza automática, fusión inteligente y auditoría completa siguiendo las mejores prácticas de seguridad y trazabilidad.

## 📋 Características Principales

### 1. Cierre Automático de PRs

El workflow cierra automáticamente PRs que cumplen cualquiera de estos criterios:

- **PRs en Draft**: Pull requests marcados como borrador que no están listos para revisión
- **PRs con Etiquetas Específicas**: 
  - `stale` - PRs obsoletos
  - `wontfix` - PRs que no serán implementados
  - `legacy` - PRs relacionados con código antiguo
- **PRs Inactivos**: PRs sin actividad por más de 72 horas

### 2. Fusión Automática

El workflow fusiona automáticamente PRs que cumplen **TODOS** estos requisitos:

- ✅ Todos los checks de CI/CD pasaron exitosamente
- ✅ No está en estado draft
- ✅ No proviene de Dependabot (requiere revisión manual)
- ✅ No tiene conflictos de merge
- ✅ Estado de merge es `clean`, `unstable` o `has_hooks`

### 3. Gestión de Dependabot

Los PRs creados por Dependabot reciben tratamiento especial:

- Se etiquetan automáticamente con `elite-review`
- Requieren revisión manual antes de fusión
- Reciben un comentario de auditoría explicando los pasos necesarios

### 4. Auditoría Completa

Cada acción automatizada incluye:

- **Comentarios de auditoría** con información detallada
- **Timestamps** de todas las operaciones
- **Run ID** del workflow para trazabilidad
- **Razones específicas** para cada acción tomada

## 🚀 Uso

### Ejecución Automática

El workflow se ejecuta automáticamente **2 veces al día**:
- 6:00 AM UTC
- 6:00 PM UTC

### Ejecución Manual

Puedes ejecutar el workflow manualmente desde GitHub:

1. Ve a la pestaña **Actions** del repositorio
2. Selecciona **Imperial Cleaner - PR Management**
3. Haz clic en **Run workflow**
4. Opcionalmente, activa **Dry Run Mode** para simular sin hacer cambios reales

#### Dry Run Mode

El modo de prueba (`dry_run: true`) permite:
- Ver qué acciones se tomarían sin ejecutarlas
- Validar la configuración
- Revisar logs sin afectar PRs reales

## 🔒 Seguridad y Permisos

### Permisos Mínimos

El workflow sigue el principio de **menor privilegio**:

```yaml
permissions:
  contents: write        # Para merge de PRs
  pull-requests: write   # Para cerrar, etiquetar y comentar
  issues: write          # Para gestionar etiquetas
```

### Controles de Seguridad

- ✅ Validación de estados antes de acciones destructivas
- ✅ Manejo robusto de errores
- ✅ Logs detallados de todas las operaciones
- ✅ Trazabilidad completa mediante audit trails

## 📊 Estructura del Workflow

El workflow consta de 5 jobs independientes:

### 1. `analyze-prs`
Analiza todos los PRs abiertos y determina qué acciones tomar. Genera salidas para los siguientes jobs.

### 2. `manage-dependabot`
Gestiona PRs de Dependabot etiquetándolos para revisión manual elite.

### 3. `close-prs`
Cierra PRs obsoletos o no deseados con comentarios de auditoría completos.

### 4. `merge-prs`
Fusiona automáticamente PRs que cumplen todos los criterios de calidad.

### 5. `summary`
Genera un resumen ejecutivo visible en la UI de GitHub Actions.

## 📝 Ejemplos de Comentarios de Auditoría

### Cierre de PR

```markdown
🔒 **Imperial Cleaner - Automatic Closure**

This Pull Request has been automatically closed by the Imperial Cleaner workflow.

**Closure Reason:**
Inactive for 80 hours (>72h threshold)

**Statistics:**
- Last activity: 80 hours ago
- Closure threshold: 72 hours of inactivity

**Next Steps:**
If you believe this closure was inappropriate, you can:
1. Reopen this PR if you're ready to continue work
2. Contact the repository maintainers for assistance
3. Create a new PR with updated changes

**Audit Trail:**
- Timestamp: 2025-12-24T11:26:56.461Z
- Workflow: Imperial Cleaner - PR Management
- Run ID: 12345678
- Triggered by: schedule
```

### Fusión de PR

```markdown
🚀 **Imperial Cleaner - Automatic Merge**

This Pull Request has been automatically merged by the Imperial Cleaner workflow.

**Merge Criteria Met:**
- ✅ All CI/CD checks passed
- ✅ Not in draft state
- ✅ Not from Dependabot (requires manual review)
- ✅ No merge conflicts
- ✅ All required reviews approved

**Audit Trail:**
- Timestamp: 2025-12-24T11:26:56.461Z
- Commit SHA: abc123def456
- Workflow: Imperial Cleaner - PR Management
- Run ID: 12345678
- Triggered by: schedule
```

## 🔧 Configuración

### Ajustar Umbral de Inactividad

Para cambiar el umbral de 72 horas, edita esta línea en el workflow:

```javascript
const INACTIVE_THRESHOLD_MS = 72 * 60 * 60 * 1000; // 72 horas
```

### Modificar Etiquetas de Cierre

Para cambiar las etiquetas que activan el cierre automático:

```javascript
const closeLabels = ['stale', 'wontfix', 'legacy'];
```

### Cambiar Frecuencia de Ejecución

Para modificar el schedule:

```yaml
schedule:
  - cron: '0 6,18 * * *'  # Formato: minuto hora día mes día_semana
```

## 📈 Monitoreo

### Ver Resultados

1. Ve a **Actions** > **Imperial Cleaner - PR Management**
2. Selecciona una ejecución reciente
3. Revisa el **Summary** para ver estadísticas
4. Explora los logs de cada job para detalles

### Métricas Clave

El workflow genera métricas sobre:
- Número de PRs cerrados
- Número de PRs fusionados
- Número de PRs de Dependabot etiquetados
- Estado de cada job (success/failure)

## 🐛 Solución de Problemas

### El workflow no cierra PRs esperados

**Posibles causas:**
- El PR no cumple exactamente los criterios de cierre
- El PR tiene actividad reciente (<72h)
- Estás en modo Dry Run

**Solución:** Revisa los logs del job `analyze-prs` para ver por qué no se seleccionó el PR.

### El workflow no fusiona PRs listos

**Posibles causas:**
- Algún check de CI/CD falló recientemente
- Hay conflictos de merge no detectados
- Branch protection rules requieren aprobaciones adicionales
- El PR es de Dependabot (requiere revisión manual)

**Solución:** Revisa los logs del job `merge-prs` y el comentario de error en el PR.

### Error de permisos

**Causa:** El token de GitHub no tiene permisos suficientes.

**Solución:** Verifica que los permisos del workflow estén correctamente configurados en el archivo YAML.

## 🤝 Mejores Prácticas

1. **Usar etiquetas consistentemente**: Aplica etiquetas como `stale`, `wontfix`, `legacy` cuando sea apropiado
2. **Revisar logs regularmente**: Monitorea las ejecuciones del workflow para identificar patrones
3. **Ajustar umbrales**: Adapta el umbral de inactividad según las necesidades del proyecto
4. **Probar en dry-run**: Antes de cambios importantes, ejecuta en modo dry-run
5. **Mantener PRs activos**: Comenta o actualiza PRs regularmente para evitar cierre automático

## 📚 Recursos Adicionales

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub REST API - Pull Requests](https://docs.github.com/en/rest/pulls)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## 🆘 Soporte

Si encuentras problemas o tienes preguntas:

1. Revisa los logs del workflow en la pestaña Actions
2. Consulta la documentación del proyecto
3. Abre un issue en el repositorio con:
   - Descripción del problema
   - Run ID del workflow
   - Logs relevantes

---

**Imperial Cleaner** - Gestión de PRs de nivel empresarial premium
