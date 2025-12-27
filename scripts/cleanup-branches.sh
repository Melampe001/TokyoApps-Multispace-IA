#!/bin/bash

# 🧹 Branch Cleanup Script
# Automatically clean up merged branches while protecting important branches

set -euo pipefail

# Configuration
PROTECTED_BRANCHES=(
  "Main"
  "Prompt"
  "main"
  "develop"
  "mela"
)

PROTECTED_PATTERNS=(
  "feature/*"
  "hotfix/*"
  "release/*"
)

# Default values
DRY_RUN=true
DAYS_THRESHOLD=0
FORCE=false
ADDITIONAL_EXCLUDES=()
EXCLUDE_FILE=".github/branch-cleanup-exclude.txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Usage function
usage() {
  cat << EOF
🧹 Branch Cleanup Script - Limpieza automática de ramas mergeadas

Usage: $0 [OPTIONS]

OPTIONS:
  --dry-run           Solo listar ramas, no eliminar (default)
  --force             Eliminar ramas sin confirmación (DESTRUCTIVO)
  --days N            Solo eliminar ramas mergeadas hace más de N días
  --exclude PATTERN   Agregar patrón de exclusión adicional
  -h, --help          Mostrar esta ayuda

EXAMPLES:
  # Listar ramas que serían eliminadas
  $0 --dry-run

  # Eliminar ramas mergeadas hace más de 7 días
  $0 --days 7 --force

  # Eliminar todas las ramas mergeadas con confirmación
  $0 --force

  # Excluir patrón adicional
  $0 --exclude "experiment/*" --force

EOF
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --force)
      FORCE=true
      DRY_RUN=false
      shift
      ;;
    --days)
      DAYS_THRESHOLD="$2"
      shift 2
      ;;
    --exclude)
      ADDITIONAL_EXCLUDES+=("$2")
      shift 2
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo -e "${RED}Error: Opción desconocida: $1${NC}"
      usage
      ;;
  esac
done

# Print header
print_header() {
  echo ""
  echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
  echo -e "${BLUE}║   🧹 Limpieza Automática de Ramas - TokyoApps-IA         ║${NC}"
  echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
  echo ""
}

# Log function
log_info() {
  echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
  echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
  echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
  echo -e "${RED}✗${NC} $1"
}

# Detect base branch
detect_base_branch() {
  # First check local branches
  if git show-ref --verify --quiet refs/heads/Main; then
    echo "Main"
  elif git show-ref --verify --quiet refs/heads/main; then
    echo "main"
  # Then check remote branches
  elif git show-ref --verify --quiet refs/remotes/origin/Main; then
    echo "Main"
  elif git show-ref --verify --quiet refs/remotes/origin/main; then
    echo "main"
  else
    log_error "No se encontró rama base (Main o main) en local ni en remoto"
    exit 1
  fi
}

# Check if branch is protected
is_protected_branch() {
  local branch=$1
  
  # Check exact matches
  for protected in "${PROTECTED_BRANCHES[@]}"; do
    if [[ "$branch" == "$protected" ]]; then
      return 0
    fi
  done
  
  # Check patterns
  for pattern in "${PROTECTED_PATTERNS[@]}" "${ADDITIONAL_EXCLUDES[@]}"; do
    # Convert glob pattern to regex
    pattern_regex="${pattern//\*/.*}"
    if [[ "$branch" =~ ^${pattern_regex}$ ]]; then
      return 0
    fi
  done
  
  # Check exclude file
  if [[ -f "$EXCLUDE_FILE" ]]; then
    while IFS= read -r line; do
      # Skip comments and empty lines
      [[ "$line" =~ ^#.*$ ]] && continue
      [[ -z "$line" ]] && continue
      
      if [[ "$branch" == "$line" ]]; then
        return 0
      fi
    done < "$EXCLUDE_FILE"
  fi
  
  return 1
}

# Get merge date of a branch
get_merge_date() {
  local branch=$1
  local base_branch=$2
  
  # Get the last commit date on this branch
  git log -1 --format=%ct "$branch" 2>/dev/null || echo "0"
}

# Check if branch is old enough
is_old_enough() {
  local branch=$1
  local base_branch=$2
  
  if [[ $DAYS_THRESHOLD -eq 0 ]]; then
    return 0
  fi
  
  local merge_timestamp
  merge_timestamp=$(get_merge_date "$branch" "$base_branch")
  
  if [[ $merge_timestamp -eq 0 ]]; then
    return 1
  fi
  
  local current_timestamp
  current_timestamp=$(date +%s)
  local age_days=$(( (current_timestamp - merge_timestamp) / 86400 ))
  
  if [[ $age_days -ge $DAYS_THRESHOLD ]]; then
    return 0
  fi
  
  return 1
}

# Main cleanup logic
cleanup_branches() {
  print_header
  
  # Detect base branch
  local base_branch
  base_branch=$(detect_base_branch)
  log_info "Rama base detectada: ${GREEN}$base_branch${NC}"
  
  # Update remote refs
  log_info "Actualizando referencias remotas..."
  git fetch --prune origin >/dev/null 2>&1 || log_warning "No se pudo actualizar referencias remotas"
  
  # Get merged branches
  log_info "Analizando ramas mergeadas a $base_branch..."
  
  local merged_branches=()
  while IFS= read -r branch; do
    # Remove leading/trailing whitespace and remote prefix
    branch=$(echo "$branch" | sed 's/^[* ] //' | sed 's/remotes\/origin\///')
    
    # Skip base branch
    [[ "$branch" == "$base_branch" ]] && continue
    
    merged_branches+=("$branch")
  done < <(git branch -r --merged "origin/$base_branch" 2>/dev/null | grep -v "HEAD")
  
  echo ""
  log_info "Total de ramas encontradas: ${YELLOW}${#merged_branches[@]}${NC}"
  
  # Filter branches
  local branches_to_delete=()
  local protected_count=0
  local too_recent_count=0
  
  for branch in "${merged_branches[@]}"; do
    if is_protected_branch "$branch"; then
      ((protected_count++))
      continue
    fi
    
    if ! is_old_enough "$branch" "$base_branch"; then
      ((too_recent_count++))
      continue
    fi
    
    branches_to_delete+=("$branch")
  done
  
  # Print statistics
  echo ""
  log_info "Ramas protegidas (no se eliminarán): ${GREEN}$protected_count${NC}"
  
  if [[ $DAYS_THRESHOLD -gt 0 ]]; then
    log_info "Ramas demasiado recientes (<$DAYS_THRESHOLD días): ${YELLOW}$too_recent_count${NC}"
  fi
  
  log_warning "Ramas candidatas para eliminación: ${RED}${#branches_to_delete[@]}${NC}"
  
  # Print branches to delete
  if [[ ${#branches_to_delete[@]} -eq 0 ]]; then
    echo ""
    log_success "No hay ramas para eliminar. ¡Repositorio limpio! ✨"
    echo ""
    return 0
  fi
  
  echo ""
  echo -e "${YELLOW}Ramas que serían eliminadas:${NC}"
  for branch in "${branches_to_delete[@]}"; do
    local merge_date
    merge_date=$(git log -1 --format=%ai "origin/$branch" 2>/dev/null | cut -d' ' -f1)
    echo "  - $branch (último commit: $merge_date)"
  done
  echo ""
  
  # Dry run mode
  if [[ $DRY_RUN == true ]]; then
    log_info "Modo ${YELLOW}DRY-RUN${NC} - No se eliminará ninguna rama"
    log_info "Ejecuta con ${GREEN}--force${NC} para eliminar las ramas"
    echo ""
    return 0
  fi
  
  # Confirm deletion
  if [[ $FORCE == false ]]; then
    echo -e "${RED}⚠ ADVERTENCIA: Esta operación eliminará ${#branches_to_delete[@]} ramas remotas${NC}"
    echo -n "¿Continuar? (yes/no): "
    read -r confirmation
    
    if [[ "$confirmation" != "yes" ]]; then
      log_info "Operación cancelada por el usuario"
      return 1
    fi
  fi
  
  # Delete branches
  echo ""
  log_info "Eliminando ramas..."
  local deleted_count=0
  local failed_count=0
  
  for branch in "${branches_to_delete[@]}"; do
    if git push origin --delete "$branch" >/dev/null 2>&1; then
      log_success "Eliminada: $branch"
      ((deleted_count++))
    else
      log_error "Fallo al eliminar: $branch"
      ((failed_count++))
    fi
  done
  
  # Final report
  echo ""
  echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
  echo -e "${GREEN}║   📊 Reporte de Limpieza                                  ║${NC}"
  echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
  echo ""
  echo "  Total de ramas analizadas:     ${#merged_branches[@]}"
  echo "  Ramas protegidas:              $protected_count"
  [[ $DAYS_THRESHOLD -gt 0 ]] && echo "  Ramas muy recientes:           $too_recent_count"
  echo "  Ramas eliminadas exitosamente: ${GREEN}$deleted_count${NC}"
  [[ $failed_count -gt 0 ]] && echo "  Fallos:                        ${RED}$failed_count${NC}"
  echo ""
  
  log_success "Limpieza completada ✨"
  echo ""
}

# Main execution
main() {
  # Check if we're in a git repository
  if ! git rev-parse --git-dir > /dev/null 2>&1; then
    log_error "No estás en un repositorio Git"
    exit 1
  fi
  
  # Run cleanup
  cleanup_branches
}

# Run main function
main "$@"
