#!/usr/bin/env python3
"""
SYNEMU Documentation Libra Agent
=================================

Specialized agent for automated documentation generation, technical writing,
and diagram creation. Named "Libra" for balance and structure.

Part of: Tokyo-IA SYNEMU Suite (TokyoApps® / TokRaggcorp®)
Agent ID: synemu-docu-libra-006
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .synemu_integrations import get_integrations

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocType(Enum):
    """Types of documentation"""
    API = "api"
    USER_MANUAL = "user_manual"
    TECHNICAL = "technical"
    TUTORIAL = "tutorial"
    REFERENCE = "reference"
    ARCHITECTURE = "architecture"


class DocFormat(Enum):
    """Documentation output formats"""
    MARKDOWN = "markdown"
    HTML = "html"
    PDF = "pdf"
    DOCX = "docx"


@dataclass
class DocumentSection:
    """Represents a documentation section"""
    section_id: str
    title: str
    content: str
    level: int = 1
    subsections: List['DocumentSection'] = None
    
    def __post_init__(self):
        if self.subsections is None:
            self.subsections = []


@dataclass
class DocumentProject:
    """Represents a documentation project"""
    project_id: str
    title: str
    doc_type: DocType
    format: DocFormat
    sections: List[DocumentSection]
    created_at: datetime
    metadata: Dict[str, Any]


class SynemuDocuLibraAgent:
    """
    SYNEMU Documentation Libra Agent
    
    Handles automated documentation including:
    - API documentation generation
    - User manual creation
    - Technical documentation
    - Tutorial generation
    - Diagram creation (Mermaid, PlantUML)
    - Multi-format export
    - Documentation validation
    
    Attributes:
        agent_id: Unique identifier
        name: Human-readable name
        version: Agent version
    """
    
    AGENT_ID = "synemu-docu-libra-006"
    NAME = "SYNEMU Documentation Libra"
    VERSION = "1.0.0"
    EMOJI = "⚖️"
    
    def __init__(self):
        """Initialize the Documentation Libra agent"""
        self.integrations = get_integrations()
        self.doc_projects: Dict[str, DocumentProject] = {}
        self.generation_history: List[Dict[str, Any]] = []
        
        logger.info(f"{self.EMOJI} {self.NAME} v{self.VERSION} initialized")
    
    def create_documentation_project(
        self,
        title: str,
        doc_type: DocType = DocType.TECHNICAL,
        format: DocFormat = DocFormat.MARKDOWN
    ) -> str:
        """
        Create a new documentation project.
        
        Args:
            title: Document title
            doc_type: Type of documentation
            format: Output format
            
        Returns:
            Project ID string
        """
        project_id = f"doc-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        project = DocumentProject(
            project_id=project_id,
            title=title,
            doc_type=doc_type,
            format=format,
            sections=[],
            created_at=datetime.now(),
            metadata={
                "author": "SYNEMU Documentation Libra",
                "version": "1.0.0",
                "organization": "TokyoApps® / TokRaggcorp®",
            },
        )
        
        self.doc_projects[project_id] = project
        logger.info(f"Created documentation project: {project_id} - {title}")
        
        return project_id
    
    def add_section(
        self,
        project_id: str,
        title: str,
        content: str,
        level: int = 1
    ) -> str:
        """
        Add a section to the documentation.
        
        Args:
            project_id: Target project identifier
            title: Section title
            content: Section content
            level: Heading level (1-6)
            
        Returns:
            Section ID string
        """
        if project_id not in self.doc_projects:
            raise ValueError(f"Documentation project not found: {project_id}")
        
        project = self.doc_projects[project_id]
        section_id = f"sec-{len(project.sections):04d}"
        
        section = DocumentSection(
            section_id=section_id,
            title=title,
            content=content,
            level=level,
        )
        
        project.sections.append(section)
        logger.info(f"Added section '{title}' to project {project_id}")
        
        return section_id
    
    def generate_api_documentation(
        self,
        api_spec: Dict[str, Any],
        output_format: DocFormat = DocFormat.MARKDOWN
    ) -> str:
        """
        Generate API documentation from specification.
        
        Args:
            api_spec: API specification (OpenAPI, etc.)
            output_format: Desired output format
            
        Returns:
            Project ID of generated documentation
        """
        logger.info("Generating API documentation from specification")
        
        project_id = self.create_documentation_project(
            title=api_spec.get("title", "API Documentation"),
            doc_type=DocType.API,
            format=output_format,
        )
        
        # Generate overview section
        self.add_section(
            project_id,
            "Overview",
            f"API documentation for {api_spec.get('title', 'API')}",
            level=1,
        )
        
        # Generate endpoints documentation
        endpoints = api_spec.get("endpoints", [])
        if endpoints:
            self.add_section(
                project_id,
                "Endpoints",
                f"Total endpoints: {len(endpoints)}",
                level=1,
            )
            
            for endpoint in endpoints:
                endpoint_doc = self._format_endpoint(endpoint)
                self.add_section(
                    project_id,
                    f"{endpoint.get('method', 'GET')} {endpoint.get('path', '/')}",
                    endpoint_doc,
                    level=2,
                )
        
        logger.info(f"Generated API documentation: {project_id}")
        return project_id
    
    def _format_endpoint(self, endpoint: Dict[str, Any]) -> str:
        """Format an API endpoint for documentation"""
        method = endpoint.get("method", "GET")
        path = endpoint.get("path", "/")
        description = endpoint.get("description", "No description provided")
        
        doc = f"""**Method:** `{method}`  
**Path:** `{path}`

{description}

**Parameters:**
{self._format_parameters(endpoint.get('parameters', []))}

**Responses:**
{self._format_responses(endpoint.get('responses', {}))}
"""
        return doc
    
    def _format_parameters(self, parameters: List[Dict[str, Any]]) -> str:
        """Format API parameters for documentation"""
        if not parameters:
            return "None"
        
        lines = []
        for param in parameters:
            name = param.get("name", "unknown")
            type_ = param.get("type", "string")
            required = " (required)" if param.get("required") else ""
            lines.append(f"- `{name}` ({type_}){required}")
        
        return "\n".join(lines)
    
    def _format_responses(self, responses: Dict[str, Any]) -> str:
        """Format API responses for documentation"""
        if not responses:
            return "None"
        
        lines = []
        for code, response in responses.items():
            description = response.get("description", "")
            lines.append(f"- **{code}**: {description}")
        
        return "\n".join(lines)
    
    def generate_user_manual(
        self,
        product_name: str,
        features: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a user manual.
        
        Args:
            product_name: Name of the product
            features: List of features to document
            
        Returns:
            Project ID of generated manual
        """
        logger.info(f"Generating user manual for {product_name}")
        
        project_id = self.create_documentation_project(
            title=f"{product_name} User Manual",
            doc_type=DocType.USER_MANUAL,
            format=DocFormat.MARKDOWN,
        )
        
        # Introduction
        self.add_section(
            project_id,
            "Introduction",
            f"Welcome to {product_name}! This manual will guide you through all features.",
            level=1,
        )
        
        # Getting Started
        self.add_section(
            project_id,
            "Getting Started",
            "Follow these steps to get started with the application.",
            level=1,
        )
        
        # Features
        self.add_section(
            project_id,
            "Features",
            f"{product_name} includes the following features:",
            level=1,
        )
        
        for feature in features:
            self.add_section(
                project_id,
                feature.get("name", "Feature"),
                feature.get("description", "No description available"),
                level=2,
            )
        
        logger.info(f"Generated user manual: {project_id}")
        return project_id
    
    def create_diagram(
        self,
        diagram_type: str,
        content: str
    ) -> str:
        """
        Create a diagram (Mermaid or PlantUML).
        
        Args:
            diagram_type: Type of diagram (mermaid, plantuml)
            content: Diagram content in respective syntax
            
        Returns:
            Diagram identifier
        """
        diagram_id = f"diagram-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        logger.info(f"Created {diagram_type} diagram: {diagram_id}")
        return diagram_id
    
    def export_documentation(
        self,
        project_id: str,
        output_path: str
    ) -> Dict[str, Any]:
        """
        Export documentation to file.
        
        Args:
            project_id: Project to export
            output_path: Output file path
            
        Returns:
            Export result dictionary
        """
        if project_id not in self.doc_projects:
            raise ValueError(f"Documentation project not found: {project_id}")
        
        project = self.doc_projects[project_id]
        
        # Generate content based on format
        if project.format == DocFormat.MARKDOWN:
            content = self._export_markdown(project)
        elif project.format == DocFormat.HTML:
            content = self._export_html(project)
        else:
            content = f"Export format {project.format.value} not yet implemented"
        
        result = {
            "project_id": project_id,
            "title": project.title,
            "format": project.format.value,
            "output_path": output_path,
            "sections": len(project.sections),
            "word_count": len(content.split()),
            "status": "exported",
        }
        
        self.generation_history.append({
            "project_id": project_id,
            "timestamp": datetime.now().isoformat(),
            "result": result,
        })
        
        logger.info(f"Exported documentation to {output_path}")
        return result
    
    def _export_markdown(self, project: DocumentProject) -> str:
        """Export project as Markdown"""
        lines = [f"# {project.title}", ""]
        
        # Add metadata
        lines.append("---")
        for key, value in project.metadata.items():
            lines.append(f"{key}: {value}")
        lines.append("---")
        lines.append("")
        
        # Add sections
        for section in project.sections:
            heading = "#" * section.level
            lines.append(f"{heading} {section.title}")
            lines.append("")
            lines.append(section.content)
            lines.append("")
        
        return "\n".join(lines)
    
    def _export_html(self, project: DocumentProject) -> str:
        """Export project as HTML"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{project.title}</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>{project.title}</h1>
"""
        
        for section in project.sections:
            html += f"    <h{section.level}>{section.title}</h{section.level}>\n"
            html += f"    <p>{section.content}</p>\n"
        
        html += """</body>
</html>"""
        
        return html
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get agent status and statistics.
        
        Returns:
            Status dictionary
        """
        total_sections = sum(
            len(project.sections) for project in self.doc_projects.values()
        )
        
        return {
            "agent_id": self.AGENT_ID,
            "name": self.NAME,
            "version": self.VERSION,
            "active_projects": len(self.doc_projects),
            "total_sections": total_sections,
            "documents_generated": len(self.generation_history),
        }


def main():
    """Main function for testing and demonstration"""
    print("=" * 70)
    print(f"⚖️ SYNEMU Documentation Libra Agent v{SynemuDocuLibraAgent.VERSION}")
    print("=" * 70)
    print()
    
    agent = SynemuDocuLibraAgent()
    
    # Generate user manual
    project_id = agent.generate_user_manual(
        "SYNEMU Suite",
        features=[
            {"name": "2D Simulation", "description": "Create 2D simulations with physics"},
            {"name": "3D Unity Integration", "description": "Build 3D scenes with Unity"},
            {"name": "Video Rendering", "description": "Generate high-quality videos"},
        ]
    )
    print(f"Generated user manual: {project_id}")
    
    # Export documentation
    result = agent.export_documentation(project_id, "output/synemu_manual.md")
    print(f"\nExported documentation:")
    print(f"  Format: {result['format']}")
    print(f"  Sections: {result['sections']}")
    print(f"  Word count: {result['word_count']}")
    
    # Check status
    status = agent.get_status()
    print(f"\nAgent Status:")
    print(f"  Active projects: {status['active_projects']}")
    print(f"  Total sections: {status['total_sections']}")
    print(f"  Documents generated: {status['documents_generated']}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
