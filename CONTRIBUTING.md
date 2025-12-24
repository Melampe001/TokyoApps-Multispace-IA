# Guías para Contribuir

Bienvenido a las guías de contribución para el proyecto Tokyo-IA. Agradecemos tu interés en contribuir. A continuación se presentan las pautas que debes seguir para unirte a nuestro equipo de desarrollo.

## Automatización Total

Estamos comprometidos con la automatización en el desarrollo. Utilizamos agentes/bots y CI para mantener nuestro código limpio y funcional. Asegúrate de seguir estas pautas:

### Comandos Obligatorios
- **`make fmt`**: Formatea el código según nuestras convenciones.
- **`make test`**: Ejecuta los tests para asegurar que todo funcione como se espera.
- **`make ci`**: Comprueba si todo está en orden para la integración continua.
- **`make proto`**: Genera los archivos relacionados con Proto, si aplica.

### No Subir Secretos
Es fundamental que no subas secretos al repositorio. Para ello, utilizamos validaciones en CI/bots que lo aseguran.

### Testing Automatizado
Realizamos testing automatizado, el cual incluye tests unitarios y de integración donde sea aplicable. Se requiere una cobertura mínima de tests del **80%** de líneas ejecutadas, medida con `go test ./... -cover`. Los PR que hagan que la cobertura global baje por debajo de este umbral deberán incluir tests adicionales antes de ser aprobados y la CI marcará como fallo cualquier ejecución por debajo de dicho umbral. Asegúrate de que tu código esté suficientemente cubierto antes de enviar un PR.

### Flujos de Trabajo
El flujo de trabajo para PR/issues debe alinearse a las plantillas establecidas. Usamos bots para automatizar procesos como asignación de revisores y lanzamientos automáticos.

### Agentes/Bots Utilizados
Utilizamos agentes/bots para:
- Formateo
- Testing
- Generación de artefactos
- Versionado
- Documentación

Además, alentamos a los contribuidores a proponer y agregar más automatizaciones en áreas manuales.

### Ejemplo de Estructura de PR
En un PR deberías asegurarte de incluir:
- Descripción clara del cambio.
- Referencia a tickets/issues.
- Checklist de los checks automáticos que se deben cumplir.

### Agentes de IA/Coding Agents
Usamos agentes de IA/coding agents para facilitar procedimientos repetitivos. Puedes ampliar su uso en tus contribuciones.

### Reglas para Carpetas
- **cmd/**: Código de entrada
- **internal/**: Código interno del proyecto
- **lib/**: Librerías generales
- **admin/**: Archivos administrativos
- **config/**: Archivos de configuración
- **docs/**: Documentación adicional
- **proto/**: Archivos Proto
- **ruby/**: Código en Ruby
- **testing/**: Tests
- **web/**: Código web
- **app/**: Aplicaciones
- **server-mcp/**: Código de servidores MCP
- **scripts/**: Scripts automáticos

### Enlaces Relevantes
- [LICENSE](LICENSE)
- [README.md](README.md)
- [docs/](docs/)

Gracias por contribuir a Tokyo-IA!  
Esperamos tus mejoras y muy buena suerte!