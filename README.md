# Tokyo-IA

## 🚀 CI/CD & Pull Request Automation

Este proyecto utiliza un sistema avanzado de validación automática para Pull Requests.

### PR Super Agents Workflow

Cada Pull Request activa automáticamente el workflow **PR Super Agents** que incluye:

- ✅ **Linting multi-lenguaje**: Go, Python, Dart, Shell
- ✅ **Tests automáticos**: Ejecuta `make ci` con cobertura
- ✅ **Escaneo de seguridad**: Trivy, Gosec, Bandit
- ✅ **Validación de commits**: Conventional Commits
- ✅ **Validación de docs**: Alerta si falta documentación
- ✅ **Alerta de dependencias**: Monitorea cambios en go.mod, requirements.txt, etc.
- ✅ **ReviewDog**: Sugerencias automáticas de revisión

**Documentación completa**: Ver [docs/pr-super-agents-workflow.md](docs/pr-super-agents-workflow.md)

### Para Desarrolladores

```bash
# Crea un PR con conventional commit
git commit -m "feat: Add nueva funcionalidad"
git push origin mi-rama

# El workflow se ejecuta automáticamente
# Revisa los checks en la pestaña "Checks" del PR
```

## 🛠️ Build & Test

```bash
# Formatear código
make fmt

# Ejecutar tests
make test

# Build completo
make build

# CI (fmt + test)
make ci
```
