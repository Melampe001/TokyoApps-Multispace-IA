#!/usr/bin/env python3
"""
Library Cataloger - Automated file indexing and cataloging system
Scans the repository and generates comprehensive metadata for all files
"""

import os
import json
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import re

# Directories to ignore during scanning
IGNORE_DIRS = {
    '.git', 'node_modules', 'build', 'dist', 'target', '__pycache__',
    '.gradle', '.idea', '.vscode', 'vendor', 'tmp'
}

# File extensions mapped to categories
EXTENSION_CATEGORIES = {
    # Workflows
    '.yml': 'workflow', '.yaml': 'workflow',
    # Scripts
    '.py': 'script', '.sh': 'script', '.rb': 'script', '.js': 'script',
    # Documentation
    '.md': 'documentation', '.txt': 'documentation', '.rst': 'documentation',
    # Source Code
    '.go': 'source', '.kt': 'source', '.java': 'source', '.dart': 'source',
    '.jsx': 'source', '.tsx': 'source', '.ts': 'source',
    # Configuration
    '.json': 'configuration', '.toml': 'configuration', '.ini': 'configuration',
    '.env': 'configuration', '.properties': 'configuration',
    # Protobuf
    '.proto': 'schema',
    # Build
    '.gradle': 'build', 'Makefile': 'build', 'Dockerfile': 'build',
}

# Purpose detection keywords
PURPOSE_KEYWORDS = {
    'automation': ['automat', 'bot', 'schedule', 'cron', 'workflow'],
    'monitoring': ['monitor', 'alert', 'watch', 'track', 'metric'],
    'integration': ['api', 'webhook', 'sync', 'integration', 'connect'],
    'testing': ['test', 'spec', 'mock', 'fixture'],
    'documentation': ['doc', 'guide', 'readme', 'tutorial', 'howto'],
    'deployment': ['deploy', 'release', 'publish', 'build'],
    'security': ['security', 'auth', 'encrypt', 'secret', 'credential'],
}


class LibraryCataloger:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.files_metadata = []
        self.stats = defaultdict(int)
        self.category_files = defaultdict(list)
        self.purpose_files = defaultdict(list)
        self.tech_files = defaultdict(list)

    def scan_repository(self):
        """Recursively scan the repository"""
        print(f"Scanning repository: {self.repo_path}")
        
        for root, dirs, files in os.walk(self.repo_path):
            # Remove ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for filename in files:
                filepath = Path(root) / filename
                try:
                    metadata = self.extract_metadata(filepath)
                    if metadata:
                        self.files_metadata.append(metadata)
                        self.categorize_file(metadata)
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

        print(f"Scanned {len(self.files_metadata)} files")

    def extract_metadata(self, filepath):
        """Extract metadata from a file"""
        try:
            stat = filepath.stat()
            relative_path = filepath.relative_to(self.repo_path)
            
            # Skip if file is too large (>10MB)
            if stat.st_size > 10 * 1024 * 1024:
                return None
            
            # Get file extension
            ext = filepath.suffix.lower()
            if not ext and filepath.name in EXTENSION_CATEGORIES:
                ext = filepath.name
            
            # Determine category
            category = EXTENSION_CATEGORIES.get(ext, 'other')
            
            # Get git information
            git_info = self.get_git_info(relative_path)
            
            # Extract description from file content
            description = self.extract_description(filepath, category)
            
            # Detect purpose
            purpose = self.detect_purpose(filepath, description)
            
            # Detect tags
            tags = self.detect_tags(filepath, description)
            
            metadata = {
                'file': {
                    'path': str(relative_path),
                    'name': filepath.name,
                    'type': category,
                    'extension': ext,
                    'size_bytes': stat.st_size,
                    'lines': self.count_lines(filepath)
                },
                'classification': {
                    'category': category,
                    'area': self.detect_area(relative_path),
                    'purpose': purpose,
                    'tags': tags
                },
                'dates': git_info['dates'],
                'authorship': git_info['authorship'],
                'content': {
                    'description': description,
                    'dependencies': self.detect_dependencies(filepath)
                }
            }
            
            return metadata
            
        except Exception as e:
            print(f"Error extracting metadata from {filepath}: {e}")
            return None

    def get_git_info(self, relative_path):
        """Get git information for a file"""
        try:
            # Get first commit date
            result = subprocess.run(
                ['git', 'log', '--follow', '--format=%aI|%an', '--reverse', str(relative_path)],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            lines = result.stdout.strip().split('\n')
            if lines and lines[0]:
                first_date, first_author = lines[0].split('|', 1)
                last_date, last_author = lines[-1].split('|', 1) if len(lines) > 1 else (first_date, first_author)
            else:
                first_date = last_date = datetime.now().isoformat()
                first_author = last_author = "unknown"
            
            # Get all contributors
            result = subprocess.run(
                ['git', 'log', '--follow', '--format=%an', str(relative_path)],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            contributors = list(set(result.stdout.strip().split('\n')))
            if not contributors or contributors == ['']:
                contributors = ["unknown"]
            
            return {
                'dates': {
                    'created': first_date,
                    'modified': last_date
                },
                'authorship': {
                    'author': first_author,
                    'contributors': contributors,
                    'commits': len(lines)
                }
            }
            
        except Exception as e:
            return {
                'dates': {
                    'created': datetime.now().isoformat(),
                    'modified': datetime.now().isoformat()
                },
                'authorship': {
                    'author': 'unknown',
                    'contributors': ['unknown'],
                    'commits': 0
                }
            }

    def count_lines(self, filepath):
        """Count lines in a file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except:
            return 0

    def extract_description(self, filepath, category):
        """Extract description from file content"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1000)  # Read first 1000 chars
                
                # For markdown files, extract first heading or paragraph
                if category == 'documentation':
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith('#'):
                            return line.lstrip('#').strip()
                        elif line and not line.startswith('['):
                            return line[:200]
                
                # For code files, extract first comment
                elif category in ['source', 'script']:
                    # Look for docstring or comment
                    match = re.search(r'(?:"""([^"]+)"""|\'\'\'([^\']+)\'\'\'|/\*\*([^*]+)\*/|#\s*(.+))', content)
                    if match:
                        desc = next((g for g in match.groups() if g), '')
                        return desc.strip()[:200]
                
                # For workflow files
                elif category == 'workflow':
                    match = re.search(r'name:\s*(.+)', content)
                    if match:
                        return match.group(1).strip()
                
                return f"{filepath.name} - {category}"
                
        except Exception as e:
            return f"{filepath.name}"

    def detect_area(self, relative_path):
        """Detect the area/module of the file"""
        parts = str(relative_path).split(os.sep)
        
        if '.github' in parts:
            return 'ci-cd'
        elif 'docs' in parts:
            return 'documentation'
        elif any(x in parts for x in ['cmd', 'main']):
            return 'cli'
        elif 'lib' in parts or 'internal' in parts:
            return 'backend'
        elif any(x in parts for x in ['web', 'admin']):
            return 'frontend'
        elif 'config' in parts:
            return 'configuration'
        elif 'testing' in parts or 'test' in parts:
            return 'testing'
        else:
            return 'general'

    def detect_purpose(self, filepath, description):
        """Detect the purpose of the file"""
        text = (filepath.name + ' ' + description).lower()
        
        for purpose, keywords in PURPOSE_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return purpose
        
        return 'general'

    def detect_tags(self, filepath, description):
        """Detect tags for the file"""
        tags = []
        text = (filepath.name + ' ' + description).lower()
        
        # Technology tags
        tech_tags = {
            'golang': ['go', '.go'],
            'python': ['python', '.py'],
            'javascript': ['js', '.js', 'node'],
            'yaml': ['.yml', '.yaml'],
            'docker': ['docker', 'container'],
            'github-actions': ['workflow', 'action'],
        }
        
        for tag, keywords in tech_tags.items():
            if any(keyword in text for keyword in keywords):
                tags.append(tag)
        
        return tags

    def detect_dependencies(self, filepath):
        """Detect dependencies from file content"""
        dependencies = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Python imports
                imports = re.findall(r'^(?:from|import)\s+([^\s]+)', content, re.MULTILINE)
                dependencies.extend(imports[:5])  # Limit to first 5
                
                # Go imports
                go_imports = re.findall(r'import\s+["\']([^"\']+)["\']', content)
                dependencies.extend(go_imports[:5])
                
        except:
            pass
        
        return dependencies[:10]  # Max 10 dependencies

    def categorize_file(self, metadata):
        """Categorize file for different views"""
        file_info = {
            'path': metadata['file']['path'],
            'name': metadata['file']['name'],
            'description': metadata['content']['description']
        }
        
        # By category
        category = metadata['classification']['category']
        self.category_files[category].append(file_info)
        self.stats[f'category_{category}'] += 1
        
        # By purpose
        purpose = metadata['classification']['purpose']
        self.purpose_files[purpose].append(file_info)
        self.stats[f'purpose_{purpose}'] += 1
        
        # By technology (based on extension)
        ext = metadata['file']['extension']
        if ext:
            tech = ext.lstrip('.')
            self.tech_files[tech].append(file_info)
            self.stats[f'tech_{tech}'] += 1

    def generate_catalog(self):
        """Generate the main catalog markdown"""
        catalog = []
        catalog.append("# 📚 Catálogo Completo de la Biblioteca\n")
        catalog.append(f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        catalog.append(f"Total de archivos: {len(self.files_metadata)}\n")
        catalog.append("\n---\n")
        
        # Statistics
        catalog.append("## 📊 Estadísticas Generales\n")
        for category in sorted(self.category_files.keys()):
            count = len(self.category_files[category])
            catalog.append(f"- **{category.title()}**: {count} archivos\n")
        catalog.append("\n---\n")
        
        # By Category
        catalog.append("## 🗂️ Por Categoría\n")
        for category in sorted(self.category_files.keys()):
            catalog.append(f"\n### {category.title()} ({len(self.category_files[category])} archivos)\n")
            for file_info in sorted(self.category_files[category], key=lambda x: x['name'])[:20]:
                catalog.append(f"- **[{file_info['name']}]({file_info['path']})** - {file_info['description'][:100]}\n")
        
        catalog.append("\n---\n")
        
        # By Purpose
        catalog.append("## 🎯 Por Propósito\n")
        for purpose in sorted(self.purpose_files.keys()):
            catalog.append(f"\n### {purpose.title()} ({len(self.purpose_files[purpose])} archivos)\n")
            for file_info in sorted(self.purpose_files[purpose], key=lambda x: x['name'])[:10]:
                catalog.append(f"- [{file_info['name']}]({file_info['path']})\n")
        
        catalog.append("\n---\n")
        catalog.append("\n*Este catálogo se actualiza automáticamente cada día a las 2 AM*\n")
        
        return ''.join(catalog)

    def generate_timeline(self):
        """Generate timeline markdown"""
        timeline = []
        timeline.append("# 📅 Línea de Tiempo de Creaciones\n")
        timeline.append(f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Sort files by creation date
        sorted_files = sorted(self.files_metadata, 
                            key=lambda x: x['dates']['created'], 
                            reverse=True)
        
        current_date = None
        for file_meta in sorted_files[:50]:  # Show last 50 files
            try:
                created = datetime.fromisoformat(file_meta['dates']['created'].replace('Z', '+00:00'))
                date_str = created.strftime('%Y-%m-%d')
                
                if date_str != current_date:
                    timeline.append(f"\n## {date_str}\n")
                    current_date = date_str
                
                timeline.append(f"- **{file_meta['file']['name']}** - {file_meta['content']['description'][:80]}\n")
            except:
                pass
        
        return ''.join(timeline)

    def generate_search_index(self):
        """Generate JSON search index"""
        return json.dumps({
            'generated': datetime.now().isoformat(),
            'total_files': len(self.files_metadata),
            'files': self.files_metadata
        }, indent=2)

    def save_outputs(self):
        """Save all output files"""
        library_path = self.repo_path / 'LIBRARY'
        
        # Save catalog
        with open(library_path / 'CATALOG.md', 'w', encoding='utf-8') as f:
            f.write(self.generate_catalog())
        print("Generated LIBRARY/CATALOG.md")
        
        # Save timeline
        with open(library_path / 'TIMELINE.md', 'w', encoding='utf-8') as f:
            f.write(self.generate_timeline())
        print("Generated LIBRARY/TIMELINE.md")
        
        # Save search index
        with open(library_path / 'SEARCH_INDEX.json', 'w', encoding='utf-8') as f:
            f.write(self.generate_search_index())
        print("Generated LIBRARY/SEARCH_INDEX.json")
        
        # Save category files
        self.save_category_files()
        
        # Save purpose files
        self.save_purpose_files()
        
        # Save tech files
        self.save_tech_files()
        
        # Save stats
        self.save_stats()

    def save_category_files(self):
        """Save category-specific markdown files"""
        category_path = self.repo_path / 'LIBRARY' / 'by-category'
        
        for category, files in self.category_files.items():
            content = [f"# {category.title()}\n\n"]
            file_word = "archivo" if len(files) == 1 else "archivos"
            content.append(f"Total: {len(files)} {file_word}\n\n")
            
            for file_info in sorted(files, key=lambda x: x['name']):
                content.append(f"## [{file_info['name']}]({file_info['path']})\n")
                content.append(f"{file_info['description']}\n\n")
            
            filename = f"{category}.md"
            with open(category_path / filename, 'w', encoding='utf-8') as f:
                f.write(''.join(content))
        
        print(f"Generated {len(self.category_files)} category files")

    def save_purpose_files(self):
        """Save purpose-specific markdown files"""
        purpose_path = self.repo_path / 'LIBRARY' / 'by-purpose'
        
        for purpose, files in self.purpose_files.items():
            content = [f"# {purpose.title()}\n\n"]
            file_word = "archivo" if len(files) == 1 else "archivos"
            content.append(f"Total: {len(files)} {file_word}\n\n")
            
            for file_info in sorted(files, key=lambda x: x['name']):
                content.append(f"- [{file_info['name']}]({file_info['path']}) - {file_info['description'][:100]}\n")
            
            filename = f"{purpose}.md"
            with open(purpose_path / filename, 'w', encoding='utf-8') as f:
                f.write(''.join(content))
        
        print(f"Generated {len(self.purpose_files)} purpose files")

    def save_tech_files(self):
        """Save technology-specific markdown files"""
        tech_path = self.repo_path / 'LIBRARY' / 'by-technology'
        
        for tech, files in self.tech_files.items():
            if not tech:
                continue
                
            content = [f"# {tech.upper()}\n\n"]
            file_word = "archivo" if len(files) == 1 else "archivos"
            content.append(f"Total: {len(files)} {file_word}\n\n")
            
            for file_info in sorted(files, key=lambda x: x['name']):
                content.append(f"- [{file_info['name']}]({file_info['path']})\n")
            
            filename = f"{tech}.md"
            with open(tech_path / filename, 'w', encoding='utf-8') as f:
                f.write(''.join(content))
        
        print(f"Generated {len(self.tech_files)} technology files")

    def save_stats(self):
        """Save statistics files"""
        stats_path = self.repo_path / 'LIBRARY' / 'stats'
        
        # File count statistics
        content = ["# File Count Statistics\n\n"]
        content.append(f"Total files: {len(self.files_metadata)}\n\n")
        content.append("## By Category\n")
        for category in sorted(self.category_files.keys()):
            content.append(f"- {category}: {len(self.category_files[category])}\n")
        
        with open(stats_path / 'file-count.md', 'w', encoding='utf-8') as f:
            f.write(''.join(content))
        
        print("Generated statistics files")


def main():
    """Main function"""
    repo_path = os.getenv('GITHUB_WORKSPACE', os.getcwd())
    
    print(f"Starting library cataloger for: {repo_path}")
    
    cataloger = LibraryCataloger(repo_path)
    cataloger.scan_repository()
    cataloger.save_outputs()
    
    print("✅ Library cataloging complete!")


if __name__ == '__main__':
    main()
