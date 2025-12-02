# Tokyo-IA

Tokyo-IA is a mobile + web + server project that provides Tokyo-themed AI features and an MCP server.

## Repository Structure

- **tokyoia/**
    - **app/** - Android main project
    - **web/** - Website + admin panel
    - **server-mcp/** - Node server for MCP
    - **whatsnew/** - Play Store release notes
    - **.github/** - Workflows and issue templates
    - **scripts/** - Automation scripts
    - **docs/** - Project documentation

## Makefile Commands

- `make build` – Compila el binario principal de Go (`cmd/main.go`)
- `make test` – Ejecuta los tests de Go
- `make fmt` – Formatea el código Go y, si está presente un proyecto Ruby, ejecuta `rubocop`
- `make clean` – Elimina archivos binarios generados
- `make ci` – Corre las tareas de `fmt` y `test` juntas (flujo de integración continua)
- `make proto` – Si existe la carpeta `proto/`, genera código Go y Ruby a partir de archivos `.proto`

## Quick Start

- **Android (local debug):**
    - `./gradlew assembleDebug`
    - `./gradlew installDebug`
- **Web (dev):**
    - `cd web && npm install && npm run dev`
- **Server (local):**
    - `cd server-mcp && npm install && npm start`
- **Go backend (core tasks):**
    - `make build`
    - `make test`
    - `make fmt`
    - `make ci`
    - `make proto`

## Development Flow

1. Usa `make fmt` antes de hacer commit para mantener el formato del código.
2. Corre `make test` para asegurar que todo pase localmente.
3. Usa `make ci` para una verificación completa (incluye build, lint y tests).
4. Si modificas archivos en `proto/`, corre `make proto` para actualizar el código generado.
5. Para carpetas específicas revisa el árbol mostrado arriba y/o la documentación en `/docs`.

## Security / Secrets (IMPORTANT)

No almacenes credenciales, llaveros o secretos directamente en el repositorio.
- Usa [GitHub Actions Secrets](https://docs.github.com/actions/security-guides/encrypted-secrets) para CI.
- Si un secreto es expuesto: róta la credencial, elimina el secreto y notifica al equipo.

## Release Notes

- `whatsnew/en-US/whatsnew.txt`
- `whatsnew/es-MX/whatsnew.txt`

## Contributing

Consulta `docs/CONTRIBUTING.md` y abre issues/PRs para sugerencias o cambios.

## License

Consulta el archivo `LICENSE`.