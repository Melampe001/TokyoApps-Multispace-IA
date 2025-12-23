#!/usr/bin/env python3
"""
🤖 Sistema de Automatización Inteligente
Usa los 5 agentes de Tokyo-IA para automatizar tareas completas
"""

import os
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.orchestrator.agent_orchestrator import AgentOrchestrator
from typing import Dict, List, Any


class IntelligentAutomation:
    """Sistema de automatización que usa todos los agentes"""
    
    def __init__(self):
        """Inicializa el orquestador con todos los agentes"""
        self.orchestrator = AgentOrchestrator()
        
        # Inicializar agentes desde variables de entorno
        self.orchestrator.initialize_agents(
            anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'),
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            groq_api_key=os.getenv('GROQ_API_KEY'),
            google_api_key=os.getenv('GOOGLE_API_KEY')
        )
    
    def auto_review_and_improve_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Workflow completo: Review → Tests → CI/CD → Docs
        
        Args:
            code: Código a revisar
            language: Lenguaje de programación
            
        Returns:
            Resultados completos del workflow
        """
        workflow_id = self.orchestrator.create_workflow(
            name=f"Auto Review & Improve: {language} Code",
            description="Revisión completa, tests, CI/CD y documentación",
            workflow_type="full_automation"
        )
        
        tasks = [
            # 1. Akira: Security audit
            {
                "agent_id": "akira-001",
                "task_type": "security_audit",
                "description": "Auditoría de seguridad del código",
                "method": "security_audit",
                "args": [code, language]
            },
            # 2. Akira: Code review
            {
                "agent_id": "akira-001",
                "task_type": "code_review",
                "description": "Revisión completa del código",
                "method": "review_code",
                "args": [code, language],
                "kwargs": {"context": "Automated review for production"}
            },
            # 3. Yuki: Generate tests
            {
                "agent_id": "yuki-002",
                "task_type": "unit_tests",
                "description": "Generación de tests unitarios",
                "method": "generate_unit_tests",
                "args": [code, language, "pytest"]
            },
            # 4. Hiro: CI/CD pipeline
            {
                "agent_id": "hiro-003",
                "task_type": "ci_cd",
                "description": "Crear pipeline CI/CD",
                "method": "create_cicd_pipeline",
                "args": [{"language": language, "tests": True}],
                "kwargs": {"platform": "github-actions"}
            },
            # 5. Sakura: Documentation
            {
                "agent_id": "sakura-004",
                "task_type": "documentation",
                "description": "Generar documentación",
                "method": "create_readme",
                "args": [{
                    "name": f"{language} Module",
                    "description": "Auto-generated documentation"
                }]
            }
        ]
        
        return self.orchestrator.run_workflow(workflow_id, tasks)
    
    def design_and_document_feature(self, feature_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Workflow: Arquitectura → Estrategia de Tests → Documentación
        
        Args:
            feature_requirements: Requisitos del feature
            
        Returns:
            Diseño completo del feature
        """
        workflow_id = self.orchestrator.create_workflow(
            name=f"Design Feature: {feature_requirements.get('name', 'New Feature')}",
            description="Diseño de arquitectura, tests y documentación",
            workflow_type="feature_design"
        )
        
        tasks = [
            # 1. Kenji: Architecture design
            {
                "agent_id": "kenji-005",
                "task_type": "architecture",
                "description": "Diseño de arquitectura del sistema",
                "method": "design_system_architecture",
                "args": [feature_requirements]
            },
            # 2. Yuki: Test strategy
            {
                "agent_id": "yuki-002",
                "task_type": "test_planning",
                "description": "Estrategia de testing",
                "method": "generate_integration_tests",
                "args": [[
                    "Feature endpoints",
                    "Data layer",
                    "Business logic"
                ]],
                "kwargs": {"language": feature_requirements.get("language", "python")}
            },
            # 3. Sakura: Technical specification
            {
                "agent_id": "sakura-004",
                "task_type": "specification",
                "description": "Especificación técnica",
                "method": "create_user_guide",
                "args": [feature_requirements]
            }
        ]
        
        return self.orchestrator.run_workflow(workflow_id, tasks)
    
    def prepare_production_deployment(self, app_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Workflow: Review de Seguridad → Kubernetes → Monitoring → Docs
        
        Args:
            app_spec: Especificaciones de la aplicación
            
        Returns:
            Configuración completa de deployment
        """
        workflow_id = self.orchestrator.create_workflow(
            name=f"Production Deployment: {app_spec.get('name', 'App')}",
            description="Preparación completa para producción",
            workflow_type="deployment"
        )
        
        tasks = [
            # 1. Hiro: Kubernetes deployment
            {
                "agent_id": "hiro-003",
                "task_type": "kubernetes",
                "description": "Diseño de deployment en Kubernetes",
                "method": "design_kubernetes_deployment",
                "args": [app_spec]
            },
            # 2. Hiro: Monitoring setup
            {
                "agent_id": "hiro-003",
                "task_type": "monitoring",
                "description": "Configuración de monitoring",
                "method": "setup_monitoring",
                "args": [[app_spec.get("name", "app")]],
                "kwargs": {"stack": "prometheus"}
            },
            # 3. Sakura: Deployment docs
            {
                "agent_id": "sakura-004",
                "task_type": "documentation",
                "description": "Documentación de deployment",
                "method": "create_user_guide",
                "args": [{
                    "name": f"{app_spec.get('name', 'App')} Deployment Guide",
                    "features": ["Kubernetes", "Monitoring", "Scaling"]
                }]
            }
        ]
        
        return self.orchestrator.run_workflow(workflow_id, tasks)
    
    def auto_generate_github_workflow(self, workflow_type: str, language: str) -> Dict[str, Any]:
        """
        Genera workflow de GitHub Actions automáticamente
        
        Args:
            workflow_type: Tipo de workflow (ci, security, deploy)
            language: Lenguaje del proyecto
            
        Returns:
            Workflow de GitHub Actions
        """
        workflow_id = self.orchestrator.create_workflow(
            name=f"Generate {workflow_type} Workflow",
            description=f"Auto-generar workflow para {language}",
            workflow_type="github_automation"
        )
        
        tasks = [
            # 1. Hiro: CI/CD pipeline
            {
                "agent_id": "hiro-003",
                "task_type": "ci_cd",
                "description": f"Crear {workflow_type} pipeline",
                "method": "create_cicd_pipeline",
                "args": [{
                    "language": language,
                    "type": workflow_type,
                    "tests": True,
                    "security_scan": workflow_type in ["ci", "security"]
                }],
                "kwargs": {"platform": "github-actions"}
            },
            # 2. Sakura: Documentation
            {
                "agent_id": "sakura-004",
                "task_type": "documentation",
                "description": "Documentar el workflow",
                "method": "create_readme",
                "args": [{
                    "name": f"{workflow_type.upper()} Workflow",
                    "description": f"Automated {workflow_type} for {language}"
                }]
            }
        ]
        
        return self.orchestrator.run_workflow(workflow_id, tasks)


def main():
    """Ejemplos de uso"""
    print("🤖 Sistema de Automatización Inteligente - Tokyo-IA\n")
    
    automation = IntelligentAutomation()
    
    # Ejemplo 1: Review completo de código
    print("\n" + "="*70)
    print("EJEMPLO 1: Review y Mejora Automática de Código")
    print("="*70)
    
    sample_code = '''
def calculate_total(items):
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    return total
'''
    
    result = automation.auto_review_and_improve_code(sample_code, "python")
    print(f"\n✅ Workflow completado: {result['workflow_name']}")
    print(f"   Tasks completadas: {result['completed_tasks']}/{result['total_tasks']}")
    
    # Ejemplo 2: Diseño de feature
    print("\n" + "="*70)
    print("EJEMPLO 2: Diseño de Nueva Feature")
    print("="*70)
    
    feature_req = {
        "name": "User Authentication System",
        "description": "OAuth2 + JWT authentication with refresh tokens",
        "language": "python",
        "scale": "10,000 concurrent users"
    }
    
    result = automation.design_and_document_feature(feature_req)
    print(f"\n✅ Diseño completado: {result['workflow_name']}")
    
    # Ejemplo 3: Preparación para producción
    print("\n" + "="*70)
    print("EJEMPLO 3: Preparación para Producción")
    print("="*70)
    
    app_spec = {
        "name": "tokyo-api",
        "image": "tokyo-api:latest",
        "port": 8080,
        "replicas": 3
    }
    
    result = automation.prepare_production_deployment(app_spec)
    print(f"\n✅ Deployment preparado: {result['workflow_name']}")


if __name__ == "__main__":
    main()
