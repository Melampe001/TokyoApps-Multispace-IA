# Estructura en formato árbol

```
repo-root/
├── cmd/                # Puntos de entrada principales y ejecutables del servicio
├── internal/           # Lógica relacionada con interacciones internas o servicios
├── lib/                # Paquetes principales de Go para la lógica de billing
├── admin/              # Componentes de la interfaz de administración
├── config/             # Configuración y plantillas
├── docs/               # Documentación técnica, guías, manuales
├── proto/              # Definiciones de protocol buffers. Ejecuta `make proto` tras cambios.
├── ruby/               # Implementación en Ruby
│   └── lib/
│       └── tokyoia/
│           └── core.rb   # Módulo principal de Tokyo-IA en Ruby
├── testing/            # Helpers y fixtures de pruebas
├── Makefile            # Automatización de build, test, fmt, ci, proto, etc.
└── README.md           # Información principal del repositorio
```

---

## Notas sobre la estructura

- **cmd/**: Ejecutables principales del proyecto, cada entrada debe tener su propio subdirectorio.
- **internal/**: Código privado de la aplicación.
- **lib/**: Lógica fundamental del dominio, reutilizable y testeada.
- **admin/**: Código de la administración/panel o interfaces internas web.
- **config/**: YAML, plantillas o configuraciones para despliegue, CI/CD, etc.
- **docs/**: Documentos, tutoriales, diagramas, información para usuarios y desarrolladores.
- **proto/**: Archivos .proto de Protobuf, generar fuentes después de cambios.
- **ruby/**: Lógica o wrappers en Ruby, sincronizar con versión en archivo `VERSION` en la raíz del proyecto.
- **testing/**: Utilidades y datos de test.
- **Makefile**: Automatización de tareas (compilación, pruebas, formato…).
- **README.md**: Siempre actualizado para reflejar los componentes y buenas prácticas.

---

## Recordatorios de configuración

- Corre `make fmt` antes de cada commit para asegurar el formato de código.
- Corre `make build` para generar los binarios principales.
- Usa `make test` para ejecutar los tests automatizados.
- El flujo completo lo ejecuta `make ci`.
- Cambios en `proto/` requieren regenerar los artefactos con `make proto`.
- Cambios en `ruby/` y control de versiones se gestionan desde el archivo `VERSION` en la raíz del proyecto.