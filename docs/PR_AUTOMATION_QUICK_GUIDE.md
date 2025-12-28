# 🚀 Guía Rápida - Automatización de PRs

## Para Desarrolladores

### Al abrir un PR

✅ **No hagas nada** - El sistema funciona automáticamente:

1. Se añaden labels de tamaño, tipo y lenguaje
2. Se asigna prioridad automáticamente
3. Se asignan reviewers según archivos cambiados
4. Recibes un comentario de bienvenida con el resumen

### Comandos Disponibles

Comenta en tu PR para usar estos comandos:

```bash
/merge              # Mergear inmediatamente (requiere permisos)
/ready              # Marcar como listo para review
/retest             # Re-ejecutar tests
/priority P1        # Cambiar prioridad (P0, P1, P2, P3)
/duplicate #123     # Marcar como duplicado
/assign @usuario    # Asignar reviewer específico
```

### Fast-Track para Merge Rápido

Tu PR se mergeará **inmediatamente** si es:

- ✅ Solo documentación (<500 líneas)
- ✅ Fixes de linter (<100 líneas, título con "lint"/"format")
- ✅ Update de dependencias (dependabot)
- ✅ Cambios pequeños de Copilot (documentación, size/S)

Para otros PRs:
- ⏱️ Espera **1 hora** después de pasar todos los checks
- 💬 El bot te avisará cuando esté listo

### Labels que verás

**Tamaño:**
- `size/XS` (0-10 líneas)
- `size/S` (11-100 líneas)
- `size/M` (101-500 líneas)
- `size/L` (501-1000 líneas)
- `size/XL` (1001-5000 líneas)
- `size/XXL` (5000+ líneas) ⚠️ El bot recomendará dividir

**Tipo:**
- `type/documentation` - Archivos .md
- `type/tests` - Archivos de test
- `type/ci-cd` - Workflows de GitHub
- `type/agents` - Código de agentes
- `type/infrastructure` - Terraform, K8s

**Lenguaje:**
- `lang/go`, `lang/python`, `lang/javascript`, `lang/kotlin`, `lang/shell`

**Prioridad:**
- `priority/P0` 🔴 Critical (hotfix, security)
- `priority/P1` 🟠 High (bugs, fixes importantes)
- `priority/P2` 🟡 Normal (features)
- `priority/P3` 🟢 Low (documentación)

## Para Maintainers

### Dashboard de PRs

Filtra PRs por labels:

```
# Ver PRs críticos
label:priority/P0

# Ver PRs pequeños listos para merge rápido
label:size/XS label:size/S

# Ver PRs obsoletos que necesitan atención
label:stale

# Ver PRs duplicados
label:duplicate

# Ver PRs con conflictos
label:merge-conflict
```

### Workflows Activos

| Workflow | Frecuencia | Propósito |
|----------|------------|-----------|
| **pr-auto-labeler** | En cada cambio de PR | Etiquetar automáticamente |
| **pr-triage** | Al abrir PR | Priorizar y asignar |
| **pr-auto-merger** | Cada 30 min | Mergear PRs listos |
| **pr-cleanup** | Diario 2 AM | Limpiar PRs obsoletos |
| **pr-bot-commands** | Al comentar | Ejecutar comandos |

### Ejecutar Manualmente

1. Ve a **Actions** en GitHub
2. Selecciona el workflow
3. Click en **Run workflow**
4. Elige la branch (usualmente `main`)

### Reportes Diarios

Cada día a las 2 AM se genera un issue con:

- 📊 PRs marcados como stale
- 📊 PRs cerrados automáticamente
- 📊 Duplicados detectados
- 📊 Conflictos encontrados
- 🔗 Links a todos los candidatos

Busca issues con label `cleanup-report`.

## Configuración

### Modificar Comportamiento

Edita `.github/pr-automation-config.yml` para:

```yaml
# Cambiar umbrales de tamaño
auto_labels:
  size:
    - label: "size/S"
      max_lines: 150  # Aumentar límite

# Añadir reglas de fast-track
auto_merge:
  fast_track:
    - name: "Mi regla"
      conditions:
        - only_paths: ["config/**"]
        - max_lines: 100
      merge_method: "squash"

# Ajustar días de inactividad
cleanup:
  stale_pr:
    days_inactive: 45  # Aumentar de 30 a 45
```

### Añadir Reviewers

```yaml
triage:
  auto_assign:
    by_area:
      - paths: ["frontend/**"]
        reviewers: ["frontend-team"]
      - paths: ["backend/**"]
        reviewers: ["backend-team"]
```

## Troubleshooting

### El bot no responde a comandos

✅ Verifica que comentaste en un **Pull Request**, no en un Issue  
✅ Verifica que el comando empiece con `/` (ej: `/merge`)  
✅ Revisa los logs en Actions > pr-bot-commands

### PR no se mergea automáticamente

✅ Verifica que todos los checks hayan pasado  
✅ Verifica que tenga reviews aprobados necesarios  
✅ Verifica que no tenga conflictos de merge  
✅ Verifica que no sea draft  
✅ Espera 1 hora desde que cumplió requisitos (o usa `/merge`)

### Labels no se aplican

✅ Verifica que el workflow haya ejecutado en Actions  
✅ Revisa los logs en pr-auto-labeler  
✅ Verifica que las labels existan en el repositorio

### PRs marcados como stale incorrectamente

✅ Añade label `wip`, `blocked`, o `on-hold` para excluir  
✅ Ajusta `days_inactive` en la configuración  
✅ Actualiza el PR para quitar label `stale`

## FAQ

**P: ¿Puedo deshabilitar un workflow?**  
R: Sí, renombra el archivo o añade `if: false` al job.

**P: ¿Cómo evito que mi PR se cierre automáticamente?**  
R: Añade label `wip`, `blocked` o `on-hold`, o actualiza el PR cada 30 días.

**P: ¿Puedo personalizar el comentario de bienvenida?**  
R: Sí, edita `bot.auto_comments.welcome_message` en la configuración.

**P: ¿Los workflows consumen muchos minutos de Actions?**  
R: No, son muy eficientes. ~5 minutos/día para 50 PRs.

**P: ¿Funcionan con forks?**  
R: Sí, pero los comandos requieren permisos de write en el repo.

## Links Útiles

- 📖 [Documentación Completa](PR_AUTOMATION.md)
- ⚙️ [Configuración](../.github/pr-automation-config.yml)
- 🔧 [Workflows](../.github/workflows/)
- 🐛 [Reportar Issues](https://github.com/Melampe001/TokyoApps-Multispace-IA/issues/new?labels=automation)

---

**¿Necesitas ayuda?** Contacta a @Melampe001 o el equipo de DevOps.
