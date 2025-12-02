#!/bin/bash
set -euo pipefail
ROOT_DIR="$(pwd)"
README_FILES=$(find . -iname "README.md" | grep -v "^./README.md" || true)
UNIFIED_README="$ROOT_DIR/README.md"
echo -e "# Tokyo-IA (Unificado)\n" > "$UNIFIED_README"
cat >> "$UNIFIED_README" <<EOF
Este repositorio integra y organiza los proyectos:

- **core/**: Lógica principal Go/Ruby (de Tokyo-IA)
- **scripts/**: Utilidades y RNG de ruleta (de Tokyo-Apps-IA)
- **apps/**: Componentes experimentales (de bug-free-octo-winner-Tokyo-IA2)

A continuación, encontrarás los README.md originales de cada componente para consulta histórica y unificación:
---
EOF
for file in $README_FILES; do
    echo -e "\n\n---\n## Contenido de $file\n" >> "$UNIFIED_README"
    cat "$file" >> "$UNIFIED_README"
done
echo -e "\n✅ README.md unificado generado en: $UNIFIED_README"