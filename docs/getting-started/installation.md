# 📦 Installation Guide

This guide will walk you through installing Tokyo-IA on your system. Whether you're setting up a development environment or preparing for production deployment, we've got you covered.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Install (Docker)](#quick-install-docker)
- [Manual Installation](#manual-installation)
  - [macOS](#macos)
  - [Linux](#linux)
  - [Windows](#windows)
- [Database Setup](#database-setup)
- [Environment Configuration](#environment-configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

---

## Prerequisites

Before installing Tokyo-IA, ensure you have the following:

### System Requirements

- **Operating System**: macOS 10.15+, Linux (Ubuntu 20.04+, Debian 11+), or Windows 10+ with WSL2
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Disk Space**: 2GB available
- **Network**: Internet connection for package downloads

### Required Software

| Software | Minimum Version | Recommended | Purpose |
|----------|----------------|-------------|---------|
| **Go** | 1.21 | 1.22+ | Backend API server |
| **Python** | 3.10 | 3.11+ | AI agent orchestration |
| **PostgreSQL** | 14 | 16+ | Database |
| **Git** | 2.30 | Latest | Version control |

### Optional Software

- **Docker** 24.0+ & **Docker Compose** 2.20+ (for containerized deployment)
- **Make** (for build automation)
- **Node.js** 18+ (for web dashboard)
- **kubectl** 1.27+ (for Kubernetes deployment)

---

## Quick Install (Docker)

The fastest way to get Tokyo-IA running is with Docker.

### Step 1: Install Docker

If you don't have Docker installed:

**macOS/Windows:**
- Download [Docker Desktop](https://www.docker.com/products/docker-desktop)

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and back in for group changes to take effect
```

### Step 2: Clone Repository

```bash
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA
```

### Step 3: Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys (optional for development)
nano .env
```

### Step 4: Start Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- Registry API on port 8080
- Web dashboard on port 3000 (if configured)

### Step 5: Verify

```bash
curl http://localhost:8080/health
# Should return: {"status":"healthy"}
```

🎉 **Done!** Continue to [Configuration](configuration.md) or try the [Quick Start](quick-start.md).

---

## Manual Installation

For development or custom setups, install Tokyo-IA manually.

### macOS

#### 1. Install Prerequisites

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Go
brew install go

# Install Python
brew install python@3.11

# Install PostgreSQL
brew install postgresql@16
brew services start postgresql@16

# Install Make (usually pre-installed)
xcode-select --install
```

#### 2. Verify Installations

```bash
go version      # Should show go1.21 or higher
python3 --version  # Should show Python 3.10 or higher
psql --version  # Should show PostgreSQL 14 or higher
```

#### 3. Clone Repository

```bash
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA
```

#### 4. Install Go Dependencies

```bash
go mod download
go mod verify
```

#### 5. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### 6. Continue to [Database Setup](#database-setup)

---

### Linux

#### 1. Install Prerequisites

**Ubuntu/Debian:**

```bash
# Update package list
sudo apt update

# Install Go
wget https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc

# Install Python
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Install Build tools
sudo apt install -y build-essential git
```

**Fedora/RHEL/CentOS:**

```bash
# Install Go
sudo dnf install -y golang

# Install Python
sudo dnf install -y python3.11 python3-pip

# Install PostgreSQL
sudo dnf install -y postgresql-server postgresql-contrib
sudo postgresql-setup --initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Install build tools
sudo dnf install -y make git
```

#### 2. Verify Installations

```bash
go version
python3 --version
psql --version
```

#### 3. Clone and Setup

```bash
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA

# Install Go dependencies
go mod download

# Install Python dependencies
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Continue to [Database Setup](#database-setup)

---

### Windows

For Windows, we recommend using WSL2 (Windows Subsystem for Linux).

#### Option 1: WSL2 (Recommended)

1. **Install WSL2**

```powershell
# Run in PowerShell as Administrator
wsl --install
# Restart your computer
```

2. **Install Ubuntu from Microsoft Store**

3. **Follow Linux installation instructions above in your WSL2 terminal**

#### Option 2: Native Windows

1. **Install Go**
   - Download from [go.dev/dl](https://go.dev/dl/)
   - Run installer
   - Add to PATH if not automatic

2. **Install Python**
   - Download from [python.org](https://www.python.org/downloads/)
   - Check "Add Python to PATH" during installation

3. **Install PostgreSQL**
   - Download from [postgresql.org](https://www.postgresql.org/download/windows/)
   - Run installer
   - Remember the password you set for postgres user

4. **Install Git**
   - Download from [git-scm.com](https://git-scm.com/download/win)

5. **Clone and Setup**

```powershell
git clone https://github.com/Melampe001/Tokyo-IA.git
cd Tokyo-IA

# Install Go dependencies
go mod download

# Install Python dependencies
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Database Setup

### Step 1: Create Database

**macOS/Linux:**

```bash
# Create database
createdb tokyoia

# Or using psql
psql -U postgres
CREATE DATABASE tokyoia;
\q
```

**Windows:**

```powershell
# Using psql (enter your postgres password when prompted)
psql -U postgres
CREATE DATABASE tokyoia;
\q
```

### Step 2: Run Schema

```bash
# Apply database schema
psql tokyoia < db/schema.sql

# Or if you have a password-protected postgres user
psql -U postgres -d tokyoia < db/schema.sql
```

### Step 3: Verify Database

```bash
psql tokyoia -c "\dt"
```

You should see tables like: `agents`, `workflows`, `agent_tasks`, `agent_metrics`, etc.

### Step 4: Seed Initial Data (Optional)

```bash
# Load the five agents into database
psql tokyoia < db/seed_agents.sql
```

---

## Environment Configuration

### Step 1: Create Environment File

```bash
cp .env.example .env
```

### Step 2: Configure Database URL

Edit `.env`:

```bash
# Database connection
DATABASE_URL="postgresql://postgres:password@localhost:5432/tokyoia"

# Or for local development without password
DATABASE_URL="postgresql://localhost:5432/tokyoia"
```

### Step 3: Configure API Keys

Add your LLM provider API keys:

```bash
# Required for agent functionality
ANTHROPIC_API_KEY="sk-ant-..."      # For Akira (Claude)
OPENAI_API_KEY="sk-..."             # For Yuki & Kenji
GROQ_API_KEY="gsk_..."              # For Hiro (Llama)
GOOGLE_API_KEY="..."                # For Sakura (Gemini)

# Optional: Registry API configuration
PORT=8080
REGISTRY_API_URL="http://localhost:8080"
```

**💡 Tip**: You can start development without API keys by using mock responses. See [Configuration Guide](configuration.md) for details.

### Step 4: Set Environment Variables

**macOS/Linux:**

```bash
export $(cat .env | xargs)
```

Or add to your shell profile:

```bash
echo 'export DATABASE_URL="postgresql://localhost:5432/tokyoia"' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell):**

```powershell
Get-Content .env | ForEach-Object {
    $name, $value = $_.split('=')
    [Environment]::SetEnvironmentVariable($name, $value, "User")
}
```

---

## Verification

### Step 1: Build the Application

```bash
make build
```

This compiles:
- `bin/tokyo-ia` - Main application
- `bin/registry-api` - REST API server

### Step 2: Run Tests

```bash
# Go tests
make test

# Python tests (in virtual environment)
pytest lib/
```

### Step 3: Start the API Server

```bash
./bin/registry-api
# Or: go run ./cmd/registry-api/main.go
```

You should see:

```
🚀 Registry API server starting...
📊 Database: Connected
🌐 Server: Listening on :8080
✅ Ready to serve requests
```

### Step 4: Test API Endpoints

```bash
# Health check
curl http://localhost:8080/health

# List agents
curl http://localhost:8080/api/agents
```

### Step 5: Run Agent Example (Optional)

```bash
# Activate Python venv
source venv/bin/activate

# Run example
python examples/python/basic_agent.py
```

---

## Troubleshooting

### Issue: "go: command not found"

**Solution**: Go is not in PATH.

```bash
# macOS/Linux
export PATH=$PATH:/usr/local/go/bin
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc

# Verify
go version
```

### Issue: "python3: command not found"

**Solution**: Python is not installed or not in PATH.

```bash
# macOS
brew install python@3.11

# Linux
sudo apt install python3.11

# Windows
# Reinstall Python and check "Add to PATH"
```

### Issue: "createdb: command not found"

**Solution**: PostgreSQL client tools not in PATH.

```bash
# macOS
export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"

# Linux
sudo apt install postgresql-client
```

### Issue: "psql: could not connect to server"

**Solution**: PostgreSQL service not running.

```bash
# macOS
brew services start postgresql@16

# Linux
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Check status
brew services list  # macOS
systemctl status postgresql  # Linux
```

### Issue: "permission denied" when creating database

**Solution**: Need to create database as postgres user.

```bash
# Become postgres user
sudo -u postgres createdb tokyoia

# Or create postgres role for your user
sudo -u postgres createuser -s $USER
```

### Issue: "database 'tokyoia' already exists"

**Solution**: Database was already created. You can drop and recreate it:

```bash
dropdb tokyoia
createdb tokyoia
psql tokyoia < db/schema.sql
```

### Issue: Build fails with "package not found"

**Solution**: Dependencies need to be downloaded.

```bash
go mod download
go mod tidy
go mod verify
```

### Issue: Python package installation fails

**Solution**: Upgrade pip and try again.

```bash
python3 -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Issue: Port 8080 already in use

**Solution**: Change port or kill process using it.

```bash
# Change port in .env
PORT=8081

# Or find and kill process
lsof -ti:8080 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8080   # Windows (note PID and use Task Manager)
```

---

## Next Steps

Now that Tokyo-IA is installed:

1. **[Quick Start Guide](quick-start.md)** - Run your first agent workflow
2. **[Configuration Guide](configuration.md)** - Learn about all configuration options
3. **[User Guide](../guides/user-guide.md)** - Detailed usage instructions
4. **[API Reference](../api/rest-api.md)** - Explore the REST API

---

## Getting Help

- 📖 [FAQ](../guides/faq.md) - Common questions and answers
- 🐛 [Report Issues](https://github.com/Melampe001/Tokyo-IA/issues) - Found a bug?
- 💬 [Discussions](https://github.com/Melampe001/Tokyo-IA/discussions) - Ask questions
- 📧 support@tokyo-ia.example.com - Email support

---

*Last updated: 2025-12-23*
