# SYNEMU Quick Start Guide

**Time Required:** 15 minutes  
**Skill Level:** Beginner  
**Prerequisites:** Python 3.11+, pip installed

---

## Step 1: Install Dependencies (5 minutes)

### 1.1 Clone or Navigate to Project

```bash
cd /path/to/Tokyo-IA
```

### 1.2 Install Python Packages

```bash
pip install -r requirements.txt
```

**Expected packages:**
- crewai
- anthropic
- openai
- dataclasses
- python-dotenv

---

## Step 2: Configure API Keys (3 minutes)

### 2.1 Create `.env` File

```bash
# In project root
touch .env
```

### 2.2 Add Your API Keys

Edit `.env` and add:

```bash
# Required: At least one LLM provider
OPENAI_API_KEY="sk-your-openai-key-here"

# Optional: Additional providers
ANTHROPIC_API_KEY="sk-ant-your-key-here"
GROQ_API_KEY="gsk_your-key-here"
GOOGLE_API_KEY="your-google-key-here"

# Optional: SYNEMU features
SYNEMU_UNITY_API_KEY="your-unity-key"
SYNEMU_FLARE_API_KEY="your-flare-key"
```

**⚠️ Important:** Never commit this file to Git!

---

## Step 3: Test Installation (2 minutes)

### 3.1 Run Orchestrator Test

```bash
python SYNEMU/agents_bots/synemu_orchestrator.py
```

**Expected output:**
```
🎭 SYNEMU Orchestrator v1.0.0
=============================================
Active Tasks: 0
Registered Agents (X):
  ✓ SYNEMU 2D Flare Agent
  ✓ SYNEMU 3D Unity Agent
  ...
```

### 3.2 Verify Agent Status

```python
from SYNEMU.agents_bots import SynemuOrchestrator

orchestrator = SynemuOrchestrator()
status = orchestrator.get_agent_status()

print(f"Enabled agents: {sum(1 for a in status['agents'].values() if a['enabled'])}")
```

---

## Step 4: Run Your First Simulation (5 minutes)

### 4.1 Create a 2D Scene

```python
from SYNEMU.agents_bots import Synemu2DFlareAgent

# Initialize agent
agent = Synemu2DFlareAgent()

# Create scene
scene_id = agent.create_scene(width=800, height=600)
print(f"Created scene: {scene_id}")

# Add sprites
agent.add_sprite(scene_id, position=(100, 500), size=(50, 50))
agent.add_sprite(scene_id, position=(200, 500), size=(50, 50))

# Run simulation
result = agent.run_simulation(scene_id, duration=5.0)
print(f"Simulated {result['steps']} steps")
```

### 4.2 Expected Output

```
🔥 SYNEMU 2D Flare Agent v1.0.0 initialized
Created scene: scene2d-20241224001234
Added sprite sprite-0000 to scene scene2d-20241224001234
Added sprite sprite-0001 to scene scene2d-20241224001234
Running simulation for 5.0s (312 steps)
Simulated 312 steps
```

---

## Step 5: Next Steps

### Explore More Features

1. **3D Simulation:** Try `synemu_agent3d_unity.py`
2. **Video Rendering:** Try `synemu_agent_video_viz.py`
3. **QA Testing:** Try `synemu_qa_owl.py`
4. **Documentation:** Try `synemu_docu_libra.py`

### Learn Workflows

```python
from SYNEMU.agents_bots import SynemuOrchestrator

orchestrator = SynemuOrchestrator()

# Run a complete workflow
result = orchestrator.execute_workflow(
    'full_simulation',
    parameters={'simulation_type': '2d'}
)

print("Workflow stages:")
for stage in result['stages']:
    print(f"  - {stage['stage']}: {stage['task_id']}")
```

### Read Full Documentation

- **User Manual:** `manuales/synemu_user_manual.md`
- **API Docs:** `SYNEMU/docs/api_reference.md`
- **Examples:** `examples/` directory

---

## Troubleshooting

### Problem: Import errors

**Solution:**
```bash
export PYTHONPATH=/path/to/Tokyo-IA:$PYTHONPATH
```

### Problem: "API key not found"

**Solution:** Check your `.env` file and ensure it's in the project root.

### Problem: Agent shows as disabled

**Solution:** The agent requires specific API keys. Check which keys are needed:
```python
from SYNEMU.agents_bots import get_integrations

integrations = get_integrations()
print(integrations.is_feature_enabled('2d_simulation'))
```

---

## Getting Help

- **Email:** support@tokyoapps.com
- **Docs:** Full user manual in `manuales/`
- **Examples:** Check `examples/` for code samples

---

**Congratulations! 🎉**

You've successfully set up SYNEMU Suite and run your first simulation!

---

**© TokyoApps® / TokRaggcorp® 2024**
