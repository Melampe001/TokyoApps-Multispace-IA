#!/usr/bin/env python3
"""
🗼 Tokyo-IA CLI
Interfaz de línea de comandos para automatización con agentes
"""

import click
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.intelligent_automation import IntelligentAutomation


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """🗼 Tokyo-IA Agent Automation CLI"""
    pass


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--language', '-l', default='python', help='Programming language')
@click.option('--output', '-o', type=click.Path(), help='Output file for results')
def review(file_path, language, output):
    """Review code with all agents (Security → Tests → CI/CD → Docs)"""
    
    click.echo(f"🔍 Reviewing {file_path}...")
    
    # Read code
    with open(file_path, 'r') as f:
        code = f.read()
    
    # Run automation
    automation = IntelligentAutomation()
    result = automation.auto_review_and_improve_code(code, language)
    
    # Display results
    click.echo(f"\n✅ Review completed!")
    click.echo(f"   Tasks: {result['completed_tasks']}/{result['total_tasks']}")
    
    # Save if requested
    if output:
        with open(output, 'w') as f:
            json.dump(result, f, indent=2)
        click.echo(f"📄 Results saved to {output}")


@cli.command()
@click.option('--name', '-n', required=True, help='Feature name')
@click.option('--description', '-d', required=True, help='Feature description')
@click.option('--language', '-l', default='python', help='Programming language')
@click.option('--output', '-o', type=click.Path(), help='Output file')
def design(name, description, language, output):
    """Design new feature (Architecture → Tests → Docs)"""
    
    click.echo(f"🏗️ Designing feature: {name}...")
    
    requirements = {
        "name": name,
        "description": description,
        "language": language
    }
    
    automation = IntelligentAutomation()
    result = automation.design_and_document_feature(requirements)
    
    click.echo(f"\n✅ Design completed!")
    
    if output:
        with open(output, 'w') as f:
            json.dump(result, f, indent=2)
        click.echo(f"📄 Results saved to {output}")


@cli.command()
@click.option('--name', '-n', required=True, help='Application name')
@click.option('--image', '-i', required=True, help='Docker image')
@click.option('--port', '-p', default=8080, help='Application port')
@click.option('--output', '-o', type=click.Path(), help='Output file')
def deploy(name, image, port, output):
    """Prepare production deployment (K8s → Monitoring → Docs)"""
    
    click.echo(f"🚀 Preparing deployment for: {name}...")
    
    app_spec = {
        "name": name,
        "image": image,
        "port": port,
        "replicas": 3
    }
    
    automation = IntelligentAutomation()
    result = automation.prepare_production_deployment(app_spec)
    
    click.echo(f"\n✅ Deployment prepared!")
    
    if output:
        with open(output, 'w') as f:
            json.dump(result, f, indent=2)
        click.echo(f"📄 Results saved to {output}")


@cli.command()
def agents():
    """List all available agents"""
    
    automation = IntelligentAutomation()
    agents_list = automation.orchestrator.list_available_agents()
    
    click.echo("\n🤖 Available Tokyo-IA Agents:\n")
    
    for agent_id, info in agents_list.items():
        status = "✅" if info['initialized'] else "❌"
        click.echo(f"{status} {info['emoji']} {info['name']}")
        click.echo(f"   Role: {info['role']}")
        click.echo(f"   Specialties: {', '.join(info['specialties'])}")
        click.echo()


if __name__ == '__main__':
    cli()
