# Ejemplo de Flujo de Trabajo: Nueva Feature

Este documento describe el flujo de trabajo para implementar una nueva funcionalidad en Tokyo-IA.

## Pasos

### 1. Planificación

- [ ] Definir requisitos de la feature
- [ ] Identificar componentes afectados
- [ ] Estimar tiempo de desarrollo

### 2. Desarrollo

```bash
# Crear rama de feature
git checkout develop
git pull origin develop
git checkout -b feature/mi-nueva-feature

# Hacer cambios y commits
git add .
git commit -m "feat: descripción del cambio"
```

### 3. Testing

```bash
# Ejecutar tests localmente
make test

# Verificar formato
make fmt
```

### 4. Pull Request

- Crear PR hacia `develop`
- Completar template de PR
- Solicitar revisión

### 5. Merge

- Esperar aprobación
- Verificar CI
- Hacer merge

## Notas

- Mantener commits atómicos
- Documentar cambios significativos
- Actualizar tests según sea necesario
