#!/bin/bash
# Quick setup script for Tokyo-IA Agent System
# Run: ./quick_setup.sh

set -e

echo "🚀 Tokyo-IA Quick Setup Script"
echo "================================"
echo ""

# Check Python version
echo "📋 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip -q
pip install groq google-generativeai python-dotenv -q
echo "✅ Dependencies installed"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "🔑 Please edit .env and add your API keys:"
    echo "   - GROQ_API_KEY"
    echo "   - GOOGLE_API_KEY"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Test Groq API
echo "🛡️  Testing Groq API (Hiro)..."
if [ -n "$GROQ_API_KEY" ]; then
    python3 test_groq_manual.py
else
    echo "⚠️  GROQ_API_KEY not set in .env"
fi
echo ""

# Test Google API
echo "🌸 Testing Google AI API (Sakura)..."
if [ -n "$GOOGLE_API_KEY" ]; then
    python3 test_google_manual.py
else
    echo "⚠️  GOOGLE_API_KEY not set in .env"
fi
echo ""

echo "================================"
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Edit .env with your API keys if you haven't"
echo "   2. Run tests: python test_groq_manual.py"
echo "   3. Wait for PR #127 to complete with full agent system"
echo ""
echo "🔗 Monitor PR: gh pr view 127 --web"
