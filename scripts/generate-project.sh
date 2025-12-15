#!/bin/bash
# ==============================================================================
# Elite Framework - Automatic Project Generator
# ==============================================================================

set -e
set -u
set -o pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}==============================================================================${NC}"
    echo -e "${GREEN}$1${NC}"
    echo -e "${BLUE}==============================================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

detect_project_type() {
    local description="$1"
    local desc_lower
    desc_lower=$(echo "$description" | tr '[:upper:]' '[:lower:]')
    
    if echo "$desc_lower" | grep -qE "api|rest|graphql|backend|server|endpoint"; then
        echo "api"
        return
    fi
    
    if echo "$desc_lower" | grep -qE "bot|discord|telegram|whatsapp|slack"; then
        echo "bot"
        return
    fi
    
    if echo "$desc_lower" | grep -qE "pwa|web app|website|frontend|dashboard|admin panel"; then
        echo "web"
        return
    fi
    
    if echo "$desc_lower" | grep -qE "agent|ai|llm|rag|langchain|crewai|gpt|claude"; then
        echo "agent"
        return
    fi
    
    echo "api"
}

detect_language() {
    local description="$1"
    local desc_lower
    desc_lower=$(echo "$description" | tr '[:upper:]' '[:lower:]')
    
    if echo "$desc_lower" | grep -qE "\bgo\b|golang"; then
        echo "go"
        return
    fi
    
    if echo "$desc_lower" | grep -qE "typescript|node|nodejs|javascript|react|vue|next"; then
        echo "typescript"
        return
    fi
    
    if echo "$desc_lower" | grep -qE "python|django|flask|fastapi"; then
        echo "python"
        return
    fi
    
    echo "go"
}

generate_project_name() {
    local description="$1"
    local name
    
    name=$(echo "$description" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[^a-z0-9-]//g' | cut -c1-50)
    name=$(echo "$name" | sed 's/-*$//')
    
    echo "$name"
}

create_directory_structure() {
    local project_dir="$1"
    local language="$2"
    
    print_info "Creating directory structure..."
    
    mkdir -p "$project_dir"/{src,tests,docs,deploy}
    
    case "$language" in
        go)
            mkdir -p "$project_dir"/{cmd,internal,pkg}
            mkdir -p "$project_dir"/internal/{handlers,models,services,repository}
            ;;
        typescript|javascript)
            mkdir -p "$project_dir"/src/{controllers,models,services,routes,middleware,utils}
            mkdir -p "$project_dir"/{tests/{unit,integration,e2e},public}
            ;;
        python)
            mkdir -p "$project_dir"/src/{api,models,services,utils}
            mkdir -p "$project_dir"/{tests/{unit,integration},scripts}
            ;;
    esac
    
    mkdir -p "$project_dir"/deploy/{docker,k8s}
    mkdir -p "$project_dir"/.github/workflows
    
    print_success "Directory structure created"
}

generate_readme() {
    local project_dir="$1"
    local project_name="$2"
    local description="$3"
    local language="$5"
    
    cat > "$project_dir/README.md" << EOF
# $project_name

$description

## Quick Start

### Installation

\`\`\`bash
make deps
make build
make test
\`\`\`

### Running

\`\`\`bash
make run
\`\`\`

## License

MIT License

---

Generated with Tokyo-IA Elite Framework
EOF
    
    print_success "README.md generated"
}

generate_makefile() {
    local project_dir="$1"
    local project_name="$2"
    
    cat > "$project_dir/Makefile" << 'EOF'
.PHONY: help build test clean run

help:
@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

deps: ## Install dependencies
@echo "Installing dependencies..."

build: ## Build the application
@echo "Building..."

test: ## Run tests
@echo "Running tests..."

run: ## Run the application
@echo "Running application..."

clean: ## Clean build artifacts
rm -rf bin/ dist/ build/
EOF
    
    print_success "Makefile generated"
}

generate_gitignore() {
    local project_dir="$1"
    
    cat > "$project_dir/.gitignore" << 'EOF'
bin/
dist/
build/
node_modules/
vendor/
.env
.env.*
!.env.example
.vscode/
.idea/
*.log
tmp/
EOF
    
    print_success ".gitignore generated"
}

generate_project() {
    local description="$1"
    
    print_header "Elite Framework - Project Generator"
    
    print_info "Analyzing project description..."
    local project_type
    project_type=$(detect_project_type "$description")
    print_success "Detected project type: $project_type"
    
    local language
    language=$(detect_language "$description")
    print_success "Detected language: $language"
    
    local project_name
    project_name=$(generate_project_name "$description")
    print_success "Generated project name: $project_name"
    
    local project_dir="projects/$project_name"
    
    if [ -d "$project_dir" ]; then
        print_error "Project directory already exists: $project_dir"
        read -rp "Overwrite? (y/N): " confirm
        if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
            print_warning "Aborting..."
            exit 1
        fi
        rm -rf "$project_dir"
    fi
    
    print_header "Creating Project Structure"
    create_directory_structure "$project_dir" "$language"
    
    print_header "Generating Base Files"
    generate_readme "$project_dir" "$project_name" "$description" "$project_type" "$language"
    generate_makefile "$project_dir" "$project_name"
    generate_gitignore "$project_dir"
    
    print_info "Initializing git repository..."
    cd "$project_dir"
    git init > /dev/null 2>&1
    git add . > /dev/null 2>&1
    git commit -m "Initial commit - Generated by Elite Framework" > /dev/null 2>&1 || true
    cd - > /dev/null
    print_success "Git repository initialized"
    
    print_header "Project Generated Successfully! 🎉"
    echo -e "${CYAN}Project:${NC} $project_name"
    echo -e "${CYAN}Type:${NC} $project_type"
    echo -e "${CYAN}Language:${NC} $language"
    echo -e "${CYAN}Location:${NC} $project_dir"
    echo ""
    echo -e "${GREEN}Next steps:${NC}"
    echo -e "  cd $project_dir"
    echo -e "  make deps"
    echo -e "  make build"
    echo ""
    print_success "Happy coding! 🚀"
}

interactive_mode() {
    print_header "Elite Framework - Interactive Project Generator"
    
    echo ""
    echo -e "${CYAN}Describe your project:${NC}"
    read -rp "> " description
    
    if [ -z "$description" ]; then
        print_error "Description cannot be empty"
        exit 1
    fi
    
    generate_project "$description"
}

main() {
    mkdir -p projects
    
    if [ $# -eq 0 ]; then
        interactive_mode
    else
        description="$*"
        generate_project "$description"
    fi
}

main "$@"
