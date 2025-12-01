# Guía de Colaboración - Tokyo-IA

Este documento describe las mejores prácticas y flujos de trabajo para colaborar en el proyecto Tokyo-IA.

## Índice

1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Flujo de Ramas](#flujo-de-ramas)
3. [Convenciones de Código](#convenciones-de-código)
4. [Proceso de Revisión](#proceso-de-revisión)
5. [Automatización y CI](#automatización-y-ci)

## Estructura del Proyecto

```
tokyoia/
├── cmd/                    # Puntos de entrada de Go
│   ├── main.go            # Aplicación principal
│   └── tokyoia.go         # Entrada para Tokyo-IA
├── internal/              # Paquetes internos de Go
│   └── ai/               # Módulo de IA
├── lib/                   # Bibliotecas compartidas
├── ruby/                  # Código Ruby
│   └── lib/tokyoia/      # Módulo core de Ruby
├── proto/                 # Definiciones Protocol Buffers
├── testing/               # Tests del proyecto
├── docs/                  # Documentación
├── config/                # Configuraciones
├── giphu/                 # Flujos de trabajo y ejemplos
└── .github/workflows/     # CI/CD GitHub Actions
```

## Flujo de Ramas

### Ramas Principales

- **main**: Rama de producción. Solo código probado y revisado.
- **develop**: Rama de desarrollo. Integración de features.

### Ramas de Trabajo

- **feature/nombre-feature**: Para nuevas funcionalidades
- **fix/nombre-bug**: Para corrección de errores
- **docs/nombre-doc**: Para cambios en documentación

### Proceso de Merge

1. Crear rama desde `develop`
2. Desarrollar y hacer commits frecuentes
3. Abrir Pull Request hacia `develop`
4. Esperar revisión y aprobación
5. Merge cuando CI pase y haya aprobación

## Convenciones de Código

### Go

- Usar `go fmt` antes de cada commit
- Seguir las convenciones de Go
- Documentar funciones públicas
- Nombres descriptivos en camelCase

### Ruby

- Usar RuboCop para estilo
- Seguir guía de estilo Ruby
- Documentar con YARD
- Nombres en snake_case

### Protocol Buffers

- Documentar cada mensaje y servicio
- Usar nombres descriptivos
- Mantener compatibilidad hacia atrás

## Proceso de Revisión

### Checklist de PR

- [ ] Código formateado correctamente
- [ ] Tests agregados o actualizados
- [ ] Documentación actualizada si es necesario
- [ ] CI pasa exitosamente
- [ ] Sin conflictos de merge

### Criterios de Aprobación

- Al menos 1 revisión aprobada
- CI pasando
- Sin comentarios pendientes

## Automatización y CI

### GitHub Actions

El flujo de CI (`.github/workflows/main.yml`) ejecuta:

1. **Format check**: Verifica formato de código
2. **Tests**: Ejecuta suite de tests
3. **Build**: Compila el proyecto

### Comandos Make

```bash
make fmt      # Formatear código
make test     # Ejecutar tests
make build    # Compilar proyecto
make ci       # Ejecutar flujo CI completo
make proto    # Generar código desde .proto
```

## Incorporación de Nuevos Colaboradores

1. Clonar el repositorio
2. Revisar esta guía y `README.md`
3. Configurar entorno de desarrollo
4. Ejecutar `make test` para verificar setup
5. Crear rama feature para primera contribución

## Contacto

Para preguntas o sugerencias, abrir un Issue en el repositorio.
