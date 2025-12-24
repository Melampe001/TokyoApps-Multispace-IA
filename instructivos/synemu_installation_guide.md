# SYNEMU Installation Guide

**Version:** 1.0.0  
**Platform:** Linux, macOS, Windows  
**Audience:** System Administrators, DevOps Engineers

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Pre-Installation Steps](#pre-installation-steps)
3. [Installation Methods](#installation-methods)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## 1. System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Linux (Ubuntu 20.04+), macOS 11+, Windows 10+ |
| **Python** | 3.11 or higher |
| **RAM** | 8GB |
| **Disk Space** | 10GB free |
| **Network** | Internet connection for API access |

### Recommended Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Linux (Ubuntu 22.04+), macOS 13+ |
| **Python** | 3.12 |
| **RAM** | 16GB or more |
| **Disk Space** | 50GB+ (for asset storage) |
| **CPU** | 4+ cores |
| **Network** | High-speed connection (100+ Mbps) |

### Software Dependencies

- **Python packages:** Listed in `requirements.txt`
- **Optional:** Docker for containerized deployment
- **Optional:** PostgreSQL for database features
- **Optional:** Redis for caching

---

## 2. Pre-Installation Steps

### 2.1 Install Python

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip
```

#### macOS (using Homebrew)
```bash
brew install python@3.12
```

#### Windows
Download from [python.org](https://www.python.org/downloads/) and run installer.

### 2.2 Verify Python Installation

```bash
python3 --version
# Expected: Python 3.11.x or 3.12.x

pip3 --version
# Should show pip version
```

### 2.3 Install Git (if not already installed)

```bash
# Ubuntu/Debian
sudo apt install git

# macOS
brew install git

# Windows
# Download from git-scm.com
```

---

## 3. Installation Methods

### Method 1: Standard Installation (Recommended)

#### Step 1: Clone Repository

```bash
# If you have repository access
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA
```

#### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

#### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Verify Installation

```bash
python -c "from SYNEMU.agents_bots import SynemuOrchestrator; print('✓ SYNEMU installed')"
```

### Method 2: Docker Installation

#### Step 1: Build Docker Image

```bash
docker build -t synemu-suite:latest .
```

#### Step 2: Run Container

```bash
docker run -it \
  -e OPENAI_API_KEY="your-key" \
  -v $(pwd)/data:/data \
  synemu-suite:latest
```

### Method 3: System-Wide Installation

**⚠️ Not recommended for production**

```bash
pip install -r requirements.txt
```

---

## 4. Configuration

### 4.1 Environment Variables

Create `.env` file in project root:

```bash
# Copy example file
cp .env.example .env

# Edit with your keys
nano .env
```

Required variables:

```bash
# LLM Providers (at least one required)
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-ant-..."
GROQ_API_KEY="gsk_..."
GOOGLE_API_KEY="..."

# Optional: SYNEMU Features
SYNEMU_UNITY_API_KEY="..."
SYNEMU_FLARE_API_KEY="..."
SYNEMU_VIDEO_API_KEY="..."
SYNEMU_ASSET_STORAGE_KEY="..."

# Optional: Database
DATABASE_URL="postgresql://user:pass@localhost:5432/synemu"
REDIS_URL="redis://localhost:6379"

# Optional: Monitoring
DATADOG_API_KEY="..."
SENTRY_DSN="..."
```

### 4.2 Configuration File

Create `synemu_config.yaml` (optional):

```yaml
synemu:
  version: "1.0.0"
  
  agents:
    2d_flare:
      enabled: true
      max_scenes: 10
    3d_unity:
      enabled: true
      max_scenes: 5
    video_viz:
      enabled: true
      max_projects: 5
    qa_owl:
      enabled: true
    docu_libra:
      enabled: true
    asset_atlas:
      enabled: true
      max_assets: 1000
  
  orchestrator:
    max_concurrent_tasks: 10
    task_timeout: 3600
  
  logging:
    level: INFO
    file: /var/log/synemu/synemu.log
```

### 4.3 Database Setup (Optional)

If using PostgreSQL:

```bash
# Create database
createdb synemu

# Run migrations (if applicable)
psql synemu < db/schema.sql
```

---

## 5. Verification

### 5.1 Test All Agents

```bash
# Test orchestrator
python SYNEMU/agents_bots/synemu_orchestrator.py

# Test individual agents
python SYNEMU/agents_bots/synemu_agent2d_flare.py
python SYNEMU/agents_bots/synemu_agent3d_unity.py
python SYNEMU/agents_bots/synemu_agent_video_viz.py
python SYNEMU/agents_bots/synemu_qa_owl.py
python SYNEMU/agents_bots/synemu_docu_libra.py
python SYNEMU/agents_bots/synemu_asset_atlas.py
```

### 5.2 Run Integration Test

```python
from SYNEMU.agents_bots import (
    SynemuOrchestrator,
    get_integrations
)

# Test integrations
integrations = get_integrations()
print("✓ Integrations loaded")

# Test orchestrator
orchestrator = SynemuOrchestrator()
status = orchestrator.get_agent_status()
print(f"✓ Orchestrator: {len(status['agents'])} agents registered")

# Check enabled agents
enabled = sum(1 for a in status['agents'].values() if a['enabled'])
print(f"✓ {enabled} agents enabled")
```

### 5.3 Verify File Permissions

```bash
# Ensure directories are writable
mkdir -p data logs output
chmod 755 data logs output
```

---

## 6. Troubleshooting

### Issue: Python version too old

```bash
# Check version
python3 --version

# If < 3.11, install newer version
sudo apt install python3.12
```

### Issue: Module not found

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

### Issue: Permission denied

```bash
# Fix ownership
sudo chown -R $USER:$USER /path/to/Tokyo-IA

# Fix permissions
chmod -R 755 /path/to/Tokyo-IA
```

### Issue: API key errors

```bash
# Verify .env file exists
ls -la .env

# Check if environment variables are loaded
python -c "import os; print(os.environ.get('OPENAI_API_KEY', 'NOT SET'))"

# If using docker, ensure -e flags are correct
```

### Issue: Out of memory

```bash
# Check memory usage
free -h

# Reduce concurrent operations
# Edit synemu_config.yaml:
# orchestrator.max_concurrent_tasks: 5
```

---

## Post-Installation

### Set Up Monitoring (Optional)

```bash
# Install monitoring tools
pip install datadog sentry-sdk

# Configure in .env
DATADOG_API_KEY="your-key"
SENTRY_DSN="your-dsn"
```

### Enable Auto-Start (Linux)

Create systemd service:

```bash
sudo nano /etc/systemd/system/synemu.service
```

```ini
[Unit]
Description=SYNEMU Suite
After=network.target

[Service]
Type=simple
User=synemu
WorkingDirectory=/opt/Tokyo-IA
Environment="PATH=/opt/Tokyo-IA/venv/bin"
ExecStart=/opt/Tokyo-IA/venv/bin/python -m SYNEMU.agents_bots.synemu_orchestrator
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable service:

```bash
sudo systemctl enable synemu
sudo systemctl start synemu
sudo systemctl status synemu
```

---

## Security Recommendations

1. **Never commit `.env` files** - Add to `.gitignore`
2. **Use secrets management** - Consider Vault or AWS Secrets Manager
3. **Rotate keys regularly** - Update API keys every 90 days
4. **Restrict file permissions** - `chmod 600 .env`
5. **Use HTTPS** - For API communications
6. **Enable logging** - Monitor for suspicious activity

---

## Next Steps

- Read the [User Manual](../manuales/synemu_user_manual.md)
- Follow the [Quick Start Guide](synemu_quick_start.md)
- Explore [Examples](../../examples/)
- Configure [Workflows](synemu_workflow_guide.md)

---

## Support

**Installation Issues:**
- Email: support@tokyoapps.com
- Documentation: docs.tokyoapps.com
- Forum: forum.tokyoapps.com

**Enterprise Support:**
- Email: enterprise@tokyoapps.com
- Phone: Available upon request

---

**© TokyoApps® / TokRaggcorp® 2024**  
**SYNEMU Suite Installation Guide v1.0.0**
