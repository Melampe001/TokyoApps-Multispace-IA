# Code Documentation Summary

This file contains automatically extracted documentation from code files.

## Go Files
### ./admin/hello.go
// Package admin provides admin functionality for Tokyo-IA.

### ./testing/placeholder_test.go
// Package testing provides test utilities for Tokyo-IA.

### ./internal/ai/types.go
// Package ai provides AI model integration and orchestration functionality.

### ./internal/ai/metrics.go
// Package ai provides metrics collection for AI model usage.

### ./internal/ai/model_router.go
// Package ai provides the model router for intelligent AI model selection.

### ./internal/ai/model_router_test.go
// Package ai provides tests for the model router.

### ./internal/ai/cache.go
// Package ai provides caching functionality for AI model responses.

### ./internal/ai/ai_test.go
// Package ai provides tests for the AI module.

### ./internal/ai/clients/mock_client.go
// Package clients provides AI model client implementations.

### ./internal/ai/ai.go
// Package ai provides AI-related functionality for Tokyo-IA.
// Este paquete contiene la lógica central de IA del sistema.
// Se puede extender para incluir modelos de ML, procesamiento de lenguaje natural, etc.

## Python Files
### ./examples/python/basic_agent.py
"""
Tokyo-IA Basic Agent Example

This script demonstrates basic usage of CrewAI with Groq LLM inference.
It creates a Tokyo travel expert agent that provides recommendations.

Requirements:
- GROQ_API_KEY environment variable must be set
- Install dependencies: pip install -r requirements.txt

Usage:

### ./examples/orchestration_demo.py
"""
Tokyo-IA Agent Orchestration - Example Usage

This script demonstrates how to use the Tokyo-IA agent orchestration system.

Prerequisites:
1. PostgreSQL database running with schema loaded
2. Registry API server running on localhost:8080
3. API keys set as environment variables

Usage:

### ./scripts/generate_agent_report.py
"""
📊 Generador de Reportes de Agentes
Convierte resultados JSON en reportes Markdown legibles
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

# Constants

### ./.github/workflows/scripts/library_cataloger.py
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

### ./.github/workflows/scripts/library_search.py
"""
Library Search - CLI tool for searching the library catalog
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime



### ./.github/workflows/bots/scripts/check_dependencies.py
"""
Dependency Agent - Validates pubspec.yaml dependencies
Only allows specific whitelisted dependencies.
"""

import sys
import yaml
from pathlib import Path
from typing import List, Dict, Set, Tuple

# ALLOWED DEPENDENCIES - This is the whitelist

### ./.github/workflows/bots/scripts/analyze_go_code.py
"""
Backend Code Quality Analyzer for Go code.
Analyzes Go code for quality metrics: tests, documentation, error handling, imports.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

### ./.github/workflows/bots/scripts/analyze_dart_code.py
"""
Frontend Dart/Flutter Code Analyzer.
Analyzes Dart code for naming conventions, hardcoded strings, theme usage.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

### ./.github/workflows/bots/scripts/generate_report.py
"""
Bot Report Generator
Aggregates metrics from all bot runs and generates a summary report.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, List

### ./testing/dependency_agent/test_dependency_checker.py
"""
Unit tests for the dependency agent check_dependencies.py script
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

# Add the script directory to path - find repository root

