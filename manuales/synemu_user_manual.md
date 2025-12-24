# SYNEMU Suite User Manual

**Version:** 1.0.0  
**Last Updated:** December 2024  
**Organization:** TokyoApps® / TokRaggcorp®

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Core Components](#core-components)
4. [Agent Usage](#agent-usage)
5. [Workflows](#workflows)
6. [Configuration](#configuration)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)
9. [Support](#support)

---

## 1. Introduction

### What is SYNEMU Suite?

SYNEMU Suite is a premium, fully automated platform module for:
- **SIM**ulation and emulation (2D/3D)
- **E**mulation environments
- **M**ulti-agent orchestration
- **U**nified automation workflows

The suite consists of 7 specialized AI agents that work together to provide comprehensive simulation, testing, documentation, and asset management capabilities.

### Key Features

- 🔥 **2D Flare Agent** - 2D physics simulation and sprite animation
- 🎮 **3D Unity Agent** - 3D scene creation and Unity integration
- 🎬 **Video Viz Agent** - Video rendering and visualization
- 🦉 **QA Owl Agent** - Quality assurance and automated testing
- ⚖️ **Docu Libra Agent** - Automated documentation generation
- 🗺️ **Asset Atlas Agent** - Asset management and CDN deployment
- 🎭 **Orchestrator** - Multi-agent workflow coordination

### System Requirements

**Minimum Requirements:**
- Python 3.11 or higher
- 8GB RAM
- 10GB available disk space
- Internet connection for API access

**Recommended Requirements:**
- Python 3.12
- 16GB+ RAM
- 50GB+ available disk space (for asset storage)
- High-speed internet connection

---

## 2. Getting Started

### Installation

#### Step 1: Install Python Dependencies

```bash
# Navigate to project directory
cd /path/to/Tokyo-IA

# Install required packages
pip install -r requirements.txt
```

#### Step 2: Configure Environment Variables

Create a `.env` file in your project root:

```bash
# LLM Provider API Keys
ANTHROPIC_API_KEY="sk-ant-your-key-here"
OPENAI_API_KEY="sk-your-key-here"
GROQ_API_KEY="gsk_your-key-here"
GOOGLE_API_KEY="your-google-key-here"

# SYNEMU Specific Configuration
SYNEMU_UNITY_API_KEY="your-unity-key"
SYNEMU_FLARE_API_KEY="your-flare-key"
SYNEMU_VIDEO_API_KEY="your-video-key"
SYNEMU_ASSET_STORAGE_KEY="your-storage-key"

# Database (optional)
DATABASE_URL="postgresql://user:pass@localhost:5432/synemu"
REDIS_URL="redis://localhost:6379"
```

**⚠️ SECURITY WARNING:** Never commit API keys to version control!

#### Step 3: Verify Installation

```bash
# Test the orchestrator
python SYNEMU/agents_bots/synemu_orchestrator.py

# Test individual agents
python SYNEMU/agents_bots/synemu_agent2d_flare.py
```

### Quick Start Example

```python
from SYNEMU.agents_bots import (
    SynemuOrchestrator,
    Synemu2DFlareAgent,
    get_integrations
)

# Initialize integrations
integrations = get_integrations()

# Create orchestrator
orchestrator = SynemuOrchestrator()

# Get agent status
status = orchestrator.get_agent_status()
print(f"Active agents: {len(status['agents'])}")

# Create a 2D simulation
agent_2d = Synemu2DFlareAgent()
scene_id = agent_2d.create_scene(width=800, height=600)
agent_2d.add_sprite(scene_id, position=(100, 100), size=(50, 50))
result = agent_2d.run_simulation(scene_id, duration=5.0)
```

---

## 3. Core Components

### SYNEMU Integrations

The integration module manages all API keys and external service connections.

**Features:**
- Centralized credential management
- Automatic feature detection
- Secure environment variable handling
- Configuration validation

**Usage:**
```python
from SYNEMU.agents_bots import get_integrations

integrations = get_integrations()

# Check if features are available
if integrations.is_feature_enabled('llm'):
    llm_config = integrations.get_llm_config('openai')
    print(f"Using model: {llm_config['model']}")
```

### SYNEMU Orchestrator

The orchestrator coordinates multiple agents for complex workflows.

**Capabilities:**
- Task creation and assignment
- Multi-agent workflow execution
- Task status tracking
- Agent coordination

**Example:**
```python
from SYNEMU.agents_bots import SynemuOrchestrator, TaskType

orchestrator = SynemuOrchestrator()

# Create a task
task_id = orchestrator.create_task(
    TaskType.SIMULATION_2D,
    parameters={'width': 1920, 'height': 1080}
)

# Execute a workflow
result = orchestrator.execute_workflow(
    'full_simulation',
    parameters={'simulation_type': '2d'}
)
```

---

## 4. Agent Usage

### 2D Flare Agent

**Purpose:** 2D physics simulation and sprite-based animation.

**Creating a Scene:**
```python
from SYNEMU.agents_bots import Synemu2DFlareAgent

agent = Synemu2DFlareAgent()
scene_id = agent.create_scene(width=1920, height=1080)
```

**Adding Sprites:**
```python
sprite_id = agent.add_sprite(
    scene_id,
    position=(100, 500),
    size=(50, 50),
    texture="assets/ball.png"
)
```

**Running Simulation:**
```python
result = agent.run_simulation(
    scene_id,
    duration=10.0,
    record=True  # Record frames for video
)
```

### 3D Unity Agent

**Purpose:** 3D scene creation and Unity project generation.

**Creating a Scene:**
```python
from SYNEMU.agents_bots import Synemu3DUnityAgent, PrimitiveType

agent = Synemu3DUnityAgent()
scene_id = agent.create_scene("GameScene", camera_position=(5, 3, -10))
```

**Adding Objects:**
```python
# Add ground plane
agent.add_game_object(
    scene_id,
    "Ground",
    PrimitiveType.PLANE,
    position=(0, 0, 0),
    scale=(10, 1, 10)
)

# Add player capsule
agent.add_game_object(
    scene_id,
    "Player",
    PrimitiveType.CAPSULE,
    position=(0, 1, 0),
    physics_enabled=True
)
```

**Exporting Unity Project:**
```python
unity_project = agent.export_unity_project(scene_id)
```

### Video Viz Agent

**Purpose:** Video rendering and visualization.

**Creating a Video Project:**
```python
from SYNEMU.agents_bots import SynemuVideoVizAgent, VideoFormat

agent = SynemuVideoVizAgent()
project_id = agent.create_project(
    "Demo Video",
    width=1920,
    height=1080,
    fps=60,
    format=VideoFormat.MP4
)
```

**Rendering Video:**
```python
result = agent.render_video(
    project_id,
    output_path="output/demo.mp4"
)
```

### QA Owl Agent

**Purpose:** Automated testing and quality assurance.

**Creating Test Suite:**
```python
from SYNEMU.agents_bots import SynemuQAOwlAgent, TestType

agent = SynemuQAOwlAgent()
suite_id = agent.create_test_suite("Integration Tests")

# Add test cases
agent.add_test_case(suite_id, "test_2d_simulation", TestType.INTEGRATION)
agent.add_test_case(suite_id, "test_video_render", TestType.E2E)
```

**Running Tests:**
```python
result = agent.run_test_suite(suite_id)
print(f"Passed: {result['passed']}/{result['total_tests']}")

# Analyze coverage
coverage = agent.analyze_coverage(suite_id)
print(f"Coverage: {coverage['line_coverage']:.1f}%")
```

### Docu Libra Agent

**Purpose:** Automated documentation generation.

**Generating API Documentation:**
```python
from SYNEMU.agents_bots import SynemuDocuLibraAgent

agent = SynemuDocuLibraAgent()

api_spec = {
    "title": "SYNEMU API",
    "endpoints": [
        {
            "method": "POST",
            "path": "/api/simulate",
            "description": "Run a simulation"
        }
    ]
}

project_id = agent.generate_api_documentation(api_spec)
agent.export_documentation(project_id, "docs/api.md")
```

### Asset Atlas Agent

**Purpose:** Asset management and CDN deployment.

**Uploading Assets:**
```python
from SYNEMU.agents_bots import SynemuAssetAtlasAgent, AssetType

agent = SynemuAssetAtlasAgent()

asset_id = agent.upload_asset(
    "/path/to/logo.png",
    AssetType.IMAGE,
    tags=["branding", "logo"]
)

# Deploy to CDN
cdn_url = agent.deploy_to_cdn(asset_id)
print(f"Asset available at: {cdn_url}")
```

---

## 5. Workflows

### Full Simulation Workflow

This workflow combines 2D/3D simulation, QA testing, and documentation:

```python
orchestrator = SynemuOrchestrator()

result = orchestrator.execute_workflow(
    'full_simulation',
    parameters={
        'simulation_type': '2d',
        'width': 1920,
        'height': 1080,
        'duration': 10.0
    }
)

# Check workflow stages
for stage in result['stages']:
    print(f"{stage['stage']}: {stage['task_id']}")
```

### Asset Deployment Workflow

```python
result = orchestrator.execute_workflow(
    'asset_deployment',
    parameters={
        'assets': ['asset-001', 'asset-002'],
        'target': 'cdn'
    }
)
```

---

## 6. Configuration

### Environment Variables

All sensitive configuration is managed through environment variables. See the complete list in the [Getting Started](#getting-started) section.

### Agent Configuration

Each agent can be configured through the integrations module:

```python
integrations = get_integrations()

# Get simulation configuration
sim_config = integrations.get_simulation_config('2d')
print(f"Max instances: {sim_config['max_instances']}")

# Get asset configuration
asset_config = integrations.get_asset_config()
print(f"Max file size: {asset_config['max_file_size_mb']}MB")
```

---

## 7. Troubleshooting

### Common Issues

#### Issue: "API key not found"

**Solution:** Ensure all required environment variables are set:
```bash
# Check if variables are set
echo $ANTHROPIC_API_KEY
echo $OPENAI_API_KEY
```

#### Issue: "Agent not enabled"

**Solution:** Check agent status and enable required features:
```python
orchestrator = SynemuOrchestrator()
status = orchestrator.get_agent_status()

for agent_id, agent_info in status['agents'].items():
    print(f"{agent_id}: {'✓' if agent_info['enabled'] else '✗'}")
```

#### Issue: "Module import error"

**Solution:** Ensure you're in the correct directory and Python path is set:
```bash
export PYTHONPATH=/path/to/Tokyo-IA:$PYTHONPATH
```

---

## 8. Best Practices

### Security

1. **Never hardcode API keys** - Always use environment variables
2. **Use .gitignore** - Ensure `.env` files are not committed
3. **Rotate keys regularly** - Update API keys periodically
4. **Limit permissions** - Use least-privilege access for API keys

### Performance

1. **Batch operations** - Process multiple items together when possible
2. **Use async rendering** - For large video projects, use async mode
3. **Optimize assets** - Use the Asset Atlas optimization features
4. **Monitor resources** - Track memory and CPU usage during simulations

### Code Organization

1. **Modular workflows** - Break complex workflows into smaller tasks
2. **Error handling** - Always wrap agent calls in try-except blocks
3. **Logging** - Enable appropriate logging levels for debugging
4. **Documentation** - Document custom workflows and configurations

---

## 9. Support

### Getting Help

- **Documentation:** This manual and API documentation
- **Technical Support:** support@tokyoapps.com
- **Emergency Support:** emergency@tokyoapps.com (24/7)
- **Community Forum:** forum.tokyoapps.com

### Reporting Issues

When reporting issues, include:
1. SYNEMU Suite version
2. Python version
3. Error messages and stack traces
4. Steps to reproduce the issue
5. Expected vs actual behavior

### Training & Consulting

For training sessions or consulting services:
- **Email:** consulting@tokyoapps.com
- **Website:** www.tokyoapps.com/training

---

**© TokyoApps® / TokRaggcorp® 2024**  
**SYNEMU Suite - All Rights Reserved**

---

*This manual is continually updated. Check the website for the latest version.*
